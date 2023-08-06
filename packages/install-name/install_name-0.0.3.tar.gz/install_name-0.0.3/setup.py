# setup.py
# ==========================================
from setuptools import find_packages, setup, Extension
import pathlib

packages = find_packages(exclude = [])
install_requires=[
    'numpy==1.19.5',
    'pandas',
]

import os
if os.path.exists('requirements.txt'):
    print('[+] use requirements.txt')
    with open('requirements.txt', 'r') as f:
        lines = [x.strip() for x in f.readlines() if len(x.strip()) > 0]
        install_requires = lines

print(packages)
print(install_requires)

entry_points={
     'console_scripts': ['import_name=import_name:hello_world'],
     # 'console_scripts': ['import_name=import_name.utils.utils:show_info'],
}

setup(
    name='install_name',
    version='0.0.3',
    description='runningz_automl',
    url='https://github.com/RunxingZhong/stacking_automl_001',
    author='zhongrunxinig',
    author_email='zhongrunxing@gmail.com',
    packages=packages,
    install_requires=install_requires,
    # python_requires='>=3.6',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    entry_points = entry_points,
)
