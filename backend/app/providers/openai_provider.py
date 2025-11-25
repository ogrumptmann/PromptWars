"""
OpenAI LLM Provider
Implements LLM provider for OpenAI's GPT models
"""
import os
from typing import List, Optional
from openai import AsyncOpenAI
from app.providers.llm_provider import LLMProvider, LLMMessage, LLMResponse


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider implementation"""
    
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize OpenAI provider
        
        Args:
            model_name: OpenAI model name (default: gpt-4o-mini)
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            **kwargs: Additional configuration
        """
        super().__init__(model_name, api_key, **kwargs)
        
        # Use provided API key or fall back to environment variable
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        # Initialize OpenAI client
        if self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    async def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a response using OpenAI's API
        
        Args:
            messages: List of conversation messages
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional OpenAI-specific parameters
            
        Returns:
            LLMResponse with generated content
            
        Raises:
            ValueError: If client is not initialized
            Exception: If API call fails
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized. Please provide an API key.")
        
        # Convert LLMMessage to OpenAI format
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        try:
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=openai_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            # Extract response
            choice = response.choices[0]
            content = choice.message.content or ""
            
            # Build usage stats
            usage = None
            if response.usage:
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            
            return LLMResponse(
                content=content,
                model=response.model,
                usage=usage,
                finish_reason=choice.finish_reason
            )
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def is_available(self) -> bool:
        """
        Check if OpenAI provider is available
        
        Returns:
            True if API key is configured, False otherwise
        """
        if not self.client or not self.api_key:
            return False
        
        try:
            # Try a minimal API call to verify connectivity
            await self.client.models.retrieve(self.model_name)
            return True
        except Exception:
            return False

