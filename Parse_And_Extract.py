from email import policy
import os
from bs4 import BeautifulSoup
import base64
import hashlib
from html2image import Html2Image
import email
import cv2
import numpy as np




def inline_cid_images(html, image_assets):
    resolved_html = html
    for cid, asset in image_assets.items():

        b64_payload = base64.b64encode(asset["payload"]).decode("ascii")
        data_uri = f"data:{asset['mimetype']};base64,{b64_payload}"

        target_str = f"cid:{cid}"
        resolved_html = resolved_html.replace(target_str, data_uri)

    return resolved_html



def walk_the_email(eml_path):
    image_assets = {}
    html_body = ""


    msg = email.message_from_binary_file(eml_path, policy=policy.default)
    from_header = msg.get('From', '')
    sender_domain = ""
    if '@' in from_header:
        sender_domain = from_header.split('@')[-1].strip(' <>')
    received_headers = msg.get_all('Received', [])
    sender_ip = "Unknown"
    if received_headers:
        import re
        ip_match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', received_headers[0])
        if ip_match:
            sender_ip = ip_match.group()

    analysis_manifest = {
        "metadata": {
            "subject": msg['subject'],
            "sender": from_header,
            "domain": sender_domain,
            "sender_ip": sender_ip
        },
        "fragments": []
    }
    for part in msg.walk():
        content_type = part.get_content_type()

        if content_type == "text/html":
            html = part.get_content()
            html_body = html_body + html
        elif part.get_content_maintype() == "image":
            cid = part.get("Content-ID", "").strip("<>")
            x_id = part.get("X-Attachment-Id", "")
            if (cid):
                asset_id = cid
            elif x_id:
                asset_id = x_id
            else:
                asset_id = "no_id"


            if asset_id:
                image_assets[asset_id] = {
                    "hash":hashlib.sha256(asset_id.encode("utf-8")).hexdigest(),
                    "mimetype": content_type,
                    "disposition": part.get_content_disposition(),
                    "payload": part.get_payload(decode=True)}
        elif html_body:
            soup = BeautifulSoup(html_body, 'html.parser')
            for img in soup.find_all('img'):
                src = img.get('src', '')
                style = img.get('style', '')
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


    html_part_from_body = msg.get_body(preferencelist=('html'))
    if html_part_from_body:
        clean_html = html_part_from_body.get_content()
        resolved_html = inline_cid_images(clean_html, image_assets)

        hti = Html2Image()
        paths = hti.screenshot(html_str=resolved_html, save_as='temp_qr.png')
        temp_path = paths[0]
        with open(temp_path, "rb") as f:
            binary_data_of_html_image = f.read()
            b = binary_data_of_html_image
        os.remove(temp_path)

    image_assets["Html_Photo"] = {
        "hash": hashlib.sha256("Html_Photo".encode("utf-8")).hexdigest(),
        "mimetype": "Email_Photo",
        "disposition": "None",
        "payload": b}
    return analysis_manifest, image_assets


def prepare_qr_for_model(binary_data):
    nparr = np.frombuffer(binary_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detector = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(gray)

    if retval:
        return decoded_info[0]
    else:
        return None











if __name__ == "__main__":
    pass


