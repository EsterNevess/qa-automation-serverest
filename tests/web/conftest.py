"""Fixtures dos testes web.

Os dados (usuários e produtos) são criados pela API, que é rápida.
Assim o teste de tela foca só no que importa: o comportamento da tela.
"""
import pytest

from utils.api_client import ServeRestClient
from utils.data_factory import novo_produto, novo_usuario


@pytest.fixture(scope="session")
def api():
    return ServeRestClient()


@pytest.fixture
def cliente(api):
    """Usuário comum (não administrador) criado pela API."""
    dados = novo_usuario(administrador=False)
    dados["_id"] = api.cadastrar_usuario(dados).json()["_id"]
    yield dados
    api.excluir_usuario(dados["_id"])


@pytest.fixture
def admin(api):
    """Usuário administrador criado pela API."""
    dados = novo_usuario(administrador=True)
    dados["_id"] = api.cadastrar_usuario(dados).json()["_id"]
    yield dados
    api.excluir_usuario(dados["_id"])


@pytest.fixture
def produto(api, admin):
    """Produto criado pela API, para aparecer na loja."""
    token = api.login(admin["email"], admin["password"]).json()["authorization"]
    dados = novo_produto()
    dados["_id"] = api.cadastrar_produto(dados, token).json()["_id"]
    yield dados
    api.excluir_produto(dados["_id"], token)


@pytest.fixture(autouse=True)
def tempo_de_espera(page):
    """Tempo máximo que o Playwright espera um elemento aparecer."""
    page.set_default_timeout(15000)
    yield
