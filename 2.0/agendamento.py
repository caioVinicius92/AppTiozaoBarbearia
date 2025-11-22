import flet as ft
import json
import os
from datetime import datetime, timedelta

# Usar Colors do flet diretamente
Colors = ft.Colors

# Arquivo de armazenamento de agendamentos
DATA_DIR = "storage"
AGENDAMENTOS_FILE = os.path.join(DATA_DIR, "agendamentos.json")

# Horários disponíveis para agendamento
HORARIOS_DISPONIVEIS = [
    "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
    "12:00", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00",
    "16:30", "17:00"
]

def ensure_agendamentos_storage():
    """Garante que o arquivo de agendamentos existe"""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(AGENDAMENTOS_FILE):
        with open(AGENDAMENTOS_FILE, "w", encoding="utf-8") as f:
            json.dump({"agendamentos": []}, f, indent=2, ensure_ascii=False)

def load_agendamentos():
    """Carrega todos os agendamentos"""
    ensure_agendamentos_storage()
    try:
        with open(AGENDAMENTOS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("agendamentos", [])
    except Exception:
        return []

def save_agendamentos(agendamentos):
    """Salva agendamentos no arquivo"""
    ensure_agendamentos_storage()
    with open(AGENDAMENTOS_FILE, "w", encoding="utf-8") as f:
        json.dump({"agendamentos": agendamentos}, f, indent=2, ensure_ascii=False)

def get_horarios_disponiveis_dia(data_str: str):
    """Retorna horários disponíveis para um determinado dia"""
    agendamentos = load_agendamentos()
    horarios_ocupados = [
        a["horario"] for a in agendamentos if a["data"] == data_str
    ]
    return [h for h in HORARIOS_DISPONIVEIS if h not in horarios_ocupados]

def snackbar(page: ft.Page, msg: str, *, bg=Colors.BLUE_GREY_900, color=Colors.WHITE):
    """Mostra uma notificação na tela"""
    snack = ft.SnackBar(
        content=ft.Text(msg, color=color),
        bgcolor=bg,
        show_close_icon=True,
        behavior=ft.SnackBarBehavior.FLOATING,
    )
    page.overlay.append(snack)
    snack.open = True
    page.update()

def agendamento_view(page: ft.Page) -> ft.Column:
    """View principal de agendamento com calendário e horários"""
    page.bgcolor = "#546b7b"
    
    ensure_agendamentos_storage()
    
    # Estado da view
    data_selecionada = {"value": None}
    horario_selecionado = {"value": None}
    
    # Botão de voltar
    back_btn = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=Colors.WHITE,
        on_click=lambda _: page.go("/home"),
        style=ft.ButtonStyle(bgcolor=None, padding=10)
    )

    # Título
    title = ft.Text(
        "Agendar Horário",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=Colors.WHITE
    )

    # Container para exibir calendário
    calendario_container = ft.Column(spacing=10)
    
    # Container para exibir horários disponíveis
    horarios_container = ft.Column(spacing=10)
    
    # Label de data selecionada
    data_label = ft.Text(
        "Selecione uma data",
        size=14,
        color=Colors.BLUE_GREY_100,
        weight=ft.FontWeight.W_500
    )
    
    # Label de horário selecionado
    horario_label = ft.Text(
        "Selecione um horário",
        size=14,
        color=Colors.BLUE_GREY_100,
        weight=ft.FontWeight.W_500
    )

    # Label do serviço selecionado (vindo de servicos.py)
    service_label = ft.Text(
        f"Serviço: {page.session.get('selected_service') or 'Nenhum selecionado'}",
        size=14,
        color=Colors.BLUE_GREY_100,
        weight=ft.FontWeight.W_500,
    )

    # Resumo do agendamento (mostrado após seleção completa)
    resumo_data_text = ft.Text("Data: Selecione uma data", size=11, color=Colors.BLUE_GREY_100)
    resumo_horario_text = ft.Text("Horário: Selecione um horário", size=11, color=Colors.BLUE_GREY_100)
    resumo_servico_text = ft.Text(f"Serviço: {page.session.get('selected_service') or 'Nenhum'}", size=11, color=Colors.BLUE_GREY_100)
    
    resumo_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("RESUMO", size=12, weight=ft.FontWeight.BOLD, color=Colors.WHITE),
                ft.Divider(thickness=1, color=ft.Colors.WHITE24),
                resumo_data_text,
                resumo_horario_text,
                resumo_servico_text,
            ],
            spacing=3,
        ),
        padding=8,
        bgcolor=Colors.BLUE_GREY_700,
        border_radius=6,
        visible=False,
    )
    
    # referência para atualizar resumo
    resumo_texts = {
        "data": resumo_data_text,
        "horario": resumo_horario_text,
        "servico": resumo_servico_text,
    }

        # (removido campo de observações e seleção de serviço por solicitação)

    def gerar_calendario():
        """Gera o calendário do mês atual"""
        hoje = datetime.now()
        primeiro_dia = datetime(hoje.year, hoje.month, 1)
        month_title = primeiro_dia.strftime("%B %Y")
        
        # Encontrar o dia da semana do primeiro dia (0=segunda, 6=domingo)
        primeiro_dia_semana = primeiro_dia.weekday()
        
        # Calcular última data do mês
        if hoje.month == 12:
            ultimo_dia = datetime(hoje.year + 1, 1, 1) - timedelta(days=1)
        else:
            ultimo_dia = datetime(hoje.year, hoje.month + 1, 1) - timedelta(days=1)
        
        # Cabeçalho com nome do mês e dias da semana
        month_text = ft.Text(month_title, size=14, weight=ft.FontWeight.BOLD, color=Colors.WHITE)
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
        header_dias = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(dia, size=10, weight=ft.FontWeight.BOLD, color=Colors.WHITE),
                    width=38,
                    height=28,
                    alignment=ft.alignment.center
                )
                for dia in dias_semana
            ],
            spacing=3,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        # Criar linhas de dias
        linhas = [header_dias]
        semana_atual = []
        
        # Preencher espaços vazios antes do primeiro dia
        for _ in range(primeiro_dia_semana):
            semana_atual.append(ft.Container(width=40))
        
        # Preencher os dias do mês
        for dia in range(1, ultimo_dia.day + 1):
            data = datetime(hoje.year, hoje.month, dia)
            data_str = data.strftime("%d/%m/%Y")
            
            # Desabilitar datas passadas
            eh_passado = data < hoje.replace(hour=0, minute=0, second=0, microsecond=0)
            
            def criar_btn_dia(d, data_formatada):
                def selecionar_data(_):
                    data_selecionada["value"] = data_formatada
                    data_label.value = f"Data selecionada: {data_formatada}"
                    resumo_texts["data"].value = f"Data: {data_formatada}"
                    horario_selecionado["value"] = None
                    horario_label.value = "Selecione um horário"
                    atualizar_horarios()
                    # atualizar_resumo removed — update resumo inline when needed
                    resumo_container.visible = False
                    page.update()
                
                return ft.Container(
                    content=ft.Text(
                        str(d),
                        size=10,
                        color=Colors.WHITE if not eh_passado else Colors.BLUE_GREY_400,
                        weight=ft.FontWeight.BOLD
                    ),
                    width=38,
                    height=38,
                    bgcolor=Colors.BLUE_600 if not eh_passado else Colors.BLUE_GREY_700,
                    border_radius=6,
                    alignment=ft.alignment.center,
                    on_click=selecionar_data if not eh_passado else None,
                    opacity=1.0 if not eh_passado else 0.5
                )
            
            btn = criar_btn_dia(dia, data_str)
            semana_atual.append(btn)
            
            # Quando completar uma semana, adicionar à linha
            if len(semana_atual) == 7:
                linhas.append(ft.Row(
                    controls=semana_atual,
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER
                ))
                semana_atual = []
        
        # Preencher espaços vazios da última semana
        while len(semana_atual) < 7:
            semana_atual.append(ft.Container(width=40))
        if semana_atual:
            linhas.append(ft.Row(
                controls=semana_atual,
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER
            ))
        
        # incluir o título do mês acima das linhas
        controls = [month_text, header_dias] + linhas[1:]
        return ft.Column(
            controls=controls,
            spacing=3,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def atualizar_horarios():
        """Atualiza a lista de horários disponíveis"""
        horarios_container.clean()
        
        if not data_selecionada["value"]:
            horarios_container.controls.append(
                ft.Text("Selecione uma data primeiro", color=Colors.AMBER_600)
            )
            return
        
        horarios_disponiveis = get_horarios_disponiveis_dia(data_selecionada["value"])
        
        if not horarios_disponiveis:
            horarios_container.controls.append(
                ft.Text("Nenhum horário disponível nesta data", color=Colors.AMBER_600)
            )
            return
        
        # Criar grade de horários
        grid_horarios = []
        linha_atual = []
        
        for horario in horarios_disponiveis:
            def criar_btn_horario(h):
                def selecionar_horario(_):
                    horario_selecionado["value"] = h
                    horario_label.value = f"Horário selecionado: {h}"
                    # atualizar resumo com horário e serviço selecionado
                    resumo_texts["horario"].value = f"Horário: {h}"
                    resumo_texts["servico"].value = f"Serviço: {page.session.get('selected_service') or 'Nenhum'}"
                    resumo_container.visible = True
                    page.update()
                
                return ft.Container(
                    content=ft.Text(
                        h,
                        size=11,
                        color=Colors.WHITE,
                        weight=ft.FontWeight.BOLD
                    ),
                    width=60,
                    height=38,
                    bgcolor=Colors.GREEN_600,
                    border_radius=6,
                    alignment=ft.alignment.center,
                    on_click=selecionar_horario
                )
            
            btn = criar_btn_horario(horario)
            linha_atual.append(btn)
            
            if len(linha_atual) == 4:
                grid_horarios.append(ft.Row(
                    controls=linha_atual,
                    spacing=4,
                    alignment=ft.MainAxisAlignment.CENTER
                ))
                linha_atual = []
        
        if linha_atual:
            grid_horarios.append(ft.Row(
                controls=linha_atual,
                spacing=4,
                alignment=ft.MainAxisAlignment.CENTER
            ))
        
        horarios_container.controls.extend(grid_horarios)

    def confirmar_agendamento(_):
        """Confirma e salva o agendamento"""
        if not data_selecionada["value"]:
            snackbar(page, "Selecione uma data", bg=Colors.RED_400)
            return
        if not horario_selecionado["value"]:
            snackbar(page, "Selecione um horário", bg=Colors.RED_400)
            return
        # pegar serviço selecionado (se houver)
        selected_servico = page.session.get("selected_service") or ""
        
        usuario = page.session.get("user") or page.client_storage.get("logged_user") or "usuário"
        
        agendamentos = load_agendamentos()
        novo_agendamento = {
            "usuario": usuario,
            "data": data_selecionada["value"],
            "horario": horario_selecionado["value"],
            "servico": selected_servico,
            "observacoes": "",
            "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        agendamentos.append(novo_agendamento)
        save_agendamentos(agendamentos)
        
        snackbar(page, "Agendamento confirmado com sucesso!", bg=Colors.GREEN_500)
        
        # Resetar formulário
        data_selecionada["value"] = None
        horario_selecionado["value"] = None
        data_label.value = "Selecione uma data"
        horario_label.value = "Selecione um horário"
        # manter seleção de serviço em sessão ou limpar se desejar
        # page.session.remove("selected_service")
        horarios_container.clean()
        
        # atualizar UI e retornar para a tela principal
        page.go("/home")
        page.update()

    # Botão de confirmar
    btn_confirmar = ft.ElevatedButton(
        "Confirmar Agendamento",
        on_click=confirmar_agendamento,
        style=ft.ButtonStyle(
            color=Colors.WHITE,
            bgcolor=Colors.GREEN_600,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=7),
        ),
        width=250
    )

    # Gerar calendário inicial
    calendario = gerar_calendario()
    calendario_container.controls.append(calendario)

    # Formulário principal com scroll
    form = ft.Column(
        controls=[
            title,
            ft.Divider(thickness=2, color=ft.Colors.WHITE24),
            ft.Text("CALENDÁRIO", size=12, weight=ft.FontWeight.BOLD, color=Colors.BLUE_GREY_100),
            calendario_container,
            ft.Container(height=5),
            data_label,
            ft.Divider(thickness=1, color=ft.Colors.WHITE24),
            ft.Text("HORÁRIOS", size=12, weight=ft.FontWeight.BOLD, color=Colors.BLUE_GREY_100),
            horarios_container,
            ft.Container(height=5),
            horario_label,
            ft.Divider(thickness=1, color=ft.Colors.WHITE24),
            ft.Container(height=8),
            btn_confirmar,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=4,
    )

    # Card com scroll
    card = ft.Container(
        content=ft.Column(
            controls=[form],
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=12,
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
                controls=[
                    ft.Container(
                        width=340,
                        padding=10,
                        content=card,
                        alignment=ft.alignment.center,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ],
        spacing=10,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return root
