"""
LLM Provider Factory
Creates LLM provider instances based on configuration
"""
import os
from typing import Optional
from app.providers.llm_provider import LLMProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.ollama_provider import OllamaProvider


class LLMFactory:
    """Factory for creating LLM provider instances"""
    
    # Registry of available providers
    PROVIDERS = {
        "openai": OpenAIProvider,
        "gemini": GeminiProvider,
        "ollama": OllamaProvider,
    }
    
    @staticmethod
    def create_provider(
        provider_name: Optional[str] = None,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ) -> LLMProvider:
        """
        Create an LLM provider instance
        
        Args:
            provider_name: Name of the provider ("openai", "gemini", "ollama")
                          Defaults to LLM_PROVIDER env var or "openai"
            model_name: Model name to use
                       Defaults to LLM_MODEL env var or provider-specific default
            api_key: API key for authentication
                    Defaults to provider-specific env var
            **kwargs: Additional provider-specific configuration
            
        Returns:
            LLMProvider instance
            
        Raises:
            ValueError: If provider name is invalid
        """
        # Get provider name from parameter or environment
        provider_name = provider_name or os.getenv("LLM_PROVIDER", "openai")
        provider_name = provider_name.lower()
        
        # Validate provider
        if provider_name not in LLMFactory.PROVIDERS:
            available = ", ".join(LLMFactory.PROVIDERS.keys())
            raise ValueError(
                f"Unknown LLM provider: {provider_name}. "
                f"Available providers: {available}"
            )
        
        # Get provider class
        provider_class = LLMFactory.PROVIDERS[provider_name]
        
        # Get model name from parameter or environment
        if model_name is None:
            model_name = os.getenv("LLM_MODEL")
        
        # Create provider instance
        if model_name:
            return provider_class(model_name=model_name, api_key=api_key, **kwargs)
        else:
            return provider_class(api_key=api_key, **kwargs)
    
    @staticmethod
    def get_available_providers() -> list[str]:
        """
        Get list of available provider names
        
        Returns:
            List of provider names
        """
        return list(LLMFactory.PROVIDERS.keys())
    
    @staticmethod
    async def test_provider(provider: LLMProvider) -> bool:
        """
        Test if a provider is available and working
        
        Args:
            provider: LLMProvider instance to test
            
        Returns:
            True if provider is available, False otherwise
        """
        return await provider.is_available()


# Singleton instance
_default_provider: Optional[LLMProvider] = None


def get_llm_provider() -> LLMProvider:
    """
    Get the default LLM provider instance (singleton)
    
    Returns:
        LLMProvider instance
    """
    global _default_provider
    if _default_provider is None:
        _default_provider = LLMFactory.create_provider()
    return _default_provider


def set_llm_provider(provider: LLMProvider) -> None:
    """
    Set the default LLM provider instance
    
    Args:
        provider: LLMProvider instance to use as default
    """
    global _default_provider
    _default_provider = provider

