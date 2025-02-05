import requests
import requests_unixsocket

if __name__=="__main__":
    full_url = "http+unix://tmp/webshop.sock"
    session = requests_unixsocket.Session()

    r = session.get(full_url)
    registry_config = r.json()['RegistryConfig']
    print(json.dumps(registry_config, indent=4))
    # with requests_unixsocket.monkeypatch():
    #     response = requests.get(full_url)
    # print(response.text)