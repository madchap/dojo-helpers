## quick replace for google social info

File to contain the creds: `_google_creds.txt` (in .gitignore of course...)
Content of file:
```
DD_SOCIAL_AUTH_GOOGLE_OAUTH2_ENABLED=(bool, True),
DD_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=(str, 'xxxxxxxxxxxxxx.apps.googleusercontent.com'),
DD_SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=(str, 'xxxxx-xxxxx-xxxx'),
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = ['xxxxxx@gmail.com']
```

sed to replace in settings.py file:
```
IFS=$'\n'; for line in $(cat _google_creds.txt); do sed -r -i "s/(.*)${line%=*}=.*/\1${line}/" ~/gitrepos/madchap_ddojo/dojo/settings/settings.py; done
```

You can run it as many times as you want.


## Load initial data
Run `import_initial_data.py`. It will create a product, an engagement and a test and import reports if you have any.

`_config.py` to contain the top-level directory, like

```
dd_api_url="http://localhost:8080/api/v2"
reports_directory="/your/directory"
```

Create sub-directories for each scanner. The name of these directory must exactly match the scanner names per `factory.py`.
Put corresponding valid reports in each of these directories. They will be slurped in.

## JIRA creds
Create a file `_jira_creds.py` with the following format:

```
username="likely_your_email_address"
password="your_api_key"
```

