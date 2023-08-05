.PHONY: install clean clean-venv

# Variables
PYTHON_INTERPRETER = python3
SRC_DIR = bloic

# Commandes
install:
	$(PYTHON_INTERPRETER) -m venv venv 
	source venv/bin/activate && pip install -r requirements.txt

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf dist
	rm -rf build
	rm -rf bloic.egg-info
	rm -rf bloic/_version.py

clean-venv:
	rm -rf venv
