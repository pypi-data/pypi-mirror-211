import requests, time


def makeRequest(url:str, request_type:str="post", params=None, body=None, timeout=60, max_tries=1):
    """
    Esegue una richiesta HTTP di tipo 'request_type' e restituisce un oggetto Response contenente:
    - response: contenuto JSON (se possibile) o testuale della risposta
    - status: esito sull'esecuzione della richiesta (True/False)
    - status_code: status code HTTP sull'esecuzione della richiesta (es. 200,400,500)
    - exceptions: lista delle eccezioni (un elemento per ogni tentativo fallito)
    - duration: durata, in secondi, della singola richiesta
    - tries: numero di tentativi effettuati
    """
    class Response:
        def __init__(self,response,status,exceptions,tries,duration):
            self.status = status
            try:
                self.status_code = response.status_code
            except:
                self.status_code = None
            self.exceptions = exceptions
            self.tries = tries
            self.duration = round(duration,2)
            try:
                self.response = response.json()
            except AttributeError:
                self.response = response
            except:
                self.response = response.text
        def __repr__(self):
            return(f"<Response status_code='{self.status_code}' in {self.duration}s>")

    gotSuccessResponse, tries, exceptions = False, 1, [] 
    while not gotSuccessResponse and tries <= max_tries:
        print(f"Making {request_type.upper()} request to '{url}' ({tries}/{max_tries})...")
        try:
            startTimestamp = time.time()
            if request_type.lower() == "post":
                response = requests.post(url, params=params, json=body, timeout=timeout)
            elif request_type.lower() == "get":
                response = requests.get(url, params=params, json=body, timeout=timeout)
            else:
                response = requests.get(url, params=params, json=body, timeout=timeout)
            if str(response.status_code)[0] not in ["5","4"]:
                gotSuccessResponse = True
                print(f"Made {request_type.upper()} requests to '{url}'. Done in '{tries}/{max_tries}' attempts!")
                output = Response(response,True,exceptions,tries,time.time() - startTimestamp)
            else:
                print(f"Made {request_type.upper()} requests to '{url}'. Failed {tries}/{max_tries} times!")
                output = Response(response,False,exceptions,tries,time.time() - startTimestamp)
                tries += 1
                time.sleep(int(1+tries/4))
        except Exception as e:
            print(f"Made {request_type.upper()} requests to '{url}'. Failed {tries}/{max_tries} times!")
            exceptions.append(e)
            output = Response(None,False,exceptions,tries,time.time() - startTimestamp)
            tries += 1
            time.sleep(int(1+tries/4))
    return output