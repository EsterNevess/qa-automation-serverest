# QA Automation – ServeRest

![Testes automatizados](https://github.com/EsterNevess/qa-automation-serverest/actions/workflows/testes.yml/badge.svg)

Projeto de automação de testes da API REST e da loja web do **[ServeRest](https://serverest.dev)**, um sistema de e-commerce feito para estudo e prática de testes.

O projeto cobre **cadastro de usuários, login, produtos e lista de compras**, com testes positivos e negativos, validação de contrato e execução automática a cada alteração do código.

## O que é testado

| Camada | Quantidade | Ferramentas |
|---|---|---|
| API REST | 27 testes | pytest + requests + jsonschema |
| Web (E2E) | 8 testes | Playwright + Page Object Model |

**Destaques:**
- Testes **negativos** e de **permissão** (sem token, usuário sem perfil de administrador, campos vazios, dados duplicados)
- **Valores-limite** (preço zero e negativo)
- **Validação de contrato** das respostas com JSON Schema
- Dados de teste gerados com **Faker** e limpeza automática ao final de cada teste, usando **fixtures**
- Testes web organizados com **Page Object Model**
- Print automático da tela quando um teste web falha
- **Integração contínua** com GitHub Actions e relatório HTML

Os cenários estão descritos em [`docs/casos_de_teste.md`](docs/casos_de_teste.md) e a estratégia em [`docs/plano_de_testes.md`](docs/plano_de_testes.md).

## Estrutura do projeto

```
qa-automation-serverest/
├── .github/
│   ├── workflows/testes.yml      # integração contínua (GitHub Actions)
│   └── ISSUE_TEMPLATE/           # modelo de bug report
├── docs/                         # plano de testes e casos de teste
├── schemas/                      # contratos JSON das respostas da API
├── tests/
│   ├── api/                      # testes de API (usuários, login, produtos)
│   └── web/
│       ├── pages/                # Page Objects (uma classe por tela)
│       └── test_*.py             # testes web
├── utils/                        # cliente da API, geração de dados, configurações
├── pytest.ini                    # configurações do pytest
└── requirements.txt              # bibliotecas do projeto
```

## Como rodar

Pré-requisitos: **Python 3.10 ou superior** e **Git**.

```bash
# 1. Baixar o projeto
git clone https://github.com/EsterNevess/qa-automation-serverest.git
cd qa-automation-serverest

# 2. Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac

# 3. Instalar as dependências e o navegador
pip install -r requirements.txt
playwright install chromium

# 4. Rodar os testes
pytest                 # todos
pytest -m api          # só API
pytest -m web          # só web
pytest -m smoke        # só os essenciais
pytest -m web --headed # web com o navegador aparecendo na tela
```

### Relatório HTML

```bash
pytest --html=reports/relatorio.html --self-contained-html
```

O relatório fica em `reports/relatorio.html` e pode ser aberto no navegador.

### Usando outro endereço

Por padrão os testes usam o ServeRest público. Para usar outro endereço (por exemplo, o ServeRest rodando localmente com `npx serverest`), defina as variáveis `API_URL` e `WEB_URL`:

```bash
set API_URL=http://localhost:3000      # Windows
# export API_URL=http://localhost:3000 # Linux/Mac
pytest -m api
```

## Integração contínua

A cada push na branch `main`, o GitHub Actions:
1. Sobe uma instância local do ServeRest e roda os **testes de API** contra ela, o que deixa a execução estável e independente do servidor público.
2. Roda os **testes web** contra a loja pública no navegador Chromium.
3. Guarda os relatórios HTML e os prints de falha como artefatos da execução.

## Autora

**Ester Neves** – QA Júnior
[LinkedIn](https://linkedin.com/in/esterneves) · [GitHub](https://github.com/EsterNevess)
