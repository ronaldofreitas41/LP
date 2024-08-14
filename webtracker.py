import abc 
import requests 
import bs4

def imprimir_dados(filme_info):
    for chave, valor in filme_info.items():
        print(f"{chave}", end="")
        if isinstance(valor, list):
            print()
            for item in valor:
                print(f"    - {item}")
        else:
            print(f"{valor}\n")

def main():

    #Url dos filmes para extração de dados
    print("============================================================="
        +"\nTrabalho de Linguagens de Programação I"
        +"\n"
        +"\nAlunos: Ronaldo Luiz de Freitas Santos 20.1.8113"
        +"\n        Stephane de Oliveira Matos 19.2.8983"
        +"\n"
        +"\n=============================================================")
    movies = [
        'https://pt.wikipedia.org/wiki/Titanic_(filme_de_1997)',
        'https://pt.wikipedia.org/wiki/Ben-Hur',
        'https://pt.wikipedia.org/wiki/Raiders_of_the_Lost_Ark',
        'https://pt.wikipedia.org/wiki/O_Auto_da_Compadecida_(filme)'
    ]

    opcao = 0
    while opcao != 5:
        opcao = int(input("Escolha uma opção:" 
                        +"\n1 - Titanic"
                        +"\n2 - Ben-Hur"
                        +"\n3 - Raiders of the Lost Ark"
                        +"\n4 - O Auto da Compadecida"
                        +"\n5 - Sair\n"))

        match opcao:
            case 1:
                titanic = Titanic(movies[0])
                titanic.getData()
                imprimir_dados(titanic.data)
            case 2:
                benHur = BenHur(movies[1])
                benHur.getData()
                imprimir_dados(benHur.data)
            case 3:
                raiders = Raiders(movies[2])
                raiders.getData()
                imprimir_dados(raiders.data)
            case 4:
                auto = Auto(movies[3])
                auto.getData()
                imprimir_dados(auto.data)
            case 5:
                print("Saindo...")
            case _:
                print("Opção inválida")


#Superclasse abstrata Filme
class Filmes(abc.ABC):
    def __init__(self, url):
        self.url = url

    @abc.abstractmethod
    def getData (self, url):
        pass

#Classe Titanic
class Titanic(Filmes):
    def __init__(self, url):
        Filmes.__init__(self, url)
        self.url = url
        response = requests.get(self.url)
        self.soup = bs4.BeautifulSoup(response.text, 'html.parser')
        self.data = {}
        self.getData()

    #Retorna os dados coletados da Obra
    def getData(self):
        self.getTitle()
        self.getGender()
        self.getPlot()
        self.getElenco()
        self.getMusic()
        self.getAwards()
        self.getReleaseDate()
        return self.data

    #Retorna o titulo da obra
    def getTitle(self):
        try:
            titulo = self.soup.find('h1', class_='firstHeading').text
            self.data['Titulo: '] = titulo
        except AttributeError:
            self.data['Titulo: '] = None

    #Retorna o genero da obra
    def getGender(self):
        info_box = self.soup.find('table', class_='infobox')

        if info_box:
            # Encontrando todas as <tr> dentro da tabela
            rows = info_box.find_all('tr')

            for row in rows:
                header = row.find('td', scope="row")
                if header and "Gênero" in header.get_text():
                    # Encontrando a próxima <td> onde o genero está listado
                    gender_td = header.find_next_sibling('td')

                    if gender_td:
                        # Extraindo os nomes do genero
                        gender = [a_tag.get_text() for a_tag in gender_td.find_all('a')]
                        # print(gender)
                        self.data['Gênero: '] = gender
                    break
            #Caso por algum motivo não seja possivel encontrar o genero por meio da tag <td> essa mensagem será exibida
            else:
                print("Não foi possível encontrar a tag <td> com o elenco.")

    #Retorna o enredo da obra
    def getPlot(self):
        try:
            enredo = self.soup.find('h2', id='Enredo').find_next('p').text
            self.data['Enredo: '] = enredo
        except AttributeError:
            self. data['Enredo: '] = None

    #Retorna o elenco da obra
    def getElenco(self):
        info_box = self.soup.find('table', class_='infobox')

        if info_box:
            # Encontrando todas as <tr> dentro da tabela
            rows = info_box.find_all('tr')

            for row in rows:
                header = row.find('td', scope="row")
                if header and "Elenco" in header.get_text():
                    # Encontrando a próxima <td> onde o elenco está listado
                    elenco_td = header.find_next_sibling('td')

                    if elenco_td:
                        # Extraindo os nomes do elenco
                        elenco = [a_tag.get_text() for a_tag in elenco_td.find_all('a')]

                        self.data['Elenco: '] = elenco
                    break
            #Caso por algum motivo não seja possivel encontrar o elenco por meio da tag <td> essa mensagem será exibida
            else:
                print("Não foi possível encontrar a tag <td> com o elenco.")

    #Retorna a musica da obra
    def getMusic(self):
        info_box = self.soup.find('table', class_='infobox')

        if info_box:
            # Encontrando todas as <tr> dentro da tabela
            rows = info_box.find_all('tr')

            for row in rows:
                header = row.find('td', scope="row")
                if header and "Música" in header.get_text():
                    # Encontrando a próxima <td> onde o Música está listado
                    music_td = header.find_next_sibling('td')

                    if music_td:
                        # Extraindo os nomes do genero
                        music = [a_tag.get_text() for a_tag in music_td.find_all('a')]
                        # print(music)
                        self.data['Música: '] = music
                    break
            #Caso por algum motivo não seja possivel encontrar o genero por meio da tag <td> essa mensagem será exibida
            else:
                print("Não foi possível encontrar a tag <td> com o elenco.")

    #Retorna os premios da obra
    def getAwards(self):
        try:
            awards = self.soup.find('h3', id='Prêmios').find_next('p').text
            # print(awards)
            self.data['Prêmios: '] = awards
        except AttributeError:
            self. data['Prêmios: '] = None

    #Retorna a data de lançamento da obra
    def getReleaseDate(self):
        try:
            data_lancamento = self.soup.find('span', class_='bday').text
            self.data['Data_Lancamento: '] = data_lancamento
        except AttributeError:
            self.data['Data_Lancamento: '] = None


