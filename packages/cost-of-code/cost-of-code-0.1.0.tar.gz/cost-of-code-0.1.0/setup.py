from setuptools import setup, find_packages

setup(
    name="cost-of-code",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["GitPython", "tiktoken", "pathspec"],
    entry_points={
        "console_scripts": [
            "cost-of-code = cost_of_code.main:main",
        ]
    },
)
