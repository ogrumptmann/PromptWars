"""
LLM Provider Abstract Base Class
Defines the interface for all LLM providers
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class LLMMessage(BaseModel):
    """Message in a conversation"""
    role: str  # "system", "user", or "assistant"
    content: str


class LLMResponse(BaseModel):
    """Response from an LLM provider"""
    content: str
    model: str
    usage: Optional[Dict[str, int]] = None  # Token usage stats
    finish_reason: Optional[str] = None


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers
    All LLM providers must implement this interface
    """
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize the LLM provider
        
        Args:
            model_name: Name of the model to use
            api_key: API key for authentication (if required)
            **kwargs: Additional provider-specific configuration
        """
        self.model_name = model_name
        self.api_key = api_key
        self.config = kwargs
    
    @abstractmethod
    async def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a response from the LLM
        
        Args:
            messages: List of conversation messages
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Returns:
            LLMResponse with generated content
            
        Raises:
            Exception: If generation fails
        """
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """
        Check if the provider is available and configured correctly
        
        Returns:
            True if provider is ready to use, False otherwise
        """
        pass
    
    def get_provider_name(self) -> str:
        """
        Get the name of this provider
        
        Returns:
            Provider name (e.g., "openai", "gemini", "ollama")
        """
        return self.__class__.__name__.replace("Provider", "").lower()
    
    def get_model_name(self) -> str:
        """
        Get the model name being used
        
        Returns:
            Model name
        """
        return self.model_name

