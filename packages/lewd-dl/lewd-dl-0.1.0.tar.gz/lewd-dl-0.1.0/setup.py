from setuptools import setup
from lewd_dl.__vars__ import __version__, __name__, __author__, __email__, __description__

with open('README.md', 'r') as rmdf:
    long_description = rmdf.read()

setup(
    name=__name__,
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/b3yc0d3/lewd-dl",
    author=__author__,
    author_email=__email__,
    packages=["lewd_dl"],
    classifiers=[
        "Environment :: Console",
        "Natural Language :: English",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Internet"
    ],
    install_requires = [
        "m3u8==3.5.0",
        "rich==13.3.5",
        "requests==2.30.0",
        "validators==0.20.0",
        "beautifulsoup4==4.12.2"
    ],
    project_urls={
        "Issue tracker": "https://github.com/b3yc0d3/lewd-dl/issues"
    },
    entry_points = {
        'console_scripts': ['lewd-dl=lewd_dl.__main__:main'],
    }
)