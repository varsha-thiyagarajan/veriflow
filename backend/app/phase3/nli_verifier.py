import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_NAME = "cross-encoder/nli-deberta-v3-base"

_tokenizer = None
_model = None


def load_model():
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        _model.eval()

    return _tokenizer, _model


def verify_claim(claim: str, evidence: str) -> dict:
    """
    Verify whether evidence supports, contradicts, or is neutral
    to the given claim using DeBERTa-v3 NLI.
    """

    tokenizer, model = load_model()

    inputs = tokenizer(
        evidence,
        claim,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=-1)[0]

    id2label = {
        0: "contradiction",
        1: "entailment",
        2: "neutral"
    }

    scores = {
        id2label[i]: round(float(probabilities[i]), 4)
        for i in range(len(probabilities))
    }

    label = max(scores, key=scores.get)

    return {
        "claim": claim,
        "evidence": evidence,
        "verdict": label,
        "entailment_probability": scores["entailment"],
        "neutral_probability": scores["neutral"],
        "contradiction_probability": scores["contradiction"],
    }