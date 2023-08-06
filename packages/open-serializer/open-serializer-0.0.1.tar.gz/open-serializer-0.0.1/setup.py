import setuptools

setuptools.setup(
    name="open-serializer",
    version="0.0.1",
    author="Jia-Yau Shiau",
    author_email="jiayau.shiau@gmail.com",
    description="python object serializer",
    url="https://github.com/Janus-Shiau/open-serializer",
    packages=setuptools.find_packages(),
    entry_points={},
    include_package_data=False,
    python_requires=">=3.7",
    license="LICENSE",
    install_requires=["rich", "ruamel.yaml", "toml"],
)
