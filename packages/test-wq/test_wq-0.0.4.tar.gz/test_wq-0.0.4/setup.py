import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="test_wq",
  version="0.0.4",
  author="wq",
  author_email="osakemon@gmail.com",
  description="test for pypi",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/osakemon/pypiTest",
  package_dir={'': 'src'},
  packages=setuptools.find_packages(where='src'),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)