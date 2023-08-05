from setuptools import setup, find_packages

setup(
    name='tlcloud',
    version='0.2.1',
    author='tlcloud',
    author_email='oyty@tonglucloud.com',
    description='A geo tools for tlcloud',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
