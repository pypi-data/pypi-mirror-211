from setuptools import setup

setup(
    name="jsonxmlsatsiuk2",
    version="0.1.2",
    description="Library for python (de)serialization in Json and Xml",
    url="https://github.com/panton8/igi-labs/tree/lab3",
    author="stady09",
    author_email="stassatsiukgg@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["serializers"],
    include_package_data=True,
    install_requires=["regex"]
)
