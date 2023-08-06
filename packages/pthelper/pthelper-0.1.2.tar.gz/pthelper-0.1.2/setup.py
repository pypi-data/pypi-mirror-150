from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as desc_file:
    long_description = desc_file.read()


setup(
    name="pthelper",
    packages=find_packages(exclude=[]),
    version="0.1.2",
    license="MIT",
    description="pthelper - boilerplate code for training, logging and evaluation in PyTorch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Lakshya Malhotra",
    author_email="lakshya9009@gmail.com",
    url="https://github.com/LakshyaMalhotra/pt_helper",
    keywords=[
        "artificial-intelligence",
        "deep-learning",
        "pytorch",
        "ml",
        "torchinfo",
        "model",
    ],
    install_requires=["torch>=1.10.1", "torchinfo>=1.6.0", "numpy>=1.22.0"],
    classifiers=[
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
)
