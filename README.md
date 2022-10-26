# Search-url-from-file

This program extracts all urls from a file with format "dat", and creates two dictionaries: one dictionary whit url key : response value,
    and second dictionary whit short url key : origin url value

Python must be already installed

```shell
git clone https://github.com/Igor-Cegelnyk/web_scraping_flights_tickets.git
cd Search-url-from-file/
python3 -m venv venv
source venv/bin/activate (on macOS/Linux) #source venv/Scripts/activate (on Windows)
pip install -r requirements.txt
```

## Features

* Length dictionary urls with response - 70
* Length dictionary short urls with origin - 53
* The program  is covered with logs.
* This program uses threads because it has many blocking I/O operations, such as the request URL.
* The httpx modul is used instead of request because it works well with threads.
* The program execution time is 38.94 second.

