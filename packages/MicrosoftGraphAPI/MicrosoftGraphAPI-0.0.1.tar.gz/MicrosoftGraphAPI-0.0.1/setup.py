from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    # metadata here
    name="MicrosoftGraphAPI",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="0.0.1",
    author="Ashlin Darius Govindasamy",
    author_email="adg@adgstudios.co.za",
    url="https://www.adgstudios.co.za",
    description="A Python package to interact with the Microsoft Graph API",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # license here
    license='MIT',
    # modules here
    install_requires=[
        'requests',
        'pandas',
        'msal',
    ],
)
