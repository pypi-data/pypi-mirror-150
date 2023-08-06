from setuptools import setup, find_packages
import re

VERSIONFILE = "ExecParser/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

ep = {
    'console_scripts': [
        'ExecParser = ExecParser.__main__:main',
    ],
}

setup(
    name="ExecParser",
    version=verstr,
    author='Vladislav Burtsev',
    author_email='study.white.fox@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/r33-L1/ExecParser',
    zip_safe=True,
    license='MIT License',
    description='Parse PE, ELF, and Mach-O using lief',
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        'lief>=0.12.0',
    ],
)