#Classe Ben-Hur
class BenHur(Filmes):
    def __init__(self, url):
        Filmes.__init__(self, url)
        self.url = url
        response = requests.get(self.url)
        self.soup = bs4.BeautifulSoup(response.text, 'html.parser')
        self.data = {}
        self.getData()

    #Retorna os dados coletados da Obra
    def getData(self):
        self.getTitle()
        self.getGender()
        self.getPlot()
        self.getElenco()
        self.getMusic()
        self.getAwards()
        self.getReleaseDate()
        return self.data

    #Retorna o titulo da obra
    def getTitle(self):
        try:
            titulo = self.soup.find('h1', class_='firstHeading').text

            self.data['Titulo: '] = titulo
        except AttributeError:
            self.data['Titulo: '] = None

    #Retorna o genero da obra
    def getGender(self):
        info_box = self.soup.find('table', class_='infobox')

        if info_box:
            # Encontrando todas as <tr> dentro da tabela
            rows = info_box.find_all('tr')

            for row in rows:
                header = row.find('td', scope="row")
                if header and "Gênero" in header.get_text():
                    # Encontrando a próxima <td> onde o genero está listado
                    gender_td = header.find_next_sibling('td')

                    if gender_td:
                        # Extraindo os nomes do genero
                        gender = [a_tag.get_text() for a_tag in gender_td.find_all('a')]
                        # print(gender)
                        self.data['Gênero: '] = gender
                    break
            #Caso por algum motivo não seja possivel encontrar o genero por meio da tag <td> essa mensagem será exibida
            else:
                print("Não foi possível encontrar a tag <td> com o elenco.")

    #Retorna o enredo da obra
    def getPlot(self):
        try:
            enredo = self.soup.find('h2', id='Enredo').find_next('p').text
            self.data['Enredo: '] = enredo
        except AttributeError:
            self. data['Enredo: '] = None

    #Retorna o elenco da obra
    def getElenco(self):
        info_box = self.soup.find('table', class_='infobox')

        if info_box:
            # Encontrando todas as <tr> dentro da tabela
            rows = info_box.find_all('tr')

            for row in rows:
                header = row.find('td', scope="row")
                if header and "Elenco" in header.get_text():
                    # Encontrando a próxima <td> onde o elenco está listado
                    elenco_td = header.find_next_sibling('td')

                    if elenco_td:
                        # Extraindo os nomes do elenco
                        elenco = [a_tag.get_text() for a_tag in elenco_td.find_all('a')]

                        self.data['Elenco: '] = elenco
                    break
            #Caso por algum motivo não seja possivel encontrar o elenco por meio da tag <td> essa mensagem será exibida
            else:
                print("Não foi possível encontrar a tag <td> com o elenco.")

    #Retorna a musica da obra
    def getMusic(self):
        info_box = self.soup.find('table', class_='infobox')

        if info_box:
            # Encontrando todas as <tr> dentro da tabela
            rows = info_box.find_all('tr')

            for row in rows:
                header = row.find('td', scope="row")
                if header and "Música" in header.get_text():
                    # Encontrando a próxima <td> onde o Música está listado
                    music_td = header.find_next_sibling('td')

                    if music_td:
                        # Extraindo os nomes do genero
                        music = [a_tag.get_text() for a_tag in music_td.find_all('a')]
                        # print(music)
                        self.data['Música: '] = music
                    break
            #Caso por algum motivo não seja possivel encontrar o genero por meio da tag <td> essa mensagem será exibida
            else:
                print("Não foi possível encontrar a tag <td> com o elenco.")

    #Retorna os premios da obra
    def getAwards(self):
        try:
            awards = self.soup.find('h2', id='Prêmios').find_next('p').text
            # print(awards)
            self.data['Prêmios: '] = awards
        except AttributeError:
            self. data['Prêmios: '] = None

    #Retorna a data de lançamento da obra
    def getReleaseDate(self):
        try:
            data_lancamento = self.soup.find('span', class_='bday').text
            self.data['Data_Lancamento: '] = data_lancamento
        except AttributeError:
            self.data['Data_Lancamento: '] = None


