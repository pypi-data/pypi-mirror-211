import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="engine4",
    version='0.0.2',
    description="ENGINE4 API Wrapper",
    long_description=README,
    long_description_content_type="text/markdown",
    project_urls={
        'Documentation': 'https://docs.engine4.io/api',
        'Github': 'https://github.com/robingenz/engine4-python'
    },
    url="https://github.com/robingenz/engine4-python",
    author="Robin Genz",
    author_email="mail@robingenz.dev",
    license="MIT",
    python_requires='>=3.6',
    packages=['engine4'],
    install_requires=["requests"],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
