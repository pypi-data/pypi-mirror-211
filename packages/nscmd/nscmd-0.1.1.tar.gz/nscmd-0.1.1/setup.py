from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nscmd",
    version="0.1.1",
    description="A terminal user interface (TUI) for GNU/Linux systems which implements namespaces.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ropbear/nscmd",
    author="ropbear",
    author_email="pypi@selfhosted.systems",
    license="GPLv3",
    project_urls={
        'Bug Tracker': 'https://github.com/ropbear/nscmd/issues',
    },
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.8',
)
