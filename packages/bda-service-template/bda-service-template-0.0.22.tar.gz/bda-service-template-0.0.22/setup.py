import setuptools

setuptools.setup(
    name="bda-service-template",
    version="0.0.22",
    author="Alida research team",
    author_email="salvatore.cipolla@eng.it",
    description="Bda templates to build python services for Alida",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = [
        "file-io-utilities>=0.0.1.27",
        "ds-io-utilities>=0.0.1",
        "pyspark-utilities>=0.0.19",
        "bda-service-utils>=0.0.5",
        "kafka-python>=2.0.2",
        "pyarrow>=6.0.0",
        "alida-arg-parser"
        ],
)
