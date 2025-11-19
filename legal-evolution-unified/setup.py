"""
Setup configuration for Legal Evolution Unified
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="legal-evolution-unified",
    version="1.0.0",
    author="Legal Evolution Unified Project",
    author_email="adrianlerer@example.com",
    description="Integrated platform for legal concept evolution analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adrianlerer/legal-evolution-unified",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scipy>=1.10.0",
        "scikit-learn>=1.3.0",
        "networkx>=3.1",
        "python-louvain>=0.16",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "plotly>=5.14.0",
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "pydantic>=2.5.0",
        "neo4j>=5.14.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "jupyter>=1.0.0",
        ],
        "viz": [
            "dash>=2.10.0",
            "dash-bootstrap-components>=1.4.0",
            "kaleido>=0.2.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "legal-evolution=src.api.main:main",
        ],
    },
)
