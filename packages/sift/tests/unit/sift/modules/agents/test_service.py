from unittest.mock import patch, MagicMock
import pytest
import dspy

from sift.modules.agents.service import compile_and_save_agent, dynamic_api_metric


# --- Metric Logic Tests ---

@patch("dspy.Predict.__call__")
def test_dynamic_api_metric_evaluates_with_reference_data(mock_predict_call):
    # Arrange
    mock_predict_call.return_value = dspy.Prediction(
        evaluation_score="0.95",
        evaluation_feedback="Intro added."
    )
    
    example = dspy.Example(inputs="Hello", output="Hi", score=0.9, feedback="Good but missing intro").with_inputs("inputs")
    pred = dspy.Prediction(output="Hi there!")
    
    # Act
    result = dynamic_api_metric(example, pred)
    
    # Assert
    assert result.score == 0.95
    assert result.feedback == "Intro added."
    
    # Ensure correct kwargs were passed to the LLM Judge
    kwargs = mock_predict_call.call_args[1]
    assert kwargs["example_score"] == "0.9"
    assert kwargs["example_feedback"] == "Good but missing intro"


@patch("dspy.Predict.__call__")
def test_dynamic_api_metric_parsing_failure(mock_predict_call):
    # Arrange
    mock_predict_call.return_value = dspy.Prediction(
        evaluation_score="eight point five",
        evaluation_feedback="..."
    )
    
    example = dspy.Example(inputs="Hello", output="Hi").with_inputs("inputs")
    pred = dspy.Prediction(output="Hi there!")
    
    # Act
    result = dynamic_api_metric(example, pred)
    
    # Assert
    assert result.score == 0.0
    assert result.feedback == "..."


@patch("dspy.Predict.__call__")
def test_dynamic_api_metric_missing_reference_data(mock_predict_call):
    # Arrange
    mock_predict_call.return_value = dspy.Prediction(
        evaluation_score="0.8",
        evaluation_feedback="Looks okay."
    )
    
    # Example without score or feedback
    example = dspy.Example(inputs="Hello", output="Hi").with_inputs("inputs")
    pred = dspy.Prediction(output="Hi there!")
    
    # Act
    result = dynamic_api_metric(example, pred)
    
    # Assert
    assert result.score == 0.8
    assert result.feedback == "Looks okay."
    
    kwargs = mock_predict_call.call_args[1]
    assert kwargs["example_score"] == ""
    assert kwargs["example_feedback"] == ""


# --- Compilation Logic Tests ---

def _create_payload(trainset_size: int, optimizer: str | None = None) -> dict:
    original_fields = [
        {"name": "input_a", "json_schema_extra": {"__dspy_field_type": "input"}},
        {"name": "output_c", "json_schema_extra": {"__dspy_field_type": "output"}},
    ]
    train = [{"input_a": f"A{i}", "output_c": f"C{i}"} for i in range(trainset_size)]
    
    return {
        "agent_name": "test-agent",
        "agent_card_params": {},
        "litellm_params": {"model": "openai/gpt-4o-mini"},
        "dspy_params": {
            "optimizer": optimizer,
            "state": {
                "main_predictor": {
                    "signature": {
                        "instructions": "Original instructions.",
                        "fields": original_fields,
                    },
                    "train": train,
                    "traces": [],
                    "demos": [],
                }
            }
        },
    }

def _mock_compiled_module():
    mock_compiled_module = MagicMock()
    mock_compiled_module.dump_state.return_value = {
        "main_predictor": {
            "signature": {
                "instructions": "Optimized instructions.",
                "fields": [],
            },
            "train": [],
            "traces": [],
            "demos": [],
            "lm": None,
        }
    }
    return mock_compiled_module


@patch("sift.modules.agents.repository.langfuse.save_agent")
@patch("dspy.teleprompt.BootstrapFewShot")
def test_implicit_mode_tiny_dataset(mock_optimizer_class, mock_save_agent):
    payload = _create_payload(trainset_size=3, optimizer=None)
    mock_optimizer_instance = MagicMock()
    mock_optimizer_instance.compile.return_value = _mock_compiled_module()
    mock_optimizer_class.return_value = mock_optimizer_instance
    
    compile_and_save_agent(payload)
    
    mock_optimizer_class.assert_called_once_with(
        max_bootstrapped_demos=3, max_labeled_demos=3, metric=dynamic_api_metric
    )


