"""Teste de ponta a ponta (E2E): buscar um produto e adicionar à lista de compras."""
import pytest
from playwright.sync_api import expect

from tests.web.pages.home_page import HomeClientePage, ListaDeComprasPage
from tests.web.pages.login_page import LoginPage

pytestmark = pytest.mark.web


def test_pesquisar_produto_pelo_nome(page, cliente, produto):
    LoginPage(page).abrir().fazer_login(cliente["email"], cliente["password"])
    loja = HomeClientePage(page)

    loja.pesquisar_produto(produto["nome"])

    expect(loja.card_do_produto(produto["nome"])).to_be_visible()


@pytest.mark.smoke
def test_buscar_produto_e_adicionar_na_lista(page, cliente, produto):
    LoginPage(page).abrir().fazer_login(cliente["email"], cliente["password"])
    loja = HomeClientePage(page)
    expect(loja.titulo()).to_be_visible()

    loja.pesquisar_produto(produto["nome"])
    expect(loja.card_do_produto(produto["nome"])).to_be_visible()
    loja.adicionar_primeiro_produto_na_lista()

    lista = ListaDeComprasPage(page)
    expect(lista.titulo()).to_be_visible()
    expect(lista.nomes_dos_produtos().first).to_contain_text(produto["nome"])


def test_limpar_lista_de_compras(page, cliente, produto):
    LoginPage(page).abrir().fazer_login(cliente["email"], cliente["password"])
    loja = HomeClientePage(page)
    loja.pesquisar_produto(produto["nome"])
    loja.adicionar_primeiro_produto_na_lista()

    lista = ListaDeComprasPage(page)
    lista.limpar_lista()

    expect(lista.mensagem_lista_vazia()).to_have_text("Seu carrinho está vazio")
