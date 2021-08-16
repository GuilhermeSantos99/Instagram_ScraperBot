from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from random import randint
from time import sleep

class Instagram_ScraperBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        sleep(randint(5, 6)) # Pausa.

        caixa_usuário = driver.find_element_by_xpath('//input[@name="username"]')
        caixa_usuário.click() # Clica na caixa "usuário".
        caixa_usuário.clear() # Limpa a caixa, caso haja algo.
        caixa_usuário.send_keys(self.username) # Digita o usuário informada.
        
        caixa_senha = driver.find_element_by_xpath('//input[@name="password"]')
        caixa_senha.click() # Clica na caixa "password"
        caixa_senha.clear() # Limpa a caixa, caso haja algo.
        caixa_senha.send_keys(self.password) # Digita a senha informada.

        sleep(randint(2, 4)) # Pausa.
        caixa_senha.send_keys(Keys.RETURN) # Aperta o botão "Enter".

        self.raspando_seguidores()

    def raspando_seguidores(self):

        contador = 0 
        seg_num = int(input('Digite o número de usuários coletados: '))
        user_alvo = input('Digite o perfil do alvo: @').strip().lower()

        driver = self.driver
        driver.get(f'https://www.instagram.com/{user_alvo}/')

        sleep(randint(3, 4)) # Pausa.
        driver.find_elements_by_class_name('-nal3')[1].click() # Clica no botão 'Seguidores'.
        
        sleep(5) # Pausa.
        pop_up = driver.find_element_by_xpath("//div[@class='isgrP']")
        scroll = 0
        
        while True:
            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', pop_up
                ) # Rola a página do pop-up para poder carregar os usuários. 
            
            sleep(1) # Pausa.
            scroll += 1
        
            hrefs = driver.find_elements_by_tag_name('a') # Procura os elementos da tag "hrefs".
            usernames = [elem.get_attribute("title") for elem in hrefs]
            while '' in usernames:
                usernames.remove('')
            
            contador = len(usernames)
            if contador >= seg_num: 
                break
            
            print(f'{contador} usernames salvos...')
        del usernames[seg_num:]

        with open(f'seguidores_de_@{user_alvo}.txt', 'w') as arquivo:
            for username in usernames:
                if username != '':
                    arquivo.write(str('@' + username) + '\n')           

Instagram_ScraperBot = Instagram_ScraperBot('Enter your username here', 'Enter your password here')
Instagram_ScraperBot.login()
