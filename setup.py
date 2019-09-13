import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="holidays_co",
    version="1.0.0",
    author="Javier Mejía",
    author_email="jmjaviermejiaest@gmail.com",
    description="Módulo de utilidades para festivos en Colombia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jmejia32/holidays_co",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)