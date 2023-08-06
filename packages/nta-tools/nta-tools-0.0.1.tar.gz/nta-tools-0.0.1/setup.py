from setuptools import setup, find_packages

requirements = [
    'nfstream>=6.5.0',
    'pynvml>=11.4.1'
]

setup(
    name='nta-tools',
    version='0.0.1',
    python_requires='>=3.6',
    author='NTA-Tools Developers',
    author_email='wellshark.net@gmail.com',
    description='Network Traffic Analysis Tools',
    license='MIT-0',
    url='https://pypi.org/project/nta-tools/',
    packages=find_packages(),
    zip_safe=True,
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
