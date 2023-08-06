# python setup.py sdist bdist_wheel  
# twine upload --repository testpypi dist/*    
#twine upload dist/*    

from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='openi-beta',
    version='0.0.2',
    description='A test packages for openi pypi',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://openi.pcl.ac.cn/OpenIOSSG/openi-pypi',
    author='chenzh05',
    author_email='chenzh.ds@outlook.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    install_requires=['emoji>=2.4.0', 'requests>=2.30.0','tqdm>=4.65.0'],
    python_requires='>=3.6',
)