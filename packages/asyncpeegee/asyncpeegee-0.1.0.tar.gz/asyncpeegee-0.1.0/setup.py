from setuptools import setup, find_packages

setup(
    name="asyncpeegee",
    version="0.1.0",
    license="GPL 3",
    author="Violet McKinney",
    author_email="opensource@viomck.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/viomck/peegee",
    keywords="postgres",
    install_requires=[
        "asyncpg",
        "asyncpg-stubs"
	]
)
