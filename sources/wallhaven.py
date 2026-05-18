import os
import requests

def buscar(tag, pagina=1, limite=20):
    try:
        headers = {'User-Agent': 'PICLY/1.0'}
        api_key = os.getenv('WALLHAVEN_API_KEY')
        if api_key:
            headers['X-API-Key'] = api_key

        r = requests.get('https://wallhaven.cc/api/v1/search', params={
            'q': tag.replace('_', ' '),
            'categories': '010',
            'purity': '100',
            'page': pagina,
            'per_page': limite,
            'sorting': 'relevance'
        }, headers=headers, timeout=8)
        data = r.json()
        posts = data.get('data', [])
        resultados = []
        if isinstance(posts, list):
            for post in posts:
                url = post.get('path', '')
                if url and not url.endswith('.mp4'):
                    resultados.append({
                        'url': url,
                        'tipo': 'imagem',
                        'fonte': 'wallhaven',
                        'tags': tag,
                        'rating': post.get('purity', 'sfw')
                    })
        return resultados
    except:
        return []
