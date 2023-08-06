import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="404-optimistic-pkg-404 Not Found", # Replace with your own username
    version="0.0.1",
    author="404 Not Found",
    author_email="siaka1316@gmail.com",
    description="We must live optimistically.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.11',
)
