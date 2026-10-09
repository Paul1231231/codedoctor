from codedoctor.llm.models import ModelName


def select_model(complexity: str) -> ModelName:

    if complexity == "simple":
        return ModelName.CODEDOCTOR_QWEN

    return ModelName.CODEDOCTOR_QWEN

def classify_complexity(code: str, error: str) -> str:
    score = 0
    if len(code) > 3000:
        score += 1

    if "async" in code:
        score += 1

    if "concurrent" in code:
        score += 1

    if "race condition" in error.lower():
        score += 2

    if score >= 2:
        return "complex"

    return "simple"