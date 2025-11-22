import flet as ft

#tamanho geral da pagina
def first_view(page: ft.Page) -> ft.Column:
    # Avoid forcing a fixed window size; allow responsiveness
    try:
        if hasattr(page, "window"):
            pass
    except Exception:
        pass
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 0
    
    # botão Login -> vai para /login
    button_login = ft.OutlinedButton(
        text="Login",
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE),
                ft.Text("Login", color=ft.Colors.WHITE),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        #estilo do botao
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_800,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=6),
        ),
        width=200,
        #click que muda page view
        on_click=lambda _: page.go("/login"),
    )

    container = ft.Stack(
        controls=[
            ##background
            ft.Image(src='2.0/pageinicial.png', width=320, height=480, fit=ft.ImageFit.COVER),
            ft.Container(
                #margens e borda dentro do container
                width= 220,
                height= 400,
                border_radius= 16,
                #adiçao de tudo
                content=ft.Column(
                    controls=[
                        ft.Divider(thickness=2, color=ft.Colors.WHITE24),
                        button_login,
                    ],alignment= ft.MainAxisAlignment.END, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )  
        ],
        #tamanho do container
        alignment= ft.alignment.center,
        width= 320,
        height= 480,
        expand= True
    )

    return ft.Column(
        controls=[container],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )