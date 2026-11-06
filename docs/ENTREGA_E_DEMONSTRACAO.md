# Demonstração e entrega — PJI240 Grupo 5

## Links publicados

- Solução: https://pji240-logistica-grupo5.knowingmedal1.chatgpt.site
- Slides: https://pji240-logistica-grupo5.knowingmedal1.chatgpt.site/apresentacao
- Acesso: privado, com autenticação da plataforma.

## Identificação

UNIVESP, PJI240, A2026S2N8, Grupo 5, Turma T008, Polo DRP14.
João Vitor da Silva Oliveira, RA 24207633.

## Relato externo

O estudante informou a realização da atividade com Elisete Aparecida Nobre Oliveira. Não foram informados data, tarefas específicas, depoimento ou indicadores de impacto. Complemente o relato apenas com informações verdadeiras. A presença do nome não substitui a explicação de como a solução foi aplicada e quais resultados foram observados.

## Sequência de demonstração

1. Abra o painel e mostre a conexão com o banco.
2. Carregue dados fictícios ou cadastre cliente, motorista e veículo próprios de demonstração.
3. Tente criar entrega com peso acima da capacidade. Confira a rejeição.
4. Corrija o peso, salve e confira o protocolo pendente.
5. Mostre os recursos reservados. Uma segunda entrega ativa para o mesmo recurso é bloqueada.
6. Inicie o transporte, conclua e confira a liberação dos recursos.
7. Recarregue a página e confira a persistência.
8. Abra Relatórios. Confira as somas e exporte CSV.

## Matriz dos critérios

| Critério | Conteúdo preparado | Verificação final |
| --- | --- | --- |
| Identificação | Capa e slides com grupo, título, integrante, RA, turma e polo | Conferir dados no AVA |
| Problema e tema | Problema de centralização logística, relevância externa e tema do plano | Conferir formulação oficial do tema norteador |
| Solução funcionando | Operações persistentes e demonstração real | Gravar a sequência de interação |
| Aplicação externa | Participante informada pelo estudante | Complementar contexto, tarefas e retorno reais |
| Recursos | Slides integrados e capturas reais do sistema | Combinar explicação com interação na gravação |
| Tempo | Roteiro sugerido de 7min10s | Vídeo final deve ter de 5 a 10 minutos |
| Entrega | Links de solução e apresentação | YouTube, capa do relatório, AVA e ficha de prototipagem |

O link da aplicação não substitui o link do vídeo no YouTube. Verifique que a banca consegue acessar os materiais. A hospedagem começa com acesso privado. Convite a avaliadores ou mudança de audiência precisa de definição própria.

## Verificações desta revisão

- Fluxo web observado no navegador: recusa de carga excessiva, criação, início, conclusão, liberação de recursos, persistência após recarga e relatório.
- Cenário fictício: duas entregas de R$ 250 e R$ 350; total de fretes R$ 600.
- Testes de integridade SQLite: alocação duplicada, valores negativos, referência inválida e reutilização de recursos após conclusão.
- Testes Flask locais: 10 passaram e 4 de integração foram ignorados por ausência de TEST_DATABASE_URL. A execução PostgreSQL real deve ser confirmada pelo workflow desta revisão.
- Não houve postagem no AVA, aprovação pela instituição ou publicação no YouTube nesta etapa.
