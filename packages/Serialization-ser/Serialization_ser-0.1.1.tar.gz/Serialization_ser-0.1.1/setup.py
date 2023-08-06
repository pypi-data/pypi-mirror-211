from setuptools import setup

setup(
    name="Serialization_ser",
    version="0.1.1",
    description="Library for python (de)serialization in Json and Xml",
    url="https://github.com/Uporotka/Igi_labs/tree/lab_3",
    author="Uporotka",
    author_email="godam5759@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["Serialization_ser"],
    include_package_data=True,
    install_requires=["regex"]
)