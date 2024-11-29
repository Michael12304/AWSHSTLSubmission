import requests
import json

endpoint = "https://zvwfqyhe57vruod3eu80.us-west-2.aoss.amazonaws.com"
headers = {
    "Content-Type": "application/json",
    # Add authentication headers as needed
}

# Inserting a document
doc = {
    "housing-vector": [10, 20, 30],
    "title": "2 bedroom in downtown Seattle",
    "price": 2800,
    "location": "47.71, 122.00"
}
response = requests.put(f"{endpoint}/events/_doc", headers=headers, data=json.dumps(doc))

print(response)
# Performing a vector search
search_query = {
    "size": 5,
    "query": {
        "knn": {
            "housing-vector": {
                "vector": [10, 20, 30],
                "k": 5
            }
        }
    }
}
response = requests.get(f"{endpoint}/events/_search", headers=headers, data=json.dumps(search_query))
results = response.json()
print(results)