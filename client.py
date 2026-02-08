import requests
with open("attachment_only.eml", "rb") as f:
    files={"file": f}
    response = requests.post("http://127.0.0.1:5001/submit",files=files)
    print(response.text)