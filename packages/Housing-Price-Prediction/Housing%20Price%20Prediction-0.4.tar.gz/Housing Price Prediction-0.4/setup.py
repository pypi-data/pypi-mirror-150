from setuptools import setup
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
       name='Housing Price Prediction',
       version = '0.4',
       description = 'Package for assignment-4.1',
       author = 'Palle Lakshmi Parimala',
       author_email = 'parimala.palle@tigeranalytics.com',
       url = 'https://github.com/Parimala01/mle-training',
       classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
       ],
       package_dir={"": "src"},
       packages=setuptools.find_packages(where="src"),
       python_requires=">=3.6",

)
