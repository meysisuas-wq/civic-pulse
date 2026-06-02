# CivicPulse Architecture

## Overview

CivicPulse follows a clean architecture pattern:

```
Presentation Layer (FastAPI Routes)
    ↓
Service Layer (CitizenService / WorkflowService)
    ↓
Core Layer (ProcessingEngine / Queue / Cache)
    ↓
Data Layer (SQLAlchemy / PostgreSQL / Redis)
```

## Key Design Decisions

1. **Async-First** — All I/O operations are async
2. **Event-Driven** — State machine with event-driven transitions
3. **Cache-Aside** — Redis cache with automatic invalidation
4. **Priority Queue** — Critical requests handled first
5. **GPU-Accelerated** — ML classification via AMD ROCm

## Data Flow

```
Citizen submits request
    → API validates (Pydantic)
    → Service creates record
    → Engine classifies priority (ML)
    → Queue assigns processor
    → Processor executes logic
    → Workflow updates status
    → Notification alerts citizen
```

## Security

- JWT authentication with short-lived tokens
- RBAC authorization
- TLS 1.3 + AES-256
- Input validation (Pydantic + custom)
- Rate limiting per IP/user
- Audit logging
