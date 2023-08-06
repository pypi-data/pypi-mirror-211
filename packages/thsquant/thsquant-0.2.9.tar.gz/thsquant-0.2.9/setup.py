from setuptools import setup, find_packages

setup(
    name="thsquant",
    version="0.2.9",
    packages=find_packages(),
    install_requires=[
        'safetensors==0.3.0',
        'datasets==2.10.1',
        'sentencepiece',
        'accelerate==0.17.1',
        'triton==2.0.0',
        'texttable',
        'toml',
        'numpy',
        'protobuf==3.20.2',
        'gptq',
    ],
    dependency_links=[
        'git+https://github.com/huggingface/transformers.git#egg=transformers',
    ],
    entry_points={
        'console_scripts': [
            'thsquant-llama = thsquant.llama:llama_quant'
        ]
    },
    author="qinbo",
    author_email="qinbo@myhexin.com",
    description="A short description of your awesome package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/qinbo23/ths-quant",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
