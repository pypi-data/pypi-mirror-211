from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="PyBaseConfig",
    version="0.1.0",
    description="Ein Python-Paket zur Verwaltung Ihrer Umgebungsvariablen.",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)