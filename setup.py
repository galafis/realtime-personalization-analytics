from setuptools import setup, find_packages

setup(
    name="banking-analytics-gcp-looker",
    version="1.0.0",
    description="Banking Analytics Dashboard using GCP BigQuery and Looker Studio",
    author="BRQ Digital Solutions",
    author_email="contact@brq.com",
    packages=find_packages(),
    install_requires=[
        "google-cloud-bigquery>=3.10.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "plotly>=5.14.0",
        "streamlit>=1.22.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial Services",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

