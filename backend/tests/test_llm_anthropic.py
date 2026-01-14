"""
Unit tests for Anthropic LLM implementation
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.infrastructure.external.llm.anthropic_llm import AnthropicLLM


class TestAnthropicLLM:
    """Test Anthropic LLM message and tool format conversions"""

    def setup_method(self):
        """Setup test fixtures"""
        # Mock settings to avoid needing .env file
        with patch('app.infrastructure.external.llm.anthropic_llm.get_settings') as mock_settings:
            settings = Mock()
            settings.anthropic_api_key = "test-key"
            settings.anthropic_api_base = None
            settings.model_name = "claude-3-sonnet-20240229"
            settings.temperature = 0.7
            settings.max_tokens = 2000
            mock_settings.return_value = settings

            with patch('app.infrastructure.external.llm.anthropic_llm.AsyncAnthropic'):
                self.llm = AnthropicLLM()

    def test_convert_messages_user(self):
        """Test conversion of user messages"""
        messages = [
            {"role": "user", "content": "Hello"}
        ]

        converted, system = self.llm._convert_messages(messages)

        assert len(converted) == 1
        assert converted[0]["role"] == "user"
        assert converted[0]["content"] == "Hello"
        assert system is None

    def test_convert_messages_system(self):
        """Test conversion of system messages"""
        messages = [
            {"role": "system", "content": "You are a helpful assistant"}
        ]

        converted, system = self.llm._convert_messages(messages)

        assert len(converted) == 0
        assert system == "You are a helpful assistant"

    def test_convert_messages_assistant_with_tool_calls(self):
        """Test conversion of assistant messages with tool calls"""
        messages = [
            {
                "role": "assistant",
                "content": "I'll search for that",
                "tool_calls": [
                    {
                        "id": "call_123",
                        "type": "function",
                        "function": {
                            "name": "search",
                            "arguments": '{"q": "test"}'
                        }
                    }
                ]
            }
        ]

        converted, system = self.llm._convert_messages(messages)

        assert len(converted) == 1
        assert converted[0]["role"] == "assistant"
        assert len(converted[0]["content"]) == 2

        # Check text block
        assert converted[0]["content"][0]["type"] == "text"
        assert converted[0]["content"][0]["text"] == "I'll search for that"

        # Check tool_use block
        assert converted[0]["content"][1]["type"] == "tool_use"
        assert converted[0]["content"][1]["id"] == "call_123"
        assert converted[0]["content"][1]["name"] == "search"
        assert converted[0]["content"][1]["input"] == {"q": "test"}

    def test_convert_messages_tool_result(self):
        """Test conversion of tool result messages"""
        messages = [
            {
                "role": "tool",
                "tool_call_id": "call_123",
                "content": "Search results here"
            }
        ]

        converted, system = self.llm._convert_messages(messages)

        assert len(converted) == 1
        assert converted[0]["role"] == "user"
        assert len(converted[0]["content"]) == 1
        assert converted[0]["content"][0]["type"] == "tool_result"
        assert converted[0]["content"][0]["tool_use_id"] == "call_123"
        assert converted[0]["content"][0]["content"] == "Search results here"

    def test_convert_tools(self):
        """Test conversion of OpenAI tool format to Anthropic format"""
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "search",
                    "description": "Search the web",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "q": {"type": "string"}
                        }
                    }
                }
            }
        ]

        converted = self.llm._convert_tools(tools)

        assert len(converted) == 1
        assert converted[0]["name"] == "search"
        assert converted[0]["description"] == "Search the web"
        assert converted[0]["input_schema"]["type"] == "object"

    def test_convert_tool_choice(self):
        """Test conversion of tool_choice parameter"""
        assert self.llm._convert_tool_choice("none") == {"type": "none"}
        assert self.llm._convert_tool_choice("auto") == {"type": "auto"}
        assert self.llm._convert_tool_choice("required") == {"type": "any"}
        assert self.llm._convert_tool_choice(None) is None

    def test_convert_response_text_only(self):
        """Test conversion of Anthropic response with text only"""
        # Mock Anthropic response
        response = Mock()
        text_block = Mock()
        text_block.type = "text"
        text_block.text = "Here is the answer"
        response.content = [text_block]

        converted = self.llm._convert_response(response)

        assert converted["role"] == "assistant"
        assert converted["content"] == "Here is the answer"
        assert "tool_calls" not in converted

    def test_convert_response_with_tool_use(self):
        """Test conversion of Anthropic response with tool use"""
        # Mock Anthropic response
        response = Mock()

        text_block = Mock()
        text_block.type = "text"
        text_block.text = "Let me search"

        tool_block = Mock()
        tool_block.type = "tool_use"
        tool_block.id = "toolu_123"
        tool_block.name = "search"
        tool_block.input = {"q": "test"}

        response.content = [text_block, tool_block]

        converted = self.llm._convert_response(response)

        assert converted["role"] == "assistant"
        assert converted["content"] == "Let me search"
        assert len(converted["tool_calls"]) == 1
        assert converted["tool_calls"][0]["id"] == "toolu_123"
        assert converted["tool_calls"][0]["type"] == "function"
        assert converted["tool_calls"][0]["function"]["name"] == "search"
        assert '"q": "test"' in converted["tool_calls"][0]["function"]["arguments"]

    def test_parse_json_safe(self):
        """Test safe JSON parsing"""
        assert self.llm._parse_json_safe('{"key": "value"}') == {"key": "value"}
        assert self.llm._parse_json_safe('invalid json') == {}
        assert self.llm._parse_json_safe('') == {}

    def test_serialize_json_safe(self):
        """Test safe JSON serialization"""
        assert '"key": "value"' in self.llm._serialize_json_safe({"key": "value"})
        # Test with non-serializable object
        assert self.llm._serialize_json_safe(object()) == "{}"


class TestLLMFactory:
    """Test LLM factory function"""

    @patch('app.infrastructure.external.llm.get_settings')
    def test_get_llm_openai(self, mock_settings):
        """Test factory returns OpenAI LLM"""
        from app.infrastructure.external.llm import get_llm

        settings = Mock()
        settings.llm_provider = "openai"
        settings.api_key = "test-key"
        settings.api_base = "https://api.openai.com/v1"
        settings.model_name = "gpt-4"
        settings.temperature = 0.7
        settings.max_tokens = 2000
        mock_settings.return_value = settings

        # Clear cache
        get_llm.cache_clear()

        with patch('app.infrastructure.external.llm.OpenAILLM'):
            llm = get_llm()
            # Verify OpenAILLM was called
            from app.infrastructure.external.llm import OpenAILLM
            OpenAILLM.assert_called_once()

    @patch('app.infrastructure.external.llm.get_settings')
    def test_get_llm_anthropic(self, mock_settings):
        """Test factory returns Anthropic LLM"""
        from app.infrastructure.external.llm import get_llm

        settings = Mock()
        settings.llm_provider = "anthropic"
        settings.anthropic_api_key = "test-key"
        settings.anthropic_api_base = None
        settings.model_name = "claude-3-sonnet-20240229"
        settings.temperature = 0.7
        settings.max_tokens = 2000
        mock_settings.return_value = settings

        # Clear cache
        get_llm.cache_clear()

        with patch('app.infrastructure.external.llm.AnthropicLLM'):
            llm = get_llm()
            # Verify AnthropicLLM was called
            from app.infrastructure.external.llm import AnthropicLLM
            AnthropicLLM.assert_called_once()

    @patch('app.infrastructure.external.llm.get_settings')
    def test_get_llm_invalid_provider(self, mock_settings):
        """Test factory raises error for invalid provider"""
        from app.infrastructure.external.llm import get_llm

        settings = Mock()
        settings.llm_provider = "invalid"
        mock_settings.return_value = settings

        # Clear cache
        get_llm.cache_clear()

        with pytest.raises(ValueError, match="Unsupported LLM provider"):
            get_llm()
