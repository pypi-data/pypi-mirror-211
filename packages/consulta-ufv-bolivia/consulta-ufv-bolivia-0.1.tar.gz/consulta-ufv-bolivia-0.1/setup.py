from setuptools import setup

readme = open("./README.md", "r")

setup(
    name='consulta-ufv-bolivia',
    packages=['consultaufv'],  # this must be the same as the name above
    version='0.1',
    description='Este paquete le permite consultar la cotizacion de la unidad de fomento de vivienda.',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Giovanni Vega',
    # use the URL to the github repo
    url='https://github.com/zxvega/consulta-ufv-bolivia',
    install_requires=['requests'],
    license='MIT',
    include_package_data=True   
)