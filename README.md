# UNIVESP - Projeto Integrador PJI240 (A2026S2 / Turma 008 - Polo DRP14)
**Grupo 5**

## 📌 Nome do Projeto
**Sistema de Gerenciamento e Rastreamento Logístico Integrado**

---

## 👨‍🎓 Integrantes do Grupo
* **João Vitor da Silva Oliveira** — RA: 24207633

---

## 📖 Descrição do Projeto
Este projeto apresenta a modelagem e a implementação de um banco de dados relacional para otimização e controle de processos logísticos de transporte. A solução centralizada em **PostgreSQL** visa garantir a integridade relacional de dados de motoristas, frotas de veículos, clientes e ordens de entrega em tempo real, substituindo controles manuais por um modelo seguro e escalável.

---

## 🗄️ Estrutura do Banco de Dados Relacional
O esquema do banco de dados abrange as seguintes entidades principais:
* **`motorista`**: Controle de motoristas, números de CNH, categoria, EAR e status operacional.
* **`veiculo`**: Cadastro da frota (tipo, modelo, capacidade de carga em kg e status).
* **`cliente`**: Cadastro de empresas e pessoas físicas contratantes.
* **`entrega`**: Relacionamento central de fretes, rotas por CEP, distâncias em km, valores e acompanhamento do status da entrega.

---

## 🛠️ Tecnologias Utilizadas
* **SGBD**: PostgreSQL
* **Extensões**: `pgcrypto` (para geração de identificadores únicos UUID)
* **Linguagem**: SQL (DDL e DML)

---

## 🚀 Como Executar o Script SQL
1. Instale o **PostgreSQL** e abra a ferramenta de sua preferência (pgAdmin, DBeaver ou psql).
2. Crie o banco de dados:
   ```sql
   CREATE DATABASE pi_logistica;
