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

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Rich](https://img.shields.io/badge/Rich-TUI-00e5b0?style=flat-square)](https://github.com/Textualize/rich)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Lisboa14-181717?style=flat-square&logo=github)](https://github.com/Lisboa14/FinanceGestor)

</div>

---

## ✦ O que é o FinanceGestor?

O **FinanceGestor** é uma aplicação de terminal (TUI) para gestão financeira pessoal, construída em Python com uma interface powered by [Rich](https://github.com/Textualize/rich). Regista despesas, define orçamentos mensais, acompanha poupanças, define metas de poupança, visualiza gráficos e faz perguntas em linguagem natural sobre as tuas finanças — tudo sem sair do terminal.

---

## ✦ Funcionalidades

| Módulo | Funcionalidades |
|---|---|
| 💸 **Despesas** | Adicionar, editar, remover e filtrar por categoria, mês ou data. Categorização automática por palavras-chave com aprendizagem |
| 📊 **Orçamento** | Definir orçamento mensal com validações, ver histórico de todos os meses e acompanhar o progresso |
| 🏦 **Poupanças** | Cálculo automático acumulado mês a mês com base no orçamento e gastos reais |
| 🎯 **Metas** | Criar metas de poupança com prazo, acompanhar progresso com barra visual, alertas de risco e conclusão automática |
| 📈 **Gráficos** | Gráfico por categorias circulares e por intervalo de datas com `matplotlib` |
| 💬 **Modo Conversa** | Perguntas em linguagem natural — "quanto gastei este mês?", "onde gasto mais?", "como estão as metas?" |
| 🖥️ **Dashboard** | Cards com orçamento, gastos, poupanças e metas ativas |

---

## ✦ Preview

```
──────────────────────────────────────────────────────────────────────
◈ FINANCEGESTOR                    Monday, 13 de April de 2026  09:31
──────────────────────────────────────────────────────────────────────

  ╭─────────────╮  ╭─────────────╮  ╭─────────────╮  ╭─────────────╮
  │ ORÇAMENTO   │  │ GASTO       │  │ DISPONÍVEL  │  │ POUPANÇAS   │
  │ 1.500,00 €  │  │ 430,50      │  │ 1.069,50 €  │  │ 2.134,20 €  │
  ╰─────────────╯  ╰─────────────╯  ╰─────────────╯  ╰─────────────╯

  METAS ATIVAS
  ╭──────────────────╮  ╭──────────────────╮
  │ Viagem Londres   │  │ Portátil novo    │
  │ ████████░░░░     │  │ ███░░░░░░░░      │
  │ 340€ / 800€ 42%  │  │ 180€ / 1000€ 18% │
  │ Prazo: 2025-08   │  │ Prazo: 2025-12   │
  ╰──────────────────╯  ╰──────────────────╯

  ╭──────────────────────────────────Menu Principal───────────────────────────────╮
  │                              [1] → Adicionar despesa                          │
  │                              [2] → Ver despesas                               │
  │                              [3] → Gráficos                                   │
  │                              [4] → Definir orçamento                          │
  │                              [5] → Ver orçamento mensal                       │
  │                              [6] → Modo Conversa                              │
  │                              [7] → Metas de poupança                          │
  │                              [0] → Sair                                       │
  ╰───────────────────────────────────────────────────────────────────────────────╯
```

---

## ✦ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|---|---|---|
| [Python](https://www.python.org/) | 3.10+ | Linguagem principal |
| [MySQL](https://www.mysql.com/) | 8.0+ | Base de dados relacional |
| [mysql-connector-python](https://pypi.org/project/mysql-connector-python/) | 8.0+ | Ligação Python ↔ MySQL |
| [Rich](https://github.com/Textualize/rich) | 13.0+ | Interface TUI (tabelas, painéis, cores, prompts) |
| [Matplotlib](https://matplotlib.org/) | 3.5+ | Gráficos de visualização |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | 1.0+ | Gestão de variáveis de ambiente (.env) |

---

## ✦ Pré-requisitos

Antes de instalar, garante que tens:

- **Python 3.10+** → [download](https://www.python.org/downloads/)
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

### 2 — Instalar dependências

```bash
pip install mysql-connector-python rich matplotlib python-dotenv
```


### 3 — Configurar variáveis de ambiente

O projeto usa um ficheiro `.env` para guardar as credenciais da base de dados. Cria o ficheiro `.env` na raiz do projeto com base no `.env.example`:

```bash
cp .env.example .env
```

Abre o `.env` e preenche com as tuas credenciais:

```env
DB_HOST=127.0.0.1
DB_PORT=...
DB_USER=root
DB_PASSWORD=a_tua_password
DB_NAME=financegestor
```

### 4 — Configurar a base de dados MySQL

Abre o teu cliente MySQL (Workbench, TablePlus, terminal, etc.) e executa o ficheiro SQL incluído no projeto:

```bash
mysql -u root -p < DataBase.sql
```

Ou copia e executa o conteúdo de `DataBase.sql` manualmente. O script cria a base de dados, todas as tabelas e insere categorias iniciais (Alimentação, Transporte, Habitação, Saúde).

As tabelas criadas são as seguintes:

```
categorias    — categorias de despesas
despesas      — registo de todas as despesas
orcamento     — orçamentos mensais
poupancas     — poupanças acumuladas mês a mês
metas         — metas de poupança com prazo e progresso
palavra_chave — aprendizagem de categorização automática
```

### 5 — Executar a aplicação

```bash
cd src
python main.py
```

---

## ✦ Utilização

### Menu principal

Navega com os números do teclado:

```
[1] Adicionar despesa     → valor, descrição e categoria (com sugestão automática)
[2] Ver despesas          → todas / por categoria / por mês / por data / editar / remover
[3] Gráficos              → por categoria ou por intervalo de datas
[4] Definir orçamento     → orçamento mensal com validação de formato e data
[5] Ver orçamento mensal  → histórico de todos os orçamentos com estado
[6] Modo Conversa         → perguntas em linguagem natural
[7] Metas de poupança     → criar, ver progresso, concluir metas
[0] Sair
```

### Categorização automática

Ao adicionar uma despesa, o programa sugere automaticamente a categoria com base na descrição:

```
Valor (€): 9.99
Descrição: Netflix

  🪄 Sugestão automática: [Subscrições]
  Aceitar? (Enter para confirmar, 'n' para escolher outra):
```

O sistema aprende com as tuas escolhas e melhora com o uso.

### Modo Conversa

Acede ao modo conversa com a opção `[6]` e faz perguntas em português:

```
› quanto gastei este mês?
› quanto gastei em alimentação?
› qual foi o maior gasto?
› estou dentro do orçamento?
› média em transportes
› qual o mês mais caro?
› onde gasto mais?
› quantas despesas tenho?
› último gasto
› total do ano
› quanto poupei?
› como estão as metas?
› quanto falta para a meta viagem?
› metas em risco
› ajuda
```

---

## ✦ Estrutura do Projeto

```
FinanceGestor/
├── src/
│   ├── main.py          — ponto de entrada, dashboard e menus
│   ├── despesas.py      — gestão de despesas e categorização automática
│   ├── orcamento.py     — orçamentos mensais com validações
│   ├── poupancas.py     — cálculo de poupanças acumuladas
│   ├── metas.py         — metas de poupança com progresso e alertas
│   ├── graficos.py      — gráficos com matplotlib
│   ├── conversa.py      — modo conversa em linguagem natural
│   └── db.py            — ligação à base de dados (lê do .env)
├── DataBase.sql         — script SQL para criar a base de dados
├── .env                 — credenciais locais (não vai para o GitHub)
├── .gitignore
├── LICENSE
└── README.md
```

---

## ✦ Dependências — Referência Completa

| Pacote | Versão mínima | Instalação | Uso |
|---|---|---|---|
| `mysql-connector-python` | 8.0+ | pip | Ligação à base de dados MySQL |
| `rich` | 13.0+ | pip | Interface TUI (tabelas, painéis, cores) |
| `matplotlib` | 3.5+ | pip | Gráficos de visualização |
| `python-dotenv` | 1.0+ | pip | Leitura do ficheiro `.env` |
| `re` | stdlib | — | Expressões regulares (categorização e validação) |
| `unicodedata` | stdlib | — | Normalização de texto (remoção de acentos) |
| `datetime` | stdlib | — | Datas e formatação de meses |
| `os` | stdlib | — | Limpeza do terminal e caminhos de ficheiros |

Instalar todos os pacotes externos de uma vez:

```bash
pip install mysql-connector-python rich matplotlib python-dotenv reportlab
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

- [x] Registo e filtragem de despesas
- [x] Orçamentos mensais com validação
- [x] Poupanças acumuladas automáticas
- [x] Categorização automática com aprendizagem
- [x] Modo conversa em linguagem natural
- [x] Metas de poupança com progresso e alertas
- [x] Gráficos por categoria e por intervalo
---

## ✦ Licença

Distribuído sob a licença **MIT**. Consulta o ficheiro [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">

Feito por **[Lisboa14](https://github.com/Lisboa14)**

⭐ Se achaste útil, deixa uma estrela no repositório!

</div>
