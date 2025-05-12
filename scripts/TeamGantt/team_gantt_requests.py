import requests
from requests.auth import HTTPBasicAuth

# TeamGantt Token
client_id = '23c6d10e-fd7c-4e6b-bd0f-0d78410cb263'
client_secret = 'DG0LAmIC7U/mqkL8iPiOPmtJltU6dRGex8xIiVg1ewGM716Q7jTuhJFswWdoU/YG'
token = 'eyJraWQiOiJKT3ljWjRYNk1ubkhkRU9nQUxiWDI1ZlN4Wk1HWCtNXC9LTzIxb1ZjbER5QT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI0YzUxMTc3ZS00NDNkLTQ4NGUtYTdkZi0yMDNkMWEzNTJjOTgiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0yLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMl9RSHo0MzM4SW0iLCJjdXN0b206dXNlcl9pZCI6IjE0ODE5MDIzIiwiY29nbml0bzp1c2VybmFtZSI6IjRjNTExNzdlLTQ0M2QtNDg0ZS1hN2RmLTIwM2QxYTM1MmM5OCIsImF1ZCI6IjVlcGRnNWtvaGw4dHRvbWo2a2NlOHJ1Y2pkIiwiaWRlbnRpdGllcyI6W3sidXNlcklkIjoiMTAxMjg2NzY5NTgwMDA3MzY4MjQzIiwicHJvdmlkZXJOYW1lIjoiR29vZ2xlIiwicHJvdmlkZXJUeXBlIjoiR29vZ2xlIiwiaXNzdWVyIjpudWxsLCJwcmltYXJ5IjoiZmFsc2UiLCJkYXRlQ3JlYXRlZCI6IjE3NDI3ODEwMzU5ODgifV0sImV2ZW50X2lkIjoiYjc2ZDFlMWMtMTE4My00YmFhLWE1ZTAtZTZkNjMwYWViNzA1IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NDU2NTE2ODYsImV4cCI6MTc0NTc0MjMwMCwiaWF0IjoxNzQ1NzM4NzAwLCJlbWFpbCI6Im1pa3lsZS5tb3NxdWVyYUBzanN1LmVkdSJ9.CjvxcM1byIIG9xk3TPhkYaOuBk5ZTlyKDPnHKZcV5iZigo4pqCEsimftBJkgZZEGNMLUvAMDc-pZpsCGOHXwJ_jP8i-HT82FnU55C_DwxFLEPbbhZDiZTxQmsA-o1L3onRf4aUV6KtD_0qKCXJTaUOCbeAs8NrkKWQCw4IJ4FO77QBI75JHkkzscB-_qSrXeLBlUPCkN3zI7wJ2CA-smc9pulr1rfy7wH5a0hQRcktfmH4Y3lx7eJIET9vNSZ-lttGf_uMSpNO8Xoa1Y4kYyS_kRpyJ35deKGk3ODiRKdDThCr4QFVBPa5YlMNXjvjtcoSS_z_FNaOJl17gGW52udg'
def request_token(username, password):
    """Prints the requested token or an error if the request fails. Returns the response."""
    auth_url = 'https://auth.teamgantt.com/oauth2/token'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }

    response = requests.post(auth_url, data=data, auth=HTTPBasicAuth(client_id, client_secret), headers=headers)

    if response.ok:
        print('Access Token', response.json()['id_token'])
        print('Access Token', response.json()['refresh_token'])
        print('Access Token', response.json()['access_token'])
        print('Expires: ', response.json()['expires_in'])
    else:
        print(f'Error: {response.status_code}')
        print(response.text)

    return response

def request_revoke_refresh_tokens():
    """Revokes all refresh tokens which are used to fresh your session and obtain new id tokens"""
    auth_url = 'https://auth.teamgantt.com/revoke'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {'token': 'eyJraWQiOiJtRVNwOVFJUzNBMVluQWJVUXFaUHZWZjM1Rk5PZGlLeTNWSFFRbTRNR0prPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI0YzUxMTc3ZS00NDNkLTQ4NGUtYTdkZi0yMDNkMWEzNTJjOTgiLCJldmVudF9pZCI6ImMzNzMzM2Y3LTQ5MDItNDVjMy04YTY2LTkyYWNmYzY5NDYzMyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3NDU2NTEyMjQsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTIuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0yX1FIejQzMzhJbSIsImV4cCI6MTc0NTY1NDgyNCwiaWF0IjoxNzQ1NjUxMjI0LCJqdGkiOiI4ZjUxMjg0Zi01YjFhLTQzZTUtOWIzNi1jMTZkNDhmYmQ2NDQiLCJjbGllbnRfaWQiOiI1ZXBkZzVrb2hsOHR0b21qNmtjZThydWNqZCIsInVzZXJuYW1lIjoiNGM1MTE3N2UtNDQzZC00ODRlLWE3ZGYtMjAzZDFhMzUyYzk4In0.L64um-UPqt6fEGDknf_TZ0_dyrVYNdr8ZyZq3EASx9MZZWpvtx9u7Wi-H2_vZoddoLnZLfdNFvEkYDyvMXVK9d8rLbf9PMxie1byqeemb8I9KNUyT2wue4y6ev1R_vq7Z3ys4i9qg4qp-wWF0mkij9Oq2t7Ogtnxg0fQxH5u9bSgx5nsBYdWlMUowec16u9oHaaYxDCzi53c2RrbG3tEqIs3IMCC5fZpCWVsqls1aP6vqRZ5IIfiAQ6o9KURaxBaCy7ezkzAGuoupOL-ooob4oiTu0AGx4HszoSUwSdhsPsXbf9EpnFj9rTg5-7ZZAKeI0LdkvtN-k6P68jd1OOn_w'}

    response = requests.post(auth_url, data=data, auth=HTTPBasicAuth(client_id, client_secret), headers=headers)

    if response.ok:
        pass
    else:
        print(f'Error: {response.status_code}')
        print(response.text)

    return response

