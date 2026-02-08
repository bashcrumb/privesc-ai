from setuptools import setup, find_packages

setup(
        name="privesc-ai",
        version="0.1.0",
        packages=find_packages(),
        install_requires=[
            "anthropic>=0.18.0",
            "requests>=2.31.0",
            "rich>=13.0.0",
            "pydantic>=2.0.0",
            "python-dotenv>=1.0.0",
            "click>=8.0.0",
        ],
        entry_points={
            'console_scripts': [
                'privesc-ai=privesc_ai.cli:cli',
            ],
        },
)
