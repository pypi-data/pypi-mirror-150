import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="json-updater",
    version="0.0.5",
    author="Craig McConomy",
    author_email="cmcconomy@fwig.com",
    description="Updates JSON according to a change spec",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FortressEngineering/json-updater",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning",
        "Operating System :: POSIX :: Linux"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=['jsonpath-ng ~= 1.5.3', 'dataclasses-json ~= 0.5.7']
)