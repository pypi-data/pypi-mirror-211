import base64
import json
import urllib.request

class HyperSphereAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def shadow_string(self, string):
        shadow_url = "https://qaapi.hyperspheretech.com/api/Shadow"
        request_headers = {
            "Bearer-Token": self.api_key,
            "Content-Type": "application/json"
        }
        request_body = {
            "data": base64.b64encode(string.encode("utf-8")).decode("utf-8")
        }

        req = urllib.request.Request(shadow_url, headers=request_headers, data=json.dumps(request_body).encode("utf-8"))
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode("utf-8")

        if response_body == "[\"" + self.api_key + "\"]":
            raise Exception("Fatal: Failed to authenticate, check your API key!")

        json_response = json.loads(response_body)
        shadow_one = Shadow(json_response["shadowOne"])
        shadow_two = Shadow(json_response["shadowTwo"])

        return [shadow_one, shadow_two]

    def revive_string(self, shadows):
        revive_url = "https://qaapi.hyperspheretech.com/api/Revive"
        if len(shadows) < 2:
            raise Exception("Fatal: must have at least two shadows to revive!")

        request_headers = {
            "Bearer-Token": self.api_key,
            "Content-Type": "application/json"
        }
        request_body = {
            "shadowOne": shadows[0].get_shadow_content(),
            "shadowTwo": shadows[1].get_shadow_content()
        }

        req = urllib.request.Request(revive_url, headers=request_headers, data=json.dumps(request_body).encode("utf-8"))
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode("utf-8")

        if response_body == "[\"" + self.api_key + "\"]":
            raise Exception("Fatal: Failed to authenticate, check your API key!")

        json_response = json.loads(response_body)
        return base64.b64decode(json_response["data"]).decode("utf-8")

class Shadow:
    def __init__(self, shadow_content):
        self.shadow_content = shadow_content

    def get_shadow_content(self):
        return self.shadow_content