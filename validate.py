import os
import yaml
import json
import jsonschema
from jsonschema import validate, Draft7Validator

def load_yaml(file_path):
    """
    Carga un archivo YAML y lo devuelve como un diccionario de Python.
    
    :param file_path: Ruta del archivo YAML.
    :return: Diccionario con el contenido del archivo YAML.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_json(file_path):
    """
    Carga un archivo JSON y lo devuelve como un diccionario de Python.
    
    :param file_path: Ruta del archivo JSON.
    :return: Diccionario con el contenido del archivo JSON.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def validate_yaml_with_schema(yaml_data, schema):
    """
    Valida los datos YAML contra un esquema JSON.

    :param yaml_data: Diccionario con datos YAML.
    :param schema: Esquema JSON para validar los datos YAML.
    :return: Mensaje indicando si el YAML es válido o una lista de errores.
    """
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(yaml_data), key=lambda e: e.path)
    if not errors:
        return "El fichero YAML es válido según el esquema JSON."
    else:
        error_messages = ["El fichero YAML no es válido:"]
        for error in errors:
            error_messages.append(f"Error en {list(error.path)}: {error.message}")
        return "\n".join(error_messages)

def main():
    """
    Función principal que procesa archivos YAML en un directorio, valida contra esquemas JSON y guarda los resultados.

    :param yaml_dir: Directorio que contiene los archivos YAML.
    :param schema_dir: Directorio que contiene los esquemas JSON.
    :param result_dir: Directorio donde se guardarán los resultados de la validación.
    """
    yaml_dir = 'yaml'
    schema_dir = 'schema'
    result_dir = 'result'

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    for file_name in os.listdir(yaml_dir):
        if file_name.endswith('.yaml'):
            yaml_path = os.path.join(yaml_dir, file_name)
            schema_path = os.path.join(schema_dir, file_name.replace('.yaml', '.json'))
            result_path = os.path.join(result_dir, file_name.replace('.yaml', '_result.txt'))

            if os.path.exists(schema_path):
                yaml_data = load_yaml(yaml_path)
                schema = load_json(schema_path)
                validation_result = validate_yaml_with_schema(yaml_data, schema)
            else:
                validation_result = f"Esquema JSON no encontrado para {file_name}"

            with open(result_path, 'w') as result_file:
                result_file.write(validation_result)

if __name__ == "__main__":
    main()
