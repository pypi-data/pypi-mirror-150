from setuptools import setup, find_packages

setup(
    name="datagen-example-pypi",
    version="0.0.4",
    description="Datagen SDK",
    license="MIT",
    # long_description=long_description,
    author="Oren Tech Ltd.",
    url="https://datagen.tech/",
    packages=find_packages("src"),
    # packages=find_namespace_packages(where='src'),
    package_dir={"": "src"},
    install_requires=["dependency-injector", "marshmallow-dataclass", "numpy", "opencv-python"],
)
