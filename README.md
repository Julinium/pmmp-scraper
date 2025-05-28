# pmmp-scraper
pmmp-scraper is a Python application aiming to scrape the PMMP website and store cleaned data in a separate database.
It's intended for learning pusposes only.

# Legal ?
Always remember: scraping may be illegal or cause you to be banned or blacklisted.
Before scraping a website, please make sure the owner of the website allows it.

# Docker ?
This application uses Chromium web browser and relies on Cron jobs to update database frequently. It's not pretty practical to run it as a docker container. Instead, it runs well on the server/hypervisor.

# Scraping a different website ?
This won't probably work out of the box. Because scraping depends on the target website technology and replies ...

# How to use ?
1. Clone the repo, extract and cd...
2. Setup your settings in .env file.
3. Run crony/worker.sh --level debug --links crawl --found ignore. 
Please refer to app/setting.py for more info about the args.
4. Optionally, setup a cron job to run the script periodically.

# .env files
1. .env:
    SITE_ROOT = "https://www.xxx.tld/" # Target website constants
    SITE_INDEX = "https://www.xxx.tld/index.php"
    LINK_PREFIX = 'https://www.xxx.tld/index.php?page=yyy&zzz='
    LINK_STITCH = '&aaa='

    DB_SERVER = '0.0.0.0' # Postgresql Database engine
    DB_PORT = 9999
    DB_NAME = "dbname"
    DB_USER = "dbuser"
    DB_PASS = "$trongP@ssw0rd-999"

    MEDIA_ROOT  = '/var/opt/path/to/media' # Preferably absolute paths. Make sure they exist and are writeable.
    SELENO_DIR = '/var/opt/main/path'

2. .env.creds.json: # Credentials to use to download DCE files. Use as many as possible. They are randomly shuffled.
    [
        {"fname": "John", "lname": "Doe", "email": "john@doe"},
        ...
        {"fname": "Jean", "lname": "Dupont", "email": "jean@dupont"}
    ]

3. .env.ua.json: # User-agents strings to use to navigate the target website. Use as many as possible. They are randomly shuffled.
    [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        ...
        "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    ]