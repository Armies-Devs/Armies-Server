# Armies-Server
This is going to be server behind GOTY so hold onto your butts

## Resources 
https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

https://docs.djangoproject.com/en/5.1/topics/install/

https://www.postgresql.org/docs/current/datatype-json.html

https://dev.mysql.com/doc/refman/8.4/en/json.html

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
