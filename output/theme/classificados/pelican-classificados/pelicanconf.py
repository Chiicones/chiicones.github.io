#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Seu Nome'
SITENAME = 'Gazeta de Eventos'
SITEURL = ''
SITE_DESCRIPTION = 'Classificados de Eventos'

PATH = 'content'
TIMEZONE = 'America/Sao_Paulo'
DEFAULT_LANG = 'pt'

# Tema
THEME = 'themes/classificados'

# Formatos de data em português
DEFAULT_DATE_FORMAT = '%d de %B de %Y'

# Usar summary automático (primeiros 200 caracteres)
SUMMARY_MAX_LENGTH = 200

# Slugs em lowercase
SLUG_REGEX_SUBSTITUTIONS = [
    (r'[^\w\s-]', ''),
    (r'(?u)\A\s*', ''),
    (r'(?u)\s*\Z', ''),
    (r'[-\s]+', '-'),
]

# Metadados customizados para eventos
# Uso nos arquivos .md:
#   :location: Teatro Municipal
#   :price: R$ 50,00
#   :event_date: 15/06/2025
#   :organizer: Associação Cultural XPTO
#   :contact: contato@evento.com.br

EXTRA_METADATA = {
    'location': None,
    'price': None,
    'event_date': None,
    'organizer': None,
    'contact': None,
}

# Feed / RSS
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Paginação
DEFAULT_PAGINATION = 20

# URLs limpas
ARTICLE_URL = '{category}/{slug}.html'
ARTICLE_SAVE_AS = '{category}/{slug}.html'
CATEGORY_URL = 'category/{slug}.html'
CATEGORY_SAVE_AS = 'category/{slug}.html'
TAG_URL = 'tag/{slug}.html'
TAG_SAVE_AS = 'tag/{slug}.html'
