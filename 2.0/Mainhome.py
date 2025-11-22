import flet as ft

def home_view(page: ft.Page):
    # Configurações da página
    page.title = "Home"
    page.bgcolor = "#546b7b"
    # Allow the window to be resized by the user — avoid forcing a fixed mobile size
    try:
        # preserve any existing window constraints but don't hard-code width/height
        if hasattr(page, "window"):
            pass
    except Exception:
        pass
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20

    # Recupera o usuário logado (ou nome genérico)
    user = page.session.get("user") or page.client_storage.get("logged_user") or "usuário"

    # calcular largura responsiva para o container principal (segura se page.window.width não estiver disponível)
    try:
        pw = None
        if hasattr(page, "window") and getattr(page.window, "width", None):
            pw = page.window.width
        if pw:
            # garantir integer e limites
            container_width = min(max(300, int(pw) - 40), 900)
        else:
            container_width = None
    except Exception:
        container_width = None

    # Botão de voltar
    back_btn = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.WHITE,
        on_click=lambda _: page.go("/first"),
        style=ft.ButtonStyle(bgcolor=None, padding=10)
    )

    # Título
    titulo_width = int(container_width * 0.7) if container_width else 250
    titulo = ft.Image(
        src="2.0/hometitulo.png",
        width=titulo_width,
        height=80,
        fit=ft.ImageFit.CONTAIN,
    )

    # Faixa translúcida de saudação
    saudacao_container = ft.Container(
        content=ft.Text(
            f"Bem-vindo, {user}!",
            size=18,
            color=ft.Colors.WHITE,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.W_500,
        ),
        bgcolor=ft.Colors.WHITE10,
        border_radius=10,
        padding=10,
        alignment=ft.alignment.center,
        width=container_width
    )

    # Botões principais
    btn2 = ft.Column(
        controls=[
            ft.IconButton(
                icon=ft.Icons.CONTENT_CUT,
                icon_color=ft.Colors.BLUE_700,
                icon_size=70,
                tooltip="Cortes de cabelo",
                on_click=lambda _:
                (page.session.set("return_to", "/home"), page.go("/servico")),
                style=ft.ButtonStyle(bgcolor=None),
            ),
            ft.Text(
                "Serviços",
                color=ft.Colors.WHITE,
                size=16,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD,
                font_family="Verdana"
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0
    )

    # Botão de logout (em nova linha)
    btn_logout = ft.Column(
        controls=[
            ft.IconButton(
                icon=ft.Icons.LOGOUT,
                icon_color=ft.Colors.RED_400,
                icon_size=70,
                tooltip="Sair",
                on_click=lambda _: (
                    page.session.remove("user"),
                    page.client_storage.remove("logged_user"),
                    page.go("/login"),
                    page.update()
                ),
                style=ft.ButtonStyle(bgcolor=None),
            ),
            ft.Text(
                "   Sair",
                color=ft.Colors.WHITE,
                size=16,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD,
                font_family="Verdana"
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=2
    )

    # Linha superior de botões (apenas cortes)
    botoes_grid = ft.Row(
        controls=[btn2],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    # Linha inferior (logout centralizado)
    linha_logout = ft.Row(
        controls=[btn_logout],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
    )

    # Container principal
    container_principal = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row([back_btn], alignment=ft.MainAxisAlignment.START),
                ft.Divider(thickness=3, color=ft.Colors.WHITE24),
                titulo,
                ft.Divider(thickness=3, color=ft.Colors.WHITE24),
                saudacao_container,  
                botoes_grid,
                linha_logout
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
            expand=True,
        ),
        bgcolor="#5a7889",
        padding=20,
        border_radius=15,
        width=container_width,
        shadow=ft.BoxShadow(color=ft.Colors.BLACK, blur_radius=5, offset=ft.Offset(2, 2))
    )

    # Retornar coluna principal (container no topo)
    return ft.Column(
        controls=[container_principal],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
    ##bgcolor="#5a7889",