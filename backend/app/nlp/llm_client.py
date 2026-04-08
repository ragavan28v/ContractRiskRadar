import json
import logging
from typing import Any

import httpx

from ..core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are a senior contract risk analyst AI specialized in commercial agreements.

For the given clause:
- Identify clause type.
- Detect unfair or risky patterns.
- Highlight trigger phrases.
- Assign risk level.
- Provide a risk score (0–100).
- Explain why risky.
- Suggest a safer rewrite.
- Provide negotiation advice.

IMPORTANT: Return ONLY valid JSON with no markdown, no code blocks, no extra text.

JSON Structure:
{
  "clause_type": "string",
  "risk_detected": boolean,
  "risk_level": "High|Moderate|Low",
  "risk_category": "string",
  "risk_score": number,
  "why_risky": "string",
  "trigger_phrases": ["string"],
  "financial_exposure": "string",
  "power_imbalance": "string",
  "safer_alternative": "string",
  "negotiation_tip": "string",
  "confidence_score": number
}

Do not hallucinate laws.
Base reasoning strictly on provided text.
Return ONLY the JSON object. No markdown. No extra text.
"""

USER_TEMPLATE = """
Analyze this clause:

\"\"\"{clause_text}\"\"\"

Return structured JSON.
"""


async def analyze_clause_via_llm(clause_text: str) -> dict[str, Any]:
    # If no LLM API key is configured, use a local heuristic rule-based analyzer
    api_key = settings.GROQ_API_KEY if settings.LLM_PROVIDER == "groq" else settings.OPENAI_API_KEY
    if not api_key:
        logger.warning("⚠️  No LLM API key found. Using FALLBACK HEURISTIC keyword-based scoring.")
        logger.info(f"   Provider: {settings.LLM_PROVIDER} | API Key: {settings.GROQ_API_KEY or settings.OPENAI_API_KEY or 'None'}")
        text = clause_text.lower()
        high_keywords = ["indemnif", "unlimited liability", "without limit", "sole discretion", "waive", "forfeit", "penalty", "breach", "terminate for convenience"]
        low_keywords = ["mutual", "cap", "limited liability", "governing law", "notice", "reasonable"]

        score = 50
        found_triggers = []

        for kw in high_keywords:
            if kw in text:
                score += 30
                found_triggers.append(kw)
        for kw in low_keywords:
            if kw in text:
                score -= 20
                found_triggers.append(kw)

        # clamp
        score = max(0, min(100, score))

        if score >= 70:
            level = "High"
            category = "Severe Exposure"
            detected = True
        elif score >= 40:
            level = "Moderate"
            category = "Ambiguous Language"
            detected = True
        else:
            level = "Low"
            category = "Standard"
            detected = False

        return {
            "clause_type": "General",
            "risk_detected": detected,
            "risk_level": level,
            "risk_category": category,
            "risk_score": float(score),
            "why_risky": "".join([f"Contains trigger: {t}; " for t in found_triggers]) or "No significant risky phrases found.",
            "trigger_phrases": found_triggers,
            "financial_exposure": "",
            "power_imbalance": "",
            "safer_alternative": "Consider rephrasing to limit exposure and add caps or objective standards.",
            "negotiation_tip": "Negotiate caps, specific obligations, and limits to liability.",
            "confidence_score": 0.5,
        }

    # Select endpoint based on provider
    if settings.LLM_PROVIDER == "groq":
        url = "https://api.groq.com/openai/v1/chat/completions"
        api_key = settings.GROQ_API_KEY
        logger.info(f"✅ Using GROQ Cloud | Model: {settings.LLM_MODEL_NAME}")
    else:
        url = "https://api.openai.com/v1/chat/completions"
        api_key = settings.OPENAI_API_KEY
        logger.info(f"✅ Using OPENAI | Model: {settings.LLM_MODEL_NAME}")
    
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": settings.LLM_MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT.strip()},
            {"role": "user", "content": USER_TEMPLATE.format(clause_text=clause_text)},
        ],
        "temperature": 0.2,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        try:
            resp = await client.post(url, headers=headers, json=payload)
            logger.debug(f"Groq response status: {resp.status_code}")
            resp.raise_for_status()
            
            # Parse response
            resp_data = resp.json()
            logger.debug(f"Groq response keys: {resp_data.keys()}")
            
            if "choices" not in resp_data or not resp_data["choices"]:
                logger.error(f"❌ Invalid Groq response structure: {resp_data}")
                raise ValueError("No choices in Groq response")
            
            content = resp_data["choices"][0]["message"]["content"]
            logger.info(f"✅ Received Groq response: {len(content)} chars")
            
            # Parse JSON from content
            result = json.loads(content)
            return result
        except json.JSONDecodeError as je:
            logger.error(f"❌ Failed to parse LLM response as JSON: {str(je)}. Response: {content if 'content' in locals() else 'N/A'}")
            raise
        except Exception as e:
            logger.error(f"❌ LLM API call failed: {type(e).__name__}: {str(e)}. Falling back to heuristic logic.")
            # Fall back to heuristic
            text = clause_text.lower()
            high_keywords = ["indemnif", "unlimited liability", "without limit", "sole discretion", "waive", "forfeit", "penalty", "breach", "terminate for convenience"]
            low_keywords = ["mutual", "cap", "limited liability", "governing law", "notice", "reasonable"]

            score = 50
            found_triggers = []

            for kw in high_keywords:
                if kw in text:
                    score += 30
                    found_triggers.append(kw)
            for kw in low_keywords:
                if kw in text:
                    score -= 20
                    found_triggers.append(kw)

            score = max(0, min(100, score))

            if score >= 70:
                level = "High"
                category = "Severe Exposure"
                detected = True
            elif score >= 40:
                level = "Moderate"
                category = "Ambiguous Language"
                detected = True
            else:
                level = "Low"
                category = "Standard"
                detected = False

            return {
                "clause_type": "General",
                "risk_detected": detected,
                "risk_level": level,
                "risk_category": category,
                "risk_score": float(score),
                "why_risky": "".join([f"Contains trigger: {t}; " for t in found_triggers]) or "No significant risky phrases found.",
                "trigger_phrases": found_triggers,
                "financial_exposure": "",
                "power_imbalance": "",
                "safer_alternative": "Consider rephrasing to limit exposure and add caps or objective standards.",
                "negotiation_tip": "Negotiate caps, specific obligations, and limits to liability.",
                "confidence_score": 0.5,
            }

