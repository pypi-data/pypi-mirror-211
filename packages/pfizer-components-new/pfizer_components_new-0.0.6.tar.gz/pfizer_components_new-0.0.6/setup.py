import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pfizer_components_new",
    version="0.0.6",
    author="ZS Associates",
    description="Custom Python Dash Components for Pfizer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #TODO
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["pfizer_components_new"],
    package_dir={'': 'pfizer_components_new/src'},
    # install_requires=['plotly>=5.0.0', 'dash==2.0.0rc2', ] #TODO
)
