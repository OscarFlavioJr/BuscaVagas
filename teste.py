from bs4 import BeautifulSoup
import requests

page_to_scrape = requests.get("https://www.vagas.com.br/vagas-de-Fleury")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
vagas = soup.find_all("a.link-detalhes-vaga")
for vaga in vagas:
    print(vaga.text)