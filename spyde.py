import requests
from bs4 import BeautifulSoup
import openpyxl

# URL base e número de páginas para iterar
base_url = "https://getcomics.org/page/"
start_page = 1
end_page = 17

# Lista para armazenar os dados
data = []

# Loop pelas páginas
for page_num in range(start_page, end_page + 1):
    url = f"{base_url}{page_num}/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article")
        print("Quantidade de artigos:", len(articles))

        for index, article in enumerate(articles, start=1):
            post_header = article.find("div", class_="post-header-image")
            post_category = article.find("a", class_="post-category").text.strip()
            post_title_elem = article.find( "h1",class_="post-title")
            
            if post_title_elem:
                post_title = post_title_elem.text.strip()
                post_link = post_title_elem.find("a").get("href")
            else:
                post_title = ""
                post_link = ""

            # Tente obter a imagem da capa de forma mais robusta
            post_cover_elem = article.find("img")
            if post_cover_elem:
                post_cover = post_cover_elem.get("src")
            else:
                # Se a capa não estiver disponível, você pode deixar em branco ou definir um valor padrão
                post_cover = ""

            data.append({
                "id": index,
                "cover_link": post_cover,
                "publisher": post_category,
                "title": post_title,
                "link": post_link
            })
            print(f"Coletando dados da página {page_num} - {index}")
            print(f"Capa: {post_cover}")
            print(f"Editora: {post_category}")
            print(f"Título: {post_title}")
            print(f"Link: {post_link}")
            print("-" * 50)
    
    
    else:
        print(f"Erro ao carregar a página {page_num}")



# Salvar os dados em um arquivo Excel
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append(["ID", "Capa", "Editora", "Título", "Link"])

for item in data:
    sheet.append([item["id"], item["cover_link"], item["publisher"], item["title"], item["link"]])

workbook.save("comics_data.xlsx")
print("Dados salvos com sucesso em 'comics_data.xlsx'")
