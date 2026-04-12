import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.rule import Rule
from rich.prompt import Prompt
from rich.align import Align
from rich import box
from rich.padding import Padding

# ─── importa os teus módulos ───────────────────────────────────────────────
from despesas import (
    add_despesa, ver_despesas, total_despesas,
    ver_despesas_categoria, ver_despesas_mes, ver_despesas_data,
)
from graficos import grafico_categorias
from orcamento import definir_orcamento, ver_orcamento, orcamento_dashboard

# ──────────────────────────────────────────────────────────────────────────
console = Console()

ACCENT  = "#00e5b0"
DIM     = "#6b6a65"
DANGER  = "#ff4f4f"
WARN    = "#f5a623"
TEXT    = "#e8e6e0"


# ─── UTILITÁRIOS ──────────────────────────────────────────────────────────

def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    agora = datetime.now()
    data_str = agora.strftime("%A, %d de %B de %Y  %H:%M")

    titulo = Text()
    titulo.append("◈ ", style=f"bold {ACCENT}")
    titulo.append("FINANCE", style=f"bold {TEXT}")
    titulo.append("GESTOR", style=f"bold {ACCENT}")

    console.print()
    console.print(Rule(style=f"dim {DIM}"))
    console.print(Padding(titulo, (0, 2)), end="")
    console.print(Align(Text(data_str, style=f"dim {DIM}"), align="right"))
    console.print(Rule(style=f"dim {DIM}"))


def painel_orcamento():
    restante = orcamento_dashboard()

    if restante is None:
        # Sem orçamento definido — mostra aviso simples
        aviso = Text()
        aviso.append("  ⚠  ", style=f"bold {WARN}")
        aviso.append("Sem orçamento definido para este mês. ", style=f"{WARN}")
        aviso.append("Usa a opção ", style=f"dim {DIM}")
        aviso.append("[4]", style=f"bold {ACCENT}")
        aviso.append(" para definir.", style=f"dim {DIM}")
        console.print(Padding(aviso, (1, 2)))
        console.print()
        return

    restante = float(restante)

    # Usamos total_despesas() para o gasto e inferimos o orçamento total.
    gasto = float(total_despesas() or 0)
    

    orcamento_val = gasto + restante  # orçamento = gasto + restante
    # Cor do restante
    if restante < 0:
        cor_rest = DANGER
    elif orcamento_val > 0 and restante < orcamento_val * 0.30:
        cor_rest = WARN
    else:
        cor_rest = ACCENT

    # ── Três cards ──────────────────────────────────────────────────────
    t1 = Text()
    t1.append("ORÇAMENTO\n", style=f"dim {DIM}")
    t1.append(f"{orcamento_val:,.2f} €", style=f"bold {TEXT}")

    t2 = Text()
    t2.append("GASTO\n", style=f"dim {DIM}")
    t2.append(f"{gasto:,.2f}",style=f"bold {WARN}")

    t3 = Text()
    t3.append("DISPONÍVEL\n", style=f"dim {DIM}")
    t3.append(f"{restante:,.2f} €", style=f"bold {cor_rest}")

    cards = [
        Panel(t1, border_style=DIM, box=box.ROUNDED, padding=(0, 2)),
        Panel(t2, border_style=DIM, box=box.ROUNDED, padding=(0, 2)),
        Panel(t3, border_style=DIM, box=box.ROUNDED, padding=(0, 2)),
    ]
    console.print(Padding(Columns(cards, equal=True, expand=True), (1, 2)))

# ─── MENUS ────────────────────────────────────────────────────────────────

def _render_menu(titulo_painel: str, itens: list):
    """Renderiza um menu genérico numa tabela estilizada."""
    tabela = Table(show_header=False, box=None, padding=(0, 2))
    tabela.add_column("kbd",   style="bold", width=4)
    tabela.add_column("seta",  style=DIM,    width=2)
    tabela.add_column("label", style=TEXT)

    for key, label in itens:
        cor_key = DANGER if key == "0" else ACCENT
        tabela.add_row(f"[{cor_key}][{key}][/]", "→", label)

    console.print(Padding(
        Panel(
            Align(tabela, align="center"),
            title=f"[{DIM}]{titulo_painel}[/]",
            border_style=DIM,
            box=box.ROUNDED,
            padding=(1, 4),
        ),
        (0, 2),
    ))
    console.print()


def menu_principal():
    _render_menu("Menu Principal", [
        ("1", "Adicionar despesa"),
        ("2", "Ver despesas"),
        ("3", "Gráficos por categoria"),
        ("4", "Definir orçamento"),
        ("5", "Ver orçamento mensal"),
        ("0", "Sair"),
    ])


def menu_ver_despesas():
    while True:
        limpar_terminal()
        header()

        _render_menu("ver despesas", [
            ("1", "Ver todas"),
            ("2", "Por categoria"),
            ("3", "Por mês"),
            ("4", "Por data específica"),
            ("0", "← Voltar"),
        ])

        escolha = Prompt.ask(f"  [{ACCENT}]›[/] escolha", console=console)
        limpar_terminal()

        if escolha == "1":
            ver_despesas()
        elif escolha == "2":
            ver_despesas_categoria()
        elif escolha == "3":
            ver_despesas_mes()
        elif escolha == "4":
            ver_despesas_data()
        elif escolha == "0":
            break
        else:
            console.print(f"\n  [{DANGER}]✗ Opção inválida.[/]\n")

        if escolha in ("1", "2", "3", "4"):
            console.print()
            Prompt.ask(f"  [{DIM}]prima Enter para continuar[/]", default="", console=console)


# ─── LOOP PRINCIPAL ───────────────────────────────────────────────────────

def _aguardar():
    console.print()
    Prompt.ask(f"  [{DIM}]prima Enter para continuar[/]", default="", console=console)


def main():
    while True:
        limpar_terminal()
        header()
        painel_orcamento()
        menu_principal()

        escolha = Prompt.ask(f"  [{ACCENT}]›[/] escolha", console=console)
        limpar_terminal()

        if escolha == "1":
            header()
            console.print(Rule(f"[{DIM}]adicionar despesa[/]", style=DIM))
            console.print()
            add_despesa()
            _aguardar()

        elif escolha == "2":
            menu_ver_despesas()

        elif escolha == "3":
            header()
            console.print(Rule(f"[{DIM}]gráficos por categoria[/]", style=DIM))
            console.print()
            grafico_categorias()
            _aguardar()

        elif escolha == "4":
            header()
            console.print(Rule(f"[{DIM}]definir orçamento[/]", style=DIM))
            console.print()
            definir_orcamento()
            _aguardar()

        elif escolha == "5":
            header()
            console.print(Rule(f"[{DIM}]orçamento mensal[/]", style=DIM))
            console.print()
            ver_orcamento()
            _aguardar()

        elif escolha == "0":
            limpar_terminal()
            msg = Text()
            msg.append("\n  ◈ ", style=f"bold {ACCENT}")
            msg.append("Obrigado por usar o ", style=TEXT)
            msg.append("FinanceGestor", style=f"bold {ACCENT}")
            msg.append(".\n", style=TEXT)
            console.print(msg)
            console.print(Rule(style=f"dim {DIM}"))
            console.print()
            break

        else:
            console.print(f"\n  [{DANGER}]✗ Opção inválida. Tenta novamente.[/]\n")
            _aguardar()


if __name__ == "__main__":
    main()
