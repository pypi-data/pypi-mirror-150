#!/usr/bin/env python

import os
import shutil
from os import makedirs

from setuptools import setup

NULL_PROVIDER_VERSION = "2.1.2"

RELEASE_VERSION = "5"

__version__ = f"{NULL_PROVIDER_VERSION}.post{RELEASE_VERSION}"

FILE_NAME = f"terraform-provider-null_v{NULL_PROVIDER_VERSION}_x4"

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
except ImportError:
    bdist_wheel = None

setup(
    name="terraform-null-provider-wrapper",
    version=__version__,
    description="Python wrapper for Terraform Null Provider",
    author="Iman Azari",
    author_email="azari@mahsan.co",
    url="https://github.com/imanazari70/terraform-null-provider-wrapper",
    py_modules=["terraform_null_provider_wrapper"],
    cmdclass={'bdist_wheel': bdist_wheel},
    data_files=[("lib", [f"lib/{FILE_NAME}"]), ],
    entry_points={
        "console_scripts": [
            "tf-null-provider-download = "
            "terraform_null_provider_wrapper:download",
        ]
    },
)

package_directory = os.path.abspath(os.path.dirname(__file__))
home_directory = os.environ['HOME']
plugin_directory = f"{home_directory}/.terraform.d/plugins/" \
                   f"registry.terraform.io/hashicorp/null/" \
                   f"{NULL_PROVIDER_VERSION}/linux_amd64"
makedirs(plugin_directory, exist_ok=True)

try:
    shutil.copy2(os.path.join(package_directory, 'lib', FILE_NAME),
                 plugin_directory)
except Exception as msg:
    print(msg)
