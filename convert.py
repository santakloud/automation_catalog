import os
import yaml
import json
import jsonschema
from jsonschema import Draft7Validator
from yamllint.config import YamlLintConfig
from yamllint import linter

def load_yaml(file_path):
    """
    Carga un archivo YAML y lo devuelve como un diccionario de Python.
    
    :param file_path: Ruta del archivo YAML.
    :return: Diccionario con el contenido del archivo YAML.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def lint_yaml(file_path):
    """
    Lint a un archivo YAML usando yamllint y devuelve una lista de errores.
    
    :param file_path: Ruta del archivo YAML.
    :return: Lista de errores de lint.
    """
    config = YamlLintConfig('extends: default\nrules:\n  line-length:\n    max: 1000')
    with open(file_path, 'r') as file:
        yaml_content = file.read()
    lint_errors = list(linter.run(yaml_content, config))
    return lint_errors

def generate_json_schema(yaml_data):
    """
    Genera un esquema JSON a partir de un diccionario de datos YAML.
    
    :param yaml_data: Diccionario con datos YAML.
    :return: Esquema JSON.
    """
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {},
        "required": []
    }
    for key, value in yaml_data.items():
        if isinstance(value, dict):
            schema["properties"][key] = {
                "type": "object",
                "properties": {k: {"type": "string"} for k in value.keys()},
                "required": list(value.keys())
            }
        elif isinstance(value, list):
            schema["properties"][key] = {
                "type": "array",
                "items": {"type": "string"}
            }
        else:
            schema["properties"][key] = {"type": "string"}
        schema["required"].append(key)
    return schema

def main():
    """
    Función principal que procesa archivos YAML en un directorio, realiza linting,
    carga los datos y genera esquemas JSON.
    """
    yaml_dir = 'template'
    schema_dir = 'schema'
    result_dir = 'result'

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    if not os.path.exists(schema_dir):
        os.makedirs(schema_dir)

    for file_name in os.listdir(yaml_dir):
        if file_name.endswith('.yaml'):
            yaml_path = os.path.join(yaml_dir, file_name)
            result_path = os.path.join(result_dir, file_name.replace('.yaml', '_errors_lint.txt'))
            schema_path = os.path.join(schema_dir, file_name.replace('.yaml', '.json'))

            # Lint YAML file
            lint_errors = lint_yaml(yaml_path)
            if lint_errors:
                with open(result_path, 'w') as result_file:
                    for error in lint_errors:
                        result_file.write(f"{error.line}:{error.column} {error.desc}\n")
                print(f"Lint errors found in {file_name}, written to {result_path}")
            else:
                print(f"No lint errors found in {file_name}")

            # Load YAML data
            try:
                yaml_data = load_yaml(yaml_path)
                print(f"Loaded YAML data from {file_name}")
            except Exception as e:
                print(f"Error loading YAML data from {file_name}: {e}")
                continue

            # Generate JSON schema
            try:
                json_schema = generate_json_schema(yaml_data)
                with open(schema_path, 'w') as schema_file:
                    json.dump(json_schema, schema_file, indent=2)
                print(f"Generated JSON schema for {file_name}, written to {schema_path}")
            except Exception as e:
                print(f"Error generating JSON schema for {file_name}: {e}")

if __name__ == "__main__":
    main()
