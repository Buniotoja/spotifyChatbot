import requests
import base64
import json
from urllib.parse import urlencode

class Connector:

    def __init__(self):
        self._CLIENT_ID = "345203decad2499b850b25163847ba32"
        self._SECRET_KEY = "006237d49b5140a1a2d331e060a5d451"

    def _get_token(self):
        authStr=self._CLIENT_ID+":"+self._SECRET_KEY
        authBytes=authStr.encode("utf-8")
        authBase64=str(base64.b64encode(authBytes), "utf-8")
        url="https://accounts.spotify.com/api/token"
        headers={
            "Authorization": "Basic "+authBase64,
            "Content_Type": "application/x-www-form-urlencoded"
        }
        data={"grant_type": "client_credentials"}

        result=requests.post(url, headers=headers, data=data)
        json_result=json.loads(result.content)
        return json_result["access_token"]


    def _get_auth_header(self):
        token=self._get_token()
        return {"Authorization": "Bearer "+token}

    def get_stand_request(self, subject, context):
        url="https://api.spotify.com/v1/search?"
        header=self._get_auth_header()
        query=urlencode({"q": subject, "type": context, "limit": 5, "offset": 0})
        query_url=url+query
        query_result=requests.get(query_url, headers=header)
        results=json.loads(query_result.content)[context+"s"]["items"]
        if len(results)==0:
            return None
        else:
            return results

    def get_sub_request(self, subject, source, context):
        url="https://api.spotify.com/v1/search?"
        header=self._get_auth_header()
        source_name=("album" if context=="track" else "artist")
        query=urlencode({"q": subject, "type": context, source_name: source})
        query_url=url+query
        query_result = requests.get(query_url, headers=header)
        results=json.loads(query_result.content)[context+"s"]["items"]
        if len(results)==0:
            return None
        else:
            return results

    def get_show_request(self, context_data, context_from, source_id):
        url: str
        if_items: bool
        if context_data=="track" and context_from=="artist":
            url = f"https://api.spotify.com/v1/{context_from}s/{source_id}/top-{context_data}s?market=PL"
            if_items=False
        else:
            url = f"https://api.spotify.com/v1/{context_from}s/{source_id}/{context_data}s?market=PL"
            if_items=True
        header = self._get_auth_header()
        query_result = requests.get(url, headers=header)
        results = json.loads(query_result.content)
        if len(results) > 0 and if_items==True:
            return results["items"]
        elif len(results) > 0 and if_items==False:
            return results
        else:
            return None

