import re
from typing import Dict, Any

import spacy

# load once
_nlp = spacy.load("en_core_web_sm")

EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_REGEX = re.compile(r"\b(?:\+?\d{1,3}[- ]?)?\d{10}\b")
OTP_REGEX = re.compile(r"\b\d{4,6}\b")

NER_LABELS_TO_MASK = {"PERSON", "ORG", "GPE", "LOC", "MONEY", "DATE"}

def mask_pii(text: str) -> Dict[str, Any]:
    found = {
        "emails": EMAIL_REGEX.findall(text),
        "phones": PHONE_REGEX.findall(text),
        "otps": OTP_REGEX.findall(text),
    }

    masked = text
    masked = EMAIL_REGEX.sub("[EMAIL]", masked)
    masked = PHONE_REGEX.sub("[PHONE]", masked)
    masked = OTP_REGEX.sub("[OTP]", masked)

    # spaCy NER masking
    doc = _nlp(masked)
    ner_found = {}
    # replace entities from back to front to preserve indices
    ents = [e for e in doc.ents if e.label_ in NER_LABELS_TO_MASK]
    for ent in reversed(ents):
        ner_found.setdefault(ent.label_, [])
        if len(ner_found[ent.label_]) < 5:
            ner_found[ent.label_].append(ent.text)
        masked = masked[:ent.start_char] + f"[{ent.label_}]" + masked[ent.end_char:]

    pii_found = {k: list(set(v))[:5] for k, v in found.items() if v}
    if ner_found:
        pii_found["ner_entities"] = ner_found

    return {"masked_text": masked, "pii_found": pii_found}
