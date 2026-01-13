import email
from email.message import EmailMessage
import io
import qrcode


def generate_background_attack_eml():
    # 1. Generate QR
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data('https://hidden-in-css.com')
    qr.make(fit=True)
    img = qr.make_image(fill_color="red", back_color="white")  # Red for visibility

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_data = img_byte_arr.getvalue()

    cid_id = "bg_qr_ref"

    # 2. Create Email
    msg = EmailMessage()
    msg['Subject'] = "Offer Inside: Background Image Test"
    msg['From'] = "marketing@test.com"
    msg['To'] = "user@test.com"

    # 3. HTML Body - NO <img> TAGS!
    # We use a DIV with background-image properly sized to show the QR
    html_body = f"""
    <html>
    <body>
        <h2>Exclusive Offer</h2>
        <p>Your viewer might not see this if it blocks background images.</p>

        <!-- The Trap: Using CSS background instead of img tag -->
        <div style="
            width: 350px; 
            height: 350px; 
            background-image: url('cid:{cid_id}'); 
            background-size: contain; 
            background-repeat: no-repeat;
            border: 1px solid #ccc;">

            <!-- We can even put fake text over it to confuse OCR if we wanted -->
            <br><br>
        </div>

        <p>Reference: #BG-CSS-ATTACK</p>
    </body>
    </html>
    """

    msg.add_alternative(html_body, subtype='html')

    # 4. Attach Image
    msg.get_payload()[0].add_related(
        img_data,
        maintype='image',
        subtype='png',
        cid=f"<{cid_id}>"
    )

    with open("background_attack.eml", "wb") as f:
        f.write(msg.as_bytes())

    print("Generated 'background_attack.eml'. Check your JSON manifest!")


if __name__ == "__main__":
    generate_background_attack_eml()