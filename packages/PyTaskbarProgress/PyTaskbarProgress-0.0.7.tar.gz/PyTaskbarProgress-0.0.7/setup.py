from turtle import down
import setuptools
import sys
import shutil

# Copy the PyTaskbarProgress/TaskbarLib.tlb file to the dist folder

def copy_tlb(dst):
    shutil.copy("PyTaskbarProgress\\TaskbarLib.tlb", dst)

sitepackages_path = sys.prefix + '\\Lib\\site-packages'
libpath = sitepackages_path + '\\PyTaskbarProgress\\TaskbarLib.tlb'.replace('\\', '/')

setuptools.setup(
    name='PyTaskbarProgress',
    version='0.0.7',
    author='somePythonProgrammer',
    description='The ultimate taskbar progress python package!',
    packages = setuptools.find_packages(include=['PyTaskbar']),
    package_dir={'PyTaskbarProgress': 'PyTaskbar'},
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
    ],
    python_requires='>=3.6',
    install_requires=[
        'comtypes',
        'pygetwindow',
        'setuptools',
    ],
    include_package_data=True,
    url = 'https://github.com/somePythonProgrammer/PyTaskbar',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
)
