# Checklist de aceitação — PJI240 / Grupo 5

## Estado verificado em 06/11/2026

- Correções integradas na branch `main`.
- GitHub Actions [42258367762](https://github.com/OliveiraTelecom/PJI240-DRP14-A2026S2-Grupo5/actions/runs/42258367762): **11 testes aprovados**, incluindo PostgreSQL 16 real.
- Validados: carga SQL original; abertura das seis páginas; saúde do banco; criação de cliente, motorista, veículo e entrega; persistência de status e datas; relatórios; duplicidade e bloqueio de exclusões vinculadas.
- Corrigido o tratamento de dados com formato/tamanho inválido, evitando erro 500.
- Configuração do Codespaces preserva o comando de inicialização automática (`overrideCommand: false`).
- A execução acima ocorreu no GitHub Actions; o link privado e a apresentação visual no Codespace real continuam pendentes.

## Validação da aplicação em execução

GitHub Actions [42258581344](https://github.com/OliveiraTelecom/PJI240-DRP14-A2026S2-Grupo5/actions/runs/42258581344) — **aprovado**, código `32a78bffebb4e22cbf5b9f8595021e8f53080959`.

- [x] 11 testes aprovados com PostgreSQL 16 real
- [x] Build e inicialização do Docker Compose
- [x] Contêineres web e db saudáveis
- [x] /health confirma banco conectado por HTTP
- [x] Dashboard, clientes, motoristas, veículos, entregas e relatórios respondem HTTP 200
- [ ] Abertura do link privado da porta 5000 no Codespace do usuário
- [ ] Inspeção visual e apresentação manual no navegador

Os testes de integração usam esquemas temporários e verificam as operações pelo cliente de testes Flask com banco real; a verificação HTTP adicional abre as seis páginas no servidor iniciado pelo Compose. Não houve acesso ao banco ou ao volume do Codespace do usuário. Este resultado permite seguir para a demonstração privada, mas não certifica hospedagem pública ou disponibilidade permanente.

## Inicializar no Codespaces

1. Crie o Codespace na `main`. Se ele já existe, execute `git pull` e selecione **Codespaces: Rebuild Container** na paleta de comandos.
2. Aguarde PostgreSQL e servidor web iniciarem automaticamente; não abra uma segunda instância com `python app.py`.
3. Na aba **Ports**, abra a porta `5000` e mantenha-a **Private**.
4. Dentro do terminal do contêiner web, execute:

```sh
python -m pytest -q
TEST_DATABASE_URL="$DATABASE_URL" python -m pytest tests/test_integration.py -q
python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/health', timeout=5).read().decode())"
```

O segundo comando usa esquemas temporários `aceitacao_`, criados e removidos pelo teste. Não apaga cadastros existentes. O usuário PostgreSQL precisa de permissão para criar esquemas, como ocorre no Compose do projeto.

Resposta esperada em `/health`: `{"status":"ok","database":"connected"}`.

Para diagnóstico do Compose, execute `docker compose ps` e `docker compose logs --tail=100 web db` em um terminal com acesso ao Docker. O contêiner web não inclui Docker CLI.

## Roteiro prático da apresentação

- [ ] Dashboard abre e apresenta contadores e situação das entregas
- [ ] Cadastrar cliente fictício e conferir o novo registro
- [ ] Cadastrar motorista fictício e conferir o novo registro
- [ ] Cadastrar veículo fictício e conferir o novo registro
- [ ] Criar entrega vinculando os cadastros e observar o status **pendente**
- [ ] Atualizar o status para **em_transito** e verificar a mudança após recarregar
- [ ] Atualizar para **concluida** e verificar a mudança após recarregar
- [ ] Abrir relatórios e conferir atualização dos totais e faturamento
- [ ] Tentar cadastrar dados duplicados e comprovar mensagem de validação
- [ ] Tentar excluir registro vinculado a entrega e comprovar bloqueio
- [ ] Confirmar `/health` saudável depois das operações
- [ ] Reabrir o link da porta privada em uma sessão com acesso autorizado
- [ ] Exibir o repositório, documentação e resultado do GitHub Actions

## Critérios de aceite

Aceitar somente após todos os itens acima funcionarem no **Codespaces real**. Testes unitários aprovados isoladamente não bastam. Para entrega aberta ao público são necessários autenticação, controle de acesso, CSRF, credenciais seguras e uma hospedagem apropriada; **Codespaces privado é uma opção de demonstração, não um deploy público permanente**.

## Notas de compatibilidade

- Use a branch `main`, que já contém `.devcontainer/devcontainer.json`.
- A documentação antiga do `README.md` sugere `python app.py` ou `docker compose exec web python app.py`; com a nova configuração o serviço `web` **já inicializa automaticamente**, portanto não é necessário executar uma segunda instância.
- Havendo falha de conexão ou problema no esquema, registre logs e faça backup do volume antes de qualquer reconstrução destrutiva.

