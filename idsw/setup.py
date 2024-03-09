from setuptools import setup, find_packages

idsw_description = """Full workflow for ETL, statistics, and Machine learning modelling of (usually) time-stamped industrial facilities data."""

with open("requirements.txt", "r") as file:
    required_packages = [package.strip() for package in file.readlines()]

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

setup(
    name="idsw",
    url="""https://github.com/marcosoares-92/IndustrialDataScienceWorkflow""",
    version="1.3.1",
    license='MIT',
    author="Marco Cesar Prado Soares; Gabriel Fernandes Luz; Sergio Guilherme Neto",
    author_email="marcosoares.feq@gmail.com",
    description=idsw_description,
    packages=find_packages(include=['idsw', 'idsw.*']),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        'Natural Language :: English',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    keywords=['idsw','IndustrialDataScienceWorkflow'],
    install_requires=required_packages,
    zip_safe=False,
)