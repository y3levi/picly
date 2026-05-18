import requests

def buscar(tag, pagina=1, limite=30):
    try:
        r = requests.get('https://danbooru.donmai.us/posts.json', params={
            'tags': f'{tag} rating:g',
            'limit': limite,
            'page': pagina
        }, headers={'User-Agent': 'PICLY/1.0'}, timeout=10)
        posts = r.json()
        resultados = []
        if isinstance(posts, list):
            for post in posts:
                url = post.get('large_file_url') or post.get('file_url', '')
                if url and not url.endswith('.mp4') and not url.endswith('.zip'):
                    tipo = 'gif' if url.endswith('.gif') else 'imagem'
                    resultados.append({
                        'url': url,
                        'tipo': tipo,
                        'fonte': 'danbooru',
                        'tags': post.get('tag_string', ''),
                        'rating': post.get('rating', 'g')
                    })
        return resultados
    except:
        return []
