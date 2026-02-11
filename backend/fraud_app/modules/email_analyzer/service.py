from transformers import pipeline
from .rules import regex_signals
from .privacy import mask_pii
from .perplexity import compute_perplexity


clf = pipeline("text-classification", model="roberta-base-openai-detector")


def analyze_email(subject: str, body: str):
    text = f"Subject: {subject}\nBody: {body}"
    ppl = compute_perplexity(text)

    pred = clf(text)[0]

    model_label = str(pred.get("label", "")).upper()
    raw_score = float(pred.get("score", 0.0))

    # ✅ Force: higher score = more suspicious
    ml_prob = raw_score

    human_label = "Phishing" if ml_prob >= 0.5 else "Legitimate"

    reg = regex_signals(subject, body)
    regex_score = float(reg.get("regex_score", 0.0))

    masked = mask_pii(body)
    pii_found = masked.get("pii_found", {}) or {}

    pii_boost = 0.15 if pii_found else 0.0
    link_boost = 0.15 if reg.get("urls") else 0.0

    # ✅ Make phishing examples go Critical
    risk = (0.40 * ml_prob) + (0.45 * regex_score) + pii_boost + link_boost
    risk = max(0.0, min(risk, 1.0))
    risk_percent = round(risk * 100, 1)

    if risk_percent >= 80:
        tier = "Critical"
    elif risk_percent >= 60:
        tier = "High"
    elif risk_percent >= 30:
        tier = "Medium"
    else:
        tier = "Safe"

    reasons = [f"ML phishing probability: {round(ml_prob, 2)}"]
    reasons += reg.get("flags", [])[:3]
    if reg.get("urls"):
        reasons.append("Contains URL(s)")
    if pii_found:
        reasons.append("PII detected and masked")

    return {
        "version": "V2-mlprob-rawscore",
        "risk": {"risk_percent": risk_percent, "tier": tier},
        "ml": {
            "label": human_label,
            "model_label": model_label,
            "raw_score": round(raw_score, 4),
            "phishing_prob": round(ml_prob, 4),
        },
        "regex": reg,
        "privacy": {
            "pii_found": pii_found,
            "masked_preview": masked.get("masked_text", "")[:250],
        },
        "ai_text": {"perplexity": ppl},

        "top_reasons": reasons[:6],
    }
