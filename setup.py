import setuptools


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='image-repo-backend',
    version='0.0.0.1',
    author='Zizeng Meng',
    author_email='zizengmeng98@uwaterloo.ca',
    url='https://github.com/mzzchy/shopify_challenge',
    install_requires=requirements,
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)