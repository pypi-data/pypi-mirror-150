from setuptools import setup, find_namespace_packages

setup(
    name="uesm",
    version="0.0.2",
    packages=['uesm'],
    python_requires=">=3.9",
    install_requires=["GitPython"],
    entry_points={
        'console_scripts': ['uesm=uesm.cmdline:main']
    }
)
