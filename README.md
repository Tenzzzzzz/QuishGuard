# 🛡️QuishGuard: Advanced QR Phishing (Quishing) Detection
QuishGuard is a high-performance machine learning pipeline designed to detect malicious URLs embedded in QR codes. By leveraging an XGBoost classifier trained on over 2.2 million samples, it identifies phishing attempts with a precision-first approach to minimize False Positives in security environments.
# 🚀 Key Features
## 📧 Advanced QR-Email Parsing
Stealth Extraction: Designed to parse complex .eml and multi-part MIME email files to extract all hidden "highly evasive" Qrs.
##  High-Fidelity Threat Intelligence
Fresh Dataset: Utilizes a curated live-stream of malicious URLs from top-tier threat intel sources (PhishTank, OpenPhish, phiusiil, mendeley and URLhaus).

Massive Scale: Trained on a robust corpus of 2.1M+ Benign URLs and 135k+ Fresh Malicious URLs, ensuring the model recognizes current-day attack patterns.
##  Deep Feature Engineering
Lexicographical Profiling: Transforms raw URLs into a multi-dimensional feature vector. This stage involves handling missing or inconsistent data, tokenization, and extraction of relevant features from URLs, such as domain names, subdomains, and URL lengths
##  Production-Grade Performance
Precision Focused: Optimized to maintain a near-zero False Positive Rate (FPR), critical for reducing "security fatigue" in SOC environments.

Fast Inference and integration: Real-time classification in under 10ms per URL.
#  System Architecture
* Ingestion: Receives an email file via the Flask API.

* Extraction: Scans the body and attachments for QR codes.

* Transformation: Converts the extracted URL into 15+ numerical features (length, special character ratios, tld, etc.).

* Classification: The XGBoost model detects the Malicious URLs.

* Response: Returns a JSON report with a safety verdict and other details about the email.
#  API Usage
QuishGuard provides a lightweight Flask API for seamless integration with existing SOAR or SIEM platforms.

### **Scan Email File**
`POST` `/submit`

#### **Request Body**
- `file` (binary): The `.eml` file to be analyzed.

#### **Python Integration Example**
```python
import requests

# Load your suspicious email file
with open("suspicious_email.eml", "rb") as f:
    files = {"file": f}
    response = requests.post("http://127.0.0.1:5001/submi", files=files)
    
print(response.json())
```
Sample Response
```
{
  "Email status": "Rejected",
  "fragments": [],
  "https://split-flexbox.com": "malicious",
  "metadata": {
    "domain": "test.com",
    "sender": "test@test.com",
    "sender_ip": "Unknown",
    "subject": "Split QR - Flexbox"
  }
}
```
# 📦 Installation & Setup
```
git clone https://github.com/Tenzzzzzz/Quishing.git
python -m venv .venv
source .venv/bin/activate
cd Requirments
pip install -r requirements.txt
cd ..
python app.py
```
> or if you want to reproduce from the beginning
```bash
git clone https://github.com/Tenzzzzzz/Quishing.git
python -m venv .venv
source .venv/bin/activate
cd Requirments
pip install -r requirements.txt
cd ..
```

Then execute the code in the Jupyter notebook
``` bash
python feature_extraction.py
python the_model.py
python app.py
```
# Future Roadmap
1- 
2-
3-
# Contributing
Contributions are welcome! Please open an issue or submit a pull request for any feature additions or bug fixes.
