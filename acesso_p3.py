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
    try:
        data = read_json(cat_file)
    except FileNotFoundError:
        print(f'Não foi possível encontrar o arquivo.\nCaminho: {cat_file}\n')
    else:
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
                    print(f'{nome}: {caminho_completo}')
                    api = requests.get(caminho_completo, verify=False).json()
                    if len(api) < 1:
                        print('\t> Está vazia.')
                except json.JSONDecodeError as json_err:
                    print(f'\t> Erro ao ler o JSON - [{json_err}]\n')
                except Exception as err:
                    print(f'Não foi possível ler a API - [{err}]\n')
                else:
                    print(f'\t> Acesso ok!\n')


if __name__ == '__main__':
    main()
