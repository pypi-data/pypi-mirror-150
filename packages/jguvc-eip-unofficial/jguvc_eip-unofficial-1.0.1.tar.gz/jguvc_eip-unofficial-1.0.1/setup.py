import setuptools

setuptools.setup(
    name='jguvc_eip-unofficial',
    version='1.0.1',
    author="JGU Mainz",
    description="A basic ui library for the EIP lecture at the JGU Mainz",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyqt5', 'typeguard'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
