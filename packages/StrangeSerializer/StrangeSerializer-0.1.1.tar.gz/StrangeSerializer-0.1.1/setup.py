from setuptools import setup

setup(
    name="StrangeSerializer",
    version="0.1.1",
    description="I have to do it for 3 Lab in OOP",
    author="Mihail",
    author_email="nzhdeh.baboyan@icloud.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["StrangeSerializer"],
    include_package_data=True,
    install_requires=["regex"]
)