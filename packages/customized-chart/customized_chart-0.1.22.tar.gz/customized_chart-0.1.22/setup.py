from setuptools import setup
setup(name="customized_chart",
    version="0.1.22",
    author="Johan Hagelbäck",
    author_email="johan.hagelback@gmail.com",
    description="Simplifies creation of matplotlib charts",
    long_description="Simplifies creation of matplotlib charts.",
    license="MIT",
    packages=["customized_chart"],
    url="https://github.com/jhagelback/customized_chart",
    install_requires=["termcolor", "matplotlib", "numpy"]
    )
