import setuptools

import distutils.text_file
from pathlib import Path
from typing import List

def _parse_requirements(filename: str) -> List[str]:
    """Return requirements from requirements file."""
    # Ref: https://stackoverflow.com/a/42033122/
    return distutils.text_file.TextFile(filename=str(Path(__file__).with_name(filename))).readlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tfdatamap",
    version="1.0.8",
    author="Simon L. B. Sørensen",
    author_email="siso@mmmi.sdu.dk",
    description="A implementation of the datamap shown in \"Dataset Cartography: Mapping and Diagnosing Datasets with Training Dynamics\"",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/sdurobotics/medical/datamap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="",
    python_requires='>=3.6',
    license='MIT',
    install_requires=_parse_requirements('requirements.txt'),
    include_package_data=True,
    package_data={'tfdatamap': ['tfdatamap/*.js']}
)

# python setup.py sdist bdist_wheel
# python -m twine upload dist/*
# python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
