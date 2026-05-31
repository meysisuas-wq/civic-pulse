from typing import Optional
from uuid import UUID
from datetime import datetime, timezone
import structlog
from src.models.user import Citizen
from src.api.auth import hash_password, verify_password, create_token_pair
from src.core.cache import get_cache, set_cache, delete_cache

logger = structlog.get_logger()

class CitizenService:
    async def register(self, db, data: dict) -> Citizen:
        citizen = Citizen(citizen_id=data["citizen_id"], email=data["email"], full_name=data["full_name"],
                          hashed_password=hash_password(data["password"]), address=data.get("address"),
                          district=data.get("district"), city=data.get("city"), province=data.get("province"))
        db.add(citizen)
        await db.flush()
        logger.info("citizen_registered", citizen_id=str(citizen.id))
        return citizen

    async def authenticate(self, db, email: str, password: str) -> dict:
        from sqlalchemy import select
        result = await db.execute(select(Citizen).where(Citizen.email == email))
        citizen = result.scalar_one_or_none()
        if not citizen or not verify_password(password, citizen.hashed_password):
            raise ValueError("Invalid credentials")
        citizen.last_login = datetime.now(timezone.utc)
        await db.flush()
        tokens = create_token_pair(citizen.id)
        return {**tokens, "citizen": citizen}

    async def get_by_id(self, db, citizen_id: UUID) -> Optional[Citizen]:
        cache_key = f"citizen:{citizen_id}"
        cached = await get_cache(cache_key)
        if cached: return cached
        citizen = await db.get(Citizen, citizen_id)
        if citizen:
            await set_cache(cache_key, {"id": str(citizen.id), "name": citizen.full_name})
        return citizen

citizen_service = CitizenService()
