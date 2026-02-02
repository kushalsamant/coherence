"""
Setup script for shared-backend package
Note: Directory name has hyphen but Python imports use underscore.
This setup.py installs the package so it can be imported as 'shared_backend'.
"""

from setuptools import setup
from pathlib import Path

# Get all subdirectories that are Python packages
base_dir = Path(__file__).parent

# Build package list manually to handle hyphenated directory names
packages = ["shared_backend"]
package_dir_map = {"shared_backend": "."}

# Find all subpackages and map hyphenated directory names
for item in base_dir.iterdir():
    if item.is_dir() and item.name not in ["__pycache__", ".git"] and (item / "__init__.py").exists():
        # Convert hyphen to underscore for Python package name
        pkg_name = item.name.replace("-", "_")
        full_pkg_name = f"shared_backend.{pkg_name}"
        packages.append(full_pkg_name)
        # Map subpackage: if directory has hyphen, map the underscore name to the hyphen directory
        if "-" in item.name:
            package_dir_map[full_pkg_name] = item.name

setup(
    name="shared-backend",
    version="1.0.0",
    description="Shared backend utilities for KVSHVL platform",
    author="Kushal Samant",
    # Map the hyphenated directory name to underscore import name
    package_dir=package_dir_map,
    packages=packages,
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

