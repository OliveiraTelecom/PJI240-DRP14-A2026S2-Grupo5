# Logística Integrada — UNIVESP PJI240

Sistema de Gerenciamento e Rastreamento Logístico Integrado.

Grupo 5 · A2026S2N8 · Turma T008 · Polo DRP14.
Integrante: João Vitor da Silva Oliveira — RA 24207633.

## Duas implementações identificadas

| Versão | Código | Banco | Finalidade |
| --- | --- | --- | --- |
| Original acadêmica | `app.py`, `templates/`, `sql/` | PostgreSQL 16 | Modelagem relacional e execução Flask no Docker/Codespaces |
| Adaptação hospedada | `web/` | D1/SQLite | Demonstração persistente pela web, sem depender do Codespace |

A adaptação não converte nem sincroniza o banco original. Os dados são independentes.
Não apresentar a adaptação D1 como se estivesse executando PostgreSQL.

## Execução original no Codespaces

1. Abra um Codespace na `main` atualizada.
2. O Compose inicia PostgreSQL e Flask automaticamente. Não inicie um segundo `python app.py`.
3. A verificação de inicialização confirma `/health` antes da demonstração.
4. Abra a porta privada 5000. Resposta esperada: `{"status":"ok","database":"connected"}`.
5. Se o Codespace entrar em recovery mode com `docker: command not found`, execute **Codespaces: Rebuild Container** pela paleta de comandos. No modo de recuperação, o terminal não está no contêiner de aplicação.

Execução local:

```sh
docker compose up -d --build --wait
python -m pytest -q
```

O SQL inicial roda apenas na primeira criação do volume. Preserve o volume existente para manter os registros. A aplicação Flask deve permanecer em ambiente privado: ainda não possui autenticação de usuários. Formulários usam proteção CSRF, limite de tamanho e validação de CEP e valores de entrega no servidor.

## Versão hospedada e apresentação

O link verificado da implantação e as instruções estão em [`docs/ENTREGA_E_DEMONSTRACAO.md`](docs/ENTREGA_E_DEMONSTRACAO.md).
A rota `/apresentacao` contém slides navegáveis, notas de fala, roteiro sugerido de 7min10s, impressão em PDF e botões que abrem o sistema real.

A adaptação inclui cadastro de clientes, motoristas e veículos, criação de entrega, validação de peso contra capacidade, reserva de recursos, transições de status, persistência e relatórios com CSV. Índices únicos parciais impedem duas entregas ativas para o mesmo motorista ou veículo. Cancelamentos não entram na soma dos fretes.

Para preparar a versão hospedada, consulte [`web/README.md`](web/README.md). O código de hospedagem está incluído neste repositório, sem credenciais nem banco local.

## Escopo e evidências

- Rastreamento por status, sem GPS ou cálculo automático de rota. Distância informada manualmente.
- Dados do cenário demonstrativo são fictícios. Não usar documentos pessoais reais.
- Valores dos relatórios são fretes registrados, sem comprovação de recebimento financeiro.
- A realização de atividade externa com Elisete Aparecida Nobre Oliveira foi informada pelo estudante. Não foram detalhados data, tarefas ou depoimento; não se atribuem aprovação nem impactos quantitativos à participante.
- O vídeo e o relatório devem distinguir a implementação PostgreSQL da adaptação hospedada.
- Testes de integração precisam de `TEST_DATABASE_URL`. Sem essa variável, são explicitamente marcados como ignorados. O workflow GitHub Actions configura PostgreSQL real e testa também o Compose.

## Entrega institucional

O vídeo deve durar de 5 a 10 minutos, mostrar a solução funcionando, identificar o grupo e contextualizar problema, conhecimentos e aplicação externa. Publique no YouTube, confira o acesso da banca, insira o link real na capa do relatório final e poste no AVA. Confira a ficha de prototipagem e a redação oficial do tema norteador no AVA. A avaliação e a aprovação cabem à instituição.
