"""Hooks compartilhados pelos testes de API e de interface.

Fica na raiz porque vale para as duas suítes: o que muda entre elas é
o tipo de evidência que faz sentido anexar quando algo falha.
"""
import allure
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Anexa evidência ao relatório Allure quando um teste falha.

    Nos testes web, anexa o print da tela, a URL e o HTML da página.
    Nos de API, o relatório já guarda a requisição e a resposta registradas
    pelos próprios testes, então não há o que acrescentar aqui.
    """
    resultado = yield
    relatorio = resultado.get_result()
    if relatorio.when != "call" or not relatorio.failed:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    try:
        allure.attach(
            page.screenshot(full_page=True),
            name=f"Tela no momento da falha - {item.name}",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            page.url,
            name="URL no momento da falha",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            page.content(),
            name="HTML da página",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception as erro:  # noqa: BLE001
        print(f"\nNão foi possível capturar a evidência: {erro}")
