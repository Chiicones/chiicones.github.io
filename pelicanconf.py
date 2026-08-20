#!/usr/bin/env python
# pelicanconf.py

AUTHOR   = 'Francisco'
SITENAME = 'Agenda DF'
SITEURL  = 'https://chiicones.github.io/'

# ── Conteúdo ──────────────────────────────────────────────────────────────────
# O Pelican lê todos os .md dentro de content/ recursivamente,
# incluindo subpastas por estabelecimento (brasilia/birosca/, etc.)
PATH              = 'content'
USE_FOLDER_AS_CATEGORY = False   # não usa o nome da pasta como categoria
                                  # (a categoria vem do campo Category: no .md)

THEME = 'pelican-theme'

# ── Localização ───────────────────────────────────────────────────────────────
TIMEZONE            = 'America/Sao_Paulo'
DEFAULT_LANG        = 'pt'
DEFAULT_DATE_FORMAT = '%d/%m/%Y'

# ── Feeds (desativados em desenvolvimento) ────────────────────────────────────
FEED_ALL_ATOM      = None
CATEGORY_FEED_ATOM = None

# ── Navegação ─────────────────────────────────────────────────────────────────
DISPLAY_CATEGORIES_ON_MENU = False   # categorias demais poluem o menu
MENUITEMS = [
    ('Eventos',  '/'),
    ('Agenda',   '/agenda.html'),
    ('Mapa',     '/mapa.html'),
    ('Busca',    '/pages/busca.html'),
    ('Blog',     '/blog.html'),
    ('Sobre',    '/pages/sobre.html'),
]

# ── Hero da home ──────────────────────────────────────────────────────────────
HERO_EYEBROW   = 'Próximos Eventos'
HERO_TITLE     = 'Seu Site de Eventos'
HERO_SUBTITLE  = 'A programação cultural de Brasília em um só lugar.'

# ── Metadados extras dos artigos ──────────────────────────────────────────────
# Esses campos são lidos do cabeçalho dos .md e ficam disponíveis nos templates
EXTRA_PATH_METADATA = {}
# Instrui o Pelican a não reclamar de campos desconhecidos
# (necessário para Local, Data, Horario, Entrada)

# ── URLs ──────────────────────────────────────────────────────────────────────
ARTICLE_URL     = 'eventos/{slug}.html'
ARTICLE_SAVE_AS = 'eventos/{slug}.html'

CATEGORY_URL     = 'categoria/{slug}.html'
CATEGORY_SAVE_AS = 'categoria/{slug}.html'

TAG_URL     = 'tag/{slug}.html'
TAG_SAVE_AS = 'tag/{slug}.html'

PAGE_URL     = 'pages/{slug}.html'
PAGE_SAVE_AS = 'pages/{slug}.html'

SLUGIFY_SOURCE = 'title'

# ── Agenda (índice cronológico) ───────────────────────────────────────────────
DIRECT_TEMPLATES = ['index', 'archives', 'mapa', 'blog']
ARCHIVES_SAVE_AS = 'agenda.html'
MAPA_SAVE_AS     = 'mapa.html'
BLOG_SAVE_AS     = 'blog.html'

# ── Paginação ─────────────────────────────────────────────────────────────────
DEFAULT_PAGINATION = 12

# ── Arquivos estáticos ────────────────────────────────────────────────────────
STATIC_PATHS = ['images', 'extra']

# ── Ignorar rascunhos ─────────────────────────────────────────────────────────
# Arquivos com Status: rascunho não são publicados
DEFAULT_STATUS = 'published'

# ── Slugify com suporte a caracteres especiais ────────────────────────────────
# Evita slugs quebrados com ª, º, acentos etc.
SLUGIFY_SOURCE = 'title'

from datetime import datetime
import pytz
JINJA_GLOBALS = {'now': datetime.now(pytz.timezone('America/Sao_Paulo'))}

import sys
sys.path.insert(0, 'plugins')
PLUGINS = ['search_index']