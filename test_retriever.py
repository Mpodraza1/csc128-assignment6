"""Retrieval and refusal tests for the grounded attendance bot."""

from retriever import Retriever


SHOULD_RETRIEVE = [
    (
        "What work am I responsible for if I miss class?",
        "attendance_missed_work",
    ),
    (
        "Where can I find my instructor's attendance rules?",
        "attendance_syllabus",
    ),
    (
        "Can I start attending a class after the 10 percent date?",
        "attendance_late_entry",
    ),
    (
        "How many excused absences each academic year are allowed "
        "for religious observances required by faith?",
        "attendance_religious_days",
    ),
    (
        "When do I give my instructor a written request for a "
        "religious absence?",
        "attendance_religious_request",
    ),
    (
        "How do I make up work missed for a religious observance?",
        "attendance_makeup_work",
    ),
    (
        "Are reserve active-duty or National Guard students eligible "
        "for absences because of military operations?",
        "attendance_military",
    ),
    (
        "Who should I contact and what should I bring for "
        "military absences?",
        "attendance_military_steps",
    ),
]


SHOULD_REFUSE = [
    "Does attendance change my final grade?",
    "Can I appeal an attendance decision?",
    "Are online courses required to record attendance?",
    "Can my parent view my attendance?",
    "Will an absence lower my grade?",
]


def print_score_evidence():
    """Print the best score for every test question."""
    probe = Retriever(threshold=-1.0)

    print("SCORE EVIDENCE")
    print("\nQuestions that should retrieve:")

    for question, expected_id in SHOULD_RETRIEVE:
        hits = probe.search(question, top_k=1)
        document, score = hits[0]
        print(
            f"{score:.3f} | expected {expected_id} | "
            f"found {document['id']}"
        )

    print("\nQuestions that should be refused:")

    for question in SHOULD_REFUSE:
        hits = probe.search(question, top_k=1)
        document, score = hits[0]
        print(f"{score:.3f} | {question}")


def run_tests():
    """Run eight retrieval tests and five refusal tests."""
    retriever = Retriever()
    passed = 0
    total = len(SHOULD_RETRIEVE) + len(SHOULD_REFUSE)

    for question, expected_id in SHOULD_RETRIEVE:
        hits = retriever.search(question)
        assert hits, f"Expected retrieval for: {question}"
        assert hits[0][0]["id"] == expected_id, (
            f"Wrong result for: {question}"
        )
        passed += 1

    for question in SHOULD_REFUSE:
        hits = retriever.search(question)
        assert hits == [], f"Expected refusal for: {question}"
        passed += 1

    print(f"\nPASS: {passed}/{total} retrieval tests")


if __name__ == "__main__":
    print_score_evidence()
    run_tests()
