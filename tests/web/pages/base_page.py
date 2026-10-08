"""Página base: o que todas as páginas têm em comum."""
from playwright.sync_api import Page

from utils.config import WEB_URL


class BasePage:
    caminho = "/"

    def __init__(self, page: Page):
        self.page = page

    def abrir(self):
        self.page.goto(f"{WEB_URL}{self.caminho}")
        return self

    def elemento(self, test_id: str):
        """Encontra um elemento pelo atributo data-testid."""
        return self.page.get_by_test_id(test_id)
