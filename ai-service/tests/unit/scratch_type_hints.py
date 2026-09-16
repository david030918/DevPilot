from pydantic import ValidationError

from app.models.investigation import IssueContext, PossibleCause


def build_investigation_input(
    title: str, body: str | None, assumptions: list[str], metadata: dict[str, str | int]
) -> dict[str, str | None | list[str] | dict[str, str | int]]:
    return {
        "title": title,
        "body": body,
        "assumptions": assumptions,
        "metadata": metadata,
    }


def test_build_investigation_input():
    valid_issue_data = {
        "number": 42,
        "title": "Investigation fails",
    }

    invalid_issue_data = {
        "number": "not-a-number",
        "title": "Investigation fails",
    }

    invalid_cause_data = {
        "title": "Configuration issue",
        "explanation": "Configuration may be incorrect.",
        "confidence": 5.0,
    }

    issueContext = IssueContext(
        title=valid_issue_data["title"], number=valid_issue_data["number"]
    )

    print(issueContext.number)
    print(issueContext.title)
    print(issueContext.body)

    serializes_issue_context = issueContext.model_dump()
    print(serializes_issue_context)

    try:
        issueOossibleCauseCheck = PossibleCause(
            title=invalid_cause_data["title"],
            explanation=invalid_cause_data["explanation"],
            confidence=invalid_cause_data["confidence"],
        )
    except ValidationError as e:
        print(f"An error occurred: {e}")

    try:
        issueContextCheck = IssueContext(
            title=invalid_issue_data["title"], number=invalid_issue_data["number"]
        )
    except ValidationError as e:
        print(f"An error occurred: {e}")
