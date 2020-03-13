TEST_MODULE_PATH=./wrappy

pull-makefile:
	wget https://raw.githubusercontent.com/haochuanwei/make_macros/master/python_package_dev/Makefile
clean:
	@echo "Cleaning package build files.."
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@echo "Done."
publish:
	@echo "Publishing to PyPI.."
	@python setup.py sdist bdist_wheel
	@twine check dist/*
	@twine upload dist/*
	@echo "Done."
coverage:
	@coverage run --source=$(TEST_MODULE_PATH) -m pytest
	@coverage report -m
