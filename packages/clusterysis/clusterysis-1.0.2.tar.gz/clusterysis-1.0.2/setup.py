from setuptools import find_packages, setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='clusterysis',
    packages=find_packages(include=['clusterysis']),
    version='1.0.2',
    description='A library for visualizing clusters.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    #long_description="Clusterysis",
    author='Gabriel Di Pardi Arruda',
    install_requires=[
        'pandas',
        'plotly',
        'matplotlib'
    ],
    url='https://github.com/gabrieldi95/clusterysis',
)
