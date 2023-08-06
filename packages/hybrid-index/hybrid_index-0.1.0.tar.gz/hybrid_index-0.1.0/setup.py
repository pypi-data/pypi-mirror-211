from setuptools import find_packages, setup

with open("hybrid/README.md", "r") as f:
    long_description = f.read()

setup(
    name="hybrid_index",
    version="0.0.10",
    description="Easy to use hybrid index for semantic + keyword search",
    package_dir={"": "hybrid"},
    packages=find_packages(where="hybrid"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gigagiova/hybrid-index",
    author="Giovanni del Gallo",
    author_email="giovanni@livesey.ai",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
      "aiohttp >=3.8.4",
      "aiosignal >=1.3.1",
      "async-timeout >=4.0.2",
      "attrs >=23.1.0",
      "certifi >=2023.5.7",
      "charset-normalizer >=3.1.0",
      "click",
      "distlib >=0.3.6",
      "faiss-gpu >=1.7.2",
      "filelock >=3.10.7",
      "frozenlist >=1.3.3",
      "idna >=3.4",
      "mkl-fft >=1.3.6",
      "mkl-service >=2.4.0",
      "multidict >=6.0.4",
      "nltk",
      "numpy",
      "openai >=0.27.7",
      "platformdirs >=3.2.0",
      "regex",
      "requests >=2.31.0",
      "urllib3 >=2.0.2",
      "virtualenv >=20.21.0",
      "yarl >=1.9.2",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
