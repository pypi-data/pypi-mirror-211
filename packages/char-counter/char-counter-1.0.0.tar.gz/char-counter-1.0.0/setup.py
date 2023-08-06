from setuptools import setup, find_packages

setup(
    name="char-counter",
    version="1.0.0",
    author="Uladzimir Radchanka",
    author_email="Uradchanka@gmail.com",
    description="A command-line tool to count the characters in a text file",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://git.foxminded.ua/foxstudent102513/task-5-create-the-python-package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "click==8.1.3",
        "colorama==0.4.6",
        "exceptiongroup==1.1.1",
        "joblib==1.2.0",
        "lxml==4.9.2",
        "nltk==3.8.1",
        "packaging==23.1",
        "python-docx==0.8.11",
        "regex==2023.3.23",
        "tqdm==4.65.0",
    ],
    license="MIT",
)
