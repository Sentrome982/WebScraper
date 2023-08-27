import requests
from bs4 import BeautifulSoup
import pandas as pd

cats_wiki = 'https://en.wikipedia.org/wiki/List_of_cat_breeds'

### TAKES THE PAGE AND OUTPUTS A RESPONSE OBJECT
page = requests.get(cats_wiki)

### CHECKS IF THE PAGE DOWNLOADED SUCCESFULLY (200 is good)
#print(page.status_code)

### PRINTING THE SOURCE CODE FOR THE WEBPAGE
#print(page.text)

### CREATE A BEAUTIFUL SOUP OBJECT TO USE ON THE PAGE TO IMPROVE READABILITY
soup = BeautifulSoup(page.text, 'html.parser')

#print(soup.prettify())

### FINDS THE FIRST <a> TAG IN THE SOURCE CODE
#link = soup.find('a')
#print(link)

### FINDS ALL OF THE <a> TAGS WITHIN THE SOURCE CODE
#links = soup.find_all('a')

### FROM THE 34th <a> TAG, IT EXTRACTS THE LINK THROUGH .get('href')
#print(links[33].get('href'))

### FINDS A <table> TAG WITH THE CLASS 'wikitable'
cat_table = soup.find('table', class_='wikitable')

### DECLARING LISTS TO HOLD DATA FOR THE 7 COLUMNS
breed = []
country = []
origin = []
body_type = []
coat_length = []
pattern = []
images = []

### LOOP THROUGH THE TABLE TO LOOP THROUGH EACH ROW IN THE TABLE
for row in cat_table.find('tbody').find_all('tr'):
    breed_info = row.find_all('td')
    breed_name = row.find('th')
    
    ### MAKE SURE THAT THE HEADINGS ARE NOT APPENDED TO THE LISTS
    if len(breed_info) == 6:
        breed.append(breed_name.find(text = True))
        country.append(breed_info[0].find(text = True))
        origin.append(breed_info[1].find(text = True))
        body_type.append(breed_info[2].find(text = True))
        coat_length.append(breed_info[3].find(text = True))
        pattern.append(breed_info[4].find(text = True))
        
        ### MAKING SURE THAT THE ROW HAS AN <img> BEFORE APPENDING
        if breed_info[5].find('img'):
            images.append(breed_info[5].find('img').get('src'))
        else:
            images.append('No Image')

### CREATING A DATASET USING A DICTIONARY WITH THE COLUMN NAME AS THE KEY
cat_breed_df = pd.DataFrame(
    {'Breed': breed,
     'Country': country,
     'Origin': origin,
     'Body Type': body_type,
     'Coat Length': coat_length,
     'Pattern': pattern,
     'Images': images
    })

pd.set_option('display.max_columns', None)
cat_breed_df.set_index('Breed', inplace=True)
print(cat_breed_df.head())

        