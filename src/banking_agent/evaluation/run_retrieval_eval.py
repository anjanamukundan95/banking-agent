from banking_agent.evaluation.dataset.retrieval_dataset import RETRIEVAL_TEST_CASES
from banking_agent.evaluation.retrieval import (
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)
from banking_agent.models.rag import KnowledgeSearchRequest
from banking_agent.services.rag import search_knowledge


def main():
    recall_scores = []
    precision_at_1_scores = []
    precision_at_3_scores = []
    precision_at_5_scores = []
    reciprocal_rank_scores = []
    ndcg_scores = []

    for test_case in RETRIEVAL_TEST_CASES:
        response = search_knowledge(
            KnowledgeSearchRequest(
                query=test_case.query,
                top_k=3,
            )
        )

        retrieved = [result.title for result in response.results]

        relevant = set(test_case.relevant_sources)

        recall_scores.append(recall_at_k(retrieved, relevant, 3))

        reciprocal_rank_scores.append(reciprocal_rank(retrieved, relevant))

        ndcg_scores.append(ndcg_at_k(retrieved, relevant, 3))

        # precision_at_1_scores.append(precision_at_k(retrieved, relevant, 1))
        precision_at_3_scores.append(precision_at_k(retrieved, relevant, 3))
        # precision_at_5_scores.append(precision_at_k(retrieved, relevant, 5))

        print(f"\nQuery: {test_case.query}")
        print(f"Retrieved: {retrieved}")

    print("\n========== RETRIEVAL EVALUATION ==========")

    print(f"Recall@5: {sum(recall_scores) / len(recall_scores):.3f}")

    print(f"MRR: {sum(reciprocal_rank_scores) / len(reciprocal_rank_scores):.3f}")

    print(f"NDCG@5: {sum(ndcg_scores) / len(ndcg_scores):.3f}")

    # print(f"Precision@1: {sum(precision_at_1_scores) / len(precision_at_1_scores):.3f}")
    print(f"Precision@3: {sum(precision_at_3_scores) / len(precision_at_3_scores):.3f}")
    # print(f"Precision@5: {sum(precision_at_5_scores) / len(precision_at_5_scores):.3f}")


if __name__ == "__main__":
    main()
