import requests

def buscar(tag, pagina=1, limite=30):
    try:
        r = requests.get('https://gelbooru.com/index.php', params={
            'page': 'dapi',
            's': 'post',
            'q': 'index',
            'json': 1,
            'limit': limite,
            'pid': pagina - 1,
            'tags': tag
        }, headers={'User-Agent': 'PICLY/1.0'}, timeout=8)
        data = r.json()
        posts = data.get('post', [])
        resultados = []
        if isinstance(posts, list):
            for post in posts:
                url = post.get('file_url', '')
                if url and not url.endswith('.mp4'):
                    tipo = 'gif' if url.endswith('.gif') else 'imagem'
                    resultados.append({'url': url, 'tipo': tipo, 'fonte': 'gelbooru'})
        return resultados
    except:
        return []