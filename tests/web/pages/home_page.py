"""Page Objects das telas iniciais (cliente e administrador)."""
from tests.web.pages.base_page import BasePage


class HomeClientePage(BasePage):
    caminho = "/home"

    def titulo(self):
        return self.page.get_by_role("heading", name="Serverest Store")

    def pesquisar_produto(self, nome: str):
        self.elemento("pesquisar").fill(nome)
        self.elemento("botaoPesquisar").click()

    def card_do_produto(self, nome: str):
        return self.page.locator(".card-title", has_text=nome)

    def adicionar_primeiro_produto_na_lista(self):
        self.elemento("adicionarNaLista").first.click()


class HomeAdminPage(BasePage):
    caminho = "/admin/home"

    def boas_vindas(self):
        return self.page.get_by_role("heading", name="Bem Vindo")


class ListaDeComprasPage(BasePage):
    caminho = "/minhaListaDeProdutos"

    def titulo(self):
        return self.page.get_by_role("heading", name="Lista de Compras")

    def nomes_dos_produtos(self):
        return self.elemento("shopping-cart-product-name")

    def limpar_lista(self):
        self.elemento("limparLista").click()

    def mensagem_lista_vazia(self):
        return self.elemento("shopping-cart-empty-message")
