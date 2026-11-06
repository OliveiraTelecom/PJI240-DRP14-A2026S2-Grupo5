import { env } from 'cloudflare:workers';
export const dynamic='force-dynamic';
const tables:Record<string,string[]>={cliente:['nome_razao','cpf_cnpj','telefone','endereco_base'],motorista:['nome_completo','cnh_numero','categoria_cnh','possui_ear','status'],veiculo:['placa','tipo','marca_modelo','ano_fabricacao','capacidade_kg','status']};
const ok=(x:unknown,status=200)=>Response.json(x,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
function db(){if(!env.DB)throw new Error('Banco indisponível');return env.DB;}
export async function GET(){try{const d=db();const r=await d.batch([d.prepare('SELECT * FROM cliente ORDER BY nome_razao'),d.prepare("SELECT m.*, EXISTS(SELECT 1 FROM entrega e WHERE e.motorista_id=m.id AND e.status IN ('pendente','em_transito')) AS ocupado FROM motorista m ORDER BY nome_completo"),d.prepare("SELECT v.*, EXISTS(SELECT 1 FROM entrega e WHERE e.veiculo_id=v.id AND e.status IN ('pendente','em_transito')) AS ocupado FROM veiculo v ORDER BY placa"),d.prepare('SELECT e.*,c.nome_razao AS cliente,m.nome_completo AS motorista,v.placa FROM entrega e JOIN cliente c ON c.id=e.cliente_id JOIN motorista m ON m.id=e.motorista_id JOIN veiculo v ON v.id=e.veiculo_id ORDER BY e.criado_em DESC,e.id'),d.prepare('SELECT c.nome_razao,COUNT(e.id) AS total,COALESCE(SUM(CASE WHEN e.status != \'cancelada\' THEN e.valor_frete ELSE 0 END),0) AS fretes FROM cliente c LEFT JOIN entrega e ON e.cliente_id=c.id GROUP BY c.id ORDER BY fretes DESC')]);return ok({clientes:r[0].results,motoristas:r[1].results,veiculos:r[2].results,entregas:r[3].results,relatorios:r[4].results,database:'connected'});}catch{return ok({error:'Não foi possível consultar o banco. Tente novamente.'},503);}}
function str(v:unknown,max=150){if(typeof v!=='string'||!v.trim()||v.trim().length>max)throw new Error('Preencha os campos obrigatórios com valores válidos.');return v.trim();}
function number(v:unknown,max=1e9){if(v===''||v==null||typeof v==='boolean')throw new Error('Informe valores numéricos.');const n=Number(v);if(!Number.isFinite(n)||n<0||n>max)throw new Error('Informe valores numéricos não negativos dentro do limite.');return n;}
function one(v:unknown,values:string[]){if(!values.includes(String(v)))throw new Error('Situação inválida.');return v;}
const cep=(v:unknown)=>{const s=str(v,9).replace(/\D/g,'');if(s.length!==8)throw new Error('Informe CEP com oito dígitos.');return s.slice(0,5)+'-'+s.slice(5);};
export async function POST(req:Request){
 if(req.headers.get('Origin')!==new URL(req.url).origin)return ok({error:'Origem da solicitação inválida.'},403);
 if(!req.headers.get('Content-Type')?.startsWith('application/json'))return ok({error:'Formato inválido.'},415);
 try{if(Number(req.headers.get('Content-Length')||0)>20000)return ok({error:'Solicitação muito grande.'},413);const text=await req.text();if(text.length>20000)return ok({error:'Solicitação muito grande.'},413);const b=JSON.parse(text),d=db();
 if(b.action==='seed'){
  await d.batch([
   d.prepare("INSERT OR IGNORE INTO cliente(id,nome_razao,cpf_cnpj,endereco_base) VALUES('demo-cliente','Cliente Demonstração','DEMO-CLIENTE','São Paulo - SP')"),
   d.prepare("INSERT OR IGNORE INTO motorista(id,nome_completo,cnh_numero,categoria_cnh,possui_ear,status) VALUES('demo-motorista','Motorista Demonstração','DEMO-CNH','D',1,'disponivel')"),
   d.prepare("INSERT OR IGNORE INTO veiculo(id,placa,tipo,marca_modelo,ano_fabricacao,capacidade_kg,status) VALUES('demo-veiculo','DEMO001','Van','Veículo Demonstração',2024,1000,'operacional')")]);return ok({message:'Dados fictícios de demonstração disponíveis.'});
 }
 if(b.action==='create'&&tables[b.table]){const f=b.data||{},cols=tables[b.table];let vals:unknown[];
 if(b.table==='cliente')vals=[str(f.nome_razao),str(f.cpf_cnpj,30),String(f.telefone||'').slice(0,30),String(f.endereco_base||'').slice(0,255)];
 else if(b.table==='motorista')vals=[str(f.nome_completo),str(f.cnh_numero,30),str(f.categoria_cnh,5),f.possui_ear?1:0,one(f.status,['disponivel','ferias','inativo'])];
 else{const ano=number(f.ano_fabricacao,new Date().getFullYear()+1);if(!Number.isInteger(ano)||ano<=1900)throw new Error('Ano de fabricação inválido.');const placa=str(f.placa,10).toUpperCase();if(!/^[A-Z0-9-]{6,10}$/.test(placa))throw new Error('Placa inválida.');vals=[placa,str(f.tipo,50),str(f.marca_modelo,100),ano,number(f.capacidade_kg,1000000),one(f.status,['operacional','manutencao','baixado'])];}
 await d.prepare(`INSERT INTO ${b.table}(id,${cols.join(',')}) VALUES(${cols.map(()=>'?').join(',')},?)`).bind(crypto.randomUUID(),...vals).run();return ok({message:'Cadastro salvo no banco.'},201);
 }
 if(b.action==='delivery'){
  const f=b.data||{};const ids=[str(f.cliente_id,50),str(f.motorista_id,50),str(f.veiculo_id,50)];const carga=number(f.carga_kg,1000000);
  const v=await d.prepare('SELECT capacidade_kg,status FROM veiculo WHERE id=?').bind(ids[2]).first<{capacidade_kg:number,status:string}>();const m=await d.prepare('SELECT status FROM motorista WHERE id=?').bind(ids[1]).first<{status:string}>();
  if(!v||v.status!=='operacional'||!m||m.status!=='disponivel')throw new Error('Selecione motorista disponível e veículo operacional.');if(carga>v.capacidade_kg)throw new Error('A carga excede a capacidade do veículo.');
  await d.prepare("INSERT INTO entrega(id,cliente_id,motorista_id,veiculo_id,cep_origem,cep_destino,distancia_km,valor_frete,carga_kg,status,criado_em) VALUES(?,?,?,?,?,?,?,?,?,'pendente',?)").bind(crypto.randomUUID(),...ids,cep(f.cep_origem),cep(f.cep_destino),number(f.distancia_km,100000),number(f.valor_frete,1e8),carga,new Date().toISOString()).run();return ok({message:'Entrega criada e recursos reservados.'},201);
 }
 if(b.action==='status'){
  const id=str(b.id,50);const current=await d.prepare('SELECT status FROM entrega WHERE id=?').bind(id).first<{status:string}>();if(!current)return ok({error:'Entrega não encontrada.'},404);
  const allowed:Record<string,string[]>={pendente:['em_transito','cancelada'],em_transito:['concluida','cancelada'],concluida:[],cancelada:[]};if(!allowed[current.status]?.includes(b.status))throw new Error('Transição de status inválida. Entregas finalizadas não podem ser reabertas.');
  const now=new Date().toISOString();const r=await d.prepare("UPDATE entrega SET status=?,data_saida=CASE WHEN ?='em_transito' THEN COALESCE(data_saida,?) ELSE data_saida END,data_chegada=CASE WHEN ?='concluida' THEN ? ELSE data_chegada END WHERE id=? AND status=?").bind(b.status,b.status,now,b.status,now,id,current.status).run();if(!r.meta.changes)throw new Error('Entrega alterada por outra operação. Atualize a página.');return ok({message:'Situação atualizada e persistida.'});
 }
 return ok({error:'Operação inválida.'},400);
 }catch(e){const msg=String(e);if(/UNIQUE|FOREIGN KEY|constraint/i.test(msg))return ok({error:'Registro duplicado ou recurso já reservado por outra entrega.'},409);return ok({error:e instanceof SyntaxError?'Dados inválidos.':e instanceof Error?e.message:'Não foi possível salvar.'},400);}
}
