import sift


def test_public_api_exports():
    """Verify that the public API correctly exports the expected objects."""
    expected_exports = {
        "SiftClient",
        "Agent",
        "AgentpredictRequest",
    }

    # Ensure all expected exports are present in __all__
    assert hasattr(sift, "__all__")
    assert expected_exports.issubset(set(sift.__all__))

    # Ensure each exported object is actually present in the module
    assert hasattr(sift, "SiftClient")
    assert hasattr(sift, "Agent")
    assert hasattr(sift, "AgentpredictRequest")
