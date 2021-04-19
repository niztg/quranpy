from setuptools import setup, find_packages

setup(
    name='quranpy',
    author='nizcomix',
    url='https://github.com/niztg/quranpy',
    version='1.1',
    license='MIT',
    description='Python Package to interact with the glorious Qu\'ran',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['requests'],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
)
