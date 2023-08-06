from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(name="Armstrongnumberfinder",
version="2.0.0",description="This package allows you to find armstrong number",
  long_description=long_description,
    long_description_content_type='text/markdown',
author="Shourjjo Majumder",
packages=['armstrongnbrfinder'])
