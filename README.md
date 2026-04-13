<div align="center">

```
███████╗██╗███╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████╗
██╔════╝██║████╗  ██║██╔══██╗████╗  ██║██╔════╝██╔════╝
█████╗  ██║██╔██╗ ██║███████║██╔██╗ ██║██║     █████╗  
██╔══╝  ██║██║╚██╗██║██╔══██║██║╚██╗██║██║     ██╔══╝  
██║     ██║██║ ╚████║██║  ██║██║ ╚████║╚██████╗███████╗
╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝
                     G E S T O R
```

**Gestão financeira pessoal direto no teu terminal.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Rich](https://img.shields.io/badge/Rich-TUI-00e5b0?style=flat-square)](https://github.com/Textualize/rich)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Lisboa14-181717?style=flat-square&logo=github)](https://github.com/Lisboa14/FinanceGestor)

</div>

---

## ✦ O que é o FinanceGestor?

O **FinanceGestor** é uma aplicação de terminal (TUI) para gestão financeira pessoal, construída em Python com uma interface elegante powered by [Rich](https://github.com/Textualize/rich). Regista despesas, define orçamentos mensais, acompanha as tuas poupanças e visualiza os teus gastos por categoria — tudo sem sair do terminal.

---

## ✦ Funcionalidades

| Módulo | Funcionalidade |
|---|---|
| 💸 **Despesas** | Adicionar, listar, filtrar por categoria, mês ou data |
| 📊 **Orçamento** | Definir orçamento mensal e acompanhar o progresso |
| 🏦 **Poupanças** | Cálculo automático acumulado mês a mês |
| 🍩 **Gráficos** | Gráfico de pizza por categorias com `matplotlib` |
| 🖥️ **Dashboard** | Cards em tempo real com orçamento, gastos e poupanças |

---

## ✦ Preview

```
──────────────────────────────────────────────────────────────
◈ FINANCEGÉSTOR                  Monday, 13 de April de 2026  09:31
──────────────────────────────────────────────────────────────

  ╭─────────────╮  ╭─────────────╮  ╭─────────────╮  ╭─────────────╮
  │ ORÇAMENTO   │  │ GASTO       │  │ DISPONÍVEL  │  │ Poupanças   │
  │ 1.500,00 €  │  │ 430,50      │  │ 1.069,50 €  │  │ 2.134,20 €  │
  ╰─────────────╯  ╰─────────────╯  ╰─────────────╯  ╰─────────────╯

  ╭──── Menu Principal ─────╮
  │  [1] → Adicionar despesa│
  │  [2] → Ver despesas     │
  │  [3] → Gráficos         │
  │  [4] → Definir orçamento│
  │  [5] → Ver orçamento    │
  │  [0] → Sair             │
  ╰─────────────────────────╯
```

---

## ✦ Tecnologias Utilizadas

- **[Python 3.8+](https://www.python.org/)** — Linguagem principal
- **[MySQL](https://www.mysql.com/)** — Base de dados relacional
- **[mysql-connector-python](https://pypi.org/project/mysql-connector-python/)** — Connector Python ↔ MySQL
- **[Rich](https://github.com/Textualize/rich)** — Interface TUI (tabelas, painéis, cores, prompts)
- **[Matplotlib](https://matplotlib.org/)** — Visualização de dados (gráfico de pizza)

---
---

## ✦ Pré-requisitos

Antes de instalar, garante que tens:

- **Python 3.8+** → [download](https://www.python.org/downloads/)
- **MySQL 8.0+** → [download](https://dev.mysql.com/downloads/) ou via MAMP/XAMPP
- **pip** (incluído com Python)
- **Git** → [download](https://git-scm.com/)

---

## ✦ Instalação Passo a Passo

### 1 — Clonar o repositório

```bash
git clone https://github.com/Lisboa14/FinanceGestor.git
cd FinanceGestor
```

### 2 — Criar ambiente virtual (recomendado)

```bash
# Criar
python -m venv venv

# Ativar — Windows
venv\Scripts\activate

# Ativar — macOS / Linux
source venv/bin/activate
```

### 3 — Instalar dependências

```bash
pip install mysql-connector-python rich matplotlib
```

```bash
```

### 4 — Configurar a base de dados MySQL

Abre o teu cliente MySQL (Workbench, TablePlus, terminal, etc.) e executa:

```sql
CREATE DATABASE financegestor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE financegestor;

CREATE TABLE categorias (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE despesas (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    data         DATE         NOT NULL,
    categoria_id INT          NOT NULL,
    descricao    VARCHAR(255),
    valor        DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE orcamento (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    mes   VARCHAR(7)    NOT NULL UNIQUE,  -- formato: YYYY-MM
    valor DECIMAL(10,2) NOT NULL
);

CREATE TABLE poupancas (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    mes   VARCHAR(7)    NOT NULL UNIQUE,  -- formato: YYYY-MM
    valor DECIMAL(10,2) NOT NULL
);
```

### 5 — Configurar a ligação à base de dados

Abre `db.py` e ajusta as credenciais conforme o teu ambiente:

```python
# db.py
def get_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",   # ou "localhost"
        port=3306,           # porta padrão MySQL (MAMP usa 8889)
        user="root",         # teu utilizador MySQL
        password="root",     # a tua password MySQL
        database="financegestor"
    )
    return conn
```

> **Nota MAMP:** se usas MAMP no macOS, a porta por defeito é `8889`. Ajusta conforme necessário.

### 6 — Executar a aplicação

```bash
python main.py
```

---

## ✦ Utilização Rápida

Após iniciar, navega pelo menu com os números do teclado:

```
[1] Adicionar despesa   → introduz valor, categoria e descrição
[2] Ver despesas        → filtra por todas / categoria / mês / data
[3] Gráficos            → gráfico de pizza por categorias (abre janela)
[4] Definir orçamento   → define o orçamento do mês atual (formato YYYY-MM)
[5] Ver orçamento       → mostra orçamento, gastos e saldo do mês
[0] Sair
```

O **dashboard no topo** atualiza automaticamente a cada vez que abres o menu principal, mostrando:

- 💰 Orçamento total do mês
- 📉 Total gasto até agora
- ✅ Valor disponível restante
- 🏦 Poupanças acumuladas

---

## ✦ Dependências — Referência Completa

| Pacote | Versão mínima | Uso |
|---|---|---|
| `mysql-connector-python` | 8.0+ | Ligação à base de dados MySQL |
| `rich` | 13.0+ | Interface TUI (tabelas, painéis, cores) |
| `matplotlib` | 3.5+ | Gráficos de visualização |
| `datetime` | stdlib | Datas e formatação de meses |
| `os` | stdlib | Limpeza do terminal |

Instalar tudo de uma vez:

```bash
pip install mysql-connector-python rich matplotlib
```

---

## ✦ Contribuir

Contribuições são bem-vindas! Para contribuir:

```bash
# 1. Faz fork do repositório
# 2. Cria a tua branch
git checkout -b feature/nova-funcionalidade

# 3. Faz commit das alterações
git commit -m "feat: adiciona nova funcionalidade"

# 4. Push
git push origin feature/nova-funcionalidade

# 5. Abre um Pull Request no GitHub
```

---

## ✦ Roadmap

- [ ] Exportação de relatórios em PDF/CSV
- [ ] Notificações quando o orçamento está quase esgotado
- [ ] Gráfico de evolução das poupanças ao longo dos meses

---

## ✦ Licença

Distribuído sob a licença **MIT**. Consulta o ficheiro [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">

Feito por **[Lisboa14](https://github.com/Lisboa14)**

⭐ Se achaste útil, deixa uma estrela no repositório!

</div>
