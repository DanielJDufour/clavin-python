#from distutils.core import setup
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
import os, subprocess


def post_install(command_subclass):

    orig_run = command_subclass.run

    def modified_run(self):
        orig_run(self)

        ## the code to run after install
        d = os.path.dirname(os.path.realpath(__file__)) + "/clavin/"
        subprocess.call(["curl", "-L", "https://github.com/DanielJDufour/CLAVIN/tarball/3.0", "-o", "clavin-java.tar.gz"], cwd=d)
        subprocess.call(["tar", "-xvzf", "clavin-java.tar.gz"], cwd=d)
        subprocess.call(["rm", "clavin-java.tar.gz"], cwd=d)
        os.rename(d+next(f for f in os.listdir(d) if "DanielJDufour-CLAVIN-" in f),d+"clavin-java")
        subprocess.call("./script/ci/run_build.sh", cwd=d+"clavin-java")


    command_subclass.run = modified_run
    return command_subclass

@post_install
class CustomDevelopCommand(develop):
    pass

@post_install
class CustomInstallCommand(install):
    pass

setup(
  name = 'clavin',
  packages = ['clavin'],
  version = '0.1',
  description = 'A python wrapper for CLAVIN',
  author = 'Daniel J. Dufour',
  author_email = 'daniel.j.dufour@gmail.com',
  url = 'https://github.com/danieljdufour/clavin-python',
  download_url = 'https://github.com/danieljdufour/clavin-python/tarball/0.1',
  keywords = ['geotag'],
  classifiers = [],
  cmdclass={'install': CustomInstallCommand},
)