#Classe Raiders
class Raiders(Filmes):

    def __init__(self, url):
        Filmes.__init__(self, url)
        self.url = url
        response = requests.get(self.url)
        self.soup = bs4.BeautifulSoup(response.text, 'html.parser')
        self.data = {}
        self.getData()

    #Retorna os dados coletados da Obra
    def getData(self):
        self.getTitle()
        self.getGender()
        self.getPlot()
        self.getElenco()
        self.getMusic()
        self.getAwards()
        self.getReleaseDate()
        return self.data

    #Retorna o titulo da obra
    def getTitle(self):
        try:
            titulo = self.soup.find('h1', class_='firstHeading').text
            self.data['Titulo: '] = titulo
        except AttributeError:
            self.data['Titulo: '] = None

    #Retorna o genero da obra
    def getGender(self):
        info_box = self.soup.find('table', class_='infobox')

        if info_box:
            # Encontrando todas as <tr> dentro da tabela
            rows = info_box.find_all('tr')

            for row in rows:
                header = row.find('td', scope="row")
                if header and "Gênero" in header.get_text():
                    # Encontrando a próxima <td> onde o genero está listado
                    gender_td = header.find_next_sibling('td')

                    if gender_td:
                        # Extraindo os nomes do genero
                        gender = [a_tag.get_text() for a_tag in gender_td.find_all('a')]
                        # print(gender)
                        self.data['Gênero: '] = gender
                    break
            #Caso por algum motivo não seja possivel encontrar o genero por meio da tag <td> essa mensagem será exibida
            else:
                print("Não foi possível encontrar a tag <td> com o elenco.")

    #Retorna o enredo da obra
    def getPlot(self):
        try:
            enredo = self.soup.find('h2', id='Enredo').find_next('p').text
            self.data['Enredo: '] = enredo
        except AttributeError:
            self. data['Enredo: '] = None

    #Retorna o elenco da obra
    def getElenco(self):
        info_box = self.soup.find('table', class_='infobox')

        if info_box:
            # Encontrando todas as <tr> dentro da tabela
            rows = info_box.find_all('tr')

            for row in rows:
                header = row.find('td', scope="row")
                if header and "Elenco" in header.get_text():
                    # Encontrando a próxima <td> onde o elenco está listado
                    elenco_td = header.find_next_sibling('td')

                    if elenco_td:
                        # Extraindo os nomes do elenco
                        elenco = [a_tag.get_text() for a_tag in elenco_td.find_all('a')]

                        self.data['Elenco: '] = elenco
                    break
            #Caso por algum motivo não seja possivel encontrar o elenco por meio da tag <td> essa mensagem será exibida
            else:
                print("Não foi possível encontrar a tag <td> com o elenco.")

    #Retorna a musica da obra
    def getMusic(self):
        info_box = self.soup.find('table', class_='infobox')

        if info_box:
            # Encontrando todas as <tr> dentro da tabela
            rows = info_box.find_all('tr')

            for row in rows:
                header = row.find('td', scope="row")
                if header and "Música" in header.get_text():
                    # Encontrando a próxima <td> onde o Música está listado
                    music_td = header.find_next_sibling('td')

                    if music_td:
                        # Extraindo os nomes do genero
                        music = [a_tag.get_text() for a_tag in music_td.find_all('a')]
                        # print(music)
                        self.data['Música: '] = music
                    break
            #Caso por algum motivo não seja possivel encontrar o genero por meio da tag <td> essa mensagem será exibida
            else:
                print("Não foi possível encontrar a tag <td> com o elenco.")

    #Retorna os premios da obra
    def getAwards(self):
        try:
            awards = self.soup.find('h3', id='Prêmios_e_nomeações').find_next('p').text
            # print(awards)
            self.data['Prêmios: '] = awards
        except AttributeError:
            self. data['Prêmios: '] = None

    #Retorna a data de lançamento da obra
    def getReleaseDate(self):
        try:
            data_lancamento = self.soup.find('span', class_='bday').text
            self.data['Data_Lancamento: '] = data_lancamento
        except AttributeError:
            self.data['Data_Lancamento: '] = None

