# Adaptação web hospedada

Interface React/Vinext, API server-side e banco relacional D1/SQLite. Esta versão é independente do Flask/PostgreSQL original.

## Desenvolvimento

Node 22.13 ou superior e pnpm (versão de `packageManager`).

```sh
pnpm install --frozen-lockfile
pnpm db:generate  # somente após alterar o esquema; não regenerar migrations já aplicadas
pnpm build
node --import ./scripts/sites-env.mjs ./node_modules/wrangler/bin/wrangler.js d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0000_same_lord_tyger.sql
pnpm dev
```

Aplique cada migration uma única vez no banco local. O manifesto declara o binding lógico `DB`; a plataforma de hospedagem provisiona e conecta o banco real durante a publicação. Identidade da hospedagem e credenciais não estão neste template.

## Regras

- Documentos, CNH e placa únicos.
- Chaves estrangeiras e valores não negativos.
- Entrega requer CEPs de oito dígitos e capacidade suficiente.
- Motorista e veículo não podem participar de duas entregas pendentes/em trânsito simultâneas.
- Fluxo: pendente para em trânsito ou cancelada; em trânsito para concluída ou cancelada. Registros finalizados não reabrem.
- Transições usam atualização condicional para detectar concorrência.
- POST aceita JSON e exige Origin da própria aplicação. A implantação é privada, protegida pela plataforma. Não tornar os endpoints públicos sem autorização adicional.
- Dados fictícios são inseridos por ação explícita e idempotente. Não são criados durante migrations ou leitura.

## Apresentação

`/apresentacao` inclui identificação, problema, método, arquitetura, explicação das regras, demonstração ao vivo, aplicação externa, resultados, limites e fontes. As notas orientam um vídeo de 7min10s, mas a duração da gravação deve ser conferida.
