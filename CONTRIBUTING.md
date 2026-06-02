# Contributing to CivicPulse

## Getting Started
1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Run tests
6. Submit a PR

## Development Setup
```bash
git clone https://github.com/YOUR_USERNAME/civic-pulse.git
cd civic-pulse
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest
```

## Code Style
- Black (line length 100)
- isort for imports
- Ruff for linting
- Type hints required

## Commit Format
```
feat: add new service category endpoint
fix: resolve race condition in request processing
docs: update API reference
test: add integration tests
```

## License
MIT License
