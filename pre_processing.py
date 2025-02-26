import autopep8
import os

# Faz o pré processamento do código para padronizar a tabulação
def pre_processing(code_file):

    # Lê o arquivo de entrada
    with open(code_file, 'r') as file:
        code = file.read()

    # Formata o código usando a autopep8
    # aggressive: 0 corrige espaçamento, indentação e remove espaços em branco desnecessários
    formatted_code = autopep8.fix_code(code, options={'aggressive': 0})

    # Obtem o nome do arquivo
    file_name = os.path.basename(code_file)

    # Cria o nome do arquivo temporário com base no nome do arquivo original
    temporary_file = f"{os.path.splitext(file_name)[0]}_formatted.py"

    # Salva o código processado no arquivo temporário
    with open(temporary_file, 'w') as file:
        file.write(formatted_code)

    # Retorna o nome do arquivo temporário
    return temporary_file
