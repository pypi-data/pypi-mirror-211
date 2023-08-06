from setuptools import setup

setup(
    name='nyth_dataset',
    version='0.0.2',
    description='NYT-H dataset package allows the processing of the NYT-H dataset proposed by Zhu et al., 2020. \
    NYT-H is based on the New York Times 2010 ( NYT2010) dataset proposed by Riedel et al., 2010. \
    The advantage of NYT-H dataset is the manual annotation of the test partition.',
    url='https://github.com/juanluis17/nyth-dataset',
    author='Juan-Luis García-Mendoza',
    author_email='jluisgm90@gmail.com',
    license='Apache Software License',
    install_requires=['pandas',
                      ],
)
