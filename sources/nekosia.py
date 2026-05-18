import requests

# nekosia não consegue buscar por tags específicas
# então é apenas fonte reserva
CATEGORIAS = ['catgirl', 'foxgirl', 'maid', 'uniform', 'cute']

def buscar(tag, pagina=1, limite=10):
    try:
        # apenas retorna imagens aleatórias por categoria
        categoria = 'catgirl'  # padrão
        for cat in CATEGORIAS:
            if cat in tag.lower():
                categoria = cat
                break

        r = requests.get(f'https://nekosia.cat/api/v1/images/{categoria}', params={
            'count': limite,
            'page': pagina
        }, headers={'User-Agent': 'PICLY/1.0'}, timeout=8)
        data = r.json()
        resultados = []
        imagens = data.get('images', [])
        if isinstance(imagens, list):
            for item in imagens:
                url = item.get('image', {}).get('original', {}).get('url', '')
                if url:
                    resultados.append({
                        'url': url,
                        'tipo': 'imagem',
                        'fonte': 'nekosia',
                        'tags': categoria,
                        'rating': 'general'
                    })
        return resultados
    except:
        return []
