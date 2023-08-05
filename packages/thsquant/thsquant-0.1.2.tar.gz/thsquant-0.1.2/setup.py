from setuptools import setup, find_packages

setup(
    name="thsquant",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'thsquant = quant:sayhello'
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
