# pip install pyyaml
import yaml

with open('./../_config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    print(config)

