"""
Ollama LLM Provider
Implements LLM provider for local Ollama models
"""
import os
from typing import List, Optional
import httpx
from app.providers.llm_provider import LLMProvider, LLMMessage, LLMResponse


class OllamaProvider(LLMProvider):
    """Ollama local LLM provider implementation"""
    
    def __init__(
        self,
        model_name: str = "llama3.2",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Ollama provider
        
        Args:
            model_name: Ollama model name (default: llama3.2)
            api_key: Not used for Ollama (kept for interface compatibility)
            base_url: Ollama server URL (defaults to OLLAMA_BASE_URL env var or http://localhost:11434)
            **kwargs: Additional configuration
        """
        super().__init__(model_name, api_key, **kwargs)
        
        # Ollama base URL
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.api_url = f"{self.base_url}/api/chat"
    
    async def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a response using Ollama's API
        
        Args:
            messages: List of conversation messages
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Ollama-specific parameters
            
        Returns:
            LLMResponse with generated content
            
        Raises:
            Exception: If API call fails
        """
        # Convert LLMMessage to Ollama format
        ollama_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Build request payload
        payload = {
            "model": self.model_name,
            "messages": ollama_messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                **kwargs
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(self.api_url, json=payload)
                response.raise_for_status()
                
                data = response.json()
                
                # Extract response content
                content = data.get("message", {}).get("content", "")
                
                # Build usage stats if available
                usage = None
                if "prompt_eval_count" in data or "eval_count" in data:
                    usage = {
                        "prompt_tokens": data.get("prompt_eval_count", 0),
                        "completion_tokens": data.get("eval_count", 0),
                        "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
                    }
                
                return LLMResponse(
                    content=content,
                    model=data.get("model", self.model_name),
                    usage=usage,
                    finish_reason=data.get("done_reason", "stop")
                )
                
        except httpx.HTTPStatusError as e:
            raise Exception(f"Ollama HTTP error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            raise Exception(f"Ollama connection error: {str(e)}")
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    async def is_available(self) -> bool:
        """
        Check if Ollama provider is available
        
        Returns:
            True if Ollama server is reachable and model is available, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Check if Ollama server is running
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                
                # Check if the model is available
                data = response.json()
                models = data.get("models", [])
                model_names = [m.get("name", "") for m in models]
                
                # Check if our model is in the list (exact match or prefix match)
                return any(
                    self.model_name == name or name.startswith(f"{self.model_name}:")
                    for name in model_names
                )
                
        except Exception:
            return False

