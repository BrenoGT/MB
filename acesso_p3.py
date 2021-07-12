import requests
from utils import json

cat_file = r'K:\di estrategia_riscos\Riscos Financeiros\Relatorio Pilar 3 - Circ. 3.930\Relatório e Tabelas\Programa Python - Pilar 3\JSON\API Files\catalogo\catalogo.json'


def main():
    data = json.read_json(cat_file)
    recursos = data['conjuntos'][0]['recursos']
    url_base = data['conjuntos'][0]['urlBase']
    for rec in recursos:
        nome = rec['nome'].split(' - ')[0]
        caminho = rec['caminhoRecurso']
        nome_sub = rec['parametros']['nome']
        for d in rec['parametros']['valores']:
            resto_url = caminho.replace('{%s}' % nome_sub, d)
            caminho_completo = url_base + resto_url + '/' + nome.lower() + '.json'
            print(f'Acessando: {caminho_completo}')
            try:
                api = requests.get(caminho).json()
                if len(api) < 1:
                    print('A API do ')
            except Exception:
                pass


if __name__ == '__main__':
    main()
