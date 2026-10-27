UNIVESP - Projeto Integrador PJI240 (A2026S2 / Turma 008 - Polo DRP14)

Grupo 5

📌 Nome do Projeto

Sistema de Gerenciamento e Rastreamento Logístico Integrado

👨‍🎓 Integrantes do Grupo

João Vitor da Silva Oliveira — RA: 24207633

📖 Descrição do Projeto

Este projeto apresenta a modelagem e a implementação de um banco de dados relacional para a otimização e o controle de processos logísticos de transporte. A solução centralizada em PostgreSQL visa substituir planilhas e controles manuais por um modelo estruturado, seguro e escalável, garantindo a integridade relacional entre motoristas, frotas, clientes e ordens de entrega em tempo real.

📊 Origem e Coleta das Informações

Para garantir a aderência do banco de dados às demandas reais do setor logístico, o levantamento de requisitos e a consolidação das informações basearam-se nas seguintes fontes:

Contextualização e Problema de Pesquisa:

Observação das dificuldades operacionais enfrentadas por pequenas e médias empresas de transporte no rastreamento de entregas, alocação de frota e gestão do status de fretes.

Mapeamento de Processos e Entrevistas (Pesquisa Qualitativa):

Mapeamento das rotinas logísticas essenciais (fluxo desde a contratação do cliente até a confirmação da entrega), obtido por meio de entrevistas com profissionais da área de logística e transporte de carga.

Normas e Legislações Setoriais:

Levantamento dos atributos obrigatórios para cadastro de condutores e frotas de acordo com as exigências do Contran/Senatran (ex.: Categoria da CNH, EAR - Exercício de Atividade Remunerada, capacidade de carga em kg).

Dados para Testes e Simulação:

Os dados utilizados nos scripts DML para povoamento inicial e validação de consultas são dados sintéticos (fictícios) e/ou públicos (como validação de formatos de CEP), gerados exclusivamente para fins acadêmicos e demonstrativos, respeitando as diretrizes da LGPD.

🗄️ Estrutura do Banco de Dados Relacional

O esquema conceitual e lógico abrange as seguintes entidades centrais:

motorista: Registra dados dos condutores, números de CNH, categoria, indicação de EAR e status operacional (ativo/inativo/em rota).

veiculo: Controle da frota (modelo, placa, tipo de veículo, capacidade de carga em kg e disponibilidade).

cliente: Cadastro unificado de contratantes (pessoas físicas e jurídicas).

entrega: Entidade central que relaciona cliente, veículo e motorista, armazenando rotas (origem/destino por CEP), distância (km), valores do frete e o histórico de status do transporte.

🛠️ Tecnologias Utilizadas

SGBD: PostgreSQL (v14 ou superior)

Extensões: pgcrypto (para geração de identificadores únicos via UUID)

Linguagem: SQL (DDL para criação das estruturas e DML para manipulação/testes)

🚀 Como Executar o Script SQL

Pré-requisitos

PostgreSQL instalado na máquina local ou no servidor.

Cliente SQL de sua preferência (pgAdmin, DBeaver, psql, etc.).

Passo a Passo

Abra a ferramenta SQL e conecte-se ao seu servidor PostgreSQL.

Crie o banco de dados do projeto executando o seguinte comando:

CREATE DATABASE pi_logistica;


Conecte-se ao banco de dados recém-criado (pi_logistica).

Se estiver usando o psql, utilize o comando \c pi_logistica.

Se estiver usando pgAdmin ou DBeaver, selecione o banco de dados na árvore de navegação à esquerda.

Abra o arquivo .sql fornecido (contendo os scripts DDL e DML) na sua ferramenta.

Execute o script completo para criar as tabelas estruturais e inserir os dados sintéticos de teste.
