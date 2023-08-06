# This is the setup.py for module abstract_audio_test
from setuptools import setup, find_packages
from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
  name='abstract_audio_test',
  version='0.0.1',
  author='putkoff',
  author_email='partners@abstractendeavors.com',
  description='abstract_audio_test is a Python module within the abstract_package_test package.',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/AbstractEndeavors/abstract_package_test/abstract_audio_test',
  packages=find_packages(where="src"),
  classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.11',
      "Operating System :: OS Independent",
  ],
  package_dir={"": "src"},
  python_requires=">=3.6",
  install_requires=[
      # Add your project's requirements here, e.g.,
      # 'numpy>=1.22.0',
      # 'pandas>=1.3.0',
  ],
  entry_points={
      'console_scripts': ["abstract_audio_test=abstract_audio_test.main:main"]
  },
)