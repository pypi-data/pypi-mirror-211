import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

extras = {}
extras["torch"] = ["torch>=1.5,<2.1"]
extras["all"] = extras["torch"]
extras["docs"] = ["mkdocs-material"]

install_requires = ["transformers>=4.14,<4.30"]

setuptools.setup(
    name="transformers_embedder",
    version="3.0.11",
    author="Riccardo Orlando",
    author_email="orlandoricc@gmail.com",
    description="Word level transformer based embeddings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Riccorl/transformers-embedder",
    keywords="NLP deep learning transformer pytorch BERT google subtoken wordpieces embeddings",
    packages=setuptools.find_packages(),
    include_package_data=True,
    license="Apache",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    extras_require=extras,
    install_requires=install_requires,
    python_requires=">=3.6",
)
