"""Fixtures dos testes de API.

Fixture é uma função que o pytest executa ANTES do teste para preparar
o que ele precisa (um usuário cadastrado, um token de login...) e,
depois do "yield", executa a LIMPEZA (apaga o que foi criado).
O teste só precisa pedir a fixture pelo nome, como parâmetro.
"""
import pytest

from utils.api_client import ServeRestClient
from utils.data_factory import novo_produto, novo_usuario


@pytest.fixture(scope="session")
def api():
    """Um único cliente da API, compartilhado por todos os testes."""
    return ServeRestClient()


@pytest.fixture
def usuario_cadastrado(api):
    """Cadastra um usuário administrador e o apaga ao final do teste."""
    dados = novo_usuario(administrador=True)
    resposta = api.cadastrar_usuario(dados)
    assert resposta.status_code == 201, resposta.text
    dados["_id"] = resposta.json()["_id"]
    yield dados
    api.excluir_usuario(dados["_id"])


@pytest.fixture
def usuario_comum(api):
    """Cadastra um usuário que NÃO é administrador e o apaga ao final."""
    dados = novo_usuario(administrador=False)
    resposta = api.cadastrar_usuario(dados)
    assert resposta.status_code == 201, resposta.text
    dados["_id"] = resposta.json()["_id"]
    yield dados
    api.excluir_usuario(dados["_id"])


@pytest.fixture
def token_admin(api, usuario_cadastrado):
    """Faz login com o usuário administrador e devolve o token."""
    resposta = api.login(usuario_cadastrado["email"], usuario_cadastrado["password"])
    assert resposta.status_code == 200, resposta.text
    return resposta.json()["authorization"]


@pytest.fixture
def token_comum(api, usuario_comum):
    """Faz login com o usuário comum e devolve o token."""
    resposta = api.login(usuario_comum["email"], usuario_comum["password"])
    assert resposta.status_code == 200, resposta.text
    return resposta.json()["authorization"]


@pytest.fixture
def produto_cadastrado(api, token_admin):
    """Cadastra um produto e o apaga ao final do teste."""
    dados = novo_produto()
    resposta = api.cadastrar_produto(dados, token_admin)
    assert resposta.status_code == 201, resposta.text
    dados["_id"] = resposta.json()["_id"]
    yield dados
    api.excluir_produto(dados["_id"], token_admin)
