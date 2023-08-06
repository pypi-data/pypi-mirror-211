import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="lixiang90sblog",  # Replace with your own username
    version="0.0.1",
    author="lixiang90",
    author_email="lixiang90@github.com",
    description="Lixiang90's personal blog",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lixiang90/lixiang90sblog.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)