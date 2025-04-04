# Armies-Server
This is going to be server behind GOTY so hold onto your butts

## Resources 
https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

https://docs.djangoproject.com/en/5.1/topics/install/

https://www.postgresql.org/docs/current/datatype-json.html

## DONT COMMIT PASSWORDS
Pls

## Git Branch Strategy
<!-- Maybe add a little diagram -->

```
main - releases when merged into and tagged 
    development - Development baseline
        f/{feature-name} - features
        b/{bug-name} - bug fixes 
        d/(documentation-desc) - changes that are exclusivly documentation based - could make a rule that d/ tickets don't require review 
```

## Database info
Currently the database will use SQLite which will make a little db.sqlite3 file in your code directory.

In the future postgres will probably get used since I'm used to it.

### Database Seed
We have a seed command that will allow us to create some test data. Currently just uses the same map value for everyone

- python manage.py seed <number_of_users> <number_of_turns>

eg: 
- python manage.py seed 10 10
