from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3


host = "zvwfqyhe57vruod3eu80.us-west-2.aoss.amazonaws.com"  # Replace with your actual endpoint
region = 'us-west-2'  # Replace with your AWS region
service = 'aoss'  # Use 'es' for OpenSearch Service or 'aoss' for OpenSearch Serverless

# For IAM authentication
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

index_name = 'events'
document = {
    'title': 'Moneyball',
    'director': 'Bennett Miller',
    'year': '2011'
}

index_name = 'events-index-real3'
index_body = {
    'settings': {
        'index.knn': True
    },
    'mappings': {
        'properties': {
            'event_tags_vector': {
                'type': 'knn_vector',
                'dimension': 1024  # Adjust this to match your vector dimension
            },
            'event_id': {'type': 'text'},
            'event_title': {'type': 'text'},
            'event_description': {'type': 'text'},
            'event_location': {'type': 'text'},
            'event_date': {'type': 'date'},
            'event_time': {'type': 'text'},
        }
    }
}

def insert_document(event_tags, event_id, event_title, event_description, event_location, event_date, event_time):
    document = {
        'event_tags_vector': event_tags,
        'event_id': event_id,
        'event_title': event_title,
        'event_description': event_description,
        'event_location': event_location,
        'event_date': event_date,
        'event_time': event_time
    }
    response = client.index(
        index=index_name,
        body=document,
        # refresh=True
    )
    return response


def vector_search(query_vector, k=100):
    query = {
        'size': k,
        'query': {
            'knn': {
                'event_tags_vector': {
                    'vector': query_vector,
                    'k': k
                }
            }
        }
    }
    response = client.search(
        body=query,
        index=index_name
    )
    return response

# client.indices.create(index=index_name, body=index_body)