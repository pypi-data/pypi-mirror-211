import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bppy",
    version="0.0.5",
    author="Tom Yaacov",
    author_email="tomyaacov1210@gmail.com",
    description="BPpy: Behavioral Programming In Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bThink-BGU/BPpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "z3-solver",
    ],
    #python_requires='>=3.6'
)