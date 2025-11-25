"""
Google Gemini LLM Provider
Implements LLM provider for Google's Gemini models
"""
import os
from typing import List, Optional
import google.generativeai as genai
from app.providers.llm_provider import LLMProvider, LLMMessage, LLMResponse


class GeminiProvider(LLMProvider):
    """Google Gemini provider implementation"""
    
    def __init__(
        self,
        model_name: str = "gemini-1.5-flash",
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Gemini provider
        
        Args:
            model_name: Gemini model name (default: gemini-1.5-flash)
            api_key: Google API key (defaults to GOOGLE_API_KEY env var)
            **kwargs: Additional configuration
        """
        super().__init__(model_name, api_key, **kwargs)
        
        # Use provided API key or fall back to environment variable
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        # Configure Gemini
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None
    
    async def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a response using Gemini's API
        
        Args:
            messages: List of conversation messages
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Gemini-specific parameters
            
        Returns:
            LLMResponse with generated content
            
        Raises:
            ValueError: If model is not initialized
            Exception: If API call fails
        """
        if not self.model:
            raise ValueError("Gemini model not initialized. Please provide an API key.")
        
        try:
            # Convert messages to Gemini format
            # Gemini uses a different format: system instruction + chat history
            system_instruction = None
            chat_messages = []
            
            for msg in messages:
                if msg.role == "system":
                    system_instruction = msg.content
                elif msg.role == "user":
                    chat_messages.append({"role": "user", "parts": [msg.content]})
                elif msg.role == "assistant":
                    chat_messages.append({"role": "model", "parts": [msg.content]})
            
            # Configure generation
            generation_config = genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                **kwargs
            )
            
            # Create model with system instruction if provided
            if system_instruction:
                model = genai.GenerativeModel(
                    self.model_name,
                    system_instruction=system_instruction
                )
            else:
                model = self.model
            
            # Generate response
            if chat_messages:
                # Use chat mode if there are messages
                chat = model.start_chat(history=chat_messages[:-1] if len(chat_messages) > 1 else [])
                response = await chat.send_message_async(
                    chat_messages[-1]["parts"][0],
                    generation_config=generation_config
                )
            else:
                # Single generation
                response = await model.generate_content_async(
                    system_instruction or "",
                    generation_config=generation_config
                )
            
            # Extract content
            content = response.text if hasattr(response, 'text') else ""
            
            # Build usage stats (Gemini provides token counts)
            usage = None
            if hasattr(response, 'usage_metadata'):
                usage = {
                    "prompt_tokens": response.usage_metadata.prompt_token_count,
                    "completion_tokens": response.usage_metadata.candidates_token_count,
                    "total_tokens": response.usage_metadata.total_token_count
                }
            
            return LLMResponse(
                content=content,
                model=self.model_name,
                usage=usage,
                finish_reason="stop"
            )
            
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    async def is_available(self) -> bool:
        """
        Check if Gemini provider is available
        
        Returns:
            True if API key is configured, False otherwise
        """
        if not self.model or not self.api_key:
            return False
        
        try:
            # Try a minimal generation to verify connectivity
            test_response = await self.model.generate_content_async("test")
            return test_response is not None
        except Exception:
            return False

