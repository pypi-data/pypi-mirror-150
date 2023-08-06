from setuptools import setup, find_namespace_packages


def _read(filename: str) -> str:
    """
    Reads in the content of the file.

    :param filename:    The file to read.
    :return:            The file content.
    """
    with open(filename, "r") as file:
        return file.read()


setup(
    name="wai.annotations.redis.predictions",
    description="Inline stream processor for making predictions via a Redis backend.",
    long_description=f"{_read('DESCRIPTION.rst')}\n"
                     f"{_read('CHANGES.rst')}",
    url="https://github.com/waikato-ufdl/wai-annotations-redis-predictions",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3',
    ],
    license='Apache License Version 2.0',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    namespace_packages=[
        "wai",
        "wai.annotations",
    ],
    version="1.0.1",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    install_requires=[
        "wai.annotations.core>=0.1.1",
        "redis",
        "opex",
    ],
    entry_points={
        "wai.annotations.plugins": [
            # ISPs
            "redis-predict-ic=wai.annotations.redis_predictions.isp.image_classification.specifier:PredictISPSpecifier",
            "redis-predict-is=wai.annotations.redis_predictions.isp.image_segmentation.specifier:PredictISPSpecifier",
            "redis-predict-od=wai.annotations.redis_predictions.isp.object_detection.specifier:PredictISPSpecifier",
        ]
    }
)
