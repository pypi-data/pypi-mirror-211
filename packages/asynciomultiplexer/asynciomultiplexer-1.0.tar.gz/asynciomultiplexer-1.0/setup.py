from setuptools import find_packages, setup

setup(
    name="asynciomultiplexer",
    version="1.0",
    # declare your packages
    packages=find_packages(where="src", exclude=("test",)),
    package_dir={"": "src"},
    # include data files
    # data_files=data_files,
    # entry_points=None,
    #
)
