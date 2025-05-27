# pmmp-scraper
This script aims to scrape the PMMP website and store cleaned data in a separate database.
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
3. Run crony/worker.sh --level debug --links crawl --found ignore 
Please refer to app/setting.py for more info about the args.
4. Optionally, setup a cron job to run the script periodically.