"""Testes de login pela tela do navegador."""
import re

import pytest
from playwright.sync_api import expect

from tests.web.pages.home_page import HomeAdminPage, HomeClientePage
from tests.web.pages.login_page import LoginPage

pytestmark = pytest.mark.web


@pytest.mark.smoke
def test_login_de_cliente_abre_a_loja(page, cliente):
    LoginPage(page).abrir().fazer_login(cliente["email"], cliente["password"])

    expect(page).to_have_url(re.compile(r"/home$"))
    expect(HomeClientePage(page).titulo()).to_be_visible()


def test_login_de_admin_abre_o_painel_administrativo(page, admin):
    LoginPage(page).abrir().fazer_login(admin["email"], admin["password"])

    expect(HomeAdminPage(page).boas_vindas()).to_be_visible()
    expect(HomeAdminPage(page).boas_vindas()).to_contain_text(admin["nome"])


def test_login_com_senha_errada_mostra_mensagem(page, cliente):
    login = LoginPage(page).abrir()

    login.fazer_login(cliente["email"], "senhaErrada123")

    expect(login.mensagem_de_erro()).to_contain_text("Email e/ou senha inválidos")
