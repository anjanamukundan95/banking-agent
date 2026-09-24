import math


def recall_at_k(
    retrieved: list[str],
    relevant: set[str],
    k: int,
) -> float:
    if not relevant:
        return 0.0

    retrieved_at_k = set(retrieved[:k])

    return len(retrieved_at_k & relevant) / len(relevant)


def reciprocal_rank(
    retrieved: list[str],
    relevant: set[str],
) -> float:
    for rank, source in enumerate(retrieved, start=1):
        if source in relevant:
            return 1.0 / rank

    return 0.0


def ndcg_at_k(
    retrieved: list[str],
    relevant: set[str],
    k: int,
) -> float:
    retrieved_at_k = retrieved[:k]

    dcg = 0.0

    for rank, source in enumerate(retrieved_at_k, start=1):
        if source in relevant:
            dcg += 1.0 / math.log2(rank + 1)

    ideal_hits = min(len(relevant), k)

    if ideal_hits == 0:
        return 0.0

    idcg = sum(
        1.0 / math.log2(rank + 1)
        for rank in range(1, ideal_hits + 1)
    )

    return dcg / idcg

def precision_at_k(
    retrieved: list[str],
    relevant: set[str],
    k: int,
) -> float:
    if k <= 0:
        return 0.0

    retrieved_at_k = retrieved[:k]

    if not retrieved_at_k:
        return 0.0

    relevant_retrieved = sum(
        1
        for source in retrieved_at_k
        if source in relevant
    )

    return relevant_retrieved / len(retrieved_at_k)