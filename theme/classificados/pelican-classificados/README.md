# Classificados — Tema Pelican para Eventos

Tema editorial estilo classificados de jornal para o [Pelican Static Site Generator](https://getpelican.com/).

## Instalação

```bash
# 1. Instale o Pelican
pip install pelican markdown

# 2. Copie a pasta do tema para seu projeto
cp -r themes/classificados /seu-projeto/themes/

# 3. No pelicanconf.py, configure:
THEME = 'themes/classificados'
```

## Estrutura do Tema

```
classificados/
├── templates/
│   ├── index.html       # Lista de eventos (grid de classificados)
│   ├── article.html     # Página completa do evento
│   ├── category.html    # Arquivo por categoria
│   └── tag.html         # Arquivo por tag/local
└── static/
    ├── css/style.css
    └── js/main.js
```

## Metadados do Evento

Nos arquivos `.md` de conteúdo, use os seguintes campos:

```markdown
Title: Nome do Evento
Date: 2025-06-15
Category: Música
Tags: jazz, ao vivo
Location: Teatro Municipal — São Paulo
Price: R$ 80,00
Event_date: 15/06/2025 · 20h
Organizer: Nome do Organizador
Contact: contato@evento.com.br

Descrição curta do evento (aparece no card dos classificados).

Texto completo do evento com todos os detalhes...
```

| Campo        | Exibido em            | Clicável? |
|-------------|----------------------|-----------|
| `Category`  | Badge no card e página | ✅ Filtra por categoria |
| `Location`  | Card e infobox        | ✅ Filtra por local (tag) |
| `Date`      | Card e dateline       | ✅ Filtra por data |
| `Price`     | Card e infobox        | ❌ |
| `Event_date`| Infobox da página     | ✅ |
| `Organizer` | Infobox da página     | ❌ |
| `Contact`   | Infobox da página     | ❌ |

## Personalização

No `pelicanconf.py`:

```python
SITENAME = 'Nome do Seu Site'
SITE_DESCRIPTION = 'Classificados de Eventos'
```

Cores e tipografia no `static/css/style.css` via variáveis CSS:

```css
:root {
  --ink: #1a1209;       /* cor principal do texto */
  --paper: #f5f0e8;     /* cor do fundo */
  --accent: #8b1a1a;    /* cor de destaque (categorias, links) */
  --gold: #b8860b;      /* cor do preço */
}
```
