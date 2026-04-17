import json
import os
from pelican import signals


def generate_search_index(generator):
    articles = []
    for article in generator.articles:
        articles.append({
            'title': article.title,
            'url': article.url,
            'summary': getattr(article, 'summary', ''),
            'category': str(article.category),
            'category_url': article.category.url,
            'tags': ', '.join(str(t) for t in getattr(article, 'tags', [])),
            'local': str(getattr(article, 'local', '') or ''),
            'data': str(getattr(article, 'data', '') or ''),
            'entrada': str(getattr(article, 'entrada', '') or ''),
        })

    output_path = os.path.join(generator.output_path, 'search.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)


def register():
    signals.article_generator_finalized.connect(generate_search_index)