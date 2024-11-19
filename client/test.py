import requests
creds = {"username": "quota73", "password": "test"}
r = requests.Session()
registered = True
if not registered:
    a=r.post("http://localhost:39472/register", json=creds)
    print(a.status_code, a.text)

b=r.post("http://localhost:39472/login", json=creds)
print(b.status_code, b.json())
token = b.json()["token"]

c = r.post("http://localhost:39472/new-conversation", json={"token": token, "members": ["quota73"], "title": "Balls"})
print(c.status_code, c.json())

d = r.post("http://localhost:39472/message", json={"token": token, "id": c.json()["id"], "content": "deez"})
print(d.status_code, d.text)