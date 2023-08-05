
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open('required.txt') as f:
    required = f.read().splitlines()

setup_args = dict(
    name='auto_OD',
    version='0.1',
    description='Automatic Object Detection with Tensorflow',
    long_description_content_type="text/markdown",
    long_description=readme,
    license='MIT',
    packages=find_packages(),
    author='Elina Chertova',
    author_email='elas.2015@mail.ru',
    keywords=['Tensorflow', 'Object Detection'],
    url='https://github.com/elina-chertova/tensorflow-2-object-detection.git',
    include_package_data=True
)

install_requires = [
    'split-folders',
    'scikit-image',
    'folium==0.2.1',
    'imageio',
    'ipython==5.5.0',
    'tf_slim>=1.1.0',
    'sentencepiece',
    'sacrebleu'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)


# setup(
#     name="auto_object_detection",
#     version="0.1",
#     author="Elina Chertova",
#     author_email="c",
#     description="",
#     python_requires='==3.7',
#     long_description=readme,
#     url="https://github.com/elina-chertova/tensorflow-2-object-detection.git",
#     packages=find_packages(),
#     install_requires=required,
#     include_package_data=True,
# )