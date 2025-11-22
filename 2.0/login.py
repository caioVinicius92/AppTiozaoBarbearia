import flet as ft
import os
import json

# Segurança de senhas
try:
    import bcrypt
except ImportError:
    bcrypt = None  # Mostraremos aviso na UI se não estiver instalado

# Usar Colors do flet diretamente
Colors = ft.Colors

DATA_DIR = "storage"
USERS_FILE = os.path.join(DATA_DIR, "users.json")


def ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump({"users": []}, f, indent=2, ensure_ascii=False)


def load_users():
    ensure_storage()
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("users", [])
    except Exception:
        return []


def save_users(users):
    ensure_storage()
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump({"users": users}, f, indent=2, ensure_ascii=False)


def find_user(username: str, users=None):
    if users is None:
        users = load_users()
    for u in users:
        if u.get("username", "").lower() == username.lower():
            return u
    return None


def hash_password(plain: str) -> str:
    if bcrypt is None:
        return f"PLAINTEXT::{plain}"
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(plain: str, stored: str) -> bool:
    if bcrypt is None:
        return stored == f"PLAINTEXT::{plain}"
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), stored.encode("utf-8"))
    except Exception:
        return False


def seed_admin(default_password: str = "admin"):
    users = load_users()
    if find_user("admin", users) is None:
        users.append(
            {
                "username": "admin",
                "password": hash_password(default_password),
            }
        )
        save_users(users)


def snackbar(page: ft.Page, msg: str, *, bg=Colors.BLUE_GREY_900, color=Colors.WHITE):
    snack = ft.SnackBar(
        content=ft.Text(msg, color=color),
        bgcolor=bg,
        show_close_icon=True,
        behavior=ft.SnackBarBehavior.FLOATING,
    )
    page.overlay.append(snack)
    snack.open = True
    page.update()


def build_mobile_card(content: ft.Control, width: int | None = None) -> ft.Container:
    # width: desired container width in pixels (optional)
    w = width or 390
    return ft.Container(
        width=w,
        padding=20,
        content=ft.Column(
            controls=[content],
            scroll=ft.ScrollMode.AUTO,
        ),
        alignment=ft.alignment.center,
    )


