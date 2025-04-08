from typing import List
from google import generativeai as genai
import openai

# ------------------------------
# OpenAI
# ------------------------------
class OpenAIClient:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def suggest(self, history: List[str], limit: int = 5) -> List[str]:
        prompt = self._build_prompt(history, limit)
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You're an assistant that helps users reuse their terminal commands efficiently."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        result = response.choices[0].message["content"]
        return self._parse_output(result, limit)

    def _build_prompt(self, history: List[str], limit: int) -> str:
        joined = "\n".join(history[-200:])
        return f"""Here is my terminal history:

{joined}

Based on the patterns, suggest {limit} commands I may want to reuse next. Just list them plainly, no extra text."""

    def _parse_output(self, text: str, limit: int) -> List[str]:
        lines = [line.strip("-• ").strip() for line in text.splitlines() if line.strip()]
        return lines[:limit]


# ------------------------------
# Gemini
# ------------------------------
class GeminiClient:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name="gemini-2.0-flash")

    def suggest(self, history: list[str], num_suggestions: int = 5) -> list[str]:
        """
        Analyzes command history and suggests commands using Gemini.

        Args:
            history: A list of past commands.
            num_suggestions: The exact number of suggestions to request.

        Returns:
            A list of suggested command strings.
        """
        if not history:
            return []

        joined_history = "\n".join(history)

        # --- 프롬프트 수정 ---
        # {limit} 대신 명시적으로 num_suggestions 변수 사용
        prompt = f"""You are an assistant that analyzes a list of terminal commands from a user's history.

Here is the list of real terminal commands the user previously ran:
{joined_history}

Based *only* on this list, recommend exactly {num_suggestions} distinct real terminal commands that the user might want to reuse or run next.
Focus on commands that appear frequently or seem part of a common workflow.
Do not generate new commands, variations, or guess the context. Strictly select commands from the provided list.
Do not include explanations, numbering, introductory phrases like "Here are the recommendations:", or any words other than the commands themselves.
Output each command on a new line. If you cannot find {num_suggestions} suitable commands from the list, return fewer, but only return commands directly from the list."""
        # --- --- --- --- ---

        try:
            # Gemini 호출 방식에 맞게 수정 (정확한 API 호출은 라이브러리 버전에 따라 다를 수 있음)
            response = self.model.generate_content(prompt)

            # 응답 텍스트 처리 (Gemini 응답 구조에 맞게 조정 필요)
            # 예시: response.text 또는 response.parts[0].text 등
            raw_suggestions = response.text.strip()

            # 응답이 비어있거나 예상치 못한 텍스트일 경우 빈 리스트 반환
            if not raw_suggestions or "cannot recommend" in raw_suggestions.lower():
                 return []

            # 줄바꿈으로 분리하여 리스트 생성
            suggestions = [line.strip() for line in raw_suggestions.splitlines() if line.strip()]
            return suggestions[:num_suggestions] # 혹시 LLM이 더 많이 반환할 경우 대비

        except Exception as e:
            print(f"Error calling Gemini API: {e}") # 실제로는 로깅 사용 권장
            return []


def get_llm(provider: str, api_key: str):
    if provider == "openai":
        return OpenAIClient(api_key)
    elif provider == "gemini":
        return GeminiClient(api_key)
    else:
        raise NotImplementedError(f"지원하지 않는 provider입니다: {provider}")
    
    