from flask import Flask, render_template, request, jsonify, Response
from sources import safebooru, danbooru, gelbooru, yandere, konachan, nekosia
import requests
import random
from rembg import remove
from PIL import Image
import io
import base64



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar')
def buscar():
    q = request.args.get('q', '').strip()
    filtro_tags = request.args.get('filtro_tags', '').strip()
    pagina = int(request.args.get('pagina', 1))

    if not q:
        return jsonify([])

    tag_personagem = q.replace(' ', '_')
    tag_final = f"{tag_personagem} {filtro_tags}".strip() if filtro_tags else tag_personagem

    resultados = []

    # konachan limite em wallpapers.
    if 'wallpaper' in filtro_tags:
        resultados += konachan.buscar(tag_personagem, pagina)

    resultados += safebooru.buscar(tag_final, pagina)
    resultados += gelbooru.buscar(tag_final, pagina)
    resultados += yandere.buscar(tag_final, pagina)
    resultados += danbooru.buscar(tag_final, pagina)

    # nekosia como busca reserva
    if len(resultados) < 10:
        resultados += nekosia.buscar(tag_personagem, pagina)

    #  deixar os resultados mais aleatorios
    random.shuffle(resultados)

    return jsonify(resultados)

@app.route('/relacionadas')
def relacionadas():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    tag = q.replace(' ', '_')
    resultados = []
    resultados += safebooru.buscar(tag, 2)
    resultados += gelbooru.buscar(tag, 2)
    random.shuffle(resultados)
    return jsonify(resultados[:12])

@app.route('/download')
def download():
    url = request.args.get('url', '')
    if not url:
        return 'URL inválida', 400
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent': 'PICLY/1.0'})
        ext = url.split('.')[-1].split('?')[0]
        content_type = r.headers.get('Content-Type', 'image/png')
        return Response(
            r.content,
            headers={
                'Content-Disposition': f'attachment; filename="picly.{ext}"',
                'Content-Type': content_type
            }
        )
    except:
        return 'Erro ao baixar', 500

@app.route('/autocomplete')
def autocomplete():
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])
    try:
        r = requests.get('https://danbooru.donmai.us/tags.json', params={
            'search[name_matches]': f'{q}*',
            'search[order]': 'count',
            'limit': 5
        }, headers={'User-Agent': 'PICLY/1.0'}, timeout=3)
        tags = r.json()
        return jsonify([
            {'tag': t['name'], 'count': t['post_count']}
            for t in tags if t['post_count'] > 0
        ])
    except:
        return jsonify([])

@app.route('/processar')
def processar():
    url = request.args.get('url','')
    operacao = request.args.get('op','rembg')

    if not url:
        return jsonify({'error': 'URL inválida'}), 400
    
    try:
        #baixar
        r = requests.get(url, timeout=15, headers={'User-Agent': 'PICLY/1.0'})
        img_bytes = r.content

        if operacao == 'rembg':
        #removerfundo
            resultado = remove(img_bytes)

        #converter para base64
        b64 = base64.b64encode(resultado).decode('utf-8')
        return jsonify({'imagem': f'data:image/png;base64,{b64}'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500








if __name__ == '__main__':
    app.run(debug=True)