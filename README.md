# Scrapping stats project
Provides data from scraped page

## Requirements
- Python 3.6
- Pip3




## Install
- To install all packages, use: 
```
pip3 install -r requirements.txt
```

- To change Database go to "mysite/settings.py" and find "DATABASE = " then change database (visit here for more https://docs.djangoproject.com/en/1.10/ref/settings/#databases). Default Database is MySql.

- Migrate Database by typing this:
```
python manage.py migrate
```
## Login Credentials

- To add admin user, use
```
python manage.py createsuperuser
```

## Provided data
- User details; level, vocation, name, guild
- User online details; login / logout date
- Deathlist; level, killed, killer, date
