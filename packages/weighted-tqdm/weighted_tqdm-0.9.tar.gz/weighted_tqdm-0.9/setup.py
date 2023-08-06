import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "weighted_tqdm",
    version         = "0.9",
    author = "Michael Schilling",
    author_email = "michael@ntropic.de",
    description  = "weighted_tqdm allows for weighted iterations in tqdm progress bars.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Ntropic/weighted_tqdm/archive/refs/tags/v0.9.tar.gz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["numpy", "tqdm"],
    python_requires=">=3.6",
)