def request_exchange_refresh_token():
    auth_url = 'https://auth.teamgantt.com/oauth2/token'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': 'eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.IXAf3U6-kd8_m3tJIqCp25vcQ3-8j5EGHwWlkk6nZl6PYuaKUavN0D95TXj20_dqrGyDep4JBSOjOCE2YmBAoXWmkh4Qsx2ZCiu_IpEb9c-SRoGP-Z6y3Mdzt_CMHe9_Ayq9ggGkBf1LERXolF14my0KWQCPZmXFepgsaYqHhUYd4mi1w6VItZS8zXjMv2WJLkQGp-fD6sQX7VIxyV4S0jFpz0hDUZWU4bBHDUtQBJEQpqEXhcKygXjod_LZZm8mcV8B4Ex7hNhSwLE241qBY3DuteBztAAYLm4t4cwLDiv8fvmT-l5k_GNR7bBaoipP_Bb3WDeWw_zEnCIe2SVJIg.zgjwQFD0Jz4WpWy2.JV3hDn8ozZm3fd8ci7dUYL4x1NZkVCz3u5ni0D-_WcWgMmJDn7JLLCgjiinGSF0eGJRJ_BtGmzhqweb19rfNafmoeN7d190-iO_bb8mHOd9qz3eM97tPfH78Krdg0bI2dpR9mEZYfl3ApbTvhT3gx0GnE2MOXlX16VQHl_nLoA4sFf6AEOA73reqKw8Wd1XlSbjKMTuFRWOlqtETzJ8PbME5noKpBUFOMxTxY4g_Ca7KcaZtAiPTg-7HwgGnTLmNTrLEdoJlSBZS4s2n1B-kL3TmLCLrbO_vCb6AJR3yRfbqZ6lG9sROrKOYCRO3o-KjwWjNdyTM3yi5t540HOgTRDh9kdwxLzviP-sMGjFmr28kLonZeTOXOi56LL8_6ohQMDEuWlFtNOeoPaY1FWimZ3C7TgL1LadRwlOYV7poGv9FurXqPBZh9MNeKWLmKX-kEUOJTE5aaxP2_FRwJK8H5wn3LyT_80Ce7edfBBUE8Cn0NUJ41h2cXvJ5-85ss4D1jJPhdG5oYvLXZ-emuaeFbu4TCsLxADJTnT3z0TlFor-hfVNnMjePxeOaHz4V3k-D8C8UJCiHTv9i0V5RtNN5vINNncva_RrGxrKZSLp5KUxiZktfbkSUbQ4HsQNPj8J1XX60f_YNyNVQuQZBnRMFD5RCE-QVd_8upLnmgZQHIGyYazmKocc1Jak7o03aG4196Rq_oGDUKrWCMrfNWVXqK3DJsWc-KGYLQ5vnpkM9KuQf3_Mqze1leX6PGUlN6SknNj-q2Tn6pWFFVWO1nQ67zfNlN_9rC3ta8uQnarLstcWK4l4AM4EiQxUq1AAr_vQnArVNgQrlruxt8LysKnnNp3krmjsGFneIYY-QBzj8txHj7E9hZNGV8GIacnTt8C3Vu2bYcVBOITLIswIzMyqF7zyK_Uy4Ne_VYNB68BQnrQlsUNZKQTPORt2Yykp3HSWUxiVh4x1HGYB0xVFqcINi1GURkhJQWs6Cb53qY8OSEqzh4joQn4pq2Z41yYPH_vf8RJW2HxKmtJHIAQMpnEiQatv_tZBhs45oJwdUU5UM3S9x8vqN1aq6HGsX_Xy6m8GLe3DDDTL05kbOzaYDCUWwbL9_XAqf-k6XDarV5xc8I3iSSErqgdWJ39FMUbmaFKhQpNnH29nThrNeYEEzHB-_Qjx9-g2K7HUMV2y0RDmMYfeLXUYTB2SgWqeDOB5ZgewLEOsPUDaTMIzzGNSRnXQY26fJTEUFA1BAvNvSVAd06jEImiIMXiQ39JXV_S6SeIDmKwRTCgSK3LMJ5y9KJaGtGi8UBbzOpYMlrb-CSR8ViNFq8EdK1hHOidZJFQ.liSs-7QeQwx4uoBJO-6R5g'
    }

    response = requests.post(auth_url, data=data, auth=HTTPBasicAuth(client_id, client_secret), headers=headers)

    if response.ok:
        print(response.json())
    else:
        print(f'Error: {response.status_code}')
        print(response.text)

    return response

def request_users():
    url = 'https://api.teamgantt.com/v1/companies/2319331/users'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        users = response.json()
        for user in users:
            print(f'{user["first_name"]} {user["last_name"]}')
    else:
        print(f'Error: {response.status_code}')
        print(response.text)

    return response

def request_get_task(id):
    url = f'https://api.teamgantt.com/v1/tasks/'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        print(response.json()[200])
    else:
        print(f'Error: {response.status_code}')
        print(response.text)

def request_groups():
    url= f'https://api.teamgantt.com/v1/groups/34017047 '

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        print(response.json()['children'])
    else:
        print(f'Error: {response.status_code}')
        print(response.text)


#request_get_task(12)
#request_token('mikyle.mosquera@sjsu.edu', '27972kNX')

request_groups()

#request_exchange_refresh_token()
#request_users()