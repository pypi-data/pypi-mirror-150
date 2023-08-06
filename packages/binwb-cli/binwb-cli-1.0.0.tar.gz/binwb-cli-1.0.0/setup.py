#!/usr/bin/python3
from setuptools import setup
import binwb_cli

with open("README.md", "r", encoding = "utf-8") as file: readme = file.read()
with open("requirements.txt", "r", encoding = "utf-8") as file: reqs = file.read().splitlines()

setup(
	name = "binwb-cli",
	version = binwb_cli.__version__,
	description = "Binary Workbench command line client",

	author = "Hexalinq",
	author_email = "info@hexalinq.com",

	maintainer = "Istvan Toth",
	maintainer_email = "istvan@hexalinq.com",

	license = "GPLv2",

	long_description = readme,
	long_description_content_type = "text/markdown",

	include_package_data = True,

	install_requires = reqs,

	url = "https://github.com/hexalinq/binwb-cli/",
	packages = [ "binwb_cli" ],
	scripts = [ "scripts/binwb" ],
)
