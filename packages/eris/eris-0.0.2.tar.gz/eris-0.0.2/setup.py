import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eris",
    version="0.0.2",
    author="pukkamustard",
    author_email="pukkamustard@posteo.net",
    description="Implementation of the Encoding for Robust Immutable Storage (ERIS) encoding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codeberg.org/eris/python-eris",
    project_urls={
        "Bug Tracker": "https://codeberg.org/eris/python-eris/issues",
        "Mailing list": "https://lists.sr.ht/~pukkamustard/eris",
        "Specification": "http://purl.org/eris",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Communications :: File Sharing",
        "Topic :: Internet",
        "Topic :: Multimedia",
        "Topic :: System :: Archiving",
        "Topic :: System :: Archiving :: Mirroring",
    ],
    packages=["eris"],
    python_requires=">=3.6",
    install_requires=["pycryptodome"],
)
