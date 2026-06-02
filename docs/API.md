# CivicPulse API Reference

## Base URL
```
Production: https://api.civicpulse.go.id/v1
Local:      http://localhost:8000/api/v1
```

## Authentication
```http
Authorization: Bearer <access_token>
```

## Endpoints

### Citizens
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /citizens/register | Register new citizen |
| POST | /citizens/login | Authenticate citizen |
| GET | /citizens/me | Get current profile |

### Services
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /services | List all services |
| GET | /services/{id} | Get service details |

### Requests
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /requests | Submit new request |
| GET | /requests | List my requests |
| GET | /requests/{id} | Get request details |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /stats | Service statistics |

## Error Codes
| Status | Meaning |
|--------|---------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

## Rate Limits
- Anonymous: 100 req/min
- Authenticated: 200 req/min
