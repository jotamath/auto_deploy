import json
import os
import time
import PySimpleGUI as sg

class DeployManager:
    def __init__(self):
        self.git_repo = ""
        self.docker_file = ""
        self.k8s_config = ""
        self.gitlab_url = ""
        self.log_messages = []

    def save_config(self):
        config = {
            "gitRepo": self.git_repo,
            "dockerFile": self.docker_file,
            "k8sConfig": self.k8s_config,
            "gitlabUrl": self.gitlab_url,
        }
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
        self.log_message("Configuração salva com sucesso!")

    def load_config(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
                self.git_repo = config.get("gitRepo", "")
                self.docker_file = config.get("dockerFile", "")
                self.k8s_config = config.get("k8sConfig", "")
                self.gitlab_url = config.get("gitlabUrl", "")

    def log_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_messages.append(f"[{timestamp}] {message}")

    def run_pipeline(self, progress_bar):
        stages = [
            "Clonando repositório",
            "Construindo imagem Docker",
            "Executando testes",
            "Deploy no Kubernetes",
        ]
        for i, stage in enumerate(stages):
            self.log_message(f"Iniciando: {stage}")
            time.sleep(2)  # Simula processamento
            progress_bar.update_bar((i + 1) / len(stages) * 100)
            self.log_message(f"Concluído: {stage}")

    def update_deploy_status(self):
        return "Status atual do deploy:\nPods: 3/3\nServiços: OK\nIngress: Configurado"

def main():
    manager = DeployManager()
    manager.load_config()

    # Layout da aplicação
    config_tab = [
        [sg.Text("URL do Repositório Git"), sg.Input(default_text=manager.git_repo, key="git_repo")],
        [sg.Text("Caminho do Dockerfile"), sg.Input(default_text=manager.docker_file, key="docker_file")],
        [sg.Text("Caminho do kubeconfig"), sg.Input(default_text=manager.k8s_config, key="k8s_config")],
        [sg.Text("URL do GitLab"), sg.Input(default_text=manager.gitlab_url, key="gitlab_url")],
        [sg.Button("Salvar Configuração", key="save_config")],
    ]

    pipeline_tab = [
        [sg.Text("Pipeline de Deploy")],
        [sg.ProgressBar(100, orientation='h', size=(40, 20), key="progress")],
        [sg.Button("Executar Pipeline", key="run_pipeline")],
    ]

    deploy_tab = [
        [sg.Text("Status do Deploy")],
        [sg.Multiline(manager.update_deploy_status(), size=(60, 10), key="deploy_status", disabled=True)],
        [sg.Button("Atualizar Status", key="update_status")],
    ]

    logs_tab = [
        [sg.Text("Logs do Sistema")],
        [sg.Multiline("\n".join(manager.log_messages), size=(60, 20), key="logs", disabled=True)],
    ]

    layout = [
        [sg.TabGroup([
            [sg.Tab("Configuração", config_tab),
             sg.Tab("Pipeline", pipeline_tab),
             sg.Tab("Deploy", deploy_tab),
             sg.Tab("Logs", logs_tab)],
        ])]
    ]

    window = sg.Window("Deploy Automation Tool", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == "save_config":
            manager.git_repo = values["git_repo"]
            manager.docker_file = values["docker_file"]
            manager.k8s_config = values["k8s_config"]
            manager.gitlab_url = values["gitlab_url"]
            manager.save_config()
            window["logs"].update("\n".join(manager.log_messages))

        if event == "run_pipeline":
            progress_bar = window["progress"]
            progress_bar.update_bar(0)
            manager.run_pipeline(progress_bar)
            window["logs"].update("\n".join(manager.log_messages))

        if event == "update_status":
            status = manager.update_deploy_status()
            window["deploy_status"].update(status)

    window.close()

if __name__ == "__main__":
    main()
