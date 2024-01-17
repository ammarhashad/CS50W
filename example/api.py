import requests, json, base64

api = "xxx"

pssh = "AAAAW3Bzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAADsIARIQ62dqu8s0Xpa7z2FmMPGj2hoNd2lkZXZpbmVfdGVzdCIQZmtqM2xqYVNkZmFsa3IzaioCSEQyAA=="

cert = None # <base64>

challenge = requests.post(url=api, json={"pssh": pssh, "cert": cert})

if not challenge.ok:
  print(challenge.json())
  exit(1)
  
if challenge.json().get("cached"):
  print(challenge.json()["keys"])
  exit(1)

license = requests.post(
  url="https://cwip-shaka-proxy.appspot.com/no_auth", 
  data=base64.b64decode(challenge.json()["chal"])
)
keys = requests.post(
  url=api, 
  json={
    "license": base64.b64encode(license.content).decode(), 
    "sid": challenge.json()["sid"]
  }
)
print(keys.json()["keys"])
