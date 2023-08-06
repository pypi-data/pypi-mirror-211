import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pdlpy",
    version="0.4.1",
    author="André Bienemann",
    author_email="andre.bienemann@gmail.com",
    description="Probability Distribution Library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrebienemann/pdlpy",
    extras_require={
        "dev": ["black", "coverage", "isort", "twine", "wheel"],
        "docs": ["mkdocs", "mkdocs-material", "plotly", "dash", "gunicorn"],
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)
