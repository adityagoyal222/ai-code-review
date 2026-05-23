import json
from pathlib import Path

from app.config import get_settings
from app.rag.review import review_code


def main() -> None:
    settings = get_settings()
    cases_path = Path("eval/sample_cases.jsonl")

    if not cases_path.exists():
        raise FileNotFoundError("Missing eval/sample_cases.jsonl")

    with cases_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            case = json.loads(line)
            review = review_code(
                settings,
                code=case["code"],
                language=case.get("language"),
            )
            print("=" * 40)
            print(case["id"])
            print(review)


if __name__ == "__main__":
    main()
