SAGAN

This is the system board software to be used with a Sagan board for the DreamCoder project - https://dreamcoder.dreamup.org

__Deploying to PyPi.org__

General instructions are here - https://packaging.python.org/en/latest/tutorials/packaging-projects/

1) Update the version number in _setup.py_.
2) Run _python3 -m build_. This will create 2 files in the _dist_ folder. 
3) Since all the previous package outputs are still in the _dist_ folder, running _twine upload dist/*_ would upload all the previous versions as well. If the current version is 1.2.3, run _twine upload dist/sagan-1.2.3*_. (You will need the PyPi.org credentials.)
