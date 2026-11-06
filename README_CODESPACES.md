# Iniciar a demonstração no GitHub Codespaces

## Procedimento recomendado

1. Abra o repositório no GitHub, selecione **Code > Codespaces > Create codespace** e escolha a branch `main`.
2. Aguarde a inicialização do contêiner **web** com o serviço PostgreSQL **db**.
3. Na aba **Ports**, abra a porta **5000**, configurada como **Private**.
4. Acesse a página principal e depois **/health**. A resposta esperada é `{"status":"ok","database":"connected"}`.
5. Demonstre: dashboard, cadastro de cliente/motorista/veículo, registro e atualização de entrega e relatórios.

## Diagnóstico

Dentro do terminal do Codespace (contêiner `web`):
```bash
python -m pytest -q
python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/health', timeout=5).read().decode())"
```

Para testar o banco real sem alterar seus cadastros, use `TEST_DATABASE_URL="$DATABASE_URL" python -m pytest tests/test_integration.py -q`. Os testes criam e removem apenas esquemas temporários com prefixo `aceitacao_`.

Os comandos `docker compose ps` e `docker compose logs --tail=100 web db` devem ser executados em um ambiente com acesso ao Docker, como o terminal do host ao executar localmente. O contêiner `web` não inclui o Docker CLI.

Se o Codespace já existia antes das correções, execute `git pull` e selecione **Codespaces: Rebuild Container** na paleta de comandos. Não execute `python app.py` novamente: o servidor já inicia pelo Compose.

A inicialização SQL acontece somente na criação inicial do volume de PostgreSQL. Caso já exista um volume de uma execução anterior com esquema divergente, **não apague seus dados automaticamente**. Faça backup primeiro; `docker compose down -v` remove o volume e seus dados.

## Limites e segurança

Este sistema é demonstrativo. Rastreamento significa atualização manual de status, **não GPS em tempo real**. Não há login, controle de acesso ou proteção CSRF; mantenha a porta privada e use somente dados fictícios. Não é apropriado para publicação aberta/produção sem reforço de segurança.

