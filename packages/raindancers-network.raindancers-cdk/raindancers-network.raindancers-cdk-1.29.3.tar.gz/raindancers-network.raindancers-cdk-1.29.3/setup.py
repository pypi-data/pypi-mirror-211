import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "raindancers-network.raindancers-cdk",
    "version": "1.29.3",
    "description": "Extensions to the ec2.Vpc Constructs",
    "license": "Apache-2.0",
    "url": "https://github.com/raindancers/raindancers-network.raindancers-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Andrew Frazer<andrew.frazer@raindancers.co.nz>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/raindancers/raindancers-network.raindancers-cdk"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "Evpc",
        "Evpc._jsii",
        "Evpc.apilambda",
        "Evpc.cloudwan",
        "Evpc.crowdstrike",
        "Evpc.delay",
        "Evpc.dns",
        "Evpc.ec2",
        "Evpc.endpoints",
        "Evpc.firewall",
        "Evpc.glue",
        "Evpc.ipam",
        "Evpc.lakeformation",
        "Evpc.network",
        "Evpc.redshift",
        "Evpc.regions",
        "Evpc.ssm",
        "Evpc.sso"
    ],
    "package_data": {
        "Evpc._jsii": [
            "raindancers-network@1.29.3.jsii.tgz"
        ],
        "Evpc": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.79.0, <3.0.0",
        "aws-cdk.aws-redshift-alpha==2.79.0.a0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.81.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
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
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
