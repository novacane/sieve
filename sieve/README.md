First run "pip install -r requirements.txt"

To use this, you'll need three terminals:

1. run "redis-server"

2. inside the project directory, run "celery -A main worker --loglevel=INFO"

3. run "export FLASK_APP=main", and then run "flask run" inside the project directory

The redis server runs at the default port so make sure that is open

The test.py file goes through a scenario where various functionalities of the API are tested. Run it with "python/python3 test.py"

