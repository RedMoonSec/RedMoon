import psutil
import time
import pyfiglet
from termcolor import colored

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
    network_media = 100  # bytes (1MB)
    network_desvio_padrao = 50  # bytes (500KB)

    # Verifique se o uso da CPU está acima do limite
    if cpu_percent > cpu_media + cpu_desvio_padrao:
        return "Uso anormal da CPU"

    # Obter o número de bytes enviados e recebidos no último segundo
    bytes_enviados = network_traffic.bytes_sent - last_network_traffic.bytes_sent
    bytes_recebidos = network_traffic.bytes_recv - last_network_traffic.bytes_recv

    # Verifique se o tráfego de rede está acima do limite
    if bytes_enviados > network_media + network_desvio_padrao or bytes_recebidos > network_media + network_desvio_padrao:
        interfaces_ativas = psutil.net_if_stats()
        interfaces_com_trafego = []
        for interface, stats in interfaces_ativas.items():
            if stats.isup and stats.speed > 0:
                interfaces_com_trafego.append(interface)
        print("DEBUG: Tráfego de rede suspeito nas seguintes interfaces:", interfaces_com_trafego)
        print("DEBUG: Bytes enviados no último segundo:", bytes_enviados)
        print("DEBUG: Bytes recebidos no último segundo:", bytes_recebidos)

        # Identifica os processos que estão consumindo mais rede
        processos_rede = {}
        for conexao in psutil.net_connections(kind='inet'):
            pid = conexao.pid
            if pid is not None:
                processo = psutil.Process(pid)
                io_rede = psutil.net_io_counters(pernic=False, nowrap=True)
                processos_rede[processo.name()] = processos_rede.get(processo.name(), 0) + io_rede.bytes_sent + io_rede.bytes_recv

        processo_mais_consumidor = max(processos_rede, key=processos_rede.get)
        print("DEBUG: Processo mais consumidor de rede:", processo_mais_consumidor)

        return "Tráfego de rede suspeito"

    # Se não houver desvios detectados, retorne um comportamento normal
    return "Comportamento normal"

# Função para monitorar o comportamento do sistema
def monitorar_comportamento():
    last_network_traffic = psutil.net_io_counters()
    while True:
        # Coleta de métricas do sistema (exemplo: uso de CPU, atividade de rede, etc.)
        cpu_percent = psutil.cpu_percent()
        network_traffic = psutil.net_io_counters()

        # Determinar o comportamento com base nas métricas coletadas
        comportamento = determinar_comportamento(cpu_percent, network_traffic, last_network_traffic)

        # Atualizar os valores da última medição de tráfego de rede
        last_network_traffic = network_traffic

        # Classificar o comportamento usando IA
        classificacao = classificar_comportamento(comportamento)

        # Tomar ação com base na classificação (exemplo: alertar o usuário, bloquear atividade, etc.)
        if classificacao == 'suspeito':
            alertar_usuario(comportamento)

        # Intervalo de verificação do comportamento
        time.sleep(1)

# Função para alertar o usuário sobre comportamento suspeito
def alertar_usuario(comportamento):
    print("Comportamento suspeito detectado:", comportamento)

# Função principal
if __name__ == "__main__":
    display_redmoon()
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            monitorar_comportamento()
        elif opcao == "2":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
