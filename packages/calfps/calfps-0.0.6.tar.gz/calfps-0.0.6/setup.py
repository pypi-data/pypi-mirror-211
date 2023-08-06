import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="calfps",
    version="0.0.6",
    author="Junhojuno",
    author_email="rlawnsgh2245@gmail.com",
    description="calculating fps as simple",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Junhojuno/test-fps",
    project_urls={
        "Bug Tracker": "https://github.com/Junhojuno/test-fps/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
