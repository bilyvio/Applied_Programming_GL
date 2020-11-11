# Lab #4
1. install your python version 3.8.1 with pyenv
1. install and create virtual environment using poetry
3. add flask 
$ pip install flask
4. write your code 
5. install gunicorn and create an entry point wsgi.py
6. to run $ cd your project
7. to run $ gunicorn wsgi:app
8. visit http://127.0.0.1:8000/api/v1/hello-world-3
9. to check status enter  $ curl -v -XGET http://localhost:5000/api/v1/hello-world-3
10. to check python version enter $ which --python in local terminal
