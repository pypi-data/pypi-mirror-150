import json
import os
import time
import zipfile
from pathlib import Path
from typing import Any, Dict, List

import tqdm
from dotenv import load_dotenv

from aoricaan_cli.src.utils.debugger import Debug

try:
    from core_aws.s3 import upload_file
except ImportError:
    pass

environs = load_dotenv()


def _search_all_deploy_resources(template_data: Dict[str, Any]) -> List[str]:
    return [resource for resource in template_data["Resources"]
            if template_data["Resources"][resource].get("Type", {}) == "AWS::ApiGateway::Deployment"]


def update_deploy_resource_name(path_template: Path):
    template_text = path_template.read_text()
    deploys = _search_all_deploy_resources(json.loads(template_text))
    for deploy_key in deploys:
        Debug.info(f"Update deploy resource {deploy_key}")
        template_text = template_text.replace(f'"{deploy_key}"', f'"{deploy_key}{int(time.time())}"')
    path_template.write_text(template_text)


def update_deploy_id_resource_api_gateway(path_template: Path):
    update_deploy_resource_name(path_template)


def _create_layer_zip(*, layers_zips, layer, layer_path: Path, bucket):
    zip_path_file = os.path.join(layers_zips, f'{layer}.zip')
    with zipfile.ZipFile(zip_path_file, 'w') as my_zip:
        for _sub_dir in os.listdir(layer_path):
            sub_path = layer_path.joinpath(_sub_dir)
            for file in os.listdir(sub_path) if sub_path.is_dir() else []:
                my_zip.write(sub_path.joinpath(file), os.path.join('python', _sub_dir, file))
    if not upload_file(file_name=zip_path_file, bucket=bucket):
        print(f"Error to try save the layer zip in s3 {bucket}")


def build_layers(*, layers_path: Path, bucket=None, use_zip=False):
    layers_zips = 'layers_zips'
    if not os.path.exists(layers_zips):
        os.mkdir(layers_zips)

    for layer in tqdm.tqdm(os.listdir(layers_path)):
        layer_path = layers_path.joinpath(layer)
        if not layer_path.is_dir():
            continue

        layer_path = layer_path.joinpath('python')
        try:
            print('runing command', f'pip install -r {os.path.join(layer_path, "requirements.txt")} -t {layer_path}')
            os.system(f'pip install -r {os.path.join(layer_path, "requirements.txt")} -t {layer_path}')
        except Exception as e:
            print("WARNING: ", str(e))
        if use_zip:
            _create_layer_zip(layers_zips=layers_zips, layer=layer, layer_path=layer_path, bucket=bucket)


def build_all_lambdas(*, lambdas_path: Path, path_cfn_template: Path, path_swagger_template: Path, bucket):
    cfn_template = json.loads(path_cfn_template.read_text())
    swagger_template = json.loads(path_swagger_template.read_text())

    for path in os.listdir(lambdas_path):
        name = path
        path = lambdas_path.joinpath(path)
        if (path == lambdas_path) or not path.is_dir():
            continue

        name = name.replace('-', ' ').replace("_", " ").title().replace(" ", "")
        if not path.joinpath('configuration.json').exists():
            continue
        configuration = json.loads(path.joinpath('configuration.json').read_text())
        cfn_template['Resources'][name] = configuration['cfn']
        for k, v in configuration['swagger'].items():
            if k not in swagger_template['paths']:
                swagger_template['paths'].update(configuration['swagger'])
            else:
                for vk, vv in v.items():
                    if vk not in swagger_template['paths'][k]:
                        swagger_template['paths'][k].update({vk: vv})

    path_cfn_template.write_text(json.dumps(cfn_template))
    path_swagger_template.write_text(json.dumps(swagger_template))

    # upload_file(file_name=path_swagger_template, bucket=bucket)
