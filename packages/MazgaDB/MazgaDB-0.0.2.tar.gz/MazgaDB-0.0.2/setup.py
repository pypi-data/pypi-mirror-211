from setuptools import setup, find_packages

def readme():
    with open("README.md", "r") as f:
        return f.read()

setup(
    name="MazgaDB",
    version="0.0.2",
    author="Mazga",
    author_email="agzamikail@gmail.com",
    description="ОРМ для базы данных SQlite",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mazgagzam/MazgaDB",
    packages= find_packages(),
    install_requires=['prettytable'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="example python orm sql",
    project_urls={"Documentation": "https://github.com/Mazgagzam/MazgaDB"},
    python_requires=">=3.8",
)
