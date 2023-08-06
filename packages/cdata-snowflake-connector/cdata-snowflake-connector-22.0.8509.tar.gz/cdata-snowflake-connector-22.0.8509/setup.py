import os
import sys
import platform

from setuptools import setup
from setuptools.command.install import install

MODULE_DIR = "cdata"

def setup_module():
  classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved",
    "Topic :: Database",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
  ]
  python_requires=""
  if is_linux(): 
    classifiers.append("Operating System :: POSIX")
    classifiers.append("Programming Language :: Python :: 3.7")
    python_requires = ">=3.7, <4"
  if is_mac():
    classifiers.append("Operating System :: MacOS")
    python_requires = ">=3.8, <4"

  cmdclass = { 'install': PostInstallCommand }

  setup(
    name = "cdata-snowflake-connector",
    version = "22.0.8509",
    author = "CData Software, Inc.",
    author_email = "support@cdata.com",
    description = "A Python Database API v2.0(PEP 249) module for cdata-snowflake-connector with SQLAlchemy integrated",
    python_requires = python_requires,
    url = "https://www.cdata.com",
    packages = [ MODULE_DIR ],
    package_data = { MODULE_DIR: ['*','*/*','*/*/*'] },
    classifiers = classifiers,
    cmdclass = cmdclass,
    entry_points = {
      "sqlalchemy.dialects": [
        "snowflake = cdata.sqlalchemy_snowflake.dialect:SnowflakeDBSDialect",
        "cdata_snowflake = cdata.sqlalchemy_snowflake.dialect:SnowflakeDBSDialect"
      ]
    },
  )

def is_mac():
  return platform.system().lower() == "darwin"

def is_linux():
  return platform.system().lower() == "linux"

def getArch():
  return platform.machine()

def getPythonVersion():
  return "py" + str(sys.version_info.major) + str(sys.version_info.minor)

class PostInstallCommand(install):
  def run(self):
    install.run(self)
    local_path = os.path.join(self.install_usersite, MODULE_DIR)
    base_path = os.path.join(self.install_base, "lib", "python" + self.config_vars["py_version_short"], "site-packages", MODULE_DIR)
    arch = getArch()
    os.system("./" + MODULE_DIR + "/snowflakertutil.sh -b " + base_path + " -l " + local_path + " -a " + arch)
    operating_system = platform.system().lower()
    python_version = getPythonVersion()
    os.system("./" + MODULE_DIR + "/snowflakecleanup.sh -p " + base_path + " -o " + operating_system + " -v " + python_version)

if __name__ == "__main__":
  setup_module()