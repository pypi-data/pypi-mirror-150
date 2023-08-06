
from setuptools import setup,find_packages

if __name__ == '__main__':
    setup(
        name='gyprint',
        version='0.0.1',
        description='Use for print one_s shape',
        long_description=None,
        author='PeppermintSummer',
        author_email='528129929@qq.com',
        maintainer='PeppermintSummer',
        keywords='deep learning',
        platforms=["all"],
        packages=find_packages(),
        install_requires=[],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
        ],
        license='MIT License',
        zip_safe=False
    )