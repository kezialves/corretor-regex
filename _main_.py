import argparse
import os
import corrector

def main(solutions_dir):

    # Verifica se o diretório de soluções existe
    if not os.path.exists(solutions_dir):
        print(f"\033[31mErro: Diretório '{solutions_dir}' não encontrado.\033[0m\n")
        return

    # Itera sobre os diretórios dentro do diretório de soluções
    for root, dirs, files in os.walk(solutions_dir):

        # Verifica se a solução correta existe no diretório de soluções
        if "correct_solution.py" in files:
            # Pega os caminhos das soluções
            correct_solution_path = os.path.join(root, "correct_solution.py")
            incorrect_solution_path = os.path.join(root, "incorrect_solution.py")

            # Executa o corretor para correct_solution.py
            print(f"\n- Executando corretor para \033[1;32m{correct_solution_path}\033[0m:")
            corrector.corrector(correct_solution_path, correct_solution_path)
            print()
            
            # Executa o corretor para incorrect_solution.py
            if os.path.exists(incorrect_solution_path):
                print(f"\n- Executando corretor para \033[1;31m{incorrect_solution_path}\033[0m:")
                corrector.corrector(incorrect_solution_path, correct_solution_path)
                print()
            else:
                print(f"\n\033[31mArquivo '{incorrect_solution_path}' não encontrado.\033[0m")

# Configura o parser de argumentos
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Executa o corretor para todos os diretórios dentro do diretório de soluções.")
    
    parser.add_argument(
        "solutions_dir", # nome do diretório de soluções
        help="Caminho do diretório solutions." # mensagem de ajuda
    )

    # Faz o parser dos argumentos
    args = parser.parse_args()

    # Chama a main com o diretório de soluções passado como argumento
    main(args.solutions_dir)

""" 
Exemplo de execução:
    python3 main.py solutions
"""
