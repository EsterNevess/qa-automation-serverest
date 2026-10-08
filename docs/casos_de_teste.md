# Casos de Teste

Legenda de tipo: **P** = positivo (caminho feliz), **N** = negativo (erro esperado).

## API – Usuários (`tests/api/test_usuarios.py`)
| ID | Cenário | Tipo | Resultado esperado |
|---|---|---|---|
| CT-API-01 | Cadastrar usuário com dados válidos | P | 201 e "Cadastro realizado com sucesso" |
| CT-API-02 | Cadastrar com e-mail já usado | N | 400 e "Este email já está sendo usado" |
| CT-API-03 | Cadastrar sem um campo obrigatório (nome, email, password, administrador) | N | 400 indicando o campo |
| CT-API-04 | Cadastrar com e-mail inválido | N | 400 "email deve ser um email válido" |
| CT-API-05 | Buscar usuário por id | P | 200 e resposta no formato do schema |
| CT-API-06 | Buscar usuário que não existe | N | 400 "Usuário não encontrado" |
| CT-API-07 | Buscar usuário com id em formato inválido | N | 400 indicando o campo id |
| CT-API-08 | Listar usuários filtrando por e-mail | P | 200 e exatamente 1 usuário |
| CT-API-09 | Editar usuário | P | 200 e nome alterado de fato |
| CT-API-10 | Excluir usuário | P | 200 e usuário não encontrado depois |

## API – Login (`tests/api/test_login.py`)
| ID | Cenário | Tipo | Resultado esperado |
|---|---|---|---|
| CT-API-11 | Login com dados corretos | P | 200 e token "Bearer ..." |
| CT-API-12 | Login com senha errada | N | 401 "Email e/ou senha inválidos" |
| CT-API-13 | Login com e-mail não cadastrado | N | 401 "Email e/ou senha inválidos" |
| CT-API-14 | Login com e-mail ou senha vazios | N | 400 indicando o campo |

## API – Produtos (`tests/api/test_produtos.py`)
| ID | Cenário | Tipo | Resultado esperado |
|---|---|---|---|
| CT-API-15 | Cadastrar produto como administrador | P | 201 |
| CT-API-16 | Cadastrar produto sem token | N | 401 token ausente ou inválido |
| CT-API-17 | Cadastrar produto com usuário comum | N | 403 "Rota exclusiva para administradores" |
| CT-API-18 | Cadastrar produto com nome repetido | N | 400 "Já existe produto com esse nome" |
| CT-API-19 | Cadastrar produto com preço zero ou negativo | N | 400 indicando o campo preco |
| CT-API-20 | Buscar produto por id | P | 200 e resposta no formato do schema |
| CT-API-21 | Editar preço do produto | P | 200 e preço alterado de fato |
| CT-API-22 | Excluir produto | P | 200 e produto não encontrado depois |

## Web (`tests/web/`)
| ID | Cenário | Tipo | Resultado esperado |
|---|---|---|---|
| CT-WEB-01 | Login de cliente | P | Abre a loja "Serverest Store" |
| CT-WEB-02 | Login de administrador | P | Abre o painel com "Bem Vindo" e o nome |
| CT-WEB-03 | Login com senha errada | N | Mensagem "Email e/ou senha inválidos" |
| CT-WEB-04 | Cadastrar novo cliente pela tela | P | Entra na loja após o cadastro |
| CT-WEB-05 | Cadastrar com e-mail já usado | N | Mensagem "Este email já está sendo usado" |
| CT-WEB-06 | Pesquisar produto pelo nome | P | Produto aparece na busca |
| CT-WEB-07 | Adicionar produto na lista de compras | P | Produto aparece na "Lista de Compras" |
| CT-WEB-08 | Limpar lista de compras | P | Mensagem "Seu carrinho está vazio" |
