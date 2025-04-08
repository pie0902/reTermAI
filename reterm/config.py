import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 자동 로드

def load_api_key(provider: str) -> str:
    """
    선택한 provider에 맞는 API 키를 환경변수에서 불러옵니다.
    """
    if provider == "openai":
        key = os.getenv("OPENAI_API_KEY")
    elif provider == "gemini":
        key = os.getenv("GOOGLE_API_KEY")
    else:
        raise ValueError(f"지원하지 않는 provider입니다: {provider}")

    if not key:
        raise EnvironmentError(f"{provider.upper()} API 키가 설정되어 있지 않습니다.")
    return key
