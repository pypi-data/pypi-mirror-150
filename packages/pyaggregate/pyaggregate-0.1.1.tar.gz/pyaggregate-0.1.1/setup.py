from setuptools import find_packages, setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="pyaggregate",
    version="0.1.1",
    license="MIT",
    author="Josh Liburdi",
    author_email="liburdi.joshua@gmail.com",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=["pyaggregate"],
    include_package_data=True,
    url="https://github.com/jshlbrd/pyaggregate",
)
