import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="runescape3_api",
    version="2.0.0",
    author="Baldur Óli Barkarson",
    author_email="ballioli1@gmail.com",
    description = "runescape3-api is an open-source wrapper, that allows interaction with the various APIs available for the popular MMORPG RuneScape3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ballioli/runescape3-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'requests',
    ],
    python_requires='>=3.10',
)
