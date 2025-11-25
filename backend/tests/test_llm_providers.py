"""
Tests for LLM Providers
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.providers.llm_provider import LLMMessage, LLMResponse
from app.providers.openai_provider import OpenAIProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.ollama_provider import OllamaProvider
from app.providers.llm_factory import LLMFactory, get_llm_provider, set_llm_provider


class TestLLMMessage:
    """Tests for LLMMessage model"""
    
    def test_create_message(self):
        """Test creating an LLM message"""
        msg = LLMMessage(role="user", content="Hello, AI!")
        assert msg.role == "user"
        assert msg.content == "Hello, AI!"
    
    def test_message_roles(self):
        """Test different message roles"""
        system_msg = LLMMessage(role="system", content="You are helpful")
        user_msg = LLMMessage(role="user", content="Hello")
        assistant_msg = LLMMessage(role="assistant", content="Hi there")
        
        assert system_msg.role == "system"
        assert user_msg.role == "user"
        assert assistant_msg.role == "assistant"


class TestLLMResponse:
    """Tests for LLMResponse model"""
    
    def test_create_response(self):
        """Test creating an LLM response"""
        response = LLMResponse(
            content="Hello, human!",
            model="gpt-4o-mini",
            usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            finish_reason="stop"
        )
        assert response.content == "Hello, human!"
        assert response.model == "gpt-4o-mini"
        assert response.usage["total_tokens"] == 15
        assert response.finish_reason == "stop"
    
    def test_response_without_usage(self):
        """Test response without usage stats"""
        response = LLMResponse(content="Test", model="test-model")
        assert response.content == "Test"
        assert response.usage is None


class TestOpenAIProvider:
    """Tests for OpenAI provider"""
    
    def test_initialization(self):
        """Test OpenAI provider initialization"""
        provider = OpenAIProvider(model_name="gpt-4o-mini", api_key="test-key")
        assert provider.model_name == "gpt-4o-mini"
        assert provider.api_key == "test-key"
        assert provider.get_provider_name() == "openai"
    
    def test_initialization_without_key(self):
        """Test initialization without API key"""
        with patch.dict('os.environ', {}, clear=True):
            provider = OpenAIProvider()
            assert provider.client is None
    
    @pytest.mark.asyncio
    async def test_generate_without_client(self, monkeypatch):
        """Test generate raises error without client"""
        # Clear environment variable to ensure no fallback
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        provider = OpenAIProvider(api_key=None)
        messages = [LLMMessage(role="user", content="Hello")]

        with pytest.raises(ValueError, match="OpenAI client not initialized"):
            await provider.generate(messages)
    
    @pytest.mark.asyncio
    async def test_generate_success(self):
        """Test successful generation"""
        provider = OpenAIProvider(api_key="test-key")
        
        # Mock the OpenAI client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello, human!"
        mock_response.choices[0].finish_reason = "stop"
        mock_response.model = "gpt-4o-mini"
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 5
        mock_response.usage.total_tokens = 15
        
        provider.client.chat.completions.create = AsyncMock(return_value=mock_response)
        
        messages = [LLMMessage(role="user", content="Hello")]
        response = await provider.generate(messages)
        
        assert response.content == "Hello, human!"
        assert response.model == "gpt-4o-mini"
        assert response.usage["total_tokens"] == 15
    
    @pytest.mark.asyncio
    async def test_is_available_without_key(self, monkeypatch):
        """Test is_available returns False without API key"""
        # Clear environment variable to ensure no fallback
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        provider = OpenAIProvider(api_key=None)
        assert await provider.is_available() is False


class TestGeminiProvider:
    """Tests for Gemini provider"""
    
    def test_initialization(self):
        """Test Gemini provider initialization"""
        with patch('google.generativeai.configure'):
            with patch('google.generativeai.GenerativeModel'):
                provider = GeminiProvider(model_name="gemini-1.5-flash", api_key="test-key")
                assert provider.model_name == "gemini-1.5-flash"
                assert provider.api_key == "test-key"
                assert provider.get_provider_name() == "gemini"
    
    def test_initialization_without_key(self):
        """Test initialization without API key"""
        with patch.dict('os.environ', {}, clear=True):
            provider = GeminiProvider()
            assert provider.model is None
    
    @pytest.mark.asyncio
    async def test_generate_without_model(self):
        """Test generate raises error without model"""
        provider = GeminiProvider(api_key=None)
        messages = [LLMMessage(role="user", content="Hello")]
        
        with pytest.raises(ValueError, match="not initialized"):
            await provider.generate(messages)
    
    @pytest.mark.asyncio
    async def test_is_available_without_key(self):
        """Test is_available returns False without API key"""
        provider = GeminiProvider(api_key=None)
        assert await provider.is_available() is False


class TestOllamaProvider:
    """Tests for Ollama provider"""

    def test_initialization(self):
        """Test Ollama provider initialization"""
        provider = OllamaProvider(model_name="llama3.2")
        assert provider.model_name == "llama3.2"
        assert provider.get_provider_name() == "ollama"
        assert "localhost:11434" in provider.base_url

    def test_custom_base_url(self):
        """Test Ollama with custom base URL"""
        provider = OllamaProvider(base_url="http://custom:8080")
        assert provider.base_url == "http://custom:8080"

    @pytest.mark.asyncio
    async def test_generate_success(self):
        """Test successful generation with Ollama"""
        provider = OllamaProvider()

        # Mock httpx response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "message": {"content": "Hello, human!"},
            "model": "llama3.2",
            "done_reason": "stop",
            "prompt_eval_count": 10,
            "eval_count": 5
        }
        mock_response.raise_for_status = MagicMock()

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)

            messages = [LLMMessage(role="user", content="Hello")]
            response = await provider.generate(messages)

            assert response.content == "Hello, human!"
            assert response.model == "llama3.2"
            assert response.usage["prompt_tokens"] == 10
            assert response.usage["completion_tokens"] == 5

    @pytest.mark.asyncio
    async def test_is_available_server_down(self):
        """Test is_available returns False when server is down"""
        provider = OllamaProvider()

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(side_effect=Exception("Connection failed"))

            assert await provider.is_available() is False


class TestLLMFactory:
    """Tests for LLM Factory"""

    def test_create_openai_provider(self):
        """Test creating OpenAI provider"""
        with patch.dict('os.environ', {'LLM_PROVIDER': 'openai'}):
            provider = LLMFactory.create_provider(api_key="test-key")
            assert isinstance(provider, OpenAIProvider)

    def test_create_gemini_provider(self):
        """Test creating Gemini provider"""
        with patch('google.generativeai.configure'):
            with patch('google.generativeai.GenerativeModel'):
                provider = LLMFactory.create_provider(provider_name="gemini", api_key="test-key")
                assert isinstance(provider, GeminiProvider)

    def test_create_ollama_provider(self):
        """Test creating Ollama provider"""
        provider = LLMFactory.create_provider(provider_name="ollama")
        assert isinstance(provider, OllamaProvider)

    def test_create_with_custom_model(self):
        """Test creating provider with custom model"""
        provider = LLMFactory.create_provider(provider_name="openai", model_name="gpt-4", api_key="test-key")
        assert provider.model_name == "gpt-4"

    def test_invalid_provider(self):
        """Test creating invalid provider raises error"""
        with pytest.raises(ValueError, match="Unknown LLM provider"):
            LLMFactory.create_provider(provider_name="invalid")

    def test_get_available_providers(self):
        """Test getting list of available providers"""
        providers = LLMFactory.get_available_providers()
        assert "openai" in providers
        assert "gemini" in providers
        assert "ollama" in providers

    @pytest.mark.asyncio
    async def test_test_provider(self):
        """Test testing a provider"""
        provider = OllamaProvider()

        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = {"models": [{"name": "llama3.2"}]}
            mock_response.raise_for_status = MagicMock()
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)

            result = await LLMFactory.test_provider(provider)
            assert result is True


class TestLLMFactorySingleton:
    """Tests for LLM Factory singleton"""

    def test_get_llm_provider(self):
        """Test getting default provider"""
        with patch.dict('os.environ', {'LLM_PROVIDER': 'openai'}):
            provider = get_llm_provider()
            assert isinstance(provider, OpenAIProvider)

    def test_set_llm_provider(self):
        """Test setting custom provider"""
        custom_provider = OllamaProvider()
        set_llm_provider(custom_provider)

        provider = get_llm_provider()
        assert provider is custom_provider

        # Reset to None for other tests
        set_llm_provider(None)

