"""Testes da rota /login."""
import pytest

from utils.schema_validator import validar_schema

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_login_com_sucesso(api, usuario_cadastrado):
    resposta = api.login(usuario_cadastrado["email"], usuario_cadastrado["password"])

    assert resposta.status_code == 200
    corpo = resposta.json()
    validar_schema(corpo, "login.json")
    assert corpo["message"] == "Login realizado com sucesso"


def test_login_com_senha_errada(api, usuario_cadastrado):
    resposta = api.login(usuario_cadastrado["email"], "senhaErrada123")

    assert resposta.status_code == 401
    assert resposta.json()["message"] == "Email e/ou senha inválidos"


def test_login_com_email_nao_cadastrado(api):
    resposta = api.login("ninguem_cadastrado@teste.com", "qualquer")

    assert resposta.status_code == 401
    assert resposta.json()["message"] == "Email e/ou senha inválidos"


@pytest.mark.parametrize(
    "email, senha, campo_com_erro",
    [
        ("", "senha123", "email"),
        ("teste@teste.com", "", "password"),
    ],
    ids=["email-vazio", "senha-vazia"],
)
def test_login_com_campo_vazio(api, email, senha, campo_com_erro):
    resposta = api.login(email, senha)

    assert resposta.status_code == 400
    assert campo_com_erro in resposta.json()
