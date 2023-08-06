from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='NaNbin',
    version='0.0.1',
    description='A small package to create pastes on Pastebin with the Pastebin API',
    author='copycat666',
    py_modules=['pastebin',"bin_formats"],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests'],

)