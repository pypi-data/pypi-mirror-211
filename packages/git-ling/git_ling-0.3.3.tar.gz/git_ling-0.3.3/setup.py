from setuptools import setup, find_packages

setup(
    name="git_ling",
    version="0.3.3",
    packages=find_packages(),
    author="Daniel Piro",
    description="git_ling is a small library to detect programming languages from file names and extensions",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 3 - Alpha",    
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],

    install_requires=[
        "pydantic",
        "requests",
        "pyyaml",
    ],
     entry_points={
        'console_scripts': [
            'git_ling = git_ling.cli:main',
        ],
    },
)