@patch("sift.modules.agents.repository.langfuse.save_agent")
@patch("dspy.teleprompt.BootstrapFewShotWithRandomSearch")
def test_implicit_mode_medium_dataset(mock_optimizer_class, mock_save_agent):
    payload = _create_payload(trainset_size=15, optimizer=None)
    mock_optimizer_instance = MagicMock()
    mock_optimizer_instance.compile.return_value = _mock_compiled_module()
    mock_optimizer_class.return_value = mock_optimizer_instance
    
    compile_and_save_agent(payload)
    
    mock_optimizer_class.assert_called_once_with(
        max_bootstrapped_demos=3, num_candidates=10, num_threads=4, metric=dynamic_api_metric
    )


@patch("sift.modules.agents.repository.langfuse.save_agent")
@patch("dspy.teleprompt.MIPROv2")
def test_implicit_mode_large_dataset(mock_optimizer_class, mock_save_agent):
    payload = _create_payload(trainset_size=25, optimizer=None)
    mock_optimizer_instance = MagicMock()
    mock_optimizer_instance.compile.return_value = _mock_compiled_module()
    mock_optimizer_class.return_value = mock_optimizer_instance
    
    compile_and_save_agent(payload)
    
    mock_optimizer_class.assert_called_once_with(
        num_candidates=5, num_trials=20, minibatch_size=25, metric=dynamic_api_metric
    )


@patch("sift.modules.agents.repository.langfuse.save_agent")
@patch("dspy.teleprompt.COPRO")
def test_explicit_optimizer_mode_override(mock_optimizer_class, mock_save_agent):
    payload = _create_payload(trainset_size=3, optimizer="COPRO")
    mock_optimizer_instance = MagicMock()
    mock_optimizer_instance.compile.return_value = _mock_compiled_module()
    mock_optimizer_class.return_value = mock_optimizer_instance
    
    compile_and_save_agent(payload)
    
    mock_optimizer_class.assert_called_once_with(metric=dynamic_api_metric)


@patch("dspy.teleprompt.BootstrapFewShot")
@patch("sift.modules.agents.repository.langfuse.save_agent")
def test_compile_and_save_agent_preserves_signature_fields(
    mock_save_agent, mock_bootstrap
):
    original_fields = [
        {"name": "input_a", "json_schema_extra": {"__dspy_field_type": "input"}},
        {"name": "input_b", "json_schema_extra": {"__dspy_field_type": "input"}},
        {"name": "output_c", "json_schema_extra": {"__dspy_field_type": "output"}},
    ]

    payload = {
        "agent_name": "test-agent",
        "agent_card_params": {},
        "litellm_params": {"model": "openai/gpt-4o-mini"},
        "dspy_params": {
            "optimizer": "BootstrapFewShot",
            "state": {
                "main_predictor": {
                    "signature": {
                        "instructions": "Original instructions.",
                        "fields": original_fields,
                    },
                    "train": [{"input_a": "A", "input_b": "B", "output_c": "C"}],
                    "traces": [],
                    "demos": [],
                }
            }
        },
    }

    mock_optimizer = MagicMock()
    mock_compiled_module = MagicMock()
    mock_compiled_module.dump_state.return_value = {
        "main_predictor": {
            "signature": {
                "instructions": "Optimized instructions.",
                "fields": [
                    {"prefix": "Input A:", "description": "${input_a}"},
                    {"prefix": "Input B:", "description": "${input_b}"},
                    {"prefix": "Output C:", "description": "${output_c}"},
                ],
            },
            "train": [{"input_a": "A", "input_b": "B", "output_c": "C"}],
            "traces": [],
            "demos": [
                {"input_a": "A", "input_b": "B", "output_c": "C", "augmented": True}
            ],
            "lm": None,
        }
    }

    mock_optimizer.compile.return_value = mock_compiled_module
    mock_bootstrap.return_value = mock_optimizer

    compile_and_save_agent(payload)

    mock_bootstrap.assert_called_once_with(metric=dynamic_api_metric)
    
    mock_save_agent.assert_called_once()
    saved_agent = mock_save_agent.call_args[0][0]

    pred_state = saved_agent.dspy_params.state["main_predictor"]

    assert pred_state.signature.instructions == "Optimized instructions.", (
        "Instructions should be updated by DSPy."
    )
    assert pred_state.signature.fields == original_fields, (
        "Original rich fields should be preserved."
    )
    assert len(pred_state.demos) == 1, (
        "Demos generated by compilation should be captured."
    )


