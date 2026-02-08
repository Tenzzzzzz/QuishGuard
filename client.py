import requests
f=b'\x12\x31'
lolxd={'file':("gn.eml",f)}
response = requests.post("http://127.0.0.1:5000/submit",files=lolxd)
print(response.text)