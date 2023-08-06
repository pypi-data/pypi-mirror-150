import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="win32nt",
    version="0.0.1",
    author="Itzsten",
    author_email="itzsten@gmail.com",
    description="A pywin32 compatible library to interact with the WinAPI; specifically ntdll functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Itzsten/win32nt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Education",
        "Development Status :: 4 - Beta"
    ],
)