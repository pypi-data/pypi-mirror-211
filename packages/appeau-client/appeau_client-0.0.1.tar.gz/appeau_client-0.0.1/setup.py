from setuptools import setup
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Voir https://blog.engineering.publicissapient.fr/2020/06/04/packaging-python-setup-py-et-setuptools/
setup(name="appeau_client",
version="0.0.1",
description="A client for http://appeau.api.vignevin-epicure.com API",
author="Guilhem Heinrich",
author_email="guilhem.heinrich@id2l.fr",
packages=["sample"],
install_requires=["requests"],
# extras_require={
# "dev": ["requests-mock"],
# },
license="Apache 2.0",
long_description=long_description)