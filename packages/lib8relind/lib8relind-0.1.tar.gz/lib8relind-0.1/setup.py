import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lib8relind",
    version="0.1",
    author="Stcoe",
    author_email="evanone@163.com",
    description="A set of functions to control 8-Relay board",
    long_description_content_type="text/markdown",
    long_description="README",
	license='MIT',
    url="https://github.com/zhangevanone/relind8-pylib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