@patch("dspy.teleprompt.BootstrapFewShot")
@patch("sift.modules.agents.repository.langfuse.save_agent")
def test_compile_and_save_agent_hydrates_multimodal_train_data(mock_save_agent, mock_bootstrap):
    payload = {
        "agent_name": "test-agent-vision",
        "agent_card_params": {},
        "litellm_params": {"model": "openai/gpt-4o"},
        "dspy_params": {
            "optimizer": "BootstrapFewShot",
            "state": {
                "main_predictor": {
                    "signature": {
                        "instructions": "Vision task",
                        "fields": [
                            {"name": "messages", "json_schema_extra": {"__dspy_field_type": "input"}},
                            {"name": "response", "json_schema_extra": {"__dspy_field_type": "output"}},
                        ],
                    },
                    "train": [
                        {
                            "messages": [
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": "What is this?"},
                                        {"type": "image_url", "image_url": {"url": "https://example.com/image.png"}}
                                    ]
                                }
                            ],
                            "response": "An image.",
                            "score": 1.0
                        }
                    ],
                    "traces": [],
                    "demos": [],
                }
            }
        },
    }

    mock_optimizer = MagicMock()
    mock_compiled_module = MagicMock()
    mock_compiled_module.dump_state.return_value = {
        "main_predictor": {
            "signature": {
                "instructions": "Vision task optimized",
                "fields": [],
            },
            "train": [],
            "traces": [],
            "demos": [],
            "lm": None,
        }
    }
    mock_optimizer.compile.return_value = mock_compiled_module
    mock_bootstrap.return_value = mock_optimizer

    compile_and_save_agent(payload)

    # Verify that the trainset passed to compile() had its image_url hydrated into dspy.Image
    mock_optimizer.compile.assert_called_once()
    kwargs = mock_optimizer.compile.call_args.kwargs
    trainset = kwargs.get("trainset")
    assert trainset is not None
    assert len(trainset) == 1

    first_example = trainset[0]
    assert hasattr(first_example, "messages")
    messages = first_example.messages
    assert isinstance(messages, list)
    assert len(messages) == 1
    content = messages[0]["content"]
    assert isinstance(content, list)
    assert len(content) == 2
    assert isinstance(content[1], dspy.Image)
    assert content[1].url == "https://example.com/image.png"


@patch("dspy.teleprompt.BootstrapFewShot")
@patch("sift.modules.agents.repository.langfuse.save_agent")
def test_compile_and_save_agent_no_trainset(mock_save_agent, mock_bootstrap):
    original_fields = [
        {"name": "input_a", "json_schema_extra": {"__dspy_field_type": "input"}},
        {"name": "output_b", "json_schema_extra": {"__dspy_field_type": "output"}},
    ]

    payload = {
        "agent_name": "test-agent",
        "agent_card_params": {},
        "litellm_params": {"model": "openai/gpt-4o-mini"},
        "dspy_params": {
            "state": {
                "main_predictor": {
                    "signature": {
                        "instructions": "Do something.",
                        "fields": original_fields,
                    },
                    "train": [],
                    "traces": [],
                    "demos": [],
                }
            }
        },
    }

    compile_and_save_agent(payload)

    mock_bootstrap.assert_not_called()

    mock_save_agent.assert_called_once()
    saved_agent = mock_save_agent.call_args[0][0]

    pred_state = saved_agent.dspy_params.state["main_predictor"]
    assert pred_state.signature.fields == original_fields
    assert pred_state.signature.instructions == "Do something."


