import setuptools
# used by python -m build
# python -m build needs pyproject.toml or setup.py
setuptools.setup(
    # TODO: Please update the name
    name='storage-remote',
    version='0.0.6',
    author="Circles",
    author_email="info@circles.life",
    description="PyPI Package for Circles Storage Remote Python",
    long_description="This is a package for sharing common XXX function used in different repositories",
    long_description_content_type="text/markdown",
    url="https://github.com/javatechy/dokr",
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
    ],
)