#Classe Auto da Compadecida
class Auto(Filmes):

    def __init__(self, url):
        Filmes.__init__(self, url)
        self.url = url
        response = requests.get(self.url)
        self.soup = bs4.BeautifulSoup(response.text, 'html.parser')
        self.data = {}
        self.getData()

    #Retorna os dados coletados da Obra
    def getData(self):
        self.getTitle()
        self.getGender()
        self.getPlot()
        self.getElenco()
        self.getMusic()
        self.getAwards()
        self.getReleaseDate()
        return self.data

    #Retorna o titulo da obra
    def getTitle(self):
        try:
            titulo = self.soup.find('h1', class_='firstHeading').text
            self.data['Titulo: '] = titulo
        except AttributeError:
            self.data['Titulo: '] = None

    #Retorna o genero da obra
    def getGender(self):
        info_box = self.soup.find('table', class_='infobox')

        if info_box:
            # Encontrando todas as <tr> dentro da tabela
            rows = info_box.find_all('tr')

            for row in rows:
                header = row.find('td', scope="row")
                if header and "Gênero" in header.get_text():
                    # Encontrando a próxima <td> onde o genero está listado
                    gender_td = header.find_next_sibling('td')

                    if gender_td:
                        # Extraindo os nomes do genero
                        gender = [a_tag.get_text() for a_tag in gender_td.find_all('a')]
                        # print(gender)
                        self.data['Gênero: '] = gender
                    break
            #Caso por algum motivo não seja possivel encontrar o genero por meio da tag <td> essa mensagem será exibida
            else:
                print("Não foi possível encontrar a tag <td> com o elenco.")

    #Retorna o enredo da obra
    def getPlot(self):
        try:
            enredo = self.soup.find('h2', id='Enredo').find_next('p').text
            self.data['Enredo: '] = enredo
        except AttributeError:
            self. data['Enredo: '] = None

    #Retorna o elenco da obra
    def getElenco(self):
        info_box = self.soup.find('table', class_='infobox')

        if info_box:
            # Encontrando todas as <tr> dentro da tabela
            rows = info_box.find_all('tr')

            for row in rows:
                header = row.find('td', scope="row")
                if header and "Elenco" in header.get_text():
                    # Encontrando a próxima <td> onde o elenco está listado
                    elenco_td = header.find_next_sibling('td')

                    if elenco_td:
                        # Extraindo os nomes do elenco
                        elenco = [a_tag.get_text() for a_tag in elenco_td.find_all('a')]

                        self.data['Elenco: '] = elenco
                    break
            #Caso por algum motivo não seja possivel encontrar o elenco por meio da tag <td> essa mensagem será exibida
            else:
                print("Não foi possível encontrar a tag <td> com o elenco.")

    #Retorna a musica da obra
    def getMusic(self):
        info_box = self.soup.find('table', class_='infobox')

        if info_box:
            # Encontrando todas as <tr> dentro da tabela
            rows = info_box.find_all('tr')

            for row in rows:
                header = row.find('td', scope="row")
                if header and "Música" in header.get_text():
                    # Encontrando a próxima <td> onde o Música está listado
                    music_td = header.find_next_sibling('td')

                    if music_td:
                        # Extraindo os nomes do genero
                        music = [a_tag.get_text() for a_tag in music_td.find_all('a')]
                        # print(music)
                        self.data['Música: '] = music
                    break
            #Caso por algum motivo não seja possivel encontrar o genero por meio da tag <td> essa mensagem será exibida
            else:
                print("Não foi possível encontrar a tag <td> com o elenco.")

    #Retorna os premios da obra
    def getAwards(self):
        try:
            awards = self.soup.find('h2', id='Prêmios_e_indicações').find_next('p').text
            # print(awards)
            self.data['Prêmios: '] = awards
        except AttributeError:
            self. data['Prêmios: '] = None

    #Retorna a data de lançamento da obra
    def getReleaseDate(self):
        try:
            data_lancamento = self.soup.find('span', class_='bday').text
            self.data['Data_Lancamento: '] = data_lancamento
        except AttributeError:
            self.data['Data_Lancamento: '] = None


if __name__ == '__main__':
    main()   