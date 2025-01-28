from setuptools import setup, find_packages


if __name__ == "__main__":
    setup(
        name="rsrt",
        version="0.0.1",
        author="Luca Vivona",
        author_email="lucavivona01@gmail.com",
        description="rsrt (Rust Return Types) A Python package for rustaceans sugar for return typing",
        long_description=open("README.md", encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        license="MIT",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        keywords=["result", "error-handling", "option", "utility"],
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        python_requires=">=3.9",
        install_requires=[
            "typing-extensions>=4.0.0; python_version<'3.10'"
        ],
        extras_require={
            "dev": [
                "pytest>=7.0.0",
                "flake8>=6.0.0",
                "pytest-cov>=4.0.0",
                "mypy>=1.0.0",
                "black>=23.0.0",
            ]
        }
    )