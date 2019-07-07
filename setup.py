import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nose2rt",
    version="0.4.0",
    author="Andrey Smirnov",
    author_email="and.inbx@gmail.com",
    description="nose2 data collector for Testgr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/and-sm/nose2rt",
    py_modules=["nose2rt"],
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3"],
)
