import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "transportchb",
    version = "0.0.1",
    author = "Emre Çilekci",
    author_email = "huseyin.d3r@gmail.com",
    description = "Couchbase Migration module",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/emrecilekci19/transportc",
    install_requires=[
        'tabulate'
    ],
    project_urls = {
        "Bug Tracker": "https://github.com/emrecilekci19/transportc",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)