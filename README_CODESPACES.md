# Iniciar a demonstração no GitHub Codespaces

## Procedimento recomendado

1. Abra o repositório no GitHub, selecione **Code > Codespaces > Create codespace** e escolha a branch de correção.
2. Aguarde a inicialização do contêiner **web** com o serviço PostgreSQL **db**.
3. Na aba **Ports**, abra a porta **5000**, configurada como **Private**.
4. Acesse a página principal e depois **/health**. A resposta esperada é `{"status":"ok","database":"connected"}`.
5. Demonstre: dashboard, cadastro de cliente/motorista/veículo, registro e atualização de entrega e relatórios.

## Diagnóstico

Execute no terminal:
```bash
docker compose ps
docker compose logs --tail=100 web
docker compose logs --tail=100 db
python -m pytest -q
```

A inicialização SQL acontece somente na criação inicial do volume de PostgreSQL. Caso já exista um volume de uma execução anterior com esquema divergente, **não apague seus dados automaticamente**. Faça backup primeiro; `docker compose down -v` remove o volume e seus dados.

## Limites e segurança

Este sistema é demonstrativo. Rastreamento significa atualização manual de status, **não GPS em tempo real**. Não há login, controle de acesso ou proteção CSRF; mantenha a porta privada e use somente dados fictícios. Não é apropriado para publicação aberta/produção sem reforço de segurança.
