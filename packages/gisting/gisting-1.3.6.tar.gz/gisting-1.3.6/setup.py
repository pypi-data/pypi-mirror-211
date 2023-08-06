from setuptools import find_packages, setup

setup(
    name = "gisting",
    version = "1.3.6",
    packages=['gisting','gisting/src','gisting/src/data'],
    include_package_data=True,
    author="Owais Zahid",
    author_email="owais.zahid@mail.utoronto.ca",
    scripts=[],
    description="A pip module for the Gisting Repo by Jesse Mu",
    url = "https://github.com/jayelm/gisting",
    classifiers=["Development Status :: 4 - Beta"]
    # the issue is probably in scripts, packages and dir and package-data
)