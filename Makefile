default:
	./module_testCode.py

env:
	python3 -mvenv env

pip:
	test \! -z $$VIRTUAL_ENV && pip install -r requirements.txt
