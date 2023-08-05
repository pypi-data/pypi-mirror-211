from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='alpha-filter',
    version='0.9.2',
    description='differential filter',
    py_modules=['alphafilter'],
    python_requires='>=3.8',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
