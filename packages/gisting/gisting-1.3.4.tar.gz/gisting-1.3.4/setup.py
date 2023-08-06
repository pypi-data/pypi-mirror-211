from setuptools import setup, find_packages


setup(
    name='gisting',
    packages=['gisting','gisting/src','gisting/data'],
    include_package_data=True,
    version="1.3.4",
    description='A module version of the Gisting repo by Jesse Mu',
    author='Package Author: Owais Zahid, Source Code Author: Jesse Mu',
    author_email='owais.zahid@mail.utoronto.ca',
    url='https://github.com/jayelm/gisting',
    install_requires=(
        "accelerate==0.18.0",
        "datasets==2.10.0",
        "deepspeed==0.8.3",
        "evaluate==0.3.0",
        "fire==0.5.0",
        "hydra-core==1.2.0",
        "numpy==1.21.2",
        "omegaconf>=2.1.1",
        "openai==0.27.2",
        "rouge_score==0.1.2",
        "nltk==3.6.2",
        "sentencepiece==0.1.98",
        "torch==2.0.0",
        "wandb==0.13.4"
    ),
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ],
)