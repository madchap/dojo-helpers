## quick replace for google social info

File to contain the creds: `_google_creds.txt` (in .gitignore of course...)
Content of file:
```
DD_SOCIAL_AUTH_GOOGLE_OAUTH2_ENABLE=(bool, True),
DD_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=(str, 'xxxxxxxxxxxxxx.apps.googleusercontent.com'),
DD_SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=(str, 'xxxxx-xxxxx-xxxx'),
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = ['xxxxxx@gmail.com']
```

sed to replace in settings.py file:
```
IFS=$'\n'; for line in $(cat _google_creds.txt); do sed -r -i "s/(.*)${line%=*}=.*/\1${line}/" ~/gitrepos/madchap_ddojo/dojo/settings/settings.py; done
```
