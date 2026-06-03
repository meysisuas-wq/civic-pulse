import asyncio
from datetime import datetime, timezone
from uuid import uuid4
from src.db.database import init_db, async_session
from src.models.service import ServiceCategory, Service
from src.models.user import Citizen
from src.api.auth import hash_password

CATEGORIES = [
    {"name": "Civil Registration", "slug": "civil-registration", "icon": "📋", "color": "#3B82F6"},
    {"name": "Land & Property", "slug": "land-property", "icon": "🏠", "color": "#10B981"},
    {"name": "Business Licensing", "slug": "business-licensing", "icon": "💼", "color": "#F59E0B"},
    {"name": "Social Services", "slug": "social-services", "icon": "🤝", "color": "#8B5CF6"},
    {"name": "Health Services", "slug": "health-services", "icon": "🏥", "color": "#EF4444"},
    {"name": "Education", "slug": "education", "icon": "🎓", "color": "#06B6D4"},
]

async def seed():
    await init_db()
    async with async_session() as db:
        cat_map = {}
        for cd in CATEGORIES:
            cat = ServiceCategory(**cd)
            db.add(cat)
            await db.flush()
            cat_map[cd["slug"]] = cat.id
        demo = Citizen(citizen_id="1234567890123456", email="demo@civicpulse.go.id",
                       full_name="Demo Citizen", hashed_password=hash_password("DemoPass123!"),
                       district="Central Jakarta", city="Jakarta", is_verified=True)
        db.add(demo)
        await db.commit()
        print("Database seeded!")

if __name__ == "__main__":
    asyncio.run(seed())
