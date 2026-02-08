import requests
from flask import Flask, request, jsonify
import Parse_And_Extract
import model_scan
app = Flask(__name__)
@app.route('/submit', methods=['POST'])
def receive_email_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provideddsa'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file provided'})

    if file and file.filename.endswith( '.eml'):
        print("hi")
        images_to_be_scanned=[]
        qrs_data=[]
        manifest, assets,photo =Parse_And_Extract.walk_the_email(file)
        images_to_be_scanned.append(photo)
        for i in assets.values():
            images_to_be_scanned.append(i["payload"])
        for i in images_to_be_scanned:
            qrs_data.append(Parse_And_Extract.prepare_qr_for_model(i))
        for url in qrs_data:
            response = model_scan.scan(url)
            print(response)

















if __name__ == '__main__':
    app.run(debug=True, port=5001)
    print('DONE')
