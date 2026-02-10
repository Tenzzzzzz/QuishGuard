# 🛡️QuishGuard: Advanced QR Phishing (Quishing) Detection
QuishGuard is a high-performance machine learning pipeline designed to detect malicious URLs embedded in QR codes. By leveraging an XGBoost classifier trained on over 2.2 million samples, it identifies phishing attempts with a precision-first approach to minimize False Positives in security environments.
# 🚀 Key Features
## 📧 Advanced QR-Email Parsing
Stealth Extraction: Designed to parse complex .eml and multi-part MIME email files to extract all hidden "highly evasive" Qrs.
## 💎 High-Fidelity Threat Intelligence
Fresh Dataset: Utilizes a curated live-stream of malicious URLs from top-tier threat intel sources (PhishTank, OpenPhish, phiusiil, mendeley and URLhaus).

Massive Scale: Trained on a robust corpus of 2.1M+ Benign URLs and 135k+ Fresh Malicious URLs, ensuring the model recognizes current-day attack patterns.
## 🧠 Deep Feature Engineering
Lexicographical Profiling: Transforms raw URLs into a multi-dimensional feature vector. This stage involves handling missing or inconsistent data, tokenization, and extraction of relevant features from URLs, such as domain names, subdomains, and URL lengths
## ⚡ Production-Grade Performance
Precision Focused: Optimized to maintain a near-zero False Positive Rate (FPR), critical for reducing "security fatigue" in SOC environments.

Fast Inference and integration: Real-time classification in under 10ms per URL.


