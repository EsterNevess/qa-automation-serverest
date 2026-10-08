"""Testes de cadastro de usuário pela tela."""
import pytest
from playwright.sync_api import expect

from tests.web.pages.cadastro_page import CadastroPage
from tests.web.pages.home_page import HomeClientePage
from tests.web.pages.login_page import LoginPage
from utils.data_factory import novo_usuario

pytestmark = pytest.mark.web


@pytest.mark.smoke
def test_cadastrar_usuario_pela_tela(page, api):
    dados = novo_usuario(administrador=False)
    LoginPage(page).abrir().ir_para_cadastro()

    CadastroPage(page).cadastrar(dados["nome"], dados["email"], dados["password"])

    # depois do cadastro, o sistema entra direto na loja
    expect(HomeClientePage(page).titulo()).to_be_visible()

    # limpeza: apaga pela API o usuário criado pela tela
    usuarios = api.listar_usuarios(email=dados["email"]).json()["usuarios"]
    assert len(usuarios) == 1, "o usuário cadastrado pela tela deveria existir na API"
    api.excluir_usuario(usuarios[0]["_id"])


def test_nao_cadastrar_usuario_com_email_ja_usado(page, cliente):
    cadastro = CadastroPage(page).abrir()

    cadastro.cadastrar("Outra Pessoa", cliente["email"], "senha123")

    expect(cadastro.mensagem()).to_contain_text("Este email já está sendo usado")
