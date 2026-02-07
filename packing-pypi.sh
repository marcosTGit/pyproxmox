echo "Packing..."

# DESARROLLO
# rm -rf dist/ build/ *.egg-info && python setup.py sdist bdist_wheel && python -m twine upload --repository testpypi dist/* --verbose

# PRODUCCION
rm -rf dist/ build/ *.egg-info && python setup.py sdist bdist_wheel && python -m twine upload dist/* --verbose

# echo "Ingrese el número de serie:"
# read serie
# echo "La serie ingresada es: $serie"