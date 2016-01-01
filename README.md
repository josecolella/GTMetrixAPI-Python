# GTMetrixAPI-Python

A Python client for the GTMetrixAPI. Allows for extraction of gtmetrix metrics
of applications through the RESTful interface provided by the GTMetrix team.
[https://gtmetrix.com/api/](https://gtmetrix.com/api/)


## Dependencies

```sh
pip install requests
```


## How to use

```python
import GTMetrix

# The email and api token associated with the gtmetrix account
api = GTMetrix.GTMetrixAPI(email, apiToken)

api.requestTest("http://example.com")

api.getTestResults()
```