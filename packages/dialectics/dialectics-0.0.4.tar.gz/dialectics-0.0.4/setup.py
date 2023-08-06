from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8', errors='ignore') as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding='utf-8', errors='ignore') as fh:
    requirements = [x.strip() for x in fh.read().split('\n') if x.strip()]

setup(
    name='dialectics',
    version='0.0.4',
    url='https://github.com/deterritorial/dialectics.git',
    author='Ryan Heuser',
    author_email='rj416@cam.ac.uk',
    description='Code, data, and models to support dialectics as a weapon of thinking, analysis and action.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    packages=find_packages(),    
    license='MIT',
    install_requires=requirements,
    classifiers=[
        #'Development Status :: 3 - Alpha',
        #'Intended Audience :: Science/Research',
        #'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3.6'
    ],
)