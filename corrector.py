import pre_processing
from collections import defaultdict
import re
import os

# Conta as estruturas de controle por nível de indentação
def count_structures(code):

    # Dicionário que armazena a contagem de estruturas por nível de indentação
    count = defaultdict(lambda: defaultdict(int))

    # Regex que verifica o padrão "[palavra reservada] [expressão] [:]"
    # No caso do else o padrão é apenas "[palavra reservada] [:]
    patern = re.compile(r'^\s*(for|while|if|elif|else)\b.*:$')

    # Processa cada linha do código
    for line in code.splitlines():

        # Ignora linhas em branco
        if not line: continue

        # Verifica se a linha segue o padrão definido
        if patern.match(line):
            # Identifica o nível da indentação
            indentation_level = len(line) - len(line.lstrip())
            # Extrai a palavra reservada
            reserved_word = line.lstrip().split()[0]

            # Agrupa 'if', 'elif' e 'else' como "Condição"
            if reserved_word in ['if', 'elif', 'else:']:
                structure_type = "Condição"
            
            # Agrupa 'for' e 'while' como "Laço"
            elif reserved_word in ['for', 'while']:
                structure_type = "Laço"
            
            else:
                structure_type = reserved_word

            # Incrementa a contagem da estrutura de controle correspondente
            count[indentation_level][structure_type] += 1

    # Retorna o dicionário ordenado pelo nível de indentação
    return {k: count[k] for k in sorted(count.keys())}

# Exibe o resultado do dicionário
def dict_print(dict):
 
    # Itera sobre o dicionário
    for level, structures in dict.items():
        print(f"Nível de indentação {level}:")

        # Itera sobre as estruturas
        for structure, count in structures.items():
            print(f"    {structure}: {count}")

# Calcula a taxa de similaridade entre dois dicionários
def dict_similarity(dict1, dict2):

    # ---------- Normaliza os dicionários ----------

    # Obtem as chaves (níveis de indentação) dos dois dicionários
    all_keys = set(dict1.keys()).union(set(dict2.keys()))

    # Obtem as estruturas de controle dos dois dicionários
    all_structures = set()

    for key in all_keys:
        if key in dict1:
            all_structures.update(dict1[key].keys())
        if key in dict2:
            all_structures.update(dict2[key].keys())

    # ---------- código para print ----------
    # normalized_dict1 = {}
    # normalized_dict2 = {}

    # for key in all_keys:
    #     normalized_dict1[key] = {}
    #     normalized_dict2[key] = {}

    #     for structure in all_structures:
    #         normalized_dict1[key][structure] = dict1.get(key, {}).get(structure, 0)
    #         normalized_dict2[key][structure] = dict2.get(key, {}).get(structure, 0)

    # print("----- Dicionário normalizado da solução:")
    # dict_print(normalized_dict1)
    # print("\n----- Dicionário normalizado do gabarito:")
    # dict_print(normalized_dict2)
    # ----------------------------------------

    # ---------- Calcula a similaridade ----------
    
    total_difference = 0
    total_count = 0

    for key in all_keys:
        for structure in all_structures:
            # Conta as estruturas de cada dicionário
            count1 = dict1.get(key, {}).get(structure, 0)
            count2 = dict2.get(key, {}).get(structure, 0)

            total_difference += abs(count1 - count2)
            total_count += max(count1, count2)

    # ---------- código para print ----------
    # for key in all_keys:
    #     for structure in all_structures:
    #         # Conta as estruturas de cada dicionário
    #         count1 = normalized_dict1[key][structure]
    #         count2 = normalized_dict2[key][structure]

    #         total_difference += abs(count1 - count2)
    #         total_count += max(count1, count2)
    # ----------------------------------------

    # Se ambos os dicionários forem vazios, a similaridade é de 100%
    # evita divisão por 0
    if total_count == 0:
        return 100.0

    # Retorna a similaridade
    # max entre 0.0 e outro valor para evitar valor negativo
    return max(0.0, 100.0 * (1 - (total_difference/total_count)))

# Faz a correção do código solução
def corrector(solution_file, template_file):

    # Aplica o pré-processamento
    template_temp_file = pre_processing.pre_processing(template_file)
    solution_temp_file = pre_processing.pre_processing(solution_file)

    # Lê os arquivos temporários
    with open(template_temp_file, 'r') as file:
        template = file.read()
    with open(solution_temp_file, 'r') as file:
        solution = file.read()

    # Cria os dicionários de contagem de estruturas de controle
    template_dict = count_structures(template)
    solution_dict = count_structures(solution)

    # print("----- Dicionário do gabarito:")
    # dict_print(template_dict)
    # print("\n----- Dicionário da solução:")
    # dict_print(solution_dict)

    # Calcula a similaridade entre os dicionários gerados
    similarity = dict_similarity(solution_dict, template_dict)

    # Define um limite para aceitação da solução
    if similarity >= 75.0:
        print(f"✅ Solução correta com {similarity:.2f}% de similaridade.")
    else:
        print(f"❌ Solução incorreta com {similarity:.2f}% de similaridade.")

    # Remove os arquivos temporários criados
    os.remove(template_temp_file)
    os.remove(solution_temp_file)
