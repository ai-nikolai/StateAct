# import requests
import os
import requests_unixsocket

if __name__=="__main__":
    prefix="http+unix://"
    
    socket_root_path = os.path.dirname(os.path.realpath(__file__))
    socket_name=os.path.join("tmp","flask.sock")
    full_socket_path = os.path.join(socket_root_path,socket_name)
    full_socket_path_clean = full_socket_path.replace('/', '%2F')

    url_path = "/abc"


    full_url = prefix+full_socket_path_clean+url_path
    print(full_url)

    session = requests_unixsocket.Session()
    # Access /path/to/page from /tmp/profilesvc.sock
    r = session.get(full_url)
    print(r.text)
    assert r.status_code == 200
