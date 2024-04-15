import psutil
import time
import pyfiglet
from termcolor import colored
from datetime import datetime
import subprocess
import re

# Função para exibir o texto RedMoon em ASCII art
def display_redmoon():
    red_ascii_art = pyfiglet.figlet_format("Red", font="slant")
    moon_ascii_art = pyfiglet.figlet_format("Moon", font="slant")
    red_colored = colored(red_ascii_art, 'red')
    combined_art = ""
    for red_line, moon_line in zip(red_colored.split('\n'), moon_ascii_art.split('\n')):
        combined_art += red_line + moon_line + "\n"
    print(combined_art)

# Função para exibir o menu
def exibir_menu():
    print("Selecione uma opção:")
    print("1. Iniciar monitoramento")
    print("2. Sair")
    print("3. Clonar rede Wi-Fi")

# Função para classificar o comportamento como normal ou suspeito
def classificar_comportamento(comportamento):
    # Se o comportamento for "Comportamento normal", retorne 'normal'
    if comportamento == "Comportamento normal":
        return "normal"
    else:
        return "suspeito"

# Função para determinar o comportamento com base nas métricas
def determinar_comportamento(cpu_percent, network_traffic, last_network_traffic):
    # Suponha que você defina uma média e um limite de desvio padrão para o uso da CPU e para o tráfego de rede
    cpu_media = 50
    cpu_desvio_padrao = 10
    network_media = 1000  # bytes (1MB)
    network_desvio_padrao = 500  # bytes (500KB)

    # Verifique se o uso da CPU está acima do limite
    if cpu_percent > cpu_media + cpu_desvio_padrao:
        return "Uso anormal da CPU", 0, 0

    # Obter o número de bytes enviados e recebidos no último segundo
    bytes_enviados = network_traffic.bytes_sent - last_network_traffic.bytes_sent
    bytes_recebidos = network_traffic.bytes_recv - last_network_traffic.bytes_recv

    # Verifique se o tráfego de rede está acima do limite
    if bytes_enviados > network_media + network_desvio_padrao or bytes_recebidos > network_media + network_desvio_padrao:
        return "Tráfego de rede suspeito", bytes_enviados, bytes_recebidos

    # Se não houver desvios detectados, retorne um comportamento normal
    return "Comportamento normal", 0, 0

# Função para monitorar o comportamento do sistema
def monitorar_comportamento():
    last_network_traffic = psutil.net_io_counters()
    while True:
        # Coleta de métricas do sistema (exemplo: uso de CPU, atividade de rede, etc.)
        cpu_percent = psutil.cpu_percent()
        network_traffic = psutil.net_io_counters()

        # Determinar o comportamento com base nas métricas coletadas
        comportamento, bytes_enviados, bytes_recebidos = determinar_comportamento(cpu_percent, network_traffic, last_network_traffic)

        # Atualizar os valores da última medição de tráfego de rede
        last_network_traffic = network_traffic

        # Classificar o comportamento usando IA
        classificacao = classificar_comportamento(comportamento)

        # Tomar ação com base na classificação (exemplo: alertar o usuário, bloquear atividade, etc.)
        if classificacao == 'suspeito':
            alertar_usuario(comportamento, bytes_enviados, bytes_recebidos)

        # Intervalo de verificação do comportamento
        time.sleep(1)

# Função para alertar o usuário sobre comportamento suspeito
def alertar_usuario(comportamento, bytes_enviados, bytes_recebidos):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - Comportamento suspeito detectado: {comportamento}")
    print(f"{timestamp} - Bytes enviados: {bytes_enviados}")
    print(f"{timestamp} - Bytes recebidos: {bytes_recebidos}")

# Função para clonar uma rede Wi-Fi
def clonar_rede_wifi():
    try:
        # Solicitar ao usuário o nome da rede Wi-Fi que deseja clonar
        nome_rede = input("Digite o nome da rede Wi-Fi que deseja clonar: ")

        # Use o comando 'iwconfig' para listar as interfaces de rede Wi-Fi disponíveis
        interfaces_wifi = subprocess.check_output(["iwconfig"], universal_newlines=True)

        # Encontre a interface de rede Wi-Fi disponível
        interface_wifi = None
        for linha in interfaces_wifi.split('\n'):
            if 'IEEE 802.11' in linha:
                interface_wifi = linha.split()[0]
                break

        if interface_wifi:
            # Use o comando 'ifconfig' para configurar a interface de rede Wi-Fi com o nome da rede desejada
            subprocess.run(["ifconfig", interface_wifi, "down"])
            subprocess.run(["iwconfig", interface_wifi, "essid", nome_rede])
            subprocess.run(["ifconfig", interface_wifi, "up"])

            print(f"Interface de rede Wi-Fi '{interface_wifi}' clonada com sucesso para '{nome_rede}'.")

            # Mostrar os pacotes recebidos/enviados na rede clonada
            mostrar_pacotes(interface_wifi)

        else:
            print("Nenhuma interface de rede Wi-Fi disponível.")

    except subprocess.CalledProcessError as e:
        print("Erro ao executar o comando:", e)

# Função para mostrar os pacotes recebidos/enviados na rede clonada
def mostrar_pacotes(interface_wifi):
    try:
        # Usar o comando 'tcpdump' para mostrar os pacotes recebidos/enviados na interface de rede Wi-Fi
        print("Pacotes recebidos/enviados na rede clonada:")
        subprocess.run(["tcpdump", "-i", interface_wifi])

    except subprocess.CalledProcessError as e:
        print("Erro ao executar o comando:", e)

# Função principal
if __name__ == "__main__":
    display_redmoon()
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            print("Monitorando...")
            monitorar_comportamento()
        elif opcao == "2":
            print("Saindo...")
            break
        elif opcao == "3":
            clonar_rede_wifi()
        else:
            print("Opção inválida. Tente novamente.")
