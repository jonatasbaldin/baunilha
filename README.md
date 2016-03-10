# Baunilha - Leitor de Tweets
An application that reads someone's tweets. Built with Python, Flask, Bootstrap, RespoinsiveVoice.JS and love.     
The application may be running under [my blog domain](http://baunilha.deployeveryday.com).

## How to deploy?
~~I'm going to automate the whole process, so stay tuned for more information.~~     

There are three ways to deploy this app, I call them **local-only**, **vagrant** and **production**. Each one of them has its purposes, particularities and requirements.     

## Dependencies
These are the softwares and files used to deploy Baunilha.     

### Twitter's API Key
Baunilha uses Twitter's API Key to retrieve information (tweets, usernames, profile images). As I am open sourcing the code, it does not include my own keys, you must access [Twitter's Apps](https://apps.twitter.com/) to get yours.     
You will receive four pieces of information: Consumer Key, Consumer Secret, Access Token Key and Access Token Secret. All of them are needed.    
Already got yours? Hold on that we will use it latter.

### Softwares

* **Git**: Distributed version control system.
* **Python Virtualenv**: create isolated Python environments.
* **Vagrant**: Create and configure lightweight, reproducible, and portable development environments.
* **vagrant-hostmanager**: Vagrant plugin to update `/etc/hosts` with information specified in the Vagrantfile.
* **Ansible**: Tool written in Python that uses SSH agentless to automate configuration.
* **jdauphant.nginx**: An Ansible role to manage NGINX, downloaded with ansible-galaxy.
* **CentOS 7**: Only tested in CentOS 7.

### Files

* **build/instance/config.sample**: Contains an example of how the Twitter's API Key should be configured. When used, this file must be renamed or copied to `build/instance/config.py`. Also, it contains the variable `secret_key`, used by Flask to secure against CSRF attacks, which you should populate with a random string.
* **deploy/inventory/<hostname>**: When using Ansible, this file will conaint the server FQDN. Also, you can specify the user that Ansibles uses to connect and other options.
* **deploy/host_vars/<hostname>.yml**: When using Ansible, this file will contain information about the NGINX virtualhost name and Twitter's API Key.

## Deployment Modes

### Local-only
In local-only, you won't need a webserver or CGI, the application will run directly from Flask integrated server, by default at **http://localhost:5000**.     
It requires: Git and Virtualenv.

**Instructions**:

```bash
# Clone the repo 
git clone https://github.com/jonatasbaldin/baunilha.git && cd baunilha

# Create virtualenv and activate it
virtualenv venv && . venv/bin/activate

# Install Python requirements
pip install -r build/requirements.txt

# Copy the config.sample file to config.py and edit with you API Keys
cp build/instance/config.sample build/instance/config.py && vim build/instance/config.py

# Run the application
python build/runserver.py
```

### Vagrant
Vagrant mode will run the full app (including NGINX and uWSGI) in a Vagrant box, being possible to test the full stack.     
The Vagrantfile uses vagrant-hostmanager to create an entry in `/etc/hosts` named `baunilha.test` binding to a private address. This name is also at `deploy/host_vars/vagrant.yml`, making viable to access the app at **http://baunilha.test**.     
Another useful information: the Vagrant box uses the code available on the host machine via a synced_folder option pointed to `/opt/baunilha`, allowing to rapidly test code changes. It creates a folder name `vagrant-venv` to store its virtualenv.     
It requires: Git, Vagrant, vagrant-hostmanager, Ansible and jdauphant.nginx.

**Instructions**:

```bash
# Clone the repo 
git clone https://github.com/jonatasbaldin/baunilha.git && cd baunilha

# Copy the config.sample file to config.py and edit with you API Keys
cp build/instance/config.sample build/instance/config.py && vim build/instance/config.py

# Spin up the Vagrant VM
vagrant up

# Run this  Ansible command
ansible-playbook -i deploy/inventory/vagrant -b --private-key .vagrant/machines/vagrant/virtualbox/private_key deploy/site.yml
```

### Production
Time to get it on production! Here, you're gonna to deploy the application to a remote server.     
I'm assuming the user used to connect via Ansible will have root permissions and passwordless sudo. Also, the command below uses a private key. You may use your password.     
An Ansible inventory file is used to determine which host will be used in production. You can introduce your host information at `deploy/inventory/production`.     
The API Keys for production won't go directly in `build/instances/config.py` due security reasons, so any host under the group `[production]` at `deploy/inventory/prodution` will get its Keys through an Ansible template. The template's variables are located in `deploy/host_vars/<hostname>.yml` (using the same hostname in the inventory file). You can edit it using the example `deploy/host_vars/example.com.yml`.     
It requires: Git and Ansible.

**Instructions**:

```bash
# Clone the repo 
git clone https://github.com/jonatasbaldin/baunilha.git && cd baunilha

# Add your server hostname 
vim deploy/inventory/production

# Copy the API Keys example file (substitute <hostname> to the name defined in the file above)
cat deploy/host_vars/example.com.yml > deploy/host_vars/<hostname>.yml

# Add your API Keys (substitute <hostname> to the same defined above)
vim deploy/host_vars/<hostname>.yml

# Run the Ansible command (use your own private-key or use --ask-pass and/or --ask-become-pass)
ansible-playbook -i deploy/inventory/production -b --private-key <private-key> deploy/site.yml
```

## License
The code is under MIT license.
