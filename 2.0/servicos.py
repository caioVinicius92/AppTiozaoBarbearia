import flet as ft

try:
    Colors = ft.Colors
except Exception:
    Colors = ft.Colors

SERVICOS = [
    {"nome": "Corte", "preco": 40.00},
    {"nome": "Barba", "preco": 30.00},
    {"nome": "Corte + Barba", "preco": 60.00},
]


def servico_view(page: ft.Page) -> ft.Column:
    """Página para selecionar tipo de serviço"""
    page.bgcolor = "#546b7b"

    # Botão de voltar
    back_btn = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=Colors.WHITE,
        on_click=lambda _: page.go("/agendamento"),
    )

    title = ft.Text(
        "Selecione o Tipo de Serviço",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=Colors.WHITE,
    )

    # Lista de botões de serviço
    controles = []
    for s in SERVICOS:
        nome_servico = s["nome"]
        preco_servico = s["preco"]
        texto_botao = f"{nome_servico}\nR$ {preco_servico:.2f}"
        
        def make_on_click(serv_nome):
            def _(_e):
                page.session.set("selected_service", serv_nome)
                # navegar diretamente para a tela de agendamento
                page.go("/agendamento")
                page.update()
            return _

        btn = ft.ElevatedButton(
            texto_botao,
            on_click=make_on_click(nome_servico),
            width=300,
        )
        controles.append(btn)

    coluna = ft.Column(
        controls=[
            ft.Row(controls=[back_btn], alignment=ft.MainAxisAlignment.START),
            title,
            ft.Divider(thickness=1, color=ft.Colors.WHITE24),
            ft.Column(controls=controles, spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ],
        spacing=16,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return coluna