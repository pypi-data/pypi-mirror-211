from setuptools import setup, find_packages

setup(
    name="dfmodule_test",
    version="0.0.2",
    description="A simple dfmodule example package",
    author="Your Name",
    author_email="your.email@example.com",
    url="http://github.com/yourusername/sample_package",
    install_requires=['pandas', 'numpy'],
    packages=find_packages(exclude=['tests*']),
    keywords=['dfmodule_test'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    license="",
)
