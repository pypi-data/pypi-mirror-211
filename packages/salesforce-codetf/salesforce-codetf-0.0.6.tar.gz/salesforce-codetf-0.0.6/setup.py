from setuptools import setup, find_packages, find_namespace_packages
import platform

install_requires = [
    "accelerate==0.20.0.dev0",
    "datasets==2.12.0",
    "evaluate==0.4.0",
    "huggingface-hub==0.14.1",
    "iopath==0.1.10",
    "nltk==3.8.1",
    "numpy==1.21.6",
    "omegaconf==2.3.0",
    "pandas==1.3.5",
    "peft==0.4.0.dev0",
    "pyparsing==3.0.7",
    "PyYAML==6.0",
    "requests==2.31.0",
    "rouge-score==0.1.2",
    "sacrebleu==2.3.1",
    "scikit-learn==1.0.2",
    "torch==1.13.1",
    "torchvision==0.14.1",
    "tqdm==4.63.0",
    "transformers==4.30.0.dev0",
    "tree-sitter==0.20.1",
    "bitsandbytes==0.39.0"
]

# def read_requirements():
#     with open('requirements.txt', 'r') as req:
#         content = req.read()
#         requirements = content.split('\n')

#     return requirements

# install_requires = read_requirements()

DEPENDENCY_LINKS = []
if platform.system() == "Windows":
    DEPENDENCY_LINKS.append("https://download.pytorch.org/whl/torch_stable.html")
    

setup(
  name = 'salesforce-codetf',
  version = "0.0.6",
  py_modules = ['codetf'],
  description = 'CodeTF: A Transformer-based Library for Code Intelligence',
  author = 'Nghi D. Q. Bui',
  long_description=open("README.md", "r", encoding="utf-8").read(),
  long_description_content_type="text/markdown",
  keywords="AI4Code, Code Intelligence, Generative AI, Deep Learning, Library, PyTorch, HuggingFace",
  license="Apache 2.0",
  url = 'https://github.com/Salesforce/CodeTF',
  packages=find_namespace_packages(include="codetf.*"),
  install_requires=install_requires,
  include_package_data=True,
  zip_safe=False,
  python_requires=">=3.8.0",
  package_data={'codetf': ['*.yaml']}
)