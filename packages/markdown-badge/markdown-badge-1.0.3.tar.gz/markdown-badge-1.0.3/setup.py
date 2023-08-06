import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="markdown-badge",
    version="1.0.3",
    description='Extension for python-markdown that adds markdown syntax for badges.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/BitwiseAndrea/python-markdown.git',
    author='Andrea Fletcher',
    author_email='bitwiseandrea@gmail.com',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    py_modules=["markdown-badge"],  
    install_requires=["markdown>=3.0"],
)