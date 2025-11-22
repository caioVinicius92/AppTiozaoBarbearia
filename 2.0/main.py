import flet as ft
import os
from home import first_view
from login import login_view, cadastro_view, home_view, ensure_storage, seed_admin, snackbar, Colors, bcrypt
from Mainhome import home_view as main_home_view
from agendamento import agendamento_view
from servicos import servico_view

def main(page: ft.Page):
    page.title = "Tiozão Barbearia"
    
    # Inicialização de storage e admin
    ensure_storage()
    seed_admin()

    # --------------------------
    # Função para verificar login
    # --------------------------
    def is_logged_in():
        """
        Retorna True se existir usuário salvo no armazenamento local.
        Isso permite que o usuário seja lembrado mesmo fechando o navegador.
        """
        return page.client_storage.get("logged_user") is not None

    # --------------------------
    # Função que atualiza a view quando a rota muda
    # --------------------------
    def route_change(_):
        page.views.clear()
        route = page.route or "/first"

        if route == "/first":
            page.bgcolor = Colors.BLUE_GREY_900
            page.views.append(ft.View("/first", controls=[first_view(page)], bgcolor=page.bgcolor))
        elif route == "/login":
            page.bgcolor = Colors.BLUE_GREY_50
            page.views.append(ft.View("/login", controls=[login_view(page)], bgcolor=page.bgcolor))
        elif route == "/cadastro":
            page.bgcolor = Colors.BLUE_GREY_100
            page.views.append(ft.View("/cadastro", controls=[cadastro_view(page)], bgcolor=page.bgcolor))
        elif route == "/home":
            page.bgcolor = Colors.WHITE
            page.views.append(ft.View("/home", controls=[main_home_view(page)], bgcolor=page.bgcolor))
        elif route == "/agendamento":
            page.bgcolor = Colors.BLUE_GREY_900
            page.views.append(ft.View("/agendamento", controls=[agendamento_view(page)], bgcolor=page.bgcolor))
        elif route == "/servico":
            page.bgcolor = Colors.BLUE_GREY_900
            page.views.append(ft.View("/servico", controls=[servico_view(page)], bgcolor=page.bgcolor))
        else:
            page.go("/first")
            return
        page.update()

    # --------------------------
    # Função que trata o "voltar"
    # --------------------------
    def view_pop(_):
        page.views.pop()
        if page.views:
            route = page.views[-1].route
            if route:
                page.go(route)
            else:
                page.go("/first")
        else:
            page.go("/first")

    # --------------------------
    # Configuração dos eventos
    # --------------------------
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # --------------------------
    # Aviso caso bcrypt não esteja instalado
    # --------------------------
    if bcrypt is None:
        snackbar(
            page,
            "Atenção: bcrypt não instalado. As senhas serão salvas em texto puro (apenas para testes).\nExecute: pip install bcrypt",
            bg=Colors.AMBER_600,
        )

    # --------------------------
    # Inicialização da rota
    # --------------------------
    # Se usuário já está logado → vai direto para /home
    # Se não → vai para /first
    # Optionally start directly at the login page when the environment
    # variable START_AT_LOGIN is set to '1' (useful for testing).
    # Optionally start directly at the login page when the environment
    # variable START_AT_LOGIN is set to '1' (useful for testing).
    if os.getenv("START_AT_LOGIN") == "1":
        page.go("/login")
        return

    # Optionally start directly at the main home page when START_AT_HOME=1
    if os.getenv("START_AT_HOME") == "1":
        page.go("/home")
        return

    if is_logged_in():
        page.go("/home")
    else:
        page.go("/first")

if __name__ == "__main__":
    ft.app(target=main)
