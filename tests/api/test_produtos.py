"""Testes da rota /produtos, incluindo regras de permissão."""
import pytest

from utils.data_factory import novo_produto
from utils.schema_validator import validar_schema

pytestmark = pytest.mark.api

# Conferimos só o início da mensagem, porque o final varia entre versões do ServeRest
MSG_TOKEN_INVALIDO = "Token de acesso ausente, inválido, expirado"


@pytest.mark.smoke
def test_cadastrar_produto_como_admin(api, token_admin):
    dados = novo_produto()

    resposta = api.cadastrar_produto(dados, token_admin)

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["message"] == "Cadastro realizado com sucesso"
    api.excluir_produto(corpo["_id"], token_admin)  # limpeza


def test_nao_cadastrar_produto_sem_token(api):
    resposta = api.cadastrar_produto(novo_produto())

    assert resposta.status_code == 401
    assert resposta.json()["message"].startswith(MSG_TOKEN_INVALIDO)


def test_nao_cadastrar_produto_com_usuario_comum(api, token_comum):
    resposta = api.cadastrar_produto(novo_produto(), token_comum)

    assert resposta.status_code == 403
    assert resposta.json()["message"] == "Rota exclusiva para administradores"


def test_nao_cadastrar_produto_com_nome_repetido(api, token_admin, produto_cadastrado):
    dados = novo_produto()
    dados["nome"] = produto_cadastrado["nome"]

    resposta = api.cadastrar_produto(dados, token_admin)

    assert resposta.status_code == 400
    assert resposta.json()["message"] == "Já existe produto com esse nome"


@pytest.mark.parametrize("preco", [0, -10], ids=["preco-zero", "preco-negativo"])
def test_nao_cadastrar_produto_com_preco_invalido(api, token_admin, preco):
    dados = novo_produto()
    dados["preco"] = preco

    resposta = api.cadastrar_produto(dados, token_admin)

    assert resposta.status_code == 400
    assert "preco" in resposta.json()


def test_buscar_produto_por_id(api, produto_cadastrado):
    resposta = api.buscar_produto(produto_cadastrado["_id"])

    assert resposta.status_code == 200
    corpo = resposta.json()
    validar_schema(corpo, "produto.json")
    assert corpo["nome"] == produto_cadastrado["nome"]
    assert corpo["preco"] == produto_cadastrado["preco"]


def test_editar_produto(api, token_admin, produto_cadastrado):
    novos_dados = {**produto_cadastrado, "preco": 999}
    novos_dados.pop("_id")

    resposta = api.editar_produto(produto_cadastrado["_id"], novos_dados, token_admin)

    assert resposta.status_code == 200
    assert resposta.json()["message"] == "Registro alterado com sucesso"
    assert api.buscar_produto(produto_cadastrado["_id"]).json()["preco"] == 999


def test_excluir_produto(api, token_admin):
    produto_id = api.cadastrar_produto(novo_produto(), token_admin).json()["_id"]

    resposta = api.excluir_produto(produto_id, token_admin)

    assert resposta.status_code == 200
    assert resposta.json()["message"] == "Registro excluído com sucesso"
    assert api.buscar_produto(produto_id).status_code == 400
