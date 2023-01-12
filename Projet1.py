import requests
from bs4 import BeautifulSoup
import csv 

urlo = "http://books.toscrape.com"
pageo = requests.get(urlo)
soupo = BeautifulSoup(pageo.content, 'html.parser')

#Récupérer l'URL de la catégory 

url_category = soupo.find('ul', class_="nav-list").a.get("href")



#-----------------------------------------------------------------------------------------------
# création du fichier csv 
en_tete = ["Product_page_url","universal_product_code","title" ,"price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url" ]


with open('data.csv', 'w') as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=",")
    writer.writerow(en_tete)
    
#-----------------------------------------------------------------------------------------------
#nouveau soup 


fin_url = "index.html"
urls = "http://books.toscrape.com/" + url_category
pages = requests.get(urls)
soups = BeautifulSoup(pages.content, 'html.parser')

#print(urls)

# récupérer les URLS des nexts si il y en a 

Next_page_urls = []
Next_page_urls.append(urls)
Verif_nb_livre = soups.find("form", class_="form-horizontal").strong.string
#print(Verif_nb_livre)
nb_p =1

if int(Verif_nb_livre) >20:
    while nb_p < int(Verif_nb_livre)/20 :
        Next_page = soups.find('li', class_="next").a.get('href')
        if  Next_page != " ":
            nb_p = nb_p +1
            fin_url = Next_page
            urls = "http://books.toscrape.com/" + url_category[:-10] + fin_url
            #print(urls)
            pages = requests.get(urls)
            soups = BeautifulSoup(pages.content, 'html.parser')
            Next_page_urls.append(urls)
        else:
            pass
else:
    pass

#print(Next_page_urls)  

t=0

#Récupérer l'URL de la page/les pages si il y en a plusieurs

if int(Verif_nb_livre) >20:
    for url_next_pages in Next_page_urls:

        
        urls = url_next_pages
        pages = requests.get(urls)
        soups = BeautifulSoup(pages.content, 'html.parser')
        
        alt=[]

        for images in soups.find_all("img"):

            alt.append(images.get('alt'))



        URL_page =[]

        for i in range (len(alt)):

            URL_page.append(soups.find('a', title = alt[i]).get('href'))
    
        #scraping de toutes les pages de la page sur laquelle on est 

        for j in range (len(URL_page)):
              
            t = t+1   

            url = "http://books.toscrape.com/catalogue/.." + URL_page[j]


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
            Description= soup.find("div", id="product_description").next_sibling.next_sibling.text
        

            #Récupération des notes ( cf : class p avec star-rating + le nombre d'étoiles)

            get_number_stars = soup.find( "p", class_="star-rating")
            review = get_number_stars.get('class')[1]
            

            #Récupérer la catégory 
            Category = soup.find("li", class_="active").previous_sibling.previous_sibling.text
            #Récupérer l'URL de l'image

            image = soup.find("img")
            URL_image= "http://books.toscrape.com/"+ image.get('src')

            
        #ajout des données récupérés à chaque page

            data_all = [url,Tableau['UPC'],Titre,Tableau['Price (incl. tax)'],Tableau['Price (excl. tax)'],Tableau['Availability'],Description,Category,review,URL_image]

            with open('data.csv', 'a') as fichier_csv:
                writer = csv.writer(fichier_csv, delimiter=",")
                writer.writerow(data_all)


           
            print(t)
