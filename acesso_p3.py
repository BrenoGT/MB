import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

cat_file = r''


def read_json(file_path: str, encoding: str = 'utf8') -> json:
    """
    Reads a JSON file

    :param file_path: the path os the file
    :param encoding: (optional) the encoding used in the reading
    :return: the JSON data
    """
    with open(file_path, 'r', encoding=encoding) as file:
        data = json.load(file)
        file.close()
    return data


def main():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    data = read_json(cat_file)
    recursos = data['conjuntos'][0]['recursos']
    url_base = data['conjuntos'][0]['urlBase']
    for rec in recursos:
        nome = rec['nome'].split(' - ')[0]
        caminho = rec['caminhoRecurso']
        nome_sub = rec['parametros']['nome']
        for d in rec['parametros']['valores']:
            resto_url = caminho.replace('{%s}' % nome_sub, d)
            caminho_completo = url_base + resto_url + '/' + nome.lower() + '.json'
            try:
                api = requests.get(caminho_completo, verify=False).json()
                if len(api) < 1:
                    print(f'Link: {caminho_completo}')
                    print(f'A API do {nome} está vazia.\n')
            except json.JSONDecodeError as json_err:
                print(f'Link: {caminho_completo}')
                print('Erro ao ler o JSON\n')
            except Exception as err:
                print(f'Link: {caminho_completo}')
                print('Não foi possível ler a API.')
                print(err, end='\n\n')
            else:
                print(f'Acesso a {nome} está ok!')


if __name__ == '__main__':
    main()
