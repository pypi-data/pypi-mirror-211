##https://codigofacilito.com/cursos/taller-modulos-paquetes-python

## provando un paquete
python -m utility_stella
python setup.py sdist


##pip install pip --upgrade  DA ERRORE
pip install twine
twine upload dist/*
https://pypi.org/account/login/

##TEST 
pip install utility_stella==0.0.1
python
>>> from codigofacilito_jorgef import unreleased
>>> unreleased()
