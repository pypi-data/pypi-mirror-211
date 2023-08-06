from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'airscript Type derivation package'

setup(
    name="airscript",
    version=VERSION,
    author="ITisl",
    author_email="1831207432@qq.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding="UTF8").read(),
    packages=find_packages(),
    keywords=['python', "airscript"],
    license="MIT",
classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/itisl2220/airscript",
)
