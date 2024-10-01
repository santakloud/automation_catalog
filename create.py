import os
import yaml
import subprocess

def lint_yaml(file_path):
    """
    Realiza linting a un archivo YAML usando yamllint.

    :param file_path: Ruta del archivo YAML.
    :return: Una tupla (bool, str) donde el primer elemento indica si el archivo pasó el linting y el segundo elemento contiene la salida del comando.
    """
    result = subprocess.run(['yamllint', '-d', '{extends: default, rules: {line-length: {max: 120}}}', file_path], capture_output=True, text=True)
    return result.returncode == 0, result.stdout

def lint_md(file_path):
    """
    Realiza linting a un archivo Markdown usando markdownlint.

    :param file_path: Ruta del archivo Markdown.
    :return: Una tupla (bool, str) donde el primer elemento indica si el archivo pasó el linting y el segundo elemento contiene la salida del comando.
    """
    result = subprocess.run(['markdownlint', '-c', '{"line-length": {"line_length": 120}}', file_path], capture_output=True, text=True)
    return result.returncode == 0, result.stdout

def yaml_to_md(yaml_content, indent=0):
    """
    Convierte el contenido de un archivo YAML a formato Markdown.

    :param yaml_content: Contenido del archivo YAML.
    :param indent: Nivel de indentación para el formato Markdown.
    :return: Cadena de texto en formato Markdown.
    """
    md_content = ""
    indent_str = "  " * indent
    if isinstance(yaml_content, dict):
        for key, value in yaml_content.items():
            md_content += f"{indent_str}## {key}\n\n"
            md_content += yaml_to_md(value, indent + 1)
    elif isinstance(yaml_content, list):
        for item in yaml_content:
            md_content += f"{indent_str}- {yaml_to_md(item, indent + 1)}"
    else:
        md_content += f"{indent_str}{yaml_content}\n\n"
    return md_content

def process_files(yaml_dir, md_dir, result_dir):
    """
    Procesa archivos YAML en un directorio, realiza linting, convierte a Markdown y guarda los resultados.

    :param yaml_dir: Directorio que contiene los archivos YAML.
    :param md_dir: Directorio donde se guardarán los archivos Markdown generados.
    :param result_dir: Directorio donde se guardarán los resultados del linting.
    """
    for yaml_file in os.listdir(yaml_dir):
        if yaml_file.endswith('.yaml'):
            yaml_path = os.path.join(yaml_dir, yaml_file)
            md_file_name = yaml_file.replace('.yaml', '.md')
            md_path = os.path.join(md_dir, md_file_name)
            result_file_name = yaml_file.replace('.yaml', '_result.txt')
            result_path = os.path.join(result_dir, result_file_name)

            with open(yaml_path, 'r') as file:
                yaml_content = yaml.safe_load(file)

            is_yaml_valid, yaml_lint_output = lint_yaml(yaml_path)
            if not is_yaml_valid:
                with open(result_path, 'w') as result_file:
                    result_file.write("YAML Lint Errors:\n")
                    result_file.write(yaml_lint_output)
                continue

            md_content = yaml_to_md(yaml_content)
            with open(md_path, 'w') as md_file:
                md_file.write(md_content)

            is_md_valid, md_lint_output = lint_md(md_path)
            with open(result_path, 'w') as result_file:
                if is_md_valid:
                    result_file.write("Markdown Lint Passed\n")
                else:
                    result_file.write("Markdown Lint Errors:\n")
                    result_file.write(md_lint_output)

if __name__ == "__main__":
    yaml_dir = 'yaml'
    md_dir = 'md'
    result_dir = 'result'
    os.makedirs(md_dir, exist_ok=True)
    os.makedirs(result_dir, exist_ok=True)
    process_files(yaml_dir, md_dir, result_dir)
