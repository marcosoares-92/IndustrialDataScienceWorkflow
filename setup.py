import setuptools

long_description = """
Industrial Data Science Workflow: full workflow for ETL, statistics, and Machine learning modelling of (usually) time-stamped industrial facilities data.

Check the project Github: https://github.com/marcosoares-92/IndustrialDataScienceWorkflow
"""
with open("requirements.txt", "r") as file:
    required_packages = [package.strip() for package in file.readlines()]

setuptools.setup(
    name="idsw",
    version="1.0.3",
    author="Marco César Prado Soares, Gabriel Fernandes Luz",
    author_email="marcosoares.feq@gmail.com, gfluz94@gmail.com",
    description=long_description,
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=required_packages
)