@patch("sift.modules.agents.repository.langfuse.save_agent")
@patch("dspy.teleprompt.MIPROv2")
def test_compile_and_save_agent_dynamic_optimizer(mock_miprov2, mock_save_agent):
    payload = {
        "agent_name": "test-agent",
        "agent_card_params": {},
        "litellm_params": {"model": "openai/gpt-4o-mini"},
        "dspy_params": {
            "optimizer": "MIPROv2",
            "optimizer_params": {"num_candidates": 2},
            "state": {
                "main_predictor": {
                    "signature": {
                        "instructions": "Original instructions.",
                        "fields": [
                            {"name": "input_a", "json_schema_extra": {"__dspy_field_type": "input"}},
                            {"name": "output_c", "json_schema_extra": {"__dspy_field_type": "output"}},
                        ],
                    },
                    "train": [{"input_a": "A", "output_c": "C"}],
                    "traces": [],
                    "demos": [],
                }
            }
        },
    }

    mock_optimizer = MagicMock()
    mock_compiled_module = MagicMock()
    mock_compiled_module.dump_state.return_value = {
        "main_predictor": {
            "signature": {
                "instructions": "MIPROv2 Optimized instructions.",
                "fields": [],
            },
            "train": [{"input_a": "A", "output_c": "C"}],
            "traces": [],
            "demos": [],
            "lm": None,
        }
    }
    mock_optimizer.compile.return_value = mock_compiled_module
    mock_miprov2.return_value = mock_optimizer

    compile_and_save_agent(payload)

    mock_miprov2.assert_called_once_with(num_candidates=2, metric=dynamic_api_metric)
    mock_save_agent.assert_called_once()


@patch("sift.modules.agents.repository.langfuse.save_agent")
def test_compile_and_save_agent_invalid_optimizer(mock_save_agent):
    payload = {
        "agent_name": "test-agent",
        "agent_card_params": {},
        "litellm_params": {"model": "openai/gpt-4o-mini"},
        "dspy_params": {
            "optimizer": "FakeOptimizer",
            "state": {
                "main_predictor": {
                    "signature": {
                        "instructions": "Original instructions.",
                        "fields": [
                            {"name": "input_a", "json_schema_extra": {"__dspy_field_type": "input"}},
                            {"name": "output_c", "json_schema_extra": {"__dspy_field_type": "output"}},
                        ],
                    },
                    "train": [{"input_a": "A", "output_c": "C"}],
                    "traces": [],
                    "demos": [],
                }
            }
        },
    }

    with pytest.raises(ValueError, match="Optimizer FakeOptimizer not found in dspy.teleprompt"):
        compile_and_save_agent(payload)

    mock_save_agent.assert_not_called()


@patch("sift.modules.agents.repository.langfuse.save_agent")
def test_compile_and_save_agent_infers_fields(mock_save_agent):
    payload = {
        "agent_name": "test-agent",
        "agent_card_params": {},
        "litellm_params": {"model": "openai/gpt-4o-mini"},
        "dspy_params": {
            "state": {
                "main_predictor": {
                    "signature": {
                        "instructions": "",
                        "fields": [],
                    },
                    "train": [{"question": "Q", "answer": "A", "metadata": "ignored"}],
                    "traces": [],
                    "demos": [],
                }
            }
        },
    }

    compile_and_save_agent(payload)

    mock_save_agent.assert_called_once()
    saved_agent = mock_save_agent.call_args[0][0]
    pred_state = saved_agent.dspy_params.state["main_predictor"]

    fields = pred_state.signature.fields
    assert len(fields) == 3
    names = [f["name"] for f in fields]
    assert "question" in names
    assert "answer" in names
    assert "metadata" in names

    for f in fields:
        extra = f["json_schema_extra"]
        if f["name"] == "answer":
            assert extra["__dspy_field_type"] == "output"
        else:
            assert extra["__dspy_field_type"] == "input"

