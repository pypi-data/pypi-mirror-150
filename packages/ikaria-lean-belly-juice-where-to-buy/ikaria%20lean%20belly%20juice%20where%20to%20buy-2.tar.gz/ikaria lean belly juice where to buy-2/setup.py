import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
    # pip3 ikaria lean belly juice where to buy
    name="ikaria lean belly juice where to buy", 
    version="2",
    author="ikaria lean belly juice where to buy",
    author_email="free@PsychicSoulmateSketch.com",
    description="ikaria lean belly juice where to buy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://48777bsk5mlxbx5hhkmhypqp57.hop.clickbank.net/?tid=py",
    project_urls={
        "Bug Tracker": "https://github.com/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requires,
)
