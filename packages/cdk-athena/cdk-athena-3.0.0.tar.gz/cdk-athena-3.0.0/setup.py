import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-athena",
    "version": "3.0.0",
    "description": "CDK Construct for creating Athena resources",
    "license": "Apache-2.0",
    "url": "https://github.com/udondan/cdk-athena",
    "long_description_content_type": "text/markdown",
    "author": "Daniel Schroeder",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/udondan/cdk-athena.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_athena",
        "cdk_athena._jsii"
    ],
    "package_data": {
        "cdk_athena._jsii": [
            "cdk-athena@3.0.0.jsii.tgz"
        ],
        "cdk_athena": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.0.0, <3.0.0",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.58.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
