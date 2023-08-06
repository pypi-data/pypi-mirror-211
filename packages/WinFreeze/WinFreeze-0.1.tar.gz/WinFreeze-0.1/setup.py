from setuptools import setup, find_packages

Version = "0.1"

Description = "A simple Windows=based package used for freezing and unfreezing windows."

Long_Description = f"""
A simple Windows=based package used for freezing and unfreezing windows.
Copyright pyProjects3 (github.com/pyProjects3)
"""
setup(
    name="WinFreeze",
    version=Version,
    author="pyProjects3 (github.com/pyProjects3)",
    description=Description,
    long_description_content_type="text/markdown",
    long_description=Long_Description,
    packages=find_packages(),
    license="MIT",
    install_requires=['pywin32',"psutil"],
    keywords=["Windows","Microsoft","Freeze","Unfreeze",'Processing','C++',"Python3","Python"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
