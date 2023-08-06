from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="FLWeb",
    packages=["FLWeb"],
    version="1.0.1",
    dependencies= ["Flask"],
    description="Extensión para Flask",
    long_description= long_description,
    long_description_content_type='text/markdown',
    author="Im_Cristina",
    url="https://github.com/nakato156/FLWeb",
    keywords=["flask", "extension", "web", "server"],
    license="MIT",
    include_package_data=True
)