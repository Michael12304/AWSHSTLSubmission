import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection


opensearch_client = OpenSearch(
    hosts=[{'host': 'https://zvwfqyhe57vruod3eu80.us-west-2.aoss.amazonaws.com', 'port': 443}],
    http_auth=('username', 'password'),
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


