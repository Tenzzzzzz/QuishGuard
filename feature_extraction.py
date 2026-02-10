
import re
import sys
from urllib.parse import urlparse
import logging
import pandas as pd
from tld import get_tld
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


    def abnormal_url(self, url):
        try:
            if not url.startswith(('http://', 'https://')):
                parse_url = 'http://' + url
            else:
                parse_url = url

            hostname = urlparse(parse_url).hostname

            if not hostname:
                return 1


            if str(hostname) not in url:
                return 1
            else:
                return 0  # Normal (return 0)

        except Exception as e:
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






def process_and_save_features(input_csv, output_file):
    try:
        logging.info(f"Loading raw data from {input_csv}")
        df = pd.read_csv(input_csv)

        if 'url' not in df.columns:
            df.rename(columns={df.columns[0]: 'url'}, inplace=True)

        obj = transformationFunctions()
        logging.info("Starting feature extraction...")

        # Apply each function from your transformationFunctions class
        df['use_of_ip'] = df['url'].apply(obj.having_ip_address)
        df['abnormal_url'] = df['url'].apply(obj.abnormal_url)
        df['count.'] = df['url'].apply(obj.count_dot)
        df['count-www'] = df['url'].apply(obj.count_www)
        df['count@'] = df['url'].apply(obj.count_atrate)
        df['count_dir'] = df['url'].apply(obj.no_of_dir)
        df['count_embed_domain'] = df['url'].apply(obj.no_of_embed)
        df['short_url'] = df['url'].apply(obj.shortening_service)
        df['count%'] = df['url'].apply(obj.count_per)
        df['count?'] = df['url'].apply(obj.count_ques)
        df['count-'] = df['url'].apply(obj.count_hyphen)
        df['count='] = df['url'].apply(obj.count_equal)
        df['url_length'] = df['url'].apply(obj.url_length)
        df['count_https'] = df['url'].apply(obj.count_https)
        df['count_http'] = df['url'].apply(obj.count_http)
        df['hostname_length'] = df['url'].apply(obj.hostname_length)
        df['sus_url'] = df['url'].apply(obj.suspicious_words)
        df['fd_length'] = df['url'].apply(obj.fd_length)


        def get_tld_len(url):
            try:
                res = get_tld(url, as_object=True, fail_silently=True)
                return len(res.tld) if res else 0
            except:
                return 0

        df['tld_length'] = df['url'].apply(get_tld_len)
        df['count_digits'] = df['url'].apply(obj.digit_count)
        df['count_letters'] = df['url'].apply(obj.letter_count)

        if output_file.endswith('.xlsx'):
            df.to_excel(output_file, index=False)
        else:
            df.to_csv(output_file, index=False)

        logging.info(f"Successfully saved features to {output_file}")
        print(f" Features extracted and saved to: {output_file}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    input_file = r"final_dataset\Final_clean_dataset.csv"
    output_file = "features_processed.csv"

    process_and_save_features(input_file, output_file)