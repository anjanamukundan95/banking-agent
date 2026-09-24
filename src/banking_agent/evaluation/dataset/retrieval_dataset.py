from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalTestCase:
    query: str
    relevant_sources: tuple[str, ...]


RETRIEVAL_TEST_CASES = (
    RetrievalTestCase(
        query="What fees can apply to international card transactions?",
        relevant_sources=(
            "fees.md",
            "internal_transactions.md",
        ),
    ),
    RetrievalTestCase(
        query="What happens when I make a card purchase outside the UAE?",
        relevant_sources=(
            "internal_transactions.md",
            "fees.md",
        ),
    ),
    RetrievalTestCase(
        query="What should I do if my card is lost or stolen?",
        relevant_sources=(
            "cards.md",
        ),
    ),
    RetrievalTestCase(
        query="What documents are required to open a bank account?",
        relevant_sources=(
            "accounts.md",
            "kyc.md",
        ),
    ),
    RetrievalTestCase(
        query="How can I raise a banking complaint?",
        relevant_sources=(
            "complaints.md",
        ),
    ),
)