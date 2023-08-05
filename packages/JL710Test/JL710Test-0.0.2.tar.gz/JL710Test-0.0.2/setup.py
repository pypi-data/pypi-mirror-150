from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
	long_description = f.read()

setup(
	name='JL710Test',
	version='0.0.2',
	description='Test Package',
	py_modules=["test"],
	package_dir={'': 'src'},
	long_description=long_description,
    	long_description_content_type="text/markdown",
    	url="https://github.com/JL710/test-package"
)
