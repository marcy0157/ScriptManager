import requests

def get_server_version(url):
    try:
        # Inviare una richiesta GET al sito web
        response = requests.get(url)

        # Verificare se la risposta è stata ricevuta con successo
        if response.status_code == 200:
            # Ottenere il valore dell'header 'Server'
            server_info = response.headers.get('Server')

            if server_info:
                return f"La versione del server per {url} è: {server_info}"
            else:
                return "Non è stata trovata alcuna informazione sul server."
        else:
            return f"Errore nella richiesta: {response.status_code}"
    except requests.exceptions.MissingSchema:
        return "Assicurati di fornire un URL valido, incluso il protocollo (http:// o https://)."
    except requests.exceptions.RequestException as e:
        return f"Si è verificato un errore durante la richiesta: {e}"

# Esempio di utilizzo
url_input = input("Inserisci l'indirizzo del sito web (es. http://example.com): ")
print(get_server_version(url_input))
