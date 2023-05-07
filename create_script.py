import requests
import json

data = {"title": "In Search of Lost Time",
        "publication_year": 2002,
        "author": "Marcel Proust",
        }

url = "http://localhost:5000/api/books/create"
response = requests.post(url, data=data)

movie = response.json()

for x, y in movie.items():
    print('"', x, '"', ":", '"', y, '"', sep="")
