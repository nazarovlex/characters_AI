import os
import yaml

# Получить абсолютный путь к файлу conf.yaml
current_dir = os.path.dirname(os.path.abspath(__file__))
conf_file_path = os.path.join(current_dir, "conf.yaml")
config = yaml.load(open(conf_file_path), Loader=yaml.Loader)

BOT_TOKEN = config["BOT_TOKEN"]
OPEN_API_TOKEN = config["OPEN_API_TOKEN"]
WEB_APP_HOST = config['web_app_host']
WEB_APP_PORT = config['web_app_port']
WEB_APP_URL = f"http://{config['web_app_host']}:{config['web_app_port']}"