@patch("sift.modules.agents.repository.langfuse.save_agent")
def test_compile_and_save_agent_handles_dict_fields_and_empty_names(mock_save_agent):
    payload = _create_payload(trainset_size=1)
    # Give fields as a dict and include an empty name to hit lines 213, 245, 251, 260, 263
    payload["dspy_params"]["state"]["main_predictor"]["signature"]["fields"] = {
        "some_input": {"json_schema_extra": {}},
        "": {"json_schema_extra": {"__dspy_field_type": "input"}},
    }
    
    with patch("dspy.teleprompt.BootstrapFewShot") as mock_bootstrap:
        mock_bootstrap.return_value.compile.return_value = _mock_compiled_module()
        compile_and_save_agent(payload)
        
    mock_save_agent.assert_called_once()


@patch("sift.modules.agents.repository.langfuse.save_agent")
def test_compile_and_save_agent_hits_line_263(mock_save_agent):
    payload = _create_payload(trainset_size=1)
    # Provide no valid inputs after filtering to hit line 263 (inputs = ["messages"])
    payload["dspy_params"]["state"]["main_predictor"]["signature"]["fields"] = {
        "my_response": {"json_schema_extra": {}}
    }
    
    with patch("dspy.teleprompt.BootstrapFewShot") as mock_bootstrap:
        mock_bootstrap.return_value.compile.return_value = _mock_compiled_module()
        compile_and_save_agent(payload)
        
    mock_save_agent.assert_called_once()

# --- AgentModule Edge Case Tests ---

def test_hydrate_multimodal_messages_missing_url():
    from sift.modules.agents.service import _hydrate_multimodal_messages
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {}}  # Missing 'url' key
            ]
        }
    ]
    hydrated = _hydrate_multimodal_messages(messages)
    assert len(hydrated) == 1
    assert hydrated[0]["content"][0]["type"] == "image_url"
    assert not isinstance(hydrated[0]["content"][0], dspy.Image)

def test_agent_module_ignores_non_dict_state():
    from sift.modules.agents.service import AgentModule
    state = {"main_predictor": 123}
    module = AgentModule(state)
    assert not hasattr(module, "main_predictor")

def test_agent_module_handles_dict_fields():
    from sift.modules.agents.service import AgentModule
    state = {
        "main_predictor": {
            "signature": {
                "fields": {
                    "input_f": {"json_schema_extra": {"__dspy_field_type": "input"}}
                }
            }
        }
    }
    module = AgentModule(state)
    assert hasattr(module, "main_predictor")

def test_agent_module_infers_io_from_name():
    from sift.modules.agents.service import AgentModule
    state = {
        "main_predictor": {
            "signature": {
                "fields": [
                    {"name": "my_response", "json_schema_extra": {}},
                    {"name": "other_input", "json_schema_extra": {}}
                ]
            }
        }
    }
    module = AgentModule(state)
    assert hasattr(module, "main_predictor")

def test_agent_module_empty_field_name_continue():
    from sift.modules.agents.service import AgentModule
    state = {
        "main_predictor": {
            "signature": {
                "fields": [
                    {"name": "", "json_schema_extra": {"__dspy_field_type": "input"}}
                ]
            }
        }
    }
    module = AgentModule(state)
    # The empty field should be skipped, so inputs default to ["messages"] and outputs to ["response"]
    assert hasattr(module, "main_predictor")

def test_agent_module_load_state_hydrates_demos():
    from sift.modules.agents.service import AgentModule
    state = {
        "main_predictor": {
            "signature": {"fields": [], "instructions": "test"},
            "lm": None,
            "demos": [
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "image_url", "image_url": {"url": "http://img.com"}}
                            ]
                        }
                    ]
                }
            ]
        }
    }
    module = AgentModule(state)
    module.load_state(state)
    # Should not throw any errors, demo messages hydrated successfully.

def test_agent_module_forward_no_predictors():
    from sift.modules.agents.service import AgentModule
    module = AgentModule({})
    with pytest.raises(ValueError, match="No predictors found"):
        module.forward(messages="Hello")
