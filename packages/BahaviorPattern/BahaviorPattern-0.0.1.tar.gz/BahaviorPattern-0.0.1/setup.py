import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BahaviorPattern",
    version="0.0.1",
    author="Chen Chen",
    author_email="cchen56@163.com",
    description="The tool is designed to mine behavior patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'pandas',
        'tqdm',
        'efficient_apriori==2.0.3',
        'prefixspan==0.5.2',
    ],
)
