from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="apyproxmox",
    # name="apyproxmox",  
    version="1.0.3",  
    author="Marcos Toledo",
    author_email="marcostdodev@gmail.com",
    description="api para obtener estado de las maquinas virtuales de un servidor proxmox de forma facil",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcosTGit/pyproxmox",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    python_requires=">=3.7",
    install_requires=[
        "certifi>=2024.12.14",
        "charset-normalizer>=3.4.0,<4.0.0",
        "dotenv>=0.9.0,<1.0.0",
        "idna>=3.11.0,<4.0.0",
        "python-dotenv>=1.2.0,<2.0.0",
        "requests>=2.32.0,<3.0.0",
        "urllib3>=2.6.0,<3.0.0",
    ],
)
