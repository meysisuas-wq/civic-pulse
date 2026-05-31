from typing import Dict, Any, List
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, func
import structlog
from src.models.request import ServiceRequest
from src.core.cache import get_cache, set_cache

logger = structlog.get_logger()

class AnalyticsService:
    async def get_dashboard_data(self, db) -> Dict[str, Any]:
        cache_key = "analytics:dashboard"
        cached = await get_cache(cache_key)
        if cached: return cached
        data = {
            "daily_requests": await self._get_daily_requests(db),
            "top_services": await self._get_top_services(db),
            "status_distribution": await self._get_status_distribution(db),
            "avg_response_time": await self._get_avg_response_time(db),
        }
        await set_cache(cache_key, data, ttl=300)
        return data

    async def _get_daily_requests(self, db, days: int = 30) -> List[Dict]:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        result = await db.execute(select(func.date(ServiceRequest.created_at).label("date"),
            func.count().label("count")).where(ServiceRequest.created_at >= cutoff)
            .group_by(func.date(ServiceRequest.created_at)))
        return [{"date": str(r.date), "count": r.count} for r in result.all()]

    async def _get_top_services(self, db, limit: int = 10) -> List[Dict]:
        from src.models.service import Service
        result = await db.execute(select(Service.name, Service.total_requests)
            .order_by(Service.total_requests.desc()).limit(limit))
        return [{"name": r.name, "requests": r.total_requests} for r in result.all()]

    async def _get_status_distribution(self, db) -> Dict[str, int]:
        result = await db.execute(select(ServiceRequest.status, func.count()).group_by(ServiceRequest.status))
        return {r.status.value: r.count for r in result.all()}

    async def _get_avg_response_time(self, db) -> float:
        result = await db.execute(select(func.avg(
            func.extract("epoch", ServiceRequest.completed_at - ServiceRequest.submitted_at) / 3600))
            .where(ServiceRequest.completed_at.isnot(None)))
        return round(result.scalar() or 0.0, 2)

analytics_service = AnalyticsService()
