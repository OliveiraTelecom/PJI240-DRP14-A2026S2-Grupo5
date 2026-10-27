1. Relatório Geral de Entregas (Visão Operacional)
SQL
-- Lista todas as entregas detalhando quem é o cliente, o motorista e o veículo utilizado
SELECT 
    e.id AS protocolo_entrega,
    c.nome_razao AS cliente,
    m.nome_completo AS motorista,
    v.placa AS placa_veiculo,
    e.cep_origem,
    e.cep_destino,
    e.valor_frete,
    e.status AS status_entrega
FROM 
    entrega e
INNER JOIN cliente c ON e.cliente_id = c.id
INNER JOIN motorista m ON e.motorista_id = m.id
INNER JOIN veiculo v ON e.veiculo_id = v.id
ORDER BY 
    e.data_saida DESC;
Explicação: Esta consulta usa INNER JOIN para unificar as quatro tabelas do sistema. É o relatório mais comum no dia a dia da transportadora para visualizar o panorama completo das operações.

2. Monitoramento de Frota em Trânsito
SQL
-- Busca quais veículos e motoristas estão com entregas em andamento neste momento
SELECT 
    m.nome_completo AS motorista,
    m.cnh_numero,
    v.marca_modelo AS veiculo,
    v.placa,
    e.data_saida,
    c.nome_razao AS cliente_destino
FROM 
    entrega e
INNER JOIN motorista m ON e.motorista_id = m.id
INNER JOIN veiculo v ON e.veiculo_id = v.id
INNER JOIN cliente c ON e.cliente_id = c.id
WHERE 
    e.status = 'em_transito';
Explicação: Uma consulta de monitoramento em tempo real. Essencial para a equipe de logística saber exatamente quais recursos da empresa estão ocupados rodando na rua.

3. Faturamento Total por Cliente (Análise Financeira)
SQL
-- Calcula o valor total de fretes gerados por cada cliente
SELECT 
    c.nome_razao AS cliente,
    c.cpf_cnpj,
    COUNT(e.id) AS total_entregas,
    SUM(e.valor_frete) AS faturamento_total
FROM 
    cliente c
LEFT JOIN entrega e ON c.id = e.cliente_id
GROUP BY 
    c.nome_razao, 
    c.cpf_cnpj
ORDER BY 
    faturamento_total DESC;
Explicação: Demonstra o uso de funções de agregação (COUNT e SUM) com GROUP BY. Isso comprova para o professor que o banco está preparado para gerar painéis gerenciais (dashboards) financeiros e identificar os clientes mais rentáveis.

4. Resumo de Entregas por Status
SQL
-- Conta a quantidade de entregas agrupadas pela situação atual
SELECT 
    status AS situacao_entrega,
    COUNT(*) AS quantidade_entregas,
    SUM(distancia_km) AS km_total_percorrida
FROM 
    entrega
GROUP BY 
    status
ORDER BY 
    quantidade_entregas DESC;
