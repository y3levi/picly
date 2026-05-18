import requests

def buscar(tag, pagina=1, limite=30):
    try:
        r = requests.get('https://konachan.net/post.json', params={
            'limit': limite,
            'page': pagina,
            'tags': f'{tag} rating:s'
        }, headers={'User-Agent': 'PICLY/1.0'}, timeout=8)
        posts = r.json()
        resultados = []
        if isinstance(posts, list):
            for post in posts:
                url = post.get('file_url', '')
                if url and not url.endswith('.mp4'):
                    tipo = 'gif' if url.endswith('.gif') else 'imagem'
                    resultados.append({
                        'url': url,
                        'tipo': tipo,
                        'fonte': 'konachan',
                        'tags': post.get('tags', ''),
                        'rating': post.get('rating', 's')
                    })
        return resultados
    except:
        return []
