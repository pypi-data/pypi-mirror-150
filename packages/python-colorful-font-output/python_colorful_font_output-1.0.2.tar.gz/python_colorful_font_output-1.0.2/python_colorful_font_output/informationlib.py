import os
def update_program():
    os.system("python3 setup.py sdist")
    os.system("python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*")