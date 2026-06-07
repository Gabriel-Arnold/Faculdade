# Drive Distribuido em Flask

Projeto com dois sistemas separados:

- `sistema_principal/`: site Flask com cadastro, login, painel de arquivos, painel admin, usuários e gerenciamento dos nodes.
- `node_storage/`: serviço Flask usado como node de armazenamento. Ele recebe configuração do sistema principal e guarda os arquivos reais.

## Instalação

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Rodando um node

Em um terminal:

```bash
NODE_API_KEY=node-secret NODE_PORT=7001 .venv/bin/python node_storage/node.py
```

Para simular outro node, use outra porta e outro token:

```bash
NODE_API_KEY=backup-secret NODE_PORT=7002 NODE_DATA_DIR=node_storage/data_backup .venv/bin/python node_storage/node.py
```

## Rodando o sistema principal

Em outro terminal:

```bash
.venv/bin/python sistema_principal/app.py
```

Acesse `http://127.0.0.1:5000`.

Usuário admin inicial:

- E-mail: `admin@local`
- Senha: `admin123`

Você pode trocar isso com variáveis de ambiente antes da primeira execução:

```bash
ADMIN_EMAIL=seu@email.com ADMIN_PASSWORD=senha-forte MAIN_SECRET_KEY=uma-chave-secreta .venv/bin/python sistema_principal/app.py
```

## Fluxo de uso

1. Entre como admin.
2. Vá em `Admin`.
3. Cadastre um node principal com URL `http://127.0.0.1:7001`, token `node-secret` e o tamanho em GB.
4. Clique em `Configurar` para o sistema principal enviar a configuração ao node.
5. Opcionalmente cadastre um node backup, apontando para o principal.
6. Usuários podem criar conta, entrar, enviar arquivos, baixar, renomear e excluir.

Ao enviar arquivo, o sistema escolhe um node principal online com espaço suficiente. Se existir backup online para esse node, o arquivo também é replicado para ele. No download, se o principal estiver indisponível, o sistema tenta baixar do backup vinculado.
