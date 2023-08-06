import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="callisto-python",
    version="0.0.2",
    author="Oak City Labs",
    author_email="team@oakcity.io",
    description="Callisto python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://app.callistoapp.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
