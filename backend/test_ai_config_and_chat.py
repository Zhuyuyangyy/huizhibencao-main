import asyncio
import importlib
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx

import ai_chat


class _UnauthorizedResponseClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, *args, **kwargs):
        request = httpx.Request("POST", "https://api.deepseek.com/v1/chat/completions")
        response = httpx.Response(
            401,
            request=request,
            json={
                "error": {
                    "message": "Authentication Fails, Your api key is invalid",
                }
            },
        )
        raise httpx.HTTPStatusError("401 Unauthorized", request=request, response=response)


class _CaptureSuccessClient:
    def __init__(self):
        self.calls = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return httpx.Response(
            200,
            request=httpx.Request("POST", args[0]),
            json={
                "choices": [
                    {
                        "message": {
                            "content": "测试回复"
                        }
                    }
                ]
            },
        )


class AIChatTests(unittest.TestCase):
    def test_chat_raises_on_upstream_auth_failure(self):
        expected_error_type = getattr(ai_chat, "AIServiceError", Exception)

        with patch("ai_chat.httpx.AsyncClient", return_value=_UnauthorizedResponseClient()):
            with self.assertRaises(expected_error_type) as ctx:
                asyncio.run(ai_chat.chat_with_sage("你好"))

        self.assertEqual(getattr(ctx.exception, "status_code", None), 401)

    def test_chat_uses_generic_ai_configuration_for_openai_compatible_service(self):
        capture_client = _CaptureSuccessClient()

        with patch.object(ai_chat, "AI_API_KEY", "openai-key"), \
             patch.object(ai_chat, "AI_BASE_URL", "https://api.openai.com/v1"), \
             patch.object(ai_chat, "AI_MODEL", "gpt-4o-mini"), \
             patch.object(ai_chat, "AI_PROVIDER_LABEL", "OpenAI"), \
             patch("ai_chat.httpx.AsyncClient", return_value=capture_client):
            reply = asyncio.run(ai_chat.chat_with_sage("你好"))

        self.assertEqual(reply, "测试回复")
        self.assertEqual(len(capture_client.calls), 1)
        args, kwargs = capture_client.calls[0]
        self.assertEqual(args[0], "https://api.openai.com/v1/chat/completions")
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer openai-key")
        self.assertEqual(kwargs["json"]["model"], "gpt-4o-mini")


class ConfigTests(unittest.TestCase):
    def test_backend_dotenv_overrides_stale_user_env_key(self):
        backend_dir = Path(__file__).resolve().parent
        env_file = backend_dir / ".env"
        original_env_file = env_file.read_text(encoding="utf-8") if env_file.exists() else None
        original_env_value = os.environ.get("DEEPSEEK_API_KEY")

        try:
            env_file.write_text("DEEPSEEK_API_KEY=project-valid-key\n", encoding="utf-8")
            os.environ["DEEPSEEK_API_KEY"] = "stale-user-key"
            sys.modules.pop("config", None)
            config = importlib.import_module("config")
            self.assertEqual(config.DEEPSEEK_API_KEY, "project-valid-key")
        finally:
            if original_env_file is None:
                env_file.unlink(missing_ok=True)
            else:
                env_file.write_text(original_env_file, encoding="utf-8")

            if original_env_value is None:
                os.environ.pop("DEEPSEEK_API_KEY", None)
            else:
                os.environ["DEEPSEEK_API_KEY"] = original_env_value
            sys.modules.pop("config", None)

    def test_generic_ai_dotenv_settings_are_loaded(self):
        backend_dir = Path(__file__).resolve().parent
        env_file = backend_dir / ".env"
        original_env_file = env_file.read_text(encoding="utf-8") if env_file.exists() else None

        try:
            env_file.write_text(
                "\n".join(
                    [
                        "AI_API_KEY=test-openai-key",
                        "AI_BASE_URL=https://api.openai.com/v1",
                        "AI_MODEL=gpt-4o-mini",
                    ]
                ) + "\n",
                encoding="utf-8",
            )
            sys.modules.pop("config", None)
            config = importlib.import_module("config")
            self.assertEqual(config.AI_API_KEY, "test-openai-key")
            self.assertEqual(config.AI_BASE_URL, "https://api.openai.com/v1")
            self.assertEqual(config.AI_MODEL, "gpt-4o-mini")
        finally:
            if original_env_file is None:
                env_file.unlink(missing_ok=True)
            else:
                env_file.write_text(original_env_file, encoding="utf-8")
            sys.modules.pop("config", None)

    def test_project_deepseek_key_wins_over_all_process_level_ai_keys(self):
        backend_dir = Path(__file__).resolve().parent
        env_file = backend_dir / ".env"
        original_env_file = env_file.read_text(encoding="utf-8") if env_file.exists() else None
        original_deepseek_env = os.environ.get("DEEPSEEK_API_KEY")
        original_ai_env = os.environ.get("AI_API_KEY")
        original_openai_env = os.environ.get("OPENAI_API_KEY")

        try:
            env_file.write_text(
                "\n".join(
                    [
                        "DEEPSEEK_API_KEY=project-deepseek-key",
                        "DEEPSEEK_BASE_URL=https://api.deepseek.com/v1",
                        "DEEPSEEK_MODEL=deepseek-chat",
                    ]
                ) + "\n",
                encoding="utf-8",
            )
            os.environ["DEEPSEEK_API_KEY"] = "stale-deepseek-env-key"
            os.environ["AI_API_KEY"] = "stale-ai-env-key"
            os.environ["OPENAI_API_KEY"] = "stale-openai-env-key"
            sys.modules.pop("config", None)
            config = importlib.import_module("config")
            self.assertEqual(config.AI_API_KEY, "project-deepseek-key")
            self.assertEqual(config.AI_BASE_URL, "https://api.deepseek.com/v1")
            self.assertEqual(config.AI_MODEL, "deepseek-chat")
            self.assertEqual(config.AI_PROVIDER_LABEL, "DeepSeek")
        finally:
            if original_env_file is None:
                env_file.unlink(missing_ok=True)
            else:
                env_file.write_text(original_env_file, encoding="utf-8")
            if original_deepseek_env is None:
                os.environ.pop("DEEPSEEK_API_KEY", None)
            else:
                os.environ["DEEPSEEK_API_KEY"] = original_deepseek_env
            if original_ai_env is None:
                os.environ.pop("AI_API_KEY", None)
            else:
                os.environ["AI_API_KEY"] = original_ai_env
            if original_openai_env is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = original_openai_env
            sys.modules.pop("config", None)


if __name__ == "__main__":
    unittest.main()
