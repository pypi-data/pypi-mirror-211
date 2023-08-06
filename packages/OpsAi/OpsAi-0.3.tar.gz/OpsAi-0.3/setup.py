import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

f = open('requirements.txt', 'w')
f.write('requests')

with open('requirements.txt', 'r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
    name='OpsAi',
    version='0.3',
    author='AHMED AL-AWADI',
    author_email='dev.ahmed.alawadi@gmail.com',
    description='Ai Library for developer Ahmed Al-Awadi',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Ahmed-alawadi/OpsAi',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    python_requires=">=3.7",
    packages=setuptools.find_packages(where="src"),
    install_requires=requires,
)
