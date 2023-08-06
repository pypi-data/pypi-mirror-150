import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
PKG_NAME="oneNeuron_pkg"
USER_NAME = "Vikaslakkacs"
PROJECT_NAME="oneNeuron-pkg"
setuptools.setup(
    name=f"{PKG_NAME}-{USER_NAME}",
    version="0.0.2",
    author="Example Author",
    author_email="vikaslakkacs@gmail.com",
    description="A small for perceptron",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/{USER_NAME}/{PROJECT_NAME}",
    project_urls={
        "Bug Tracker": "https://github.com/{USER_NAME}/{PROJECT_NAME}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["numpy==1.21.6",
    "pandas==1.3.5",
    "joblib==1.1.0"]
)