from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="raise-module-not-found-error",
    description="Raises ModuleNotFoundError on import",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="WTFPL",
    author="Thomas Kolar",
    author_email="thomaskolar90@gmail.com",
    url="https://github.com/ralokt/raise-module-not-found-error/",
    py_modules=["raise_module_not_found_error"],
    platforms=["all"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    version="1.0.0",
    keywords=[
        "useless",
    ],
)
