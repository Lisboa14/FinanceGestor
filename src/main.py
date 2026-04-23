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
    ver_despesas_categoria, ver_despesas_mes, ver_despesas_data, remover_despesa, editar_despesa,
)
from graficos import grafico_categorias, grafico_intervalo
from orcamento import definir_orcamento, ver_orcamento, orcamento_dashboard
from poupancas import poupancas
from conversa import interpretar
from metas import (
    criar_meta, ver_metas,remover_meta,editar_meta,
    concluir_meta, painel_metas_dashboard, verificar_metas_risco,
)
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
    mes = datetime.now().strftime("%Y-%m")
    gasto = float(total_despesas() or 0)
    
    orcamento_val = gasto + restante  # orçamento = gasto + restante
    cofre = poupancas(mes, orcamento_val , gasto)
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
    
    t4 = Text()
    t4.append("Poupanças\n", style=f"dim {DIM}")
    t4.append(f"{cofre:,.2f} €", style=f"bold {cor_rest}")

    cards = [
        Panel(t1, border_style=DIM, box=box.ROUNDED, padding=(0, 1), width=22),
        Panel(t2, border_style=DIM, box=box.ROUNDED, padding=(0, 1), width=22),
        Panel(t3, border_style=DIM, box=box.ROUNDED, padding=(0, 1), width=22),
        Panel(t4, border_style=DIM, box=box.ROUNDED, padding=(0, 1), width=22),
    ]
    console.print(Padding(Columns(cards, equal=False, expand=False, padding=(0, 0)), (1, 2)))
# ── Painel de metas
    metas_ativas = painel_metas_dashboard()
    if metas_ativas:
        console.print(Padding(Text("  METAS ATIVAS", style=f"dim {DIM}"), (0, 2)))
        meta_cards = []
        for m in metas_ativas[:4]:
            barra_cheia = int(m["pct"] / 5)
            barra = "█" * barra_cheia + "░" * (20 - barra_cheia)
            cor   = ACCENT if m["pct"] >= 100 else WARN if m["pct"] >= 60 else TEXT
            t = Text()
            t.append(m["nome"][:18] + "\n", style=f"bold {TEXT}")
            t.append(barra[:12] + "\n",     style=f"{cor}")
            t.append(f"{m['poupancas']:.0f}€ / {m['valor_alvo']:.0f}€", style=f"dim {DIM}")
            t.append(f"({m['pct']:.0f}%)\n", style=f"bold {cor}")
            if m["prazo"]:
                t.append(f"Prazo: {m['prazo']}", style=f"dim {DIM}")
            else:
                t.append(f"Faltam {m['falta']:.2f}€", style=f"dim {DIM}")
            meta_cards.append(Panel(t, border_style=DIM, box=box.ROUNDED, padding=(0, 1), width=26))
        console.print(Padding(Columns(meta_cards, equal=False, expand=False, padding=(0, 0)), (0, 2)))
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
        ("3", "Gráficos"),
        ("4", "Definir orçamento"),
        ("5", "Ver orçamento mensal"),
        ("6", "Modo Conversa"),
        ("7", "Metas de poupancas"),
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
            ("5", "Remover despesa"),
            ("6", "Editar despesa"),
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
        elif escolha == "5":
            remover_despesa()
        elif escolha == "6":
            editar_despesa()
        elif escolha == "0":
            break
        else:
            console.print(f"\n  [{DANGER}]✗ Opção inválida.[/]\n")

        if escolha in ("1", "2", "3", "4"):
            console.print()
            Prompt.ask(f"  [{DIM}]prima Enter para continuar[/]", default="", console=console)

def menu_ver_graficos():
    while True:
        limpar_terminal()
        header()

        _render_menu("ver despesas", [
            ("1", "Por categoria"),
            ("2", "Intervalo"),
            ("0", "← Voltar"),
        ])

        escolha = Prompt.ask(f"  [{ACCENT}]›[/] escolha", console=console)
        limpar_terminal()

        if escolha == "1":
            grafico_categorias()
        elif escolha == "2":
            grafico_intervalo()
        elif escolha == "0":
            break
        else:
            console.print(f"\n  [{DANGER}]✗ Opção inválida.[/]\n")

        if escolha in ("1", "2"):
            console.print()
            Prompt.ask(f"  [{DIM}]prima Enter para continuar[/]", default="", console=console)

def menu_metas():
    while True:
        limpar_terminal()
        header()
        _render_menu("metas de poupança", [
            ("1", "Ver metas e progresso"),
            ("2", "Criar nova meta"),
            ("3", "Concluir meta"),
            ("4", "Remover meta"),
            ("5", "Editar meta"),
            ("0", "← Voltar"),
        ])

        escolha = Prompt.ask(f"  [{ACCENT}]›[/] escolha", console=console)
        limpar_terminal()

        if escolha == "0":
            break

        header()
        titulos = {
            "1": "metas de poupança",
            "2": "criar nova meta",
            "3": "concluir meta",
            "4": "remover_meta",
            "5": "editar_meta",
        }
        if escolha in titulos:
            console.print(Rule(f"[{DIM}]{titulos[escolha]}[/]", style=DIM))
            console.print()

        if escolha == "1":
            ver_metas()
        elif escolha == "2":
            criar_meta()
        elif escolha == "3":
            concluir_meta()
        elif escolha == "4":
            remover_meta()
        elif escolha == "5":
            editar_meta()
        else:
            console.print(f"\n  [{DANGER}]✗ Opção inválida.[/]\n")

        if escolha in titulos:
            _aguardar()
def modo_conversa():
    limpar_terminal()
    header()
    console.print(Rule(f"[{DIM}]modo conversa[/]", style=DIM))
    console.print()

    # Dica inicial
    dica = Text()
    dica.append("  💬 ", style=f"bold {ACCENT}")
    dica.append("Faz-me perguntas em português sobre as tuas finanças.\n", style=TEXT)
    dica.append("     Escreve ", style=f"dim {DIM}")
    dica.append("'ajuda'", style=f"bold {ACCENT}")
    dica.append(" para ver exemplos  |  ", style=f"dim {DIM}")
    dica.append("'sair'", style=f"bold {DANGER}")
    dica.append(" para voltar ao menu.", style=f"dim {DIM}")
    console.print(Padding(dica, (0, 2)))
    console.print()

    historico = []  # guarda as últimas interações para contexto visual

    while True:
        try:
            pergunta = Prompt.ask(
                f"  [{ACCENT}]›[/]",
                console=console
            ).strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not pergunta:
            continue

        if pergunta.lower() in ("sair", "voltar", "exit", "quit"):
            break

        # Processa e mostra resposta
        resposta = interpretar(pergunta)

        console.print()

        # Pergunta em cinzento
        console.print(Padding(
            Text(f"  {pergunta}", style=f"dim {DIM}"),
            (0, 2)
        ))

        # Resposta em painel estilizado
        resp_text = Text()
        for linha in resposta.split("\n"):
            resp_text.append(f"{linha}\n", style=TEXT)

        console.print(Padding(
            Panel(
                resp_text,
                border_style=ACCENT,
                box=box.ROUNDED,
                padding=(0, 2),
            ),
            (0, 4)
        ))
        console.print()

        historico.append((pergunta, resposta))
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
            menu_ver_graficos()

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
        elif escolha == "6":
            modo_conversa()
        elif escolha == "7":
            menu_metas()
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
