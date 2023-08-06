from setuptools import setup

setup(
    name="Serializer_Nz",
    version="0.1.1",
    description="Library for python (de)serialization in Json",
    url="https://github.com/Nzhdeh07/Igi_labs/tree/lab_3",
    author="Nzhdeh",
    author_email="nzhdeh.baboyan@icloud.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["Serializer_Nz"],
    include_package_data=True,
    install_requires=["regex"]
)