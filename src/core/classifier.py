from typing import Dict, List, Tuple
import re, structlog

logger = structlog.get_logger()

URGENCY_KEYWORDS = {
    "critical": ["emergency", "life-threatening", "danger", "darurat"],
    "urgent": ["urgent", "immediate", "asap", "segera", "mendesak"],
    "high": ["important", "priority", "penting"],
}

CATEGORY_KEYWORDS = {
    "civil-registration": ["birth", "death", "marriage", "certificate", "kelahiran"],
    "land-property": ["land", "property", "building", "tanah", "sertifikat"],
    "business-licensing": ["business", "permit", "license", "usaha", "izin"],
    "social-services": ["social", "welfare", "assistance", "sosial", "bantuan"],
    "health-services": ["health", "medical", "insurance", "kesehatan"],
    "education": ["education", "school", "scholarship", "pendidikan"],
}

class RequestClassifier:
    def classify_urgency(self, text: str) -> str:
        text_lower = text.lower()
        for level, keywords in URGENCY_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return level
        return "normal"

    def classify_category(self, text: str) -> List[Tuple[str, float]]:
        text_lower = text.lower()
        scores = {}
        for category, keywords in CATEGORY_KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches > 0:
                scores[category] = matches / len(keywords)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    async def classify(self, subject: str, description: str, form_data: dict) -> Dict:
        text = f"{subject} {description}"
        urgency = self.classify_urgency(text)
        categories = self.classify_category(text)
        return {"urgency": urgency, "primary_category": categories[0][0] if categories else "general",
                "confidence": categories[0][1] if categories else 0.0}

classifier = RequestClassifier()
