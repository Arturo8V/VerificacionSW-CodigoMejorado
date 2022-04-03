#Arturo Valero - PROYECTOS III - VIRUSTECA

from bs4 import BeautifulSoup
import requests
from googlesearch import search
from colorama import Fore


data_list=list()

def search_exploitdb(clave):

    data_list.clear()
    aux=2

    if len(clave) != 0:

        try:
            query = str(clave) + ' ' + 'site:https://www.exploit-db.com'
            print(Fore.WHITE + "\nRESULTADOS ENCONTRADOS" + "\n")
            datas=search(query, tld='com',lang='en',num=10,start=0,stop=10, pause=2.0)

            for data in datas:
                aux=1
                if("https://www.exploit-db.com/exploits" in data and len(data_list)!=0):

                    print(Fore.CYAN+"Url: "+Fore.YELLOW+' '+data)

                    data_list.append(data)

                    header = {"User-Agent": "Moz    illa/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
                    page_tree = requests.get(data, headers=header)
                    page_soup = BeautifulSoup(page_tree.content, 'html.parser')

                    titulo = page_soup.find("meta", property="og:title")
                    comprobar_titulo(titulo)

                    autor = page_soup.find("meta", property="article:author")
                    comprobar_autor(autor)

                    date = page_soup.find("meta", property="article:published_time")
                    comprobar_date(date)

                    platform = page_soup.find_all("h6", {"class": "stats-title"})
                    comprobar_platform(platform)

                    verified = page_soup.find("i", {"style": "color: #96b365"})
                    comprobar_verified(verified)

        except Exception as e:
            print(Fore.RED + "ERROR")
            print e.message
            return 0

    if(aux==1):
        return 1
    elif(aux!=1):
        print(Fore.RED + "ERROR - NO SE HAN ENCONTRADO RESULTADOS")
        return 0


def search_exploit(id):

    language=["language-txt","language-c","language-py","language-rb","language-pdf"]

    data=data_list[id]

    header = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    page_tree = requests.get(data, headers=header)
    page_soup = BeautifulSoup(page_tree.content, 'html.parser')

    for i in language:
        exploit = page_soup.find("code", {"class": i})
        if exploit:
            print(Fore.CYAN + "\nEXPLOIT :\n" + Fore.YELLOW + exploit.getText())

        elif exploit=="language.py":
            print(Fore.YELLOW + "No se ha encontrado más información")


def menu():

    print(Fore.RED + "\nBIENENIDO A VIRUSTECA - EL INVENTARIO DE EXPLOITS\n")
    salir=1

    try:

        while int(salir) == 1:
            clave = input("\033[;36m" + "Introduce una o varias palabras claves sobre un exploit/plataforma/autor/fecha\nEjemplo: Windows EternalBlue: \n")
            seguir=search_exploitdb(clave)

            if seguir!=0:
                exploit_info=input(Fore.GREEN+"¿Quieres más información acerca de un exploit listado? 1(SI) 2(NO) ")
                while(int(exploit_info)<1 or int(exploit_info)>2):

                    print(Fore.RED+"ERROR-NUMERO INTRODUCIDO NO VALIDO")
                    exploit_info = input(Fore.GREEN + "¿Quieres más información acerca de un exploit listado? 1(SI) 2(NO) ")

                if int(exploit_info)==1:

                    exploit_number=input(Fore.GREEN+"Elige un exploit para saber más información, comenzando desde el 0 ")
                    data_length=len(data_list)
                    while(int(exploit_number)>int(data_length)-1):
                        print(Fore.RED+"ERROR - NO EXISTE ESE EXPLOIT - INTRODUCE UN INDICE MENOR")
                        exploit_number = input(
                        Fore.GREEN + "Elige un exploit para saber más información, comenzando desde el 0 ")

                    search_exploit(int(exploit_number))

            salir = input(Fore.MAGENTA+"\n1 para seguir buscando exploits\nCualquier otro numero para salir\n")
    except Exception as e:
        print(Fore.YELLOW+"ERROR-EL PROGRAMA ACABARA")
        print e.message

    print(Fore.YELLOW + "\nVuelve pronto\n")

def comprobar_titulo(titulo):
    if titulo:
        print (Fore.CYAN + "Title:" + ' ' + Fore.YELLOW + titulo["content"])
    else:
        print (Fore.MAGENTA + "No se ha encontrado una descripción del exploit")

def comprobar_autor(autor):
if autor:
    print(Fore.CYAN + "Author:" + ' ' + Fore.YELLOW + autor["content"])
else:
    print(Fore.MAGENTA + "No se ha encontrado autor")

def comprobar_date(date):
    if date:
        print(Fore.CYAN + "Publish Date:" + ' ' + Fore.YELLOW + date["content"])
    else:
        print(Fore.MAGENTA + "No se ha encontrado fecha de publicación")

def comprobar_platform(platform):
    if platform:
        print(Fore.CYAN + "Platform:" + ' ' + Fore.YELLOW + platform[4].getText().strip())
    else:
        print(Fore.MAGENTA + "No se ha encontrado plataforma")

def comprobar_verified(verified):
    if verified:
        print(Fore.CYAN + "Verificado:" + ' ' + Fore.YELLOW + "YES"+"\n")
    else:
        print(Fore.CYAN + "Verificado:" + ' ' + Fore.YELLOW + "NO"+"\n")



menu()



