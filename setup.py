import pathlib
import setuptools

from gfz_client.__version__ import version


package_data = {"gfz_client": ["CHANGELOG.md", "LICENSE"]}
readme = pathlib.Path("README.md").read_text()
history = pathlib.Path("CHANGELOG.md").read_text()
description = f"{readme}\n\n## Changelog\n\n{history}"


setuptools.setup(
    name="gfz_api_client",
    version=version,
    author="Maksim Tulin",
    description="GFZ Helmholtz Centre for Geosciences Web Service API Client",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/mmatroskin/gfz_api_client",
    project_urls={
        "Source": "https://github.com/mmatroskin/gfz_api_client",
    },
    packages=setuptools.find_packages(exclude=["tests"]),
    package_dir={"gfz_client": "./gfz_client"},
    package_data=package_data,
    include_package_data=True,
    license_files=["LICENSE"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.8",
    install_requires=pathlib.Path("requirements/lib.txt").read_text().split(),
)
