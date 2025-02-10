# Kanastra: Processador de boletos

O projeto foi criado utilizando arquitetura hexagonal (ports and adapters), FastAPI como framework web e uv como gerenciador de dependências.

## Explicando um pouco da arquitetura do projeto
Dentro da pasta domain temos o core da aplicação desacoplado da implementação. Temos os modelos das entidades do sistema, que no caso eu chamei de Invoice (boleto/pagamento) a entidade principal e as Ports que são abstrações das classes que serão implementadas.

Já na pasta adapters vamos encotrar as implementações das classes do sistema, onde repositories são implementações das entidades do sistema mas relacionadas ao acesso a dados. E entrypoints são as implementações do acesso externo do nosso sistema, nesse caso a API.

## Instalação


### Ambiente local sem docker

1. Primeiro, instale o uv globalmente usando pip:
```bash
pip install uv
```

2. Crie um ambiente virtual e ative ele:
```bash
uv venv && source .venv/bin/activate
```

3. Configure as variáveis de ambiente (pode ser em um arquivo .env):
```
HOST=
PORT=
DB_HOST=
DB_PASS=
DB_USER=
DB_PORT=
DB_BASE=billing_system
```

4. Rode as migrations:
```bas
alembic run upgrade
```

5. Rode a aplicação:
```bash
uvicorn app.main:app --reload
```
