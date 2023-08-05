from setuptools import setup, find_packages
import pathlib

# Get the base directory
here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="cost-of-code",
    version="0.1.2",
    author="Souradeep Nanda",
    description="How much would it have cost if GPT-4 had written your code?",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ghost---Shadow/cost-of-code",
    packages=find_packages(),
    install_requires=["GitPython", "tiktoken", "pathspec"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        "console_scripts": [
            "cost-of-code = cost_of_code.main:main",
        ]
    },
)
