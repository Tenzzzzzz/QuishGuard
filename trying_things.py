import email
from email.message import EmailMessage
import io
import qrcode
from PIL import Image


def generate_pdf_attack_eml():
    # 1. Generate QR Code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data('https://malicious-pdf-link.com')
    qr.make(fit=True)
    # Convert to RGB immediately to ensure compatibility with the document image
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # 2. Create a "Document" Image (A4 size roughly at 72dpi)
    a4_width, a4_height = 595, 842
    doc_img = Image.new('RGB', (a4_width, a4_height), 'white')

    # 3. Paste QR code into the document
    qr_w, qr_h = qr_img.size

    # Calculate Top-Left position (x, y)
    x = (a4_width - qr_w) // 2
    y = (a4_height - qr_h) // 2

    # FIX: Define the full 4-tuple box (Left, Top, Right, Bottom)
    box = (x, y, x + qr_w, y + qr_h)

    doc_img.paste(qr_img, box)

    # 4. Convert Image to PDF bytes
    pdf_buffer = io.BytesIO()
    doc_img.save(pdf_buffer, format='PDF', resolution=72.0)
    pdf_bytes = pdf_buffer.getvalue()

    # 5. Create Email
    msg = EmailMessage()
    msg['Subject'] = "Invoice #0034 - Please Review"
    msg['From'] = "billing@trusted-vendor.com"
    msg['To'] = "finance@target.com"
    msg.set_content("Please find the attached invoice for your review.")

    # 6. Attach the PDF
    msg.add_attachment(
        pdf_bytes,
        maintype='application',
        subtype='pdf',
        filename='Invoice_0034.pdf'
    )

    with open("pdf_attack.eml", "wb") as f:
        f.write(msg.as_bytes())

    print("Generated 'pdf_attack.eml' successfully.")


if __name__ == "__main__":
    generate_pdf_attack_eml()