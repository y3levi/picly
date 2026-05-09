import requests

def normalizar(nome):
    """Gera variações de tag a partir do nome do personagem."""
    n = nome.lower().replace(',', '').replace("'", '').replace('-', '_')
    # normaliza romanização japonesa
    n = n.replace('ou', 'o').replace('uu', 'u').replace('aa', 'a')
    partes = n.split()
    variacoes = []
    if len(partes) >= 2:
        variacoes.append('_'.join(partes))           # satoru_gojo
        variacoes.append('_'.join(reversed(partes))) # gojo_satoru
    else:
        variacoes.append(partes[0])
    return variacoes

def buscar_personagem(nome):
    try:
        r = requests.get('https://api.jikan.moe/v4/characters', params={
            'q': nome,
            'limit': 5,
            'order_by': 'favorites',
            'sort': 'desc'
        }, timeout=10)
        dados = r.json()
        personagens = []
        for item in dados.get('data', []):
            animes = item.get('anime', [])
            anime_nome = animes[0]['anime']['title'] if animes else 'Desconhecido'
            tags = normalizar(item['name'])
            personagens.append({
                'nome': item['name'],
                'imagem': item['images']['jpg']['image_url'],
                'anime': anime_nome,
                'tags': tags  # lista de variações
            })
        return personagens
    except:
        return []