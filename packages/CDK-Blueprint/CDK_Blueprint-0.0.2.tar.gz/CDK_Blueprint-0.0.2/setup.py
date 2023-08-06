import setuptools

# readme.md = github readme.md

with open('README.md', 'r') as fr:
    long_description = fr.read()

setuptools.setup(
    name="CDK_Blueprint",
    version="0.0.2",
    author="Vunk Lai",
    author_email="vunk.lai@gmail.com",
    description="Declarative Attribute for CDKv2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VunkLai/cdk-blueprint",
    packages=setuptools.find_packages(exclude=['*test*']),
    install_requires=['aws-cdk-lib', ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
