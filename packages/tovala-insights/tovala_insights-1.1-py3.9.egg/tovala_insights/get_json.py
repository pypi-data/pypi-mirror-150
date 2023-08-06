import urllib.parse
import requests
import json
import pathlib
import os
import boto3
import logging
import logging.config
import yaml

logger = logging.getLogger(__name__)

endpoint_url = 'https://newsapi.org/v2/everything'
params = {"q" : 'Tovala OR meal kit OR smart oven'}
url_encoded_params = urllib.parse.urlencode(params)

headers = {
 'Authorization': '46ce6a3531c74ad8bd2dbb781862860a',
 'Content-Type' : 'application/json'
 }

def get_data_from_api(url, headers, params):
    try:
        response_API = requests.get(url = url, headers = headers, params = params)
        response_API.raise_for_status()
        return response_API.json()["articles"]
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.TooManyRedirects:
        return logger.error("Too many redirected attempts. Try a different URL")
    except requests.exceptions.ConnectionError as errc:
        return logger.error("Error Connecting:",errc)

#Creating Session With Boto3.
session = boto3.Session(
aws_access_key_id='AKIATA2DWH5RR3EKZI62',
aws_secret_access_key='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'
)

# Creating S3 Resource From the Session.
s3 = session.resource('s3')
object = s3.Object('tovala-coding-challenge', 'api_output_data.json')
result = object.put(Body=bytes(json.dumps(get_data_from_api(endpoint_url, headers, url_encoded_params)).encode('UTF-8')))
attributes = result.get('ResponseMetadata')
if attributes.get('HTTPStatusCode') == 200:
    # logger.info('File Uploaded Successfully')
    print("File Uploaded Successfully")
else:
    logger.error('File Not Uploaded')



