from functools import lru_cache
from typing import Optional
import logging

from app.domain.external.llm import LLM
from app.core.config import get_settings

logger = logging.getLogger(__name__)

@lru_cache()
def get_llm() -> LLM:
    """Get LLM instance based on configuration"""
    from app.infrastructure.external.llm.openai_llm import OpenAILLM
    from app.infrastructure.external.llm.anthropic_llm import AnthropicLLM

    settings = get_settings()

    if settings.llm_provider == "openai":
        logger.info("Initializing OpenAI LLM")
        return OpenAILLM()
    elif settings.llm_provider == "anthropic":
        logger.info("Initializing Anthropic LLM")
        return AnthropicLLM()
    else:
        logger.error(f"Unknown LLM provider: {settings.llm_provider}")
        raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
