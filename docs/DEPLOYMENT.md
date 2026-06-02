# CivicPulse Deployment Guide

## Quick Start (Docker)
```bash
git clone https://github.com/meysisuas-wq/civic-pulse.git
cd civic-pulse
cp .env.example .env
./scripts/deploy.sh
```

## Manual Deployment
```bash
# Database
sudo -u postgres createdb civicpulse
alembic upgrade head

# Server
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Monitoring
```bash
curl http://localhost:8000/health
docker-compose logs -f api | jq .
```

## Backup
```bash
pg_dump -U civic civicpulse > backup_$(date +%Y%m%d).sql
```

## Troubleshooting
| Issue | Solution |
|-------|----------|
| DB connection refused | Check PostgreSQL and .env credentials |
| Redis connection failed | Verify Redis running on configured port |
| Migration errors | Run alembic upgrade head |
