from setuptools import setup, find_packages

setup(
    name="custom-json-serializer-123",
    version="1.0",
    description="serialization/deserialization package",
    url="https://github.com/donshester/PythonLabs/tree/lab3",
    author="Me",
    author_email="vlad.stepanov.2003@bk.ru",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(include=["core.*", "main.py"]),
    include_package_data=True
)
