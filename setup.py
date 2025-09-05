from setuptools import setup, find_packages
import os


version_path = os.path.join(os.path.dirname(file), "src", "PyDGuard", "version.py")
with open(version_path, "r", encoding="utf-8") as f:
    exec(f.read())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="PyDGuard",
    version=version,
    author="AmirAliMortazavi",
    author_email="amirali138mor@gmail.com",
    description="Smart Dependency Analyzer and Upgrade Advisor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amirali138m/pyDGuard",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pydguard=PyDGuard.cli:main",
        ],
    },
    python_requires=">=3.10",
)
