import os
import json
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
import base64
import mailparser
import hashlib
import imgkit
from html2image import Html2Image
import email

image_assets = {}
html_body = ""

def walk_the_email(eml_path):
    with open(eml_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)




    for part in msg.walk():
        print("part =>",part)
        content_type = part.get_content_type()
        print("content_type =>",content_type)

        if content_type == "text/html":
            html_body = part.get_content()


        elif part.get_content_maintype() == "image":
            cid = part.get("Content-ID", "").strip("<>")
            x_id = part.get("X-Attachment-Id", "")
            if (cid):
                asset_id = cid
            else:
                asset_id = x_id


            if asset_id:
                image_assets[asset_id] = {
                    "hash":hashlib.sha256(asset_id.encode("utf-8")).hexdigest(),
                    "filename": part.get_filename() or f"unknown_{asset_id}",
                    "mimetype": content_type,
                    "disposition": part.get_content_disposition(),
                    "payload": part.get_payload(decode=True)
                }

    with open(eml_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)

    # 2. Extract ONLY the HTML body
    # preferencelist=('html') ensures you get the rich version if it exists
    html_part = msg.get_body(preferencelist=('html'))
    clean_html = html_part.get_content()

    # 3. Convert to Photo
    hti = Html2Image()
    hti.screenshot(html_str=clean_html, save_as='clean_email.png')

    print("------------------------------------- nexistheemail\n","--------------------")















    analysis_manifest = {"metadata": {"subject": msg['subject']}, "fragments": []}





    if html_body:
        soup = BeautifulSoup(html_body, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src', '')
            style = img.get('style', '')  # Crucial for Split-QR detection
            fragment_info = {"html_tag": str(img), "style": style}

            if src.startswith('cid:'):
                clean_id = src.replace('cid:', '')
                fragment_info.update({
                    "id": clean_id,
                    "type": "inline",
                    "status": "Found" if clean_id in image_assets else "Missing"
                })
            elif src.startswith('data:image'):
                fragment_info.update({
                    "type": "embedded_data_uri",
                    "status": "Extracted",
                    "metadata": "Embedded directly in HTML"
                })
            elif src.startswith("http://") or src.startswith("https://"):
                fragment_info.update({
                    "url": src,
                    "type": "remote"
                })
            else:
                fragment_info.update({
                    "src": src,
                    "type": "other"
                })

            analysis_manifest["fragments"].append(fragment_info)

    return analysis_manifest, image_assets



"""
tests
"""
manifest, assets = walk_the_email("mail.eml")
print(manifest)
print(assets)
print(json.dumps(manifest, indent=4))
print(f"\n[+] Total Inline Images Found: {len(assets)}")
