import setuptools


setuptools.setup(
    name="bloomrpyc", # Replace with your own username
    version="0.0.2",
    license="MIT",
    author="Jinho Kim",
    author_email="sauron9973@gmail.com",
    description="bloomrpyc",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)