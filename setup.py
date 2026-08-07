from setuptools import find_packages, setup


setup(
    name="GeoSpatialPricingEngine",
    version="0.1.0",
    description="Object-oriented framework for geo-spatial pricing engines",
    url="https://github.com/antononcube/Python-GeoSpatialPricingEngine",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
        "psycopg[binary]",
        "GeometricNearestNeighborsProcessor",
    ],
)
