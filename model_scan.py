import numpy as np
import xgboost as xgb
import re
from urllib.parse import urlparse
from tld import get_tld
import sys




def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error Occured in Python Script name [{0}] Line No. [{1}] Error Message [{2}]".format(file_name,
                                                                                                          exc_tb.tb_lineno,
                                                                                                          str(error))

    return error_message


class customException(Exception):

    # Constructor or Initializer
    def __init__(self, error_message, error_detail: sys):
        super().__init__(self, error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message

class transformationFunctions():

    def __init__(self):
        pass

    def having_ip_address(self, url):
        try:
            ip_pattern = (
                r'('
                r'(?:[01]?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:[01]?\d\d?|2[0-4]\d|25[0-5])){3}|' 
                r'(?:0x[0-9a-fA-F]{1,2}\.){3}(?:0x[0-9a-fA-F]{1,2})|'  
                r'(?:[a-fA-F0-9]{1,4}:){1,7}[a-fA-F0-9]{1,4}|'  
                r'::(?:[a-fA-F0-9]{1,4}:){0,7}[a-fA-F0-9]{1,4}'  
                r')'
            )
            match = re.search(ip_pattern, url)  # Ipv6
            if match:
                return 1
            else:
                return 0

        except Exception as e:
            raise customException(e, sys)

    from urllib.parse import urlparse

    def abnormal_url(self, url):
        try:
            # 1. Handle URLs without http/https prefix so urlparse doesn't fail
            if not url.startswith(('http://', 'https://')):
                parse_url = 'http://' + url
            else:
                parse_url = url

            hostname = urlparse(parse_url).hostname

            if not hostname:
                return 1  # Abnormal: No hostname could be parsed

            # 2. Check if the parsed hostname actually exists in the original URL
            # If it's NOT in the URL, that's abnormal (return 1)
            if str(hostname) not in url:
                return 1
            else:
                return 0  # Normal (return 0)

        except Exception as e:
            # If parsing fails entirely, it's suspicious
            return 1

    def count_dot(self, url):
        try:
            count_dot = url.count('.')
            return count_dot

        except Exception as e:
            raise customException(e, sys)

    def count_www(self, url):
        try:
            url.count('www')
            return url.count('www')
        except Exception as e:
            raise customException(e, sys)

    def count_atrate(self, url):
        try:
            return url.count('@')
        except Exception as e:
            raise customException(e, sys)

    def no_of_dir(self, url):
        try:
            urldir = urlparse(url).path
            #     print(urldir)
            return urldir.count('/')
        except Exception as e:
            raise customException(e, sys)

    def no_of_embed(self, url):
        try:
            urldir = urlparse(url).path
            return urldir.count('//')
        except Exception as e:
            raise customException(e, sys)

    def suspicious_words(self, url):
        try:
            match = re.search('PayPal|login|signin|bank|account|update|free|lucky|service|bonus|ebayisapi|webscr|urgent|required|suspended|',
                              url)
            if match:
                return 1
            else:
                return 0
        except Exception as e:
            raise customException(e, sys)

    def shortening_service(self, url):
        try:
            patterns = (
                r'\b(bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|lnkd\.in|'
                r'db\.tt|qr\.ae|adf\.ly|bitly\.com|cur\.lv|tinyurl\.com|ity\.im|q\.gs|po\.st|bc\.vc|'
                r'twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|prettylinkpro\.com|'
                r'scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|link\.zip\.net)\b'
            )
            match =re.search(patterns, url, flags=re.IGNORECASE)
            if match:
                return 1
            else:
                return 0
        except Exception as e:
            raise customException(e, sys)

    def count_https(self, url):
        try:
            return url.count('https')
        except Exception as e:
            raise customException(e, sys)

    def count_http(self, url):
        try:
            return url.count('http')
        except Exception as e:
            raise customException(e, sys)

    def count_per(self, url):
        try:
            return url.count('%')
        except Exception as e:
            raise customException(e, sys)

    def count_ques(self, url):
        try:
            return url.count('?')
        except Exception as e:
            raise customException(e, sys)

    def count_hyphen(self, url):
        try:
            return url.count('-')
        except Exception as e:
            raise customException(e, sys)

    def count_equal(self, url):
        try:
            return url.count('=')
        except Exception as e:
            raise customException(e, sys)

    def url_length(self, url):
        try:
            return len(str(url))
        except Exception as e:
            raise customException(e, sys)

    def hostname_length(self, url):
        try:
            return len(urlparse(url).netloc)
        except Exception as e:
            raise customException(e, sys)

    # First Directory Length
    def fd_length(self, url):
        try:
            urlpath = urlparse(url).path
            try:
                return len(urlpath.split('/')[1])
            except:
                return 0
        except Exception as e:
            raise customException(e, sys)

    def tld_length(self, tld):
        try:
            try:
                return len(tld)
            except:
                return -1
        except Exception as e:
            raise customException(e, sys)

    def digit_count(self, url):
        try:
            digits = 0
            for i in url:
                if i.isnumeric():
                    digits += 1
            return digits
        except Exception as e:
            raise customException(e, sys)

    def letter_count(self, url):
        try:
            letters = 0
            for i in url:
                if i.isalpha():
                    letters += 1
            return letters
        except Exception as e:
            raise customException(e, sys)



class QuishingScanner:
    def __init__(self, model_path):
        self.model = xgb.XGBClassifier()
        self.model.load_model(model_path)
        self.transform = transformationFunctions()

    def extract_features(self, url):
        features = []
        features.append(self.transform.having_ip_address(url))
        features.append(self.transform.abnormal_url(url))
        features.append(self.transform.count_dot(url))
        features.append(self.transform.count_www(url))
        features.append(self.transform.count_atrate(url))
        #features.append(self.transform.no_of_dir(url))
        features.append(self.transform.no_of_embed(url))
        features.append(self.transform.shortening_service(url))
        features.append(self.transform.count_per(url))
        features.append(self.transform.count_ques(url))
        features.append(self.transform.count_hyphen(url))
        features.append(self.transform.count_equal(url))
        features.append(self.transform.url_length(url))
        features.append(self.transform.count_https(url))
        features.append(self.transform.count_http(url))
        features.append(self.transform.hostname_length(url))
        features.append(self.transform.suspicious_words(url))
        features.append(self.transform.fd_length(url))


        try:
            res = get_tld(url, as_object=True, fail_silently=True)
            tld_len = len(res.tld) if res else 0
        except:
            tld_len = 0
        features.append(tld_len)
        features.append(self.transform.digit_count(url))
        features.append(self.transform.letter_count(url))


        return np.array(features).reshape(1, -1)

    def scan(self, url):
        features = self.extract_features(url)
        prediction = self.model.predict(features)[0]
        return prediction


def scan(url):
    scanner = QuishingScanner("model/url_detection_model.json")
    r=scanner.scan(url)
    return r

if __name__ == "__main__":
    pass
