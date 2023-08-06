Pasos obtenidos de: https://antonio-fernandez-troyano.medium.com/crear-una-libreria-python-4e841fbd154f

Corremos en carpeta de libreria el comando:
python setup.py sdist bdist_wheel

Subimos a PyPi:
twine upload dist/SalesforceMinu-0.0.8.tar.gz dist/SalesforceMinu-0.0.8-py3-none-any.whl