import yaml
import json
import os
import subprocess

def lint_yaml_file(yaml_file, result_dir):
    result = subprocess.run(['yamllint', yaml_file], capture_output=True, text=True)
    lint_output = f"Linting {yaml_file}:\n{result.stdout}\n{result.stderr}"
    print(lint_output)
    
    # Guardar el resultado del linting en un archivo en el directorio result
    base_name, _ = os.path.splitext(os.path.basename(yaml_file))
    lint_file = os.path.join(result_dir, f"{base_name}_error_lint.txt")
    with open(lint_file, 'w') as lf:
        lf.write(lint_output)

def lint_all_yaml_files(directory, result_dir):
    for file_name in os.listdir(directory):
        if file_name.endswith('.yaml'):
            file_path = os.path.join(directory, file_name)
            lint_yaml_file(file_path, result_dir)

def convert_yaml_to_json(yaml_file, json_file):
    # Cargar el archivo YAML
    with open(yaml_file, 'r') as yf:
        yaml_content = yaml.safe_load(yf)
    
    # Convertir y guardar como JSON
    with open(json_file, 'w') as jf:
        json.dump(yaml_content, jf, indent=4)
    print(f"Archivo JSON guardado en {json_file}")

if __name__ == "__main__":
    yaml_dir = 'template'
    json_dir = 'json'
    result_dir = 'result'

    if not os.path.exists(json_dir):
        os.makedirs(json_dir)

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # Realizar linting de todos los archivos YAML
    lint_all_yaml_files(yaml_dir, result_dir)

    # Convertir los archivos YAML a JSON
    for yaml_file in os.listdir(yaml_dir):
        if yaml_file.endswith('.yaml'):
            base_name, _ = os.path.splitext(yaml_file)  # Solo el nombre base
            yaml_file_path = os.path.join(yaml_dir, yaml_file)
            json_file_path = os.path.join(json_dir, f"{base_name}.json")
            convert_yaml_to_json(yaml_file_path, json_file_path)
