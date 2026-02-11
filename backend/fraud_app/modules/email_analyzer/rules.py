import re
from typing import Dict, Any, List

URGENT_WORDS = [
    "urgent", "immediately", "suspend", "suspended", "verify", "action required",
    "account locked", "security alert", "limited time", "final warning"
]

CRED_WORDS = ["otp", "password", "pin", "cvv", "login", "credentials"]

URL_REGEX = re.compile(r"(https?://\S+|www\.\S+)", re.IGNORECASE)

def regex_signals(subject: str, body: str) -> Dict[str, Any]:
    text = f"{subject}\n{body}".lower()
    flags: List[str] = []
    score = 0.0

    urgent_hits = [w for w in URGENT_WORDS if w in text]
    if urgent_hits:
        flags.append(f"urgent_language({', '.join(urgent_hits[:3])})")
        score += 0.25

    cred_hits = [w for w in CRED_WORDS if w in text]
    if cred_hits:
        flags.append(f"credential_keywords({', '.join(cred_hits[:3])})")
        score += 0.25

    urls = URL_REGEX.findall(body)
    if urls:
        flags.append(f"contains_links(count={len(urls)})")
        score += 0.20
        if any("login" in u.lower() or "verify" in u.lower() for u in urls):
            flags.append("link_looks_like_login_or_verify")
            score += 0.10

    return {
        "regex_score": min(score, 1.0),
        "flags": flags,
        "urls": urls[:5]
    }
