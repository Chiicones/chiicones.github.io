import sys
sys.path.insert(0, 'plugins')
PLUGINS = ['search_index']

AUTHOR = 'Francisco Barbosa'
SITENAME = 'Agenda DF'
SITEURL = ''

PATH = 'content'
THEME = r'C:\Users\chico\projetos\classificados2'

TIMEZONE = 'America/Sao_Paulo'
DEFAULT_LANG = 'pt'
DEFAULT_DATE_FORMAT = '%d/%m/%Y'

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None

DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = [
    ('Busca', '/busca.html'),
    ('Circo', '/categoria/circo.html'),
    ('Comédia', '/categoria/comedia.html'),
    ('Exposição', '/categoria/exposicao.html'),
    ('Família', '/categoria/familia.html'),
    ('Feira', '/categoria/feira.html'),
    ('Festival', '/categoria/festival.html'),
    ('Música', '/categoria/musica.html'),
    ('Teatro', '/categoria/teatro.html'),
    ('Blog', '/categoria/blog.html'),
    ('Mapa', '/mapa.html'),
    ('Sobre', '/pages/sobre.html'),
]

HERO_EYEBROW = 'Próximos Eventos'
HERO_TITLE = 'Agenda DF'
HERO_SUBTITLE = 'Gastronomia afetiva, música ao vivo e encontros que ficam.'

EXTRA_ARTICLE_FIELDS = ['local', 'bairro', 'data', 'horario', 'entrada']

DEFAULT_PAGINATION = 50

ARTICLE_URL = 'eventos/{slug}.html'
ARTICLE_SAVE_AS = 'eventos/{slug}.html'
CATEGORY_URL = 'categoria/{slug}.html'
CATEGORY_SAVE_AS = 'categoria/{slug}.html'
TAG_URL = 'tag/{slug}.html'
TAG_SAVE_AS = 'tag/{slug}.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

STATIC_PATHS = ['images', 'extra']