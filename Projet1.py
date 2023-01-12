import requests
from bs4 import BeautifulSoup
import csv 

urlo = "http://books.toscrape.com/catalogue/category/books_1/index.html"
pageo = requests.get(urlo)

soupo = BeautifulSoup(pageo.content, 'html.parser')




#Récupérer l'URL de la page


Title = soupo.find("img").get('alt')

URL_page = soupo.find('a', title = Title).get('href')

#-----------------------------------------------------------------------------------------------

url = "http://books.toscrape.com/catalogue/.." + URL_page


page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')


#récupération du titre 

Titre = soup.h1.string

#récupération de : UPC, Prix avec taxes, Prix sans taxes et nbr dispo

Tableau = {}

infos_th = soup.find_all("th")
infos_td = soup.find_all("td")

#print(infos_th)
#print(infos_td)

for Colonne1, Colonne2 in zip(infos_th, infos_td):

    Tableau[Colonne1.text] = Colonne2.text

Tableau.pop("Product Type")
Tableau.pop('Tax')
Tableau.pop("Number of reviews")

#Récupération de la description 

Description = soup.find("div", id="product_description").next_sibling.next_sibling.text

#Récupération des notes ( cf : class p avec star-rating + le nombre d'étoiles)

get_number_stars = soup.find( "p", class_="star-rating")

review = get_number_stars.get('class')[1]

#Récupérer la catégory 

Category = soup.find("li", class_="active").previous_sibling.previous_sibling.text

#Récupérer l'URL de l'image

image = soup.find("img")

URL_image = "http://books.toscrape.com/"+ image.get('src')

# ajout dans un fichier CSV 

en_tete = ["Product_page_rul","universal_product_code","title" ,"price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url" ]

data_all = [url,Tableau['UPC'],Titre,Tableau['Price (incl. tax)'],Tableau['Price (excl. tax)'],Tableau['Availability'],Description,Category,review,URL_image]

with open('data.csv', 'w') as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=",")
    writer.writerow(en_tete)
    writer.writerow(data_all)


