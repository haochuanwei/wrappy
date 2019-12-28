import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wrappy",
    version="0.1.0",
    author="Harry Wei",
    author_email="pepsimixt@gmail.com",
    description="Decorators for common developer utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haochuanwei/wrappy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
