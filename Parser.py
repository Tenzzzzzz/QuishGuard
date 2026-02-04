import os
import matplotlib.pyplot as plt
import seaborn as sns
import json
from email import policy
import pickle
import os
from email.parser import BytesParser
from fileinput import close
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import base64
import mailparser
import hashlib
import imgkit
from html2image import Html2Image
import email
from email.message import EmailMessage
import io
import qrcode
import cv2
import numpy as np

def generate_attachment_only_eml():
    # 1. MATCH THE PAPER SPECS: Version 13, No Border
    qr = qrcode.QRCode(
        version=13,  # Crucial: 69x69 modules
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Low error correction
        box_size=10,
        border=4  # Crucial: No white margin
    )

    # We need enough data to fill a Version 13 QR
    # If the URL is too short, the library will add 'padding' modules
    # that look different from the paper's samples.
    qr.add_data('www.google.com')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_data = img_byte_arr.getvalue()

    # 2. Create Email
    msg = EmailMessage()
    msg['Subject'] = "Scanned Document from Printer"
    msg['From'] = "scanner@office.com"
    msg['To'] = "user@target.com"

    # 3. Create HTML Body (CLEAN - No IMG tags!)
    html_body = """
    <html>
    <body>
        <h2>You have a new message from OFFICE_PRINTER_01</h2>
        <p>Please review the attached scanned document.</p>
        <hr>
        <p style="font-size: small; color: gray;">Sent automatically by Canon ImageRUNNER</p>
    </body>
    </html>
    """

    msg.add_alternative(html_body, subtype='html')

    # 4. Attach the Image as a FILE (Content-Disposition: attachment)
    # We do NOT use 'add_related' here because it's not inline.
    msg.add_attachment(
        img_data,
        maintype='image',
        subtype='png',
        filename='scanned_doc_qr.png'
    )

    with open("attachment_only.eml", "wb") as f:
        f.write(msg.as_bytes())

    print("Generated 'attachment_only.eml'.")


generate_attachment_only_eml()

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

    with open(eml_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)

    html_part = msg.get_body(preferencelist=('html'))
    if html_part:
        clean_html = html_part.get_content()
        resolved_html = inline_cid_images(clean_html, image_assets)
        print("resolved_html =>",resolved_html)

        hti = Html2Image()
        paths = hti.screenshot(html_str=resolved_html, save_as='temp_qr.png')
        temp_path = paths[0]
        b=b''
        with open(temp_path, "rb") as f:
            binary_data_of_html_image = f.read()
            b=binary_data_of_html_image
        os.remove(temp_path)

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
            elif x_id:
                asset_id = x_id
            else:
                asset_id = "no_id"


            if asset_id:
                image_assets[asset_id] = {
                    "hash":hashlib.sha256(asset_id.encode("utf-8")).hexdigest(),
                    "filename": part.get_filename() or f"unknown_{asset_id}",
                    "mimetype": content_type,
                    "disposition": part.get_content_disposition(),
                    "payload": part.get_payload(decode=True)
                }




















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

    return analysis_manifest, image_assets,b


















def prepare_qr_for_model(binary_data, output_size=69):
    # 1. Load the original large image
    nparr = np.frombuffer(binary_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 2. Detect the QR code corners
    detector = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(img)

    if retval:


        return decoded_info
    else:
        print("QR Code not detected!")
        return None








manifest, assets,sh = walk_the_email("attachment_only.eml")
print(manifest)
print("assets",assets)
print(json.dumps(manifest, indent=4))
#so now i have the images assests + the photo, we need to get all images and try to detect the qr code

print("ss",sh)
#p2=prepare_qr_for_model(sh)

for i in assets.values():
    processed_qr=prepare_qr_for_model(i["payload"])
    print("data=>",processed_qr[0])
    print(type(processed_qr))

