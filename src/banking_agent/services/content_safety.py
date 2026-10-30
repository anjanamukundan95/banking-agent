import logging

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.identity import DefaultAzureCredential

from banking_agent.config import settings

logger = logging.getLogger(__name__)

_client: ContentSafetyClient | None = None


def _get_client() -> ContentSafetyClient:
    global _client

    if not settings.content_safety_endpoint:
        raise RuntimeError("CONTENT_SAFETY_ENDPOINT is mandatory")

    if _client is None:
        _client = ContentSafetyClient(
            settings.content_safety_endpoint,
            DefaultAzureCredential(),
        )

    return _client


def check_text(text: str) -> dict:
    client = _get_client()

    response = client.analyze_text(
        AnalyzeTextOptions(
            text=text,
            categories=[
                TextCategory.HATE,
                TextCategory.VIOLENCE,
                TextCategory.SEXUAL,
                TextCategory.SELF_HARM,
            ],
        )
    )

    flagged = [item for item in response.categories_analysis if item.severity >= 2]

    if flagged:
        reasons = ", ".join(
            f"{item.category}(severity={item.severity})" for item in flagged
        )

        logger.warning("Content Safety blocked text — %s", reasons)

        return {"blocked": True, "reason": reasons}

    return {"blocked": False, "reason": None}
