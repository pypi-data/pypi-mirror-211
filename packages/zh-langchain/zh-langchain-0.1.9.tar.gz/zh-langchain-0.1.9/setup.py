from setuptools import setup, find_packages
import setuptools, glob, os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

    


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('zh_langchain/nltk_data')


setup(
    name='zh-langchain',
    version='0.1.9',
    description='Chinese language processing library',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/imClumsyPanda/langchain-ChatGLM.git',
    packages=find_packages(include=['zh_langchain', 'zh_langchain.*']),
    package_data={"": extra_files},
    install_requires=[
        "torch",
        "langchain",
        "unstructured[local-inference]",
        "nltk",
        "sentence-transformers",
        "beautifulsoup4",
        "icetk",
        "cpm_kernels",
        "faiss-cpu",
        "bitsandbytes",
        "tabulate",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)