from setuptools import find_packages, setup

setup(
    name="Phusion",
    version="0.0.1",
    description="Python package used to aid with cocktail design.",
    url="https://github.com/JoshuaIszatt",
    author="Joshua Iszatt",
    author_email="joshiszatt@gmail.com",
    license="AGPL-3.0",
    install_requires=[""],
    python_requires=">3",
    packages=find_packages(),
    data_files=[("", ["LICENSE.md"])],
    entry_points={
        'console_scripts': [
            'phusion.py = Phusion.main:main',
        ],
    },
)
