# auth_module

###### This Python package helps you manage authentication & permissions so that it can be implemented into any system as a authentication module.
###### This module use JWT Authentication written in Python (Django).

## Usage

### Clone this repo with command: `git clone https://github.com/quangnguyen3499/auth_module.git`
### cd into project folder: `cd authentication`
### Migrate Django app: `python3 authentication/manage.py makemigrations && python3 authentication/manage.py migrate`
### Then run `python3 authentication/manage.py runserver` to start the development server.

###### There are 3 existing roles: IsTeam, IsFounder, IsLP.
###### Import and use roles above to class to handle authentication and authorization tasks in your views.py file.
