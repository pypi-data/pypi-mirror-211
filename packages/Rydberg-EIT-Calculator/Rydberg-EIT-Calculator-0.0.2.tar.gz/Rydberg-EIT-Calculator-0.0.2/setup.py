import setuptools

with open("readme.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="Rydberg-EIT-Calculator",
    version="0.0.2",
    author="Shengpu_Wang",
    author_email="harrywang1126@outlook.com",
    packages=["Rydberg_EIT_Calculator"],
    description="A EIT Response Calculator",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/Einspiao/EIT-Calculator",
    license='MIT',
    python_requires='>=3.8',
    install_requires=[]
)
