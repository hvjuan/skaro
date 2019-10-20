# Project Skaro - URL shortener.

This is a simple project that publishes API endpoints to create new randon or custom short URLs to existing, long URLs.

### Endpoints.

All API access requires the header *Authentication*. Message me if needed.

*Get Short URL information.*
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
*Create a new short URL*
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
