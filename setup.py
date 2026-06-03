from setuptools import setup, find_packages

setup(
    name="civic-pulse",
    version="1.0.0",
    description="Intelligent Public Service Infrastructure",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="CivicPulse Team",
    author_email="team@civicpulse.go.id",
    url="https://github.com/meysisuas-wq/civic-pulse",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=["fastapi>=0.115.0", "uvicorn[standard]>=0.32.0", "pydantic>=2.10.0",
                      "sqlalchemy>=2.0.35", "alembic>=1.14.0", "asyncpg>=0.30.0",
                      "redis>=5.2.0", "python-jose[cryptography]>=3.3.0", "passlib[bcrypt]>=1.7.4"],
)
