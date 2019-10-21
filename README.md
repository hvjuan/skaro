# Project Skaro - URL shortener.

This is a simple project that publishes API endpoints to create new randon or custom short URLs to existing, long URLs.

This project uses a very simple Python 3 stack:
* [Cherrypy](https://cherrypy.org)
* [SQLAlchemy](https://sqlalchemy.org)

To start locally, we can use docker-compose to avoid the hassle of requirements, specific servers and configuration files. It creates all the database files inside the **docker/dbdata** folder.

```bash
# cd to project directory.
cd skaro
# Build web server and project.
docker-compose build
# Start project.
docker-compose up
```

It is very important to wait for the servers to load before we run the db init script **http://my_domain/init_db**. This script runs SQLAlcemy's alembic to sync db models. We may need to run it a couple of times till the success message is displayed on the browser: **Database is ready: 0**.

All logic resides on the data models **db.url** and **db.logs** with the **api** module as the main source of the API handlers. The **db** module should have enough documentation as python docstrings to explain what they do and the reason why those technical decisions were made. 

Currently, the url [jhv.nyc](https://jhv.nyc) is hosting this project for testing. Currently, one of the custom short urls **rh**, will redirect to redhat.com. [http://jhv.nyc/rh](http://jhv.nyc/rh).

### Endpoints.

All API access requires the header *Authentication*. Message me if needed. Currently inside the **settings.py** file, there's a variable **URL** that contains the domain where the short URLs will use. As soon as a new short URL is created, it can be used with the given domain [jhv.nyc](https://jhv.nyc).

* Get Short URL information.
```
GET /api/url
  Returns all the information regarding the given short url.
GET args: 
  short_url: [REQUIRED] short url to query.
Properties:
  short_url: short url to be used.
  custom: if true, the short URL was chosen instead of created randomly.
  url: URL to redirect to.
  creation_date: date the shortURL was created.
  logs: list of detailed logs.
```
```json
// Returned Sample.
{
    "id": 2,
    "custom": true,
    "url": "https://www.npmjs.com/package/react-native-device-info",
    "short_url": "npm",
    "creation_date": "2019-10-20 22:55:12",
    "logs": [
        {
            "id": 2,
            "url_id": 2,
            "url": "https://www.npmjs.com/package/react-native-device-info",
            "ip": "127.0.0.1",
            "activity_date": "2019-10-20 19:01:17"
        },
        {
            "id": 3,
            "url_id": 2,
            "url": "https://www.npmjs.com/package/react-native-device-info",
            "ip": "127.0.0.1",
            "activity_date": "2019-10-20 19:23:16"
        }
    ]
}
```
* Create a new short URL
```
POST /api/url
  Creates a new random or custom short URL.
POST body: 
  url: [REQUIRED] URL to be shortened. 
  short_url: [OPTIONAL] Custom URL. It can have up to 7 characters max, if > 7, 
             the custom URL will be truncated.
Returns:
  Complete URL path with new short link.
```
* Stats: short_url
```
GET /api/stats/url
  Returns all the stats regarding the given short url.
GET args: 
  short_url: [REQUIRED] short url to query.
Properties:
  stats: basic stats of the given short URL.
  historagram: list of visits per day. They show total visits despite coming from the
               same ip or not.
  ```
  ```json
  {
    "stats": {
        "url": "https://www.npmjs.com/package/react-native-device-info",
        "short_url": "bsd",
        "creation_date": "2019-10-20 22:55:12",
        "times_visited": 2
    },
    "historagram": [
        {
            "visits": "2",
            "date": "2019-10-20"
        }
    ]
}
```
* Stats: total visits per short url.
```
GET /api/stats/totals
  Returns all the stats regarding the given short url.
```
```json
[
    {
        "paypal": 122
    },
    {
        "2cz8kMR": 23
    }
]
```
