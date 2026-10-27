1. Preparação do Banco de Dados
SQL
-- Habilita a extensão para geração automática de UUIDs
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
Explicação: Este comando garante que o PostgreSQL consiga gerar identificadores únicos universais (UUIDs) nativamente. O uso de UUID previne conflitos de ID em sistemas distribuídos e aumenta a segurança por não expor a contagem de registros (como faz um ID sequencial).

2. Cadastro de Motoristas
SQL
CREATE TABLE motorista (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_completo VARCHAR(150) NOT NULL,
    cnh_numero VARCHAR(20) UNIQUE NOT NULL,
    categoria_cnh VARCHAR(5) NOT NULL,
    possui_ear BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('disponivel', 'em_viagem', 'ferias', 'inativo'))
);
Explicação: Cria a entidade que opera as entregas. A regra UNIQUE na CNH impede motoristas duplicados, e a cláusula CHECK blinda a coluna de status, aceitando apenas estados predefinidos.

3. Cadastro de Veículos (Frota)
SQL
CREATE TABLE veiculo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    placa VARCHAR(10) UNIQUE NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    marca_modelo VARCHAR(100) NOT NULL,
    ano_fabricacao INT NOT NULL CHECK (ano_fabricacao > 1900),
    capacidade_kg DECIMAL(10,2) NOT NULL CHECK (capacidade_kg >= 0),
    status VARCHAR(20) NOT NULL CHECK (status IN ('operacional', 'manutencao', 'baixado'))
);
Explicação: Controla os recursos físicos. As constraints CHECK garantem a integridade dos dados (não permitindo anos de fabricação impossíveis ou capacidades de carga negativas).

4. Cadastro de Clientes
SQL
CREATE TABLE cliente (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_razao VARCHAR(150) NOT NULL,
    cpf_cnpj VARCHAR(20) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    endereco_base VARCHAR(255)
);
Explicação: Armazena as empresas ou pessoas que solicitam o frete. O documento (CPF/CNPJ) é marcado como único para evitar duplicação de cadastros no sistema de faturamento.

5. Tabela Transacional: Entregas (Relacionamentos)
SQL
CREATE TABLE entrega (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    motorista_id UUID NOT NULL,
    veiculo_id UUID NOT NULL,
    cliente_id UUID NOT NULL,
    cep_origem VARCHAR(10) NOT NULL,
    cep_destino VARCHAR(10) NOT NULL,
    distancia_km DECIMAL(8,2) CHECK (distancia_km >= 0),
    valor_frete DECIMAL(10,2) NOT NULL CHECK (valor_frete >= 0),
    data_saida TIMESTAMP,
    data_chegada TIMESTAMP,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pendente', 'em_transito', 'concluida', 'cancelada')),
    
    -- Definição das Chaves Estrangeiras
    CONSTRAINT fk_motorista FOREIGN KEY (motorista_id) REFERENCES motorista(id) ON DELETE RESTRICT,
    CONSTRAINT fk_veiculo FOREIGN KEY (veiculo_id) REFERENCES veiculo(id) ON DELETE RESTRICT,
    CONSTRAINT fk_cliente FOREIGN KEY (cliente_id) REFERENCES cliente(id) ON DELETE RESTRICT
);
Explicação: É o coração operacional do sistema. Une quem dirige, o que dirige e para quem é a entrega. A regra ON DELETE RESTRICT nas chaves estrangeiras é um mecanismo de segurança vital: impede que um motorista, veículo ou cliente seja apagado do banco de dados se houver alguma entrega vinculada a ele.

6. Otimização (Índices)
SQL
CREATE INDEX idx_entrega_status ON entrega(status);
CREATE INDEX idx_entrega_data_saida ON entrega(data_saida);
CREATE INDEX idx_veiculo_status ON veiculo(status);
Explicação: Cria "guias de busca rápida" no banco. Como relatórios frequentemente filtram entregas pela data ou status (ex: "buscar todas as entregas em trânsito hoje"), os índices impedem que o banco precise ler a tabela inteira, linha por linha.

7. População de Dados (Carga Inicial)
SQL
-- Inserindo um motorista
INSERT INTO motorista (id, nome_completo, cnh_numero, categoria_cnh, possui_ear, status)
VALUES (
    'a1b2c3d4-e5f6-7890-1234-56789abcdef0', 
    'João Vitor da Silva Oliveira', 
    '12345678900', 
    'AD/AE', 
    TRUE, 
    'disponivel'
);

-- Inserindo veículos
INSERT INTO veiculo (id, placa, tipo, marca_modelo, ano_fabricacao, capacidade_kg, status)
VALUES 
    ('b2c3d4e5-f6a7-8901-2345-6789abcdef01', 'ABC1D23', 'Utilitário', 'Toyota Hilux SW4', 2011, 700.00, 'operacional'),
    ('c3d4e5f6-a7b8-9012-3456-789abcdef012', 'XYZ9W87', 'Moto', 'Bajaj Dominar D400', 2024, 150.00, 'operacional');

-- Inserindo clientes
INSERT INTO cliente (id, nome_razao, cpf_cnpj, telefone, endereco_base)
VALUES 
    ('d4e5f6a7-b8c9-0123-4567-89abcdef0123', '3Corp Technology', '00.000.000/0001-00', '(11) 9999-9999', 'São Paulo - SP'),
    ('e5f6a7b8-c9d0-1234-5678-9abcdef01234', 'Motiva AutoBan', '11.111.111/0001-11', '(11) 8888-8888', 'Campinas - SP');

-- Registrando uma entrega em trânsito
INSERT INTO entrega (motorista_id, veiculo_id, cliente_id, cep_origem, cep_destino, distancia_km, valor_frete, data_saida, status)
VALUES (
    'a1b2c3d4-e5f6-7890-1234-56789abcdef0', 
    'b2c3d4e5-f6a7-8901-2345-6789abcdef01', 
    'e5f6a7b8-c9d0-1234-5678-9abcdef01234', 
    '01001-000', 
    '18570-000', 
    210.5, 
    850.00, 
    CURRENT_TIMESTAMP, 
    'em_transito'
);
