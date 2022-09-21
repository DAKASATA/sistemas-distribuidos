from time import time
from unicodedata import name
import requests
from bs4 import BeautifulSoup

def Data_reader(Data_name, max_lineas=None):
    with open(Data_name, 'r') as archivo:
        lineas = archivo.readlines()[1:]
        contador = 0

        for linea in lineas:
            if(contador == max_lineas):
                return

                tab = linea.split('\t')
                if tab[4] == '\n':
                    continue
                url = tab[4]
                c_url = url[:-1]
                Data = get_data_from_url(c_url)

                if Data is not None:
                    print(f'[{cont}] {Data["url"]}\n Title: {repr(Data["title"])}\n Description: {repr(Data["description"])}\n Keywords: {repr(Data["keywords"])}')
                    contador +=1

            return


def get_data_from_url(url):
    collected_data = {'url': url, 'title': None, 'description': None, 'keywords': None}
    try:
        r = requests.get(url, timeout=1)
    except Exception:
            return None

    if r.status_code == 200:
        source = requests.get(url).text
        soup = BeautifulSoup(source, features='html.parser')

        meta = soup.find("meta")
        title = soup.find("meta", {'name':"title"})
        description = soup.find("meta", {'name': "description"})
        keywords = soup.find("meta", {'name': "keywords"})

        try: 
            if keywords is None:
                return None
            else:
                description = description['content'] if description else None
                keywords = keywords['content'] if keywords else None
                
                keywords = keywords.replace(" ", "") if keywords else None
                keywords = keywords.replace(".", "") if keywords else None

        except Exception:
                return None
                title = title.get_text().replace("\n","") if title else None
                title = title.replace("\r","") if title else None
                title = title.replace("\t","") if title else None
                collected_Data['title'] = title
                collected_Data['description'] = description
                collected_Data['keywords'] = keywords 
                if collected_Data['keywords'] is None:
                    return None
                return collected_Data

        return None


if __name__ == "__main__":
    Data_name = './user-ct-test-collection-09_2.txt'
    ht = Data_reader(Data_name, 50)
