CREATE TABLE `cliente` (
	`id` text PRIMARY KEY NOT NULL,
	`nome_razao` text NOT NULL,
	`cpf_cnpj` text NOT NULL,
	`telefone` text,
	`endereco_base` text
);
--> statement-breakpoint
CREATE UNIQUE INDEX `cliente_cpf_cnpj_unique` ON `cliente` (`cpf_cnpj`);--> statement-breakpoint
CREATE TABLE `entrega` (
	`id` text PRIMARY KEY NOT NULL,
	`cliente_id` text NOT NULL,
	`motorista_id` text NOT NULL,
	`veiculo_id` text NOT NULL,
	`cep_origem` text NOT NULL,
	`cep_destino` text NOT NULL,
	`distancia_km` real NOT NULL,
	`valor_frete` real NOT NULL,
	`carga_kg` real NOT NULL,
	`status` text DEFAULT 'pendente' NOT NULL,
	`data_saida` text,
	`data_chegada` text,
	`criado_em` text NOT NULL,
	FOREIGN KEY (`cliente_id`) REFERENCES `cliente`(`id`) ON UPDATE no action ON DELETE restrict,
	FOREIGN KEY (`motorista_id`) REFERENCES `motorista`(`id`) ON UPDATE no action ON DELETE restrict,
	FOREIGN KEY (`veiculo_id`) REFERENCES `veiculo`(`id`) ON UPDATE no action ON DELETE restrict,
	CONSTRAINT "entrega_valores" CHECK("entrega"."distancia_km" >= 0 and "entrega"."valor_frete" >= 0 and "entrega"."carga_kg" >= 0),
	CONSTRAINT "entrega_status" CHECK("entrega"."status" in ('pendente','em_transito','concluida','cancelada'))
);
--> statement-breakpoint
CREATE UNIQUE INDEX `motorista_ativo` ON `entrega` (`motorista_id`) WHERE "entrega"."status" in ('pendente','em_transito');--> statement-breakpoint
CREATE UNIQUE INDEX `veiculo_ativo` ON `entrega` (`veiculo_id`) WHERE "entrega"."status" in ('pendente','em_transito');--> statement-breakpoint
CREATE INDEX `entrega_status_idx` ON `entrega` (`status`);--> statement-breakpoint
CREATE TABLE `motorista` (
	`id` text PRIMARY KEY NOT NULL,
	`nome_completo` text NOT NULL,
	`cnh_numero` text NOT NULL,
	`categoria_cnh` text NOT NULL,
	`possui_ear` integer DEFAULT 0 NOT NULL,
	`status` text DEFAULT 'disponivel' NOT NULL,
	CONSTRAINT "motorista_status" CHECK("motorista"."status" in ('disponivel','ferias','inativo'))
);
--> statement-breakpoint
CREATE UNIQUE INDEX `motorista_cnh_numero_unique` ON `motorista` (`cnh_numero`);--> statement-breakpoint
CREATE TABLE `veiculo` (
	`id` text PRIMARY KEY NOT NULL,
	`placa` text NOT NULL,
	`tipo` text NOT NULL,
	`marca_modelo` text NOT NULL,
	`ano_fabricacao` integer NOT NULL,
	`capacidade_kg` real NOT NULL,
	`status` text DEFAULT 'operacional' NOT NULL,
	CONSTRAINT "veiculo_capacidade" CHECK("veiculo"."capacidade_kg" >= 0),
	CONSTRAINT "veiculo_ano" CHECK("veiculo"."ano_fabricacao" > 1900),
	CONSTRAINT "veiculo_status" CHECK("veiculo"."status" in ('operacional','manutencao','baixado'))
);
--> statement-breakpoint
CREATE UNIQUE INDEX `veiculo_placa_unique` ON `veiculo` (`placa`);