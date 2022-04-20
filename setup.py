from setuptools import setup, find_packages
import os
import sys

if sys.version[0] == "2":
    sys.exit("Use Python 3")

requires = [
    "asciimatics==1.13.0",
    "boto3==1.21.42",
    "botocore==1.24.42",
    "click==8.1.2",
    "future==0.18.2",
    "jmespath==1.0.0",
    "mypy-extensions==0.4.3",
    "pathspec==0.9.0",
    "Pillow==9.1.0",
    "platformdirs==2.5.1",
    "pyfiglet==0.8.post1",
    "python-dateutil==2.8.2",
    "s3transfer==0.5.2",
    "six==1.16.0",
    "tomli==2.0.1",
    "typing_extensions==4.1.1",
    "urllib3==1.26.9",
    "wcwidth==0.2.5",
]

setup(
    name="s3dir",
    version="1.0.2",
    description="CLI File manager with S3 and Kubernetes",
    long_description=open("./README.rst", "r").read(),
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="S3, Kubernetes, CLI, command line, terminal",
    author="Lee JunHaeng",
    author_email="rainygirl@gmail.com",
    url="https://github.com/rainygirl/s3dir",
    license="MIT License",
    packages=find_packages(),
    package_data={"": ["*.json"]},
    include_package_data=True,
    python_requires=">=3.9",
    zip_safe=False,
    install_requires=requires,
    entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      s3dir=s3dir_src.run:main
      """,
)
