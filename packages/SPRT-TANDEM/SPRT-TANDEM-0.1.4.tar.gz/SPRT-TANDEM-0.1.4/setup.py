from setuptools import setup, find_packages
from os import path

# Get the long description from the README file
with open(
    path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8"
) as f:
    long_description = f.read()

setup(
    name="SPRT-TANDEM",
    version="0.1.4",
    license="MIT",
    description="SPRT-TANDEM for sequential density ratio estimation to simultaneously optimize both speed and accuracy of early-classification.",
    author="Akinori F. Ebihara",
    author_email="aebihara@nec.com",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={
        "data": ["SequentialGaussian_2class_offset2.0_dim2/*"],
    },
    url="https://github.com/Akinori-F-Ebihara/SPRT-TANDEM-PyTorch",
    keywords=[
        "Sequential Probability Ratio Test",
        "likelihood ratio",
        "density ratio estimation",
        "early classification",
        "artificial intelligence",
        "machine learning",
    ],
    install_requires=["torch", "torchinfo", "optuna", "loguru"],
    python_requires=">=3.8",
)
