from setuptools import setup, find_packages

setup(
    name="sunwoolabs",
    version="0.0.2",
    description="preprocessing module for time series",
    author="Heo, Sun-Woo",
    author_email="tjsdn447@hanyang.ac.kr",
    url="http://github.com/Ssunder4s/",
    install_requires=['pandas', 'numpy'], # 수정 필요
    packages=find_packages(exclude=['tests*']),
    keywords=['dfmodule_sw', 'time series', 'sequentila'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    license="MIT",
)