# Baunilha - Leitor de Tweets
An application that reads someone's tweets. Built with Python, Flask, Bootstrap, RespoinsiveVoice.JS and love.     
The application may be running under [http://baunilha.deployeveryday.com](my blog domain).

## How to deploy?
I'm going to automate the whole process, so stay tuned for more information.    
If you wanna go down the road by yourself, basically you need to:

* Get Twitter's API keys, put them in instance/config.sample, rename the file to instance/config.py.
* In the same file, populate SECRET_KEY with a random string.
* Install all the Python modules from `requirements.txt`.
* Install a webserver (NGINX recommended) with WSGI server (uWSGI).
* Run the application.

## License
The code is under MIT license.
