import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="mask_util",
  version="0.0.6",
  author="chenqixian",
  install_requires=[],
  description="a package to mask data",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  python_requires='>=3.6',
  license="Apache License, Version 2.0",
)