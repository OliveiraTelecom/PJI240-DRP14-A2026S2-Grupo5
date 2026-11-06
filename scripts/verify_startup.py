"""Verifica o serviço já iniciado pelo Compose, sem criar segunda instância."""
import json
import time
from urllib.request import urlopen
from urllib.error import URLError

for attempt in range(30):
    try:
        with urlopen('http://127.0.0.1:5000/health', timeout=2) as response:
            result = json.load(response)
        if result == {'status': 'ok', 'database': 'connected'}:
            print('Aplicação e PostgreSQL conectados. Abra a porta privada 5000.')
            break
    except (URLError, TimeoutError, json.JSONDecodeError):
        pass
    time.sleep(1)
else:
    raise SystemExit('Serviço indisponível. Consulte os logs do Compose. Se o Codespace estiver em recovery mode, use Codespaces: Rebuild Container; não inicie um segundo servidor.')
