import setuptools
__VERSION__ = "1.1rc3"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fabricauthenticator",
    version=__VERSION__,
    author="Erica Fu, Komal Thareja",
    author_email="ericafu@renci.org, kthare10@renci.org",
    description="Fabric Authenticator for Jupyterhub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fabric-testbed/fabricauthenticator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
