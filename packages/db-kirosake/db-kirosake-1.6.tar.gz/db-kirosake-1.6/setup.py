import setuptools

setuptools.setup(
    name="db-kirosake",
    version="1.6",
    author="t1rxdqq",
    author_email="danilmerkulov63@gmail.com",
    description="DataBase with GitHub Repo",
    long_description=open('README.rst', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://t1rxdqq.github.io",
    project_urls={
        "Bug Tracker": "https://github.com/t1rxdqq/db-kirosake-source/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)