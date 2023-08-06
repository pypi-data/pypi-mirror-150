import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="impossible",
    version="0.1.0",
    author="Mathstar13",
    description="Impossible is an Encoder/Decoder.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mathstar13/impossible",
    project_urls={
        "Bug Tracker": "https://github.com/mathstar13/impossible/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)