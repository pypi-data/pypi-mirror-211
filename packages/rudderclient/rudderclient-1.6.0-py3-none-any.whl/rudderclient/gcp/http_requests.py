"""
HTTP requests library.

This library provides an easy way to do HTTP request.

Functions:
---------
def iap_http_request(method: str, api_url: str, request_url: str, body: str, headers: dict[str, str]):
    Makes an http request to an API protected by Identity-Aware Proxy.

    Parameters:
    ----------
    method: Method of the request. "POST", "PATCH", "DELETE", "GET", "PUT".
    api_url: The DNS of the API. For example "api-dev.api.test.cloud"
    request_url: The request url. For example "/api/v1/users"
    body: Body of the requests.
    headers: Necessary headers for the requests. The "Authentication: Bearer {token}" token
    is mandatory. The token value is an OIDC token.
"""


import http.client


def iap_http_request(
    method: str,
    api_url: str,
    request_url: str,
    body: str,
    headers: dict[str, str],
):
    conn = http.client.HTTPSConnection(api_url)
    conn.request(method=method, url=request_url, body=body, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data.decode("utf-8")
