import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cq", # Replace with your desired package name
    version="0.1.0",
    author="greatoyster", # Replace with your name
    author_email="yangjq12022@shanghaitech.edu.cn", # Replace with your email
    description="A Textual TUI for sequential command execution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="", # Optional: Add your project's URL, e.g., GitHub repo
    py_modules=["cq"], # Specifies that cq.py is the module
    include_package_data=True, # Tells setuptools to check MANIFEST.in
    install_requires=[
        "textual",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "cq=cq:main", # Creates the 'cq' command
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # Choose an appropriate license
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
)
