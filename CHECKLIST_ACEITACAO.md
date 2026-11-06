# Checklist de aceitação — PJI240 / Grupo 5

## Estado verificado em 06/11/2026

- Código Flask + PostgreSQL + Docker Compose disponível na branch `fix/apresentacao-codespaces-2026`.
- GitHub Actions (execução 42239165554): testes de Python **aprovados** na branch de correções.
- Os testes existentes usam mocks e **não confirmam** PostgreSQL real, criação de entrega ou persistência de status.
- É necessário fazer o merge das correções em `main` antes de criar um Codespace a partir da branch principal.
- **Não divulgar o Codespaces publicamente**: não há autenticação de usuários nem proteção CSRF.
- Rastreamento significa acompanhamento manual do status, não localização GPS.
- Carga SQL executa somente na primeira criação do volume Docker; não apagar volumes com dados sem backup.

## Inicializar versão corrigida no Codespaces

1. Abra o pull request de correções e selecione a branch revisada.
2. Crie um Codespace com a branch revisada. O Compose inicia `web` e `db`.
3. Na aba **Ports**, mantenha a porta `5000` como **Private**.
4. No terminal integrado, execute:

```sh
docker compose ps
docker compose logs --tail=100 web
docker compose logs --tail=100 db
python -m pytest -q
curl -fsS http://localhost:5000/health
```

5. Espere `{"status":"ok","database":"connected"}` em `/health`. O serviço web e o banco devem estar saudáveis.

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

- Uso de `Docker Compose` no Codespaces requer que o projeto seja criado a partir da branch que contém `.devcontainer/devcontainer.json`.
- A documentação antiga do `README.md` sugere `python app.py` ou `docker compose exec web python app.py`; com a nova configuração o serviço `web` **já inicializa automaticamente**, portanto não é necessário executar uma segunda instância.
- Havendo falha de conexão ou problema no esquema, registre logs e faça backup do volume antes de qualquer reconstrução destrutiva.
