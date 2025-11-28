"""
Setup script for shared-backend package
"""

from setuptools import setup, find_packages

setup(
    name="shared-backend",
    version="1.0.0",
    description="Shared backend utilities for KVSHVL platform",
    author="Kushal Samant",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.109.0",
        "sqlalchemy>=2.0.36",
        "pydantic>=2.10.4",
        "pydantic-settings>=2.6.1",
        "python-jose[cryptography]>=3.3.0",
        "razorpay>=1.4.2",
        "python-dotenv>=1.0.0",
        "psycopg[binary]>=3.2.1",
    ],
    python_requires=">=3.11",
)

