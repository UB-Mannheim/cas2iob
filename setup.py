from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cas2iob",
    version='0.1.0',
    author="Renat Shigapov",
    license="MIT",
    description="Converter of UIMA CAS XMI files from INCEpTION with nested NER tags, NEL tags and components into "
                "IOB TSV files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UB-Mannheim/cas2iob",
    install_requires=['typer[all]', 'tqdm', 'dkpro-cassis'],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'cas2iob = cas2iob.cas2iob:cli',
        ],
    },
)
