# setup.py

from setuptools import setup, find_packages

setup(
    name="reterm-ai",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "typer",
        "python-dotenv",
        "openai",
        "google-generativeai",
    ],
    entry_points={
        "console_scripts": [
            "reterm=reterm.cli:app",  # 여기서 'app'은 cli.py 안의 Typer 객체
        ],
    },
    author="pie0902",
    description="AI-powered terminal command recommender based on your shell history",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="Apache-2.0",

    url="https://github.com/pie0902/reTermAI",  # 📦 GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
