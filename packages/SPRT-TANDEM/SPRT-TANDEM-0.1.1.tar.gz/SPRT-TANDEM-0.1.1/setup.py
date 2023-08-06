from setuptools import setup, find_packages

setup(
    name="SPRT-TANDEM",
    version="0.1.1",
    license="MIT",
    description="SPRT-TANDEM for sequential density ratio estimation to simultaneously optimize speed and accuracy of early-classification.",
    author="Akinori F. Ebihara",
    author_email="aebihara@nec.com",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/Akinori-F-Ebihara/SPRT-TANDEM-PyTorch",
    keywords=[
        "Sequential Probability Ratio Test" "likelihood ratio",
        "density ratio estimation",
        "early classification",
        "artificial intelligence",
        "machine learning",
    ],
    install_requires=["torch", "torchinfo", "optuna", "loguru"],
    python_requires=">=3.8",
)
