import pytest
from unittest.mock import patch, MagicMock
from sift.config import settings

def test_get_langfuse_client_singleton():
    from sift.integrations.langfuse import service
    # Reset singleton
    service._client = None
    
    with patch("sift.integrations.langfuse.service.Langfuse") as mock_langfuse:
        mock_instance = MagicMock()
        mock_langfuse.return_value = mock_instance
        
        settings.langfuse_public_key = "pk_test"
        settings.langfuse_secret_key = "sk_test"
        settings.langfuse_host = "https://host_test"
        
        # First call should instantiate
        client1 = service.get_langfuse_client()
        mock_langfuse.assert_called_once_with(
            public_key="pk_test",
            secret_key="sk_test",
            host="https://host_test"
        )
        assert client1 == mock_instance
        
        # Second call should return the same instance
        client2 = service.get_langfuse_client()
        assert client1 is client2
        # Assert it was not called again
        mock_langfuse.assert_called_once()
