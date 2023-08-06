from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="testaroonie",
    version="0.0.0",
    author="testaroonie joe",
    author_email="testaroonie@gmail.com",
    description="A test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/testaroonie",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/testaroonie/testaroonie",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
