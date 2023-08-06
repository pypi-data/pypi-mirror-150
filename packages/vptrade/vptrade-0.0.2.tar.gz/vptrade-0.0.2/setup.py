import pathlib
from setuptools import setup
from vptrade import version

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name='vptrade',
    version=str(version.VERSION_TEXT),
    packages=['vptrade', 'vptrade.indicators', 'vptrade.plots', 'vptrade.strategies'],
    url='https://github.com/vnpnh/vptrade',
    license='MIT',
    keywords=["technical analysis", "ta", "trading tools", "finance", "trading", "analysis"],
    author='vnpnh',
    author_email='no@email.com',
    description='vptrade is a technical indicators trading tools can be used to all instruments.',
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data=True,
    install_requires=["matplotlib", "pandas", 'numpy'],
)



