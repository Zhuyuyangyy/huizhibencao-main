"""
AI chat integration for the herb sage assistant.
"""

import httpx

from config import AI_API_KEY, AI_BASE_URL, AI_MODEL, AI_PROVIDER_LABEL


class AIServiceError(Exception):
    """Raised when the upstream AI service cannot fulfill a request."""

    def __init__(self, status_code: int, user_message: str, detail: str = ""):
        super().__init__(user_message)
        self.status_code = status_code
        self.user_message = user_message
        self.detail = detail


SYSTEM_PROMPT = """
你是“本草精灵老祖”，一位精通中医药和智慧农业的 AI 助手。
你的职责：
1. 回答关于中药材种植、养护、功效的问题。
2. 根据传感器实时数据和历史趋势提供管理建议。
3. 结合节气给出养生和农事建议。
4. 解答病虫害防治问题。
5. 分析数据变化趋势并预警风险。

回答要求：
- 风格亲切、简明，可带少量古风表达。
- 引用数据时尽量具体。
- 给出可执行建议。
- 每次回答控制在 300 字以内。
""".strip()


def _build_context_message(sensor_context: dict | None) -> str | None:
    context_parts = []

    if sensor_context:
        greenhouse = sensor_context.get("greenhouse", {})
        context_parts.append(
            "\n".join(
                [
                    "【实时传感器数据】",
                    f"- 棚内温度: {greenhouse.get('airTemp', 'N/A')} °C",
                    f"- 棚内湿度: {greenhouse.get('airHumidity', 'N/A')}%",
                    f"- CO2 浓度: {greenhouse.get('co2', 'N/A')} ppm",
                    f"- 土壤湿度: {greenhouse.get('soilMoisture', 'N/A')}%",
                    f"- 光照强度: {greenhouse.get('light', 'N/A')} lux",
                    f"- pH 值: {greenhouse.get('ph', 'N/A')}",
                ]
            )
        )

    try:
        from database import get_ai_context_summary

        history_summary = get_ai_context_summary()
        if history_summary:
            context_parts.append(f"【历史趋势】\n{history_summary}")
    except Exception:
        pass

    if not context_parts:
        return None

    return "\n\n".join(context_parts) + "\n\n请结合以上数据回答用户问题。"


async def chat_with_sage(question: str, sensor_context: dict = None) -> str:
    """
    Send a question to the configured AI provider and return the model reply.
    """
    import sys

    if not AI_API_KEY:
        raise AIServiceError(
            503,
            f"未配置 {AI_PROVIDER_LABEL} API Key，请在 backend/.env 中设置 AI_API_KEY",
        )

    print(f"[AI] 收到问题: {question}", flush=True)
    print(f"[AI] Provider: {AI_PROVIDER_LABEL}", flush=True)
    print(f"[AI] API Key 前8位: {AI_API_KEY[:8]}...", flush=True)
    print(f"[AI] API Base URL: {AI_BASE_URL}", flush=True)
    print(f"[AI] Model: {AI_MODEL}", flush=True)
    sys.stdout.flush()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    context_message = _build_context_message(sensor_context)
    if context_message:
        messages.append({"role": "system", "content": context_message})
    messages.append({"role": "user", "content": question})

    print(f"[AI] 发送请求到 {AI_PROVIDER_LABEL}...", flush=True)
    sys.stdout.flush()

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{AI_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {AI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": AI_MODEL,
                    "messages": messages,
                    "temperature": 0.8,
                    "max_tokens": 500,
                },
            )
            print(f"[AI] 响应状态码: {response.status_code}", flush=True)
            sys.stdout.flush()
            response.raise_for_status()
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
            print(f"[AI] 回复成功: {reply[:50]}...", flush=True)
            return reply
        except httpx.HTTPStatusError as exc:
            print(f"[AI] HTTP错误: {exc.response.status_code}", flush=True)
            print(f"[AI] 错误详情: {exc.response.text[:500]}", flush=True)
            sys.stdout.flush()

            if exc.response.status_code in (401, 403):
                raise AIServiceError(
                    401,
                    f"{AI_PROVIDER_LABEL} API Key 无效或已过期，请更新 backend/.env 中的 AI_API_KEY",
                    exc.response.text[:500],
                ) from exc

            raise AIServiceError(
                502,
                f"上游 AI 服务调用失败（HTTP {exc.response.status_code}）",
                exc.response.text[:500],
            ) from exc
        except Exception as exc:
            print(f"[AI] 异常: {str(exc)}", flush=True)
            sys.stdout.flush()
            if isinstance(exc, AIServiceError):
                raise
            raise AIServiceError(502, "老祖暂时无法回应，请稍后再试。", str(exc)[:500]) from exc
