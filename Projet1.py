import requests
from bs4 import BeautifulSoup

urlo = "http://books.toscrape.com/catalogue/category/books_1/index.html"
pageo = requests.get(urlo)

soupo = BeautifulSoup(pageo.content, 'html.parser')




#Récupérer l'URL de la page cf : commentaire au niveau du rating


Title = soupo.find("img").get('alt')

URL_page = soupo.find('a', title = Title).get('href')



print(URL_page)

#-----------------------------------------------------------------------------------------------

url = "http://books.toscrape.com/catalogue/.." + URL_page
print(url) 

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')


#récupération du titre 

print(soup.h1.string)


#récupération de : UPC, Prix avec taxes, Prix sans taxes et nbr dispo


Tableau = {}

infos_th = soup.find_all("th")
infos_td = soup.find_all("td")

print(infos_th)
print(infos_td)

for Colonne1, Colonne2 in zip(infos_th, infos_td):

    Tableau[Colonne1.text] = Colonne2.text

Tableau.pop("Product Type")
Tableau.pop('Tax')
Tableau.pop("Number of reviews")

print(Tableau)


#Récupération de la description 


Description = soup.find("div", id="product_description").next_sibling.next_sibling
print(Description.text)


#Récupération des notes ( cf : class p avec star-rating + le nombre d'étoiles)


get_number_stars = soup.find( "p", class_="star-rating")


review = get_number_stars.get('class')[1]

print(review)




#Récupérer la catégory 

Category = soup.find("li", class_="active").previous_sibling.previous_sibling

print(Category.text)




#Récupérer l'URL de l'image


URL_image = soup.find("img")

print("http://books.toscrape.com/"+ URL_image.get('src'))
