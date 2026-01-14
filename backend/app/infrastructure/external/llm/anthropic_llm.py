from typing import List, Dict, Any, Optional
from anthropic import AsyncAnthropic
from app.domain.external.llm import LLM
from app.core.config import get_settings
import logging
import asyncio
import json

logger = logging.getLogger(__name__)

class AnthropicLLM(LLM):
    """Anthropic Claude LLM implementation"""

    def __init__(self):
        settings = get_settings()

        # Initialize Anthropic client
        client_kwargs = {"api_key": settings.anthropic_api_key}
        if settings.anthropic_api_base:
            client_kwargs["base_url"] = settings.anthropic_api_base

        self.client = AsyncAnthropic(**client_kwargs)

        self._model_name = settings.model_name
        self._temperature = settings.temperature
        self._max_tokens = settings.max_tokens
        logger.info(f"Initialized Anthropic LLM with model: {self._model_name}")

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def temperature(self) -> float:
        return self._temperature

    @property
    def max_tokens(self) -> int:
        return self._max_tokens

    async def ask(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        response_format: Optional[Dict[str, Any]] = None,
        tool_choice: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send chat request to Anthropic API with retry mechanism"""
        max_retries = 3
        base_delay = 1.0

        # Convert messages from OpenAI format to Anthropic format
        anthropic_messages, system_message = self._convert_messages(messages)

        # Handle JSON response format by modifying system message
        if response_format and response_format.get("type") == "json_object":
            logger.warning("Anthropic does not support response_format parameter, appending JSON instruction to system message")
            json_instruction = "\n\nIMPORTANT: You must respond with valid JSON only."
            if system_message:
                system_message += json_instruction
            else:
                system_message = "You must respond with valid JSON only."

        # Convert tools from OpenAI format to Anthropic format
        anthropic_tools = None
        if tools:
            anthropic_tools = self._convert_tools(tools)

        # Convert tool_choice
        anthropic_tool_choice = self._convert_tool_choice(tool_choice)

        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.info(f"Retrying Anthropic API request (attempt {attempt + 1}/{max_retries + 1}) after {delay}s delay")
                    await asyncio.sleep(delay)

                # Build request parameters
                kwargs = {
                    "model": self._model_name,
                    "temperature": self._temperature,
                    "max_tokens": self._max_tokens,
                    "messages": anthropic_messages,
                }

                if system_message:
                    kwargs["system"] = system_message

                if anthropic_tools:
                    kwargs["tools"] = anthropic_tools

                if anthropic_tool_choice:
                    kwargs["tool_choice"] = anthropic_tool_choice

                logger.debug(f"Sending request to Anthropic, model: {self._model_name}, attempt: {attempt + 1}")
                response = await self.client.messages.create(**kwargs)

                logger.debug(f"Response from Anthropic: {response.model_dump()}")

                if not response or not response.content:
                    error_msg = f"Anthropic API returned invalid response (no content) on attempt {attempt + 1}"
                    logger.error(error_msg)
                    if attempt == max_retries:
                        raise ValueError(f"Failed after {max_retries + 1} attempts: {error_msg}")
                    continue

                # Convert response from Anthropic format to OpenAI format
                return self._convert_response(response)

            except Exception as e:
                error_msg = f"Error calling Anthropic API on attempt {attempt + 1}: {str(e)}"
                logger.error(error_msg)
                if attempt == max_retries:
                    raise e
                continue

    def _convert_messages(self, messages: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], Optional[str]]:
        """Convert OpenAI message format to Anthropic format

        Returns:
            Tuple of (anthropic_messages, system_message)
        """
        converted = []
        system_message = None

        for msg in messages:
            role = msg.get("role")

            if role == "system":
                # System messages are handled separately in Anthropic
                system_message = msg.get("content", "")

            elif role == "user":
                converted.append({
                    "role": "user",
                    "content": msg.get("content", "")
                })

            elif role == "assistant":
                # Convert assistant message with potential tool calls
                content_blocks = []

                # Add text content if present
                if msg.get("content"):
                    content_blocks.append({
                        "type": "text",
                        "text": msg.get("content")
                    })

                # Add tool calls if present
                if msg.get("tool_calls"):
                    for tool_call in msg.get("tool_calls", []):
                        content_blocks.append({
                            "type": "tool_use",
                            "id": tool_call.get("id"),
                            "name": tool_call.get("function", {}).get("name"),
                            "input": self._parse_json_safe(tool_call.get("function", {}).get("arguments", "{}"))
                        })

                converted.append({
                    "role": "assistant",
                    "content": content_blocks if content_blocks else ""
                })

            elif role == "tool":
                # Convert tool result to Anthropic format
                # In Anthropic, tool results go in user messages
                converted.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": msg.get("tool_call_id"),
                        "content": msg.get("content", "")
                    }]
                })

        return converted, system_message

    def _convert_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert OpenAI tool format to Anthropic format"""
        anthropic_tools = []

        for tool in tools:
            if tool.get("type") == "function":
                func = tool.get("function", {})
                anthropic_tools.append({
                    "name": func.get("name"),
                    "description": func.get("description"),
                    "input_schema": func.get("parameters", {})
                })

        return anthropic_tools

    def _convert_tool_choice(self, tool_choice: Optional[str]) -> Optional[Dict[str, str]]:
        """Convert OpenAI tool_choice to Anthropic format"""
        if not tool_choice:
            return None

        if tool_choice == "none":
            return {"type": "none"}
        elif tool_choice == "auto":
            return {"type": "auto"}
        elif tool_choice == "required":
            return {"type": "any"}

        return None

    def _convert_response(self, response) -> Dict[str, Any]:
        """Convert Anthropic response to OpenAI format"""
        result = {
            "role": "assistant",
            "content": None,
        }

        text_content = []
        tool_calls = []

        for block in response.content:
            if block.type == "text":
                text_content.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append({
                    "id": block.id,
                    "type": "function",
                    "function": {
                        "name": block.name,
                        "arguments": self._serialize_json_safe(block.input)
                    }
                })

        if text_content:
            result["content"] = "".join(text_content)

        if tool_calls:
            result["tool_calls"] = tool_calls

        return result

    def _parse_json_safe(self, json_str: str) -> Dict[str, Any]:
        """Safely parse JSON string"""
        try:
            return json.loads(json_str)
        except Exception as e:
            logger.warning(f"Failed to parse JSON: {e}, returning empty dict")
            return {}

    def _serialize_json_safe(self, obj: Any) -> str:
        """Safely serialize object to JSON string"""
        try:
            return json.dumps(obj)
        except Exception as e:
            logger.warning(f"Failed to serialize JSON: {e}, returning empty object")
            return "{}"
