from flask import Flask, request, jsonify
import Parse_And_Extract
import model_scan
app = Flask(__name__)
@app.route('/submit', methods=['POST'])
def receive_email_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'File name not provided'})

    if file and file.filename.endswith( '.eml'):
        Ma=False
        images_to_be_scanned=[]
        qrs_data=[]
        manifest, assets =Parse_And_Extract.walk_the_email(file)
        for i in assets.values():
            images_to_be_scanned.append(i["payload"])


        for i in images_to_be_scanned:
            R=Parse_And_Extract.prepare_qr_for_model(i)
            if(R!=None):
                qrs_data.append(R)

        for i in qrs_data:
            response = model_scan.scan(i)
            if int(response)==1:
                str="malicious"
                Ma=True
            else:
                str="benign"
            manifest[i]=str

        if Ma==True:
            manifest["Email status"]="Rejected"
        else:
            manifest["Email status"]="Accepted"
        return manifest


















if __name__ == '__main__':
    app.run(debug=True, port=5001)
