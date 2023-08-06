# -*- coding: utf-8 -*-

import setuptools

short_description = "Performing Thomas Fermi calculations of two dimensional electronic systems"
try:
    with open("README.md", "r") as handle:
        long_description = handle.read()
except: # noqa
    long_description = short_description


if __name__ == "__main__":
    setuptools.setup(
        name='ThomasFermi',
        version=0.1,
        description=short_description,
        author='Taige Wang',
        license='MIT',
        packages=setuptools.find_packages(),
        python_requires='>=3.6',
        install_requires=[
            'numpy>=1.7',
            'scipy>=1.7',
        ],
        extras_require={
            'tests': [
                'pytest'
            ],
        },

        tests_require=[
            'pytest'
        ],

        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Developers',
            'License :: OSI Approved',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
        zip_safe=True,
        long_description=long_description,
        long_description_content_type="text/markdown"
    )