# ---------- VIEWS ----------
def login_view(page: ft.Page) -> ft.Column:
    page.bgcolor = "#546b7b"  # fundo da página

    # calcular largura responsiva para o container (seguro se page.window.width não existir)
    try:
        pw = None
        if hasattr(page, "window") and getattr(page.window, "width", None):
            pw = page.window.width
        if pw:
            container_width = min(max(300, int(pw) - 40), 900)
        else:
            container_width = None
    except Exception:
        container_width = None

    # Botão de voltar
    back_btn = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=Colors.WHITE,
        on_click=lambda _: page.go("/first"),
        style=ft.ButtonStyle(bgcolor=None, padding=10)
    )

    # Título do login
    title = ft.Text(
        "Acesso ao APP",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=Colors.WHITE
    )

    # Campos de usuário e senha
    username = ft.TextField(
        label="Nome",
        autofocus=True,
        bgcolor=Colors.WHITE
    )
    password = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        bgcolor=Colors.WHITE
    )

    # Função de login
    def do_login(_=None):
        u = (username.value or "").strip()
        p = password.value or ""
        if not u or not p:
            snackbar(page, "Informe usuário e senha.", bg=Colors.RED_400)
            return
        user = find_user(u)
        if user and check_password(p, user.get("password", "")):
            # Salva login na sessão e no armazenamento local
            page.session.set("user", u)
            page.client_storage.set("logged_user", u)
            snackbar(page, "Login realizado com sucesso!", bg=Colors.GREEN_500)
            page.go("/home")
            page.update()
            return
        snackbar(page, "Usuário ou senha inválidos.", bg=Colors.RED_400)


    username.on_submit = do_login
    password.on_submit = do_login

    # Botão de login
    login_btn_width = int(container_width * 0.6) if container_width else 200
    login_btn = ft.ElevatedButton(
        "Entrar",
        on_click=do_login,
        style=ft.ButtonStyle(
            color=Colors.WHITE,
            bgcolor=Colors.BLUE_600,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=7),
        ),
        width=login_btn_width,
    )

    # Botão de cadastro
    register_btn = ft.TextButton(
        "Cadastre-se",
        on_click=lambda _: page.go("/cadastro"),
        style=ft.ButtonStyle(color=Colors.BLUE_600, bgcolor=None),
    )

    # Formulário do login
    form = ft.Column(
        controls=[
            title,
            ft.Divider(thickness=2, color=ft.Colors.WHITE24),  # borda semi-transparente
            username,
            password,
            ft.Container(height=8),
            login_btn,
            ft.Divider(thickness=2, color=ft.Colors.WHITE24),
            ft.Container(height=4),
            ft.Row(
                controls=[ft.Text("Ainda não tem conta?"), register_btn],
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    # Card
    card = ft.Container(
        content=form,
        padding=20,
        bgcolor=None,
        border_radius=12,
    )

    # Layout principal
    root = ft.Column(
        controls=[
            ft.Row(
                controls=[back_btn],
                alignment=ft.MainAxisAlignment.START
            ),
            ft.Row(
                controls=[build_mobile_card(card, container_width)],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        ],
        spacing=20,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return root

def cadastro_view(page: ft.Page) -> ft.Column:
    page.bgcolor = "#546b7b"  # fundo da página, igual ao login

    # calcular largura responsiva para o container
    try:
        pw = None
        if hasattr(page, "window") and getattr(page.window, "width", None):
            pw = page.window.width
        if pw:
            container_width = min(max(300, int(pw) - 40), 900)
        else:
            container_width = None
    except Exception:
        container_width = None

    # Botão de voltar
    back_btn = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=Colors.WHITE,
        on_click=lambda _: page.go("/login"),
        style=ft.ButtonStyle(bgcolor=None, padding=10)
    )

    # Título do cadastro
    title = ft.Text(
        "Criar Conta",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=Colors.WHITE
    )

    # Campos de usuário e senha
    user_new = ft.TextField(
        label="Usuário",
        autofocus=True,
        bgcolor=Colors.WHITE
    )
    pass_new = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        bgcolor=Colors.WHITE
    )
    pass_conf = ft.TextField(
        label="Confirmar Senha",
        password=True,
        can_reveal_password=True,
        bgcolor=Colors.WHITE
    )

    # Função de cadastro
    def do_register(_=None):
        u = (user_new.value or "").strip()
        p1 = pass_new.value or ""
        p2 = pass_conf.value or ""

        if not u or not p1 or not p2:
            snackbar(page, "Preencha todos os campos.", bg=Colors.RED_400)
            return
        if p1 != p2:
            snackbar(page, "As senhas não conferem.", bg=Colors.RED_400)
            return
        users = load_users()
        if find_user(u, users) is not None:
            snackbar(page, "Usuário já existe.", bg=Colors.RED_400)
            return

        users.append({"username": u, "password": hash_password(p1)})
        save_users(users)
        snackbar(page, "Cadastro realizado! Faça login.", bg=Colors.GREEN_500)
        page.go("/login")
        page.update()

    # Atalhos para Enter nos campos
    user_new.on_submit = do_register
    pass_new.on_submit = do_register
    pass_conf.on_submit = do_register

    # Botão de cadastro
    register_btn_width = int(container_width * 0.6) if container_width else 200
    register_btn = ft.ElevatedButton(
        "Cadastrar",
        on_click=do_register,
        style=ft.ButtonStyle(
            color=Colors.WHITE,
            bgcolor=Colors.BLUE_600,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=7),
        ),
        width=register_btn_width,
    )

    # Botão de voltar ao login
    back_login_btn = ft.TextButton(
        "Voltar ao login",
        on_click=lambda _: page.go("/login"),
        style=ft.ButtonStyle(color=Colors.BLUE_600, bgcolor=None),
    )

    # Formulário
    form = ft.Column(
        controls=[
            title,
            ft.Divider(thickness=2, color=ft.Colors.WHITE24),
            user_new,
            pass_new,
            pass_conf,
            ft.Container(height=8),
            register_btn,
            ft.Divider(thickness=2, color=ft.Colors.WHITE24),
            ft.Container(height=4),
            ft.Row(
                controls=[ft.Text("Já tem uma conta?"), back_login_btn],
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    # Card central
    card = ft.Container(
        content=form,
        padding=20,
        bgcolor=None,
        border_radius=12,
    )

    # Layout principal
    root = ft.Column(
        controls=[
            ft.Row(
                controls=[back_btn],
                alignment=ft.MainAxisAlignment.START
            ),
            ft.Row(
                controls=[build_mobile_card(card, container_width)],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        ],
        spacing=20,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return root

def home_view(page: ft.Page) -> ft.Column:
    user = page.session.get("user") or "usuário"
    # calcular largura responsiva para o container
    try:
        pw = None
        if hasattr(page, "window") and getattr(page.window, "width", None):
            pw = page.window.width
        if pw:
            container_width = min(max(300, int(pw) - 40), 900)
        else:
            container_width = None
    except Exception:
        container_width = None
    welcome = ft.Text(
        f"Bem-vindo, {user}!", size=22, weight=ft.FontWeight.BOLD
    )

    logout_btn = ft.ElevatedButton(
        "Sair",
        on_click=lambda _: (page.session.remove("user"), page.go("/login"), page.update()),
        style=ft.ButtonStyle(
            bgcolor=Colors.RED_500,
            color=Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    area = ft.Container(
        content=ft.Column(
            controls=[
                welcome,
                ft.Text("Você está autenticado. Esta é a tela inicial."),
                ft.Container(height=12),
                logout_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=20,
        bgcolor=Colors.WHITE,
        border_radius=12,
        shadow=ft.BoxShadow(
            blur_radius=20, spread_radius=1, color=Colors.BLUE_GREY_200
        ),
    )
    root = ft.Column(
        controls=[build_mobile_card(area, container_width)],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )
    return root
