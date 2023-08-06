from setuptools import setup, find_packages




VERSION = '0.0.1'
DESCRIPTION = 'Astrology Information Package'
LONG_DESCRIPTION = 'A package that allows to obtain Planets Infromation By Specific Date.'

# Setting up
setup(
    name="Astro_Lib",
    version=VERSION,
    author="AshmaKader",
    author_email="<ashmakader538@gamil.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'sqlite3'],
    keywords=['python', 'Astrology'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
