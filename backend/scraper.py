import sqlite3
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Configuração do banco de dados SQLite
db_path = os.path.abspath("vagas.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS vagas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT UNIQUE,
        link TEXT UNIQUE
    )
""")
conn.commit()

# Configurar o navegador Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Rodar em modo headless (sem abrir o navegador)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Variável para total de vagas encontradas
total_vagas_encontradas = 0

# Função para carregar todas as vagas do Vagas.com.br
def carregar_vagas_vagas():
    global total_vagas_encontradas
    print("[+] Acessando Vagas.com.br...")
    url = "https://www.vagas.com.br/vagas-de-Fleury"
    driver.get(url)
    driver.implicitly_wait(5)

    # Carregar todas as vagas clicando no botão "Mais Vagas"
    while True:
        try:
            botao = driver.find_element(By.ID, "maisVagas")
            botao.click()
            print("[+] Carregando mais vagas...")
            time.sleep(3)
        except NoSuchElementException:
            print("[+] Todas as vagas foram carregadas.")
            break

    # Coletar vagas
    base_url = "https://www.vagas.com.br"
    vagas = driver.find_elements(By.CSS_SELECTOR, "h2.cargo a")

    total = 0
    total_vagas = 0
    for vaga in vagas:
        titulo = vaga.text.strip()
        link = vaga.get_attribute("href")
        if link.startswith("/"):
            link = base_url + link

        # Inserir no banco, evitando duplicatas
        cursor.execute("INSERT OR IGNORE INTO vagas (titulo, link) VALUES (?, ?)", (titulo, link))
        print(f"[+] {titulo} - {link}")
        total_vagas += 1
        total += 1

    total_vagas_encontradas += total_vagas
    print(f"[+] Total de vagas coletadas do Grupo Fleury: {total_vagas}")

# Função para coletar vagas do NaturaCarreiras
def carregar_vagas_natura(): 
    global total_vagas_encontradas #controle do numero total de vagas encontradas!
    print("[+] Acessando NaturaCarreiras...") #Avisar que está dando certo!
    url_natura = "https://avon.wd5.myworkdayjobs.com/pt-BR/NaturaCarreiras" #link do site
    driver.get(url_natura) #Faz o Selenium acessar o site
    driver.implicitly_wait(5) #Gera um tempo de espera de 5 segundos para que o site carregue por completo

    total_vagas = 0 #0 vagas encontradas na Natura até este estágio
    pagina_atual = 1  # Controla a página atual

    while True:
        print(f"[+] Coletando vagas da página {pagina_atual}...") #enquanto houver página, ele está imprimindo "Coletando"

        # Coletar as vagas da página atual
        vagas_natura = driver.find_elements(By.CSS_SELECTOR, "a.css-19uc56f") #Selenium busca por estas DIVS para fazer o scrap

        for vaga in vagas_natura:  #tira da variável vaga e atribui à função
            titulo = vaga.text.strip() #Pega os caracteres
            link = vaga.get_attribute("href")

            # Inserir no banco, evitando duplicatas
            cursor.execute("INSERT OR IGNORE INTO vagas (titulo, link) VALUES (?, ?)", (titulo, link)) 
            print(f"[+] {titulo} - {link}")
            total_vagas += 1

        try:
            # Encontrar o botão da próxima página com base no número
            pagina_atual += 1
            botao_proxima = driver.find_element(By.XPATH, f"//button[@aria-label='page {pagina_atual}']")

            if "disabled" in botao_proxima.get_attribute("class"):  # Se estiver desativado, paramos
                print("[+] Última página alcançada. Encerrando...")
                break

            botao_proxima.click()
            print(f"[+] Avançando para a página {pagina_atual}...")
            time.sleep(3)  # Tempo para garantir o carregamento da página

        except NoSuchElementException:
            print("[+] Não há mais páginas disponíveis.")
            break  # Sai do loop quando não há mais páginas

    total_vagas_encontradas += total_vagas
    print(f"[+] Total de vagas coletadas do NaturaCarreiras: {total_vagas}")


def carregar_vagas_raizen():
    global total_vagas_encontradas
    url = "https://genteraizen.gupy.io/"
    driver.get(url)

    total_vagas = 0

    while True:
        print("Acessando Raízen na Gupy")

        # Captura os elementos <a> que contêm os links das vagas
        vagas_raizen = driver.find_elements(By.XPATH, "//a[@data-testid='job-list__listitem-href']")
        
        for vaga in vagas_raizen:
            titulo = vaga.get_attribute("aria-label").strip()  # Obtém o nome da vaga
            link = vaga.get_attribute("href")  # Obtém o link
            
            # Inserir no banco, evitando duplicatas
            cursor.execute("INSERT OR IGNORE INTO vagas (titulo, link) VALUES (?, ?)", (titulo, link))
            print(f"[+] {titulo} - {link}")
            total_vagas += 1

        conn.commit()
        
        # Tenta encontrar o botão "Próxima Página"
        try:
            botao_proximo = driver.find_element(By.XPATH, "//button[@data-testid='pagination-next-button']")
            
            # Verifica se o botão está desativado
            if botao_proximo.get_attribute("aria-disabled") == "true":
                print("[+] Última página alcançada. Encerrando...")
                break

            # Clica no botão para avançar para a próxima página
            driver.execute_script("arguments[0].click();", botao_proximo)
            print("[+] Avançando para a próxima página...")
            time.sleep(5)  # Aguarda carregamento da página

        except NoSuchElementException:
            print("[+] Botão de próxima página não encontrado. Encerrando...")
            break
    total_vagas_encontradas += total_vagas
    print(f"[+] Total de vagas coletadas da Raízen: {total_vagas}")


def carregar_vagas_cosan():
    global total_vagas_encontradas
    url = "https://cosan.gupy.io/"
    driver.get(url)
    driver.implicitly_wait(5)

    total_vagas = 0

    while True:
        print("[+] Coletando vagas da página atual...")

        # Captura os títulos das vagas
        vagas_cosan = driver.find_elements(By.XPATH, "//div[contains(@class, 'sc-d1f2599d-2')]")

        for vaga in vagas_cosan:
            titulo = vaga.text.strip()
            print(f"[+] {titulo}")
            total_vagas += 1

        # Tenta encontrar o botão da próxima página
        try:
            botao_proxima = driver.find_element(By.XPATH, "//button[@data-testid='pagination-page-button']")
            
            # Verifica se o botão está desativado
            if "disabled" in botao_proxima.get_attribute("class"):
                print("[+] Última página alcançada. Encerrando...")
                break  # Se o botão estiver desabilitado, encerra o loop.

            # Usa JavaScript para clicar no botão
            driver.execute_script("arguments[0].click();", botao_proxima)
            print("[+] Avançando para a próxima página...")
            time.sleep(5)  # Aguarda carregamento

        except NoSuchElementException:
            print("[+] Não há mais páginas disponíveis.")
            break

    total_vagas_encontradas += total_vagas
    print(f"[+] Total de vagas coletadas da Cosan: {total_vagas}")


# Executar as funções de scraping
carregar_vagas_vagas()
carregar_vagas_natura()
carregar_vagas_raizen()
carregar_vagas_cosan()

# Exibir o total de vagas encontradas
print(f"[+] Total de vagas encontradas: {total_vagas_encontradas}")

# Salvar e fechar conexões
conn.commit()
conn.close()
driver.quit()

print("[+] Scraping finalizado e dados salvos no banco de dados!")
