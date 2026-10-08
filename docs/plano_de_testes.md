# Plano de Testes – ServeRest

## 1. Objetivo
Verificar as principais funcionalidades do ServeRest (API REST e loja web), com foco em cadastro de usuários, autenticação, gestão de produtos e lista de compras, por meio de testes automatizados.

## 2. Sistema sob teste
- **API:** https://serverest.dev (documentação Swagger no próprio endereço)
- **Web:** https://front.serverest.dev

## 3. Escopo

### Dentro do escopo
| Módulo | API | Web |
|---|---|---|
| Usuários (cadastro, consulta, edição, exclusão) | Sim | Cadastro |
| Login e token de acesso | Sim | Sim |
| Produtos (CRUD e permissões) | Sim | Pesquisa |
| Lista de compras do cliente | – | Sim |

### Fora do escopo
- Carrinhos e finalização de compra pela API
- Upload de imagem de produto
- Testes de desempenho, carga e segurança
- Compatibilidade com navegadores além do Chromium

## 4. Estratégia
- **Testes de API (maior quantidade):** rápidos e estáveis; cobrem regras de negócio, cenários positivos e negativos, códigos de status, mensagens e contrato (JSON Schema).
- **Testes Web E2E (menor quantidade):** cobrem os fluxos mais importantes do usuário na tela.
- Segue a ideia da **pirâmide de testes**: muitos testes rápidos na base (API) e poucos testes de tela no topo.
- Cada teste cria os próprios dados (Faker + e-mails únicos) e apaga ao final, para não depender de outros testes.

## 5. Técnicas utilizadas
- Particionamento de equivalência (dados válidos e inválidos)
- Análise de valor-limite (preço zero e negativo)
- Testes negativos (sem token, sem permissão, campos vazios)
- Validação de contrato com JSON Schema

## 6. Ferramentas
Python, pytest, requests, Faker, jsonschema, Playwright, pytest-html e GitHub Actions.

## 7. Critérios de aceite
- 100% dos testes passando na integração contínua
- Defeitos encontrados registrados no GitHub Issues, seguindo o modelo de bug report

## 8. Riscos
- O ServeRest público é compartilhado e pode ficar instável ou ter dados alterados por outras pessoas. Para reduzir esse risco, os testes de API na integração contínua rodam em uma instância local do ServeRest.
