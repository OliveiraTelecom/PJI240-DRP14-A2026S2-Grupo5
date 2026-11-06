UNIVESP - Projeto Integrador PJI240 (A2026S2 / Turma 008 - Polo DRP14)

Grupo 5

📌 Nome do Projeto

Sistema de Gerenciamento e Rastreamento Logístico Integrado

👨‍🎓 Integrantes do Grupo

João Vitor da Silva Oliveira — RA: 24207633

📖 Descrição do Projeto

Este projeto apresenta a modelagem e a implementação de um banco de dados relacional para a otimização e o controle de processos logísticos de transporte. A solução, centralizada em PostgreSQL, visa substituir planilhas e controles manuais por um modelo estruturado, seguro e escalável, garantindo a integridade relacional entre motoristas, frotas, clientes e ordens de entrega em tempo real.

📊 Origem e Coleta das Informações

Para garantir a aderência do banco de dados às demandas reais do setor logístico, o levantamento de requisitos e a consolidação das informações basearam-se nas seguintes fontes:

Contextualização e Problema de Pesquisa: Observação das dificuldades operacionais enfrentadas por pequenas e médias empresas de transporte no rastreamento de entregas, alocação de frota e gestão do status de fretes.

Mapeamento de Processos e Entrevistas (Pesquisa Qualitativa): Mapeamento das rotinas logísticas essenciais (fluxo desde a contratação do cliente até a confirmação da entrega), obtido por meio de entrevistas com profissionais da área de logística e transporte de carga.

Normas e Legislações Setoriais: Levantamento dos atributos obrigatórios para cadastro de condutores e frotas, de acordo com as exigências do Contran/Senatran (ex.: Categoria da CNH, EAR - Exercício de Atividade Remunerada, capacidade de carga em kg).

Dados para Testes e Simulação: Os dados utilizados nos scripts DML para povoamento inicial e validação de consultas são dados sintéticos (fictícios) e/ou públicos (como validação de formatos de CEP). Eles foram gerados exclusivamente para fins acadêmicos e demonstrativos, respeitando rigorosamente as diretrizes da LGPD.

🗄️ Estrutura do Banco de Dados Relacional

O esquema conceitual e lógico abrange as seguintes entidades centrais:

motorista: Registra os dados dos condutores, números de CNH, categoria, indicação de EAR e status operacional (disponível/inativo/em viagem).

veiculo: Realiza o controle da frota (modelo, placa, tipo de veículo, capacidade de carga em kg e disponibilidade).

cliente: Mantém o cadastro unificado de contratantes (pessoas físicas e jurídicas).

entrega: Entidade transacional central que relaciona cliente, veículo e motorista, armazenando rotas (origem e destino por CEP), distâncias (km), valores do frete e o histórico de status do transporte.

🛠️ Tecnologias Utilizadas

SGBD: PostgreSQL (v14 ou superior)

Extensões: pgcrypto (para geração de identificadores únicos via UUID)

Linguagem: SQL (DDL para criação das estruturas e DML para manipulação/testes)

🚀 Como Executar o Script SQL

Pré-requisitos

PostgreSQL instalado na máquina local ou em servidor.

Cliente SQL de sua preferência (pgAdmin, DBeaver, psql, etc.).

Passo a Passo

Abra a ferramenta SQL e conecte-se ao seu servidor PostgreSQL.

Crie o banco de dados do projeto executando o comando:

CREATE DATABASE pi_logistica;


Conecte-se ao banco de dados recém-criado (pi_logistica).

Se estiver usando o terminal psql, utilize o comando \c pi_logistica.

Se estiver usando pgAdmin ou DBeaver, selecione o banco de dados na árvore de navegação à esquerda.

Abra os arquivos .sql fornecidos (contendo os scripts DDL, DML e consultas) na sua ferramenta.

Execute os scripts na ordem apropriada para criar as tabelas estruturais, inserir os dados sintéticos e validar as consultas.

---

## Interface web (Flask) e GitHub Codespaces

O projeto agora inclui uma interface web acadêmica para dashboard, cadastro de clientes,
motoristas e veículos, gestão de entregas e relatórios. Os scripts SQL originais foram
preservados, com o arquivo de criação em `sql/01_criacao_e_insercao.sql`.

### Iniciar no Codespaces

1. No repositório do GitHub, clique em **Code → Codespaces → Create codespace on main**.
2. Aguarde a criação do contêiner e a instalação das dependências.
3. No terminal do Codespaces, execute `python app.py`.
4. Abra a porta **5000** na aba **Ports** (ou aceite a abertura automática).
5. Verifique `/health`: deve responder `{"status":"ok","database":"connected"}`.

O Docker Compose inicia o PostgreSQL 16, cria o banco `pi_logistica` e executa o
script SQL **somente na primeira inicialização do volume**. Para reinicializar
com os dados fictícios, use `docker compose down -v` com cuidado: **isso apaga
os dados do banco**. No Codespaces, a porta 5000 deve permanecer **Private**.

### Executar localmente com Docker

```bash
docker compose up -d --build
# Inicie o servidor Flask dentro do contêiner:
docker compose exec web python app.py
```

Abra http://localhost:5000. Para executar os testes:

```bash
python -m pytest -q
```

### Limitações da versão acadêmica

- O rastreamento é por **status da entrega**, não por GPS em tempo real.
- Não há autenticação de usuários nem controle de permissões. **Não publique a
  porta como pública** e não utilize dados reais ou senhas de produção.
- Os dados de demonstração são fictícios. O banco e a aplicação não devem ser
  utilizados em produção sem autenticação, CSRF, validações e segurança adicionais.
- A exclusão de clientes, veículos e motoristas associados a entregas é bloqueada
  pelas chaves estrangeiras, conforme o esquema original.
