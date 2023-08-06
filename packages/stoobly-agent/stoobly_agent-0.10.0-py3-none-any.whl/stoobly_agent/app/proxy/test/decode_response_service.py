import cgi
import json
import pdb
import urllib.parse

from typing import Union

JSON = 'application/json'
WWW_FORM_URLENCODED = 'application/x-www-form-urlencoded'

def decode_response(content, content_type: Union[bytes, None, str]):
    if not content_type:
        return content

    content_type = __normalize_header(content_type)

    decoded_response = content
    if content_type == JSON:
        if isinstance(content, bytes):
            content = content.decode('utf-8')

        if not content_type:
            content_type = ''

        decoded_response = __parse_json(content)
    elif content_type == WWW_FORM_URLENCODED:
        decoded_response = __parse_www_form_urlencoded(content)

    return decoded_response

def __parse_json(content):
    try:
        return json.loads(content)
    except:
        return {}

def __parse_www_form_urlencoded(content):
    try:
        return urllib.parse.parse_qs(content)
    except:
        return {}

def __normalize_header( header):
    if isinstance(header, bytes):
        header = header.decode('utf-8')
    return cgi.parse_header(header)[0].lower()