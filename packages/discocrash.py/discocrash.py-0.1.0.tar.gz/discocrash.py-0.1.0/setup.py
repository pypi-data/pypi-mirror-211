from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["disnake==1.7.3", "requests>=2"]

setup(
    name="discocrash.py",
    version="0.1.0",
    author="JanekDeveloper",
    author_email="ivanbogynsky@gmail.com",
    description="Module for creating discord crash bots",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/discocrash-py/discorash.py",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)