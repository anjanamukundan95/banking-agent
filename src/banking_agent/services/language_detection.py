import logging

from azure.ai.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential

from banking_agent.config import settings

logger = logging.getLogger(__name__)

_client: TextAnalyticsClient | None = None

_SUPPORTED_LANGUAGES = {"en", "ar"}


def _get_client() -> TextAnalyticsClient:
    global _client
    if _client is None:
        _client = TextAnalyticsClient(
            settings.language_endpoint,
            DefaultAzureCredential(),
        )
    return _client


def detect_language(text: str) -> str:
    """
    Detect the language of the input text.
    Returns ISO 639-1 code e.g. 'en', 'ar'.
    Falls back to 'en' if detection fails or language is unsupported.
    """
    client = _get_client()

    results = client.detect_language(documents=[{"id": "1", "text": text}])
    result = results[0]

    if result.is_error:
        logger.warning("Language detection failed: %s — defaulting to en", result.error)
        return "en"

    lang = result.primary_language.iso6391_name
    confidence = result.primary_language.confidence_score

    logger.debug("Detected language: %s (confidence=%.2f)", lang, confidence)

    if lang not in _SUPPORTED_LANGUAGES:
        logger.warning("Unsupported language detected: %s — defaulting to en", lang)
        return "en"

    return lang

