#import urllib.request
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.firefox.options import Options

from selenium.common.exceptions import NoSuchElementException

import json


# 1.Entrar e logar no Esaj

url = "https://esaj.tjsp.jus.br/sajcas/login?service=https%3A%2F%2Fesaj.tjsp.jus.br%2Fesaj%2Fj_spring_cas_security_check"

option = Options()
driver = webdriver.Firefox(options=option)


driver.get(url)

# colocando em variaveis os itens css selector
login_path = '#usernameForm'
password_path = '#passwordForm'
botao_path = '#pbEntrar'

# criando variaveis para encontrar e preencher
login_element = driver.find_element_by_css_selector(login_path)
password_element = driver.find_element_by_css_selector(password_path)
botao_element = driver.find_element_by_css_selector(botao_path)

#login e senha
loginsaj = input('Digite seu CPF sem pontos: ')
senhasaj = input('Digite sua senha: ')

# dados a enviar para login
login_element.send_keys(loginsaj)
password_element.send_keys(senhasaj)

#clicando para logar
botao_element.click()

# esperando logar para continuar
time.sleep(2)

#url para consulta
driver.get("https://esaj.tjsp.jus.br/esaj/portal.do?servico=740000")

#encontrando "consultas processuais"
driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td[1]/ul/li[2]/a').click()
# entrando em "consultas de 1 grau"
driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td[1]/ul/li[2]/ul/li[1]/a').click()

#esperar carregar
time.sleep(2)

#endereco da consulta
driver.get('https://esaj.tjsp.jus.br/cpopg/open.do?gateway=true')

#criando lista com numero de processos
numprocessos = []

#arquivo onde estao os numeros para consultar
processotabela = open('proc.csv', 'r')
#lendo a planilha
leitor = csv.reader(processotabela)

#para cada linha da planilha, incluir na lista de numprocessos
for linha in leitor:
    numprocessos.append(linha)

i = 0 #iniciando o contador em 0
while i < len(numprocessos):

    numproc_path = '#numeroDigitoAnoUnificado'
    botaoconsult_path = '#botaoConsultarProcessos'

    numproc_element = driver.find_element_by_css_selector(numproc_path)
    botaoconsult_element = driver.find_element_by_css_selector(botaoconsult_path)

    numprocesso = numprocessos[i]
    #print(numprocessos[i])

    #preenchendo o numero do processo no campo de consulta
    numproc_element.clear()
    numproc_element.send_keys(numprocesso)
    #clicando no botao de consulta apos o preenchimento
    botaoconsult_element.click()

    #substituir time.sleep por um while que verifique se a url atual é diferente da anterior
    time.sleep(2)
    
    



    try:
        erro_num = driver.find_element_by_css_selector('.tabelaMensagem')
        
        
    except:
                
        try:
            #senha = driver.find_element_by_css_selector('#popupSenha')
            senha = driver.find_element_by_css_selector('div.blockUI:nth-child(9)')
        
        
        except:
                                
            try:
                proc = driver.find_element_by_css_selector('#numeroProcesso')
                
            except:
                proc = numprocesso
                
            else:
                proc = driver.find_element_by_css_selector('#numeroProcesso').text
                
            finally:
            
                vara = driver.find_elements_by_xpath('//*[@id="varaProcesso"]')[0].text
                #print(vara) teste
                
                executado = driver.find_elements_by_xpath('/html/body/div[2]/table[1]/tbody/tr[2]/td[2]')[0].text
                #print(executado) teste
                
                datamov1 = driver.find_element_by_css_selector('#tabelaUltimasMovimentacoes > tr:nth-child(1) > td:nth-child(1)').text
                #print(datamov1) // ver, em alguns casos nao puxa
            
            
                mov1 = driver.find_element_by_css_selector('#tabelaUltimasMovimentacoes > tr:nth-child(1) > td:nth-child(3)').text
               
                
                datamov2 = driver.find_element_by_css_selector('#tabelaUltimasMovimentacoes > tr:nth-child(2) > td:nth-child(1)').text
                #print(datamov2)
                
                mov2 = driver.find_element_by_css_selector('#tabelaUltimasMovimentacoes > tr:nth-child(2) > td:nth-child(3)').text
                #print(mov2)
            
            
        
            try:
                element = driver.find_element_by_id('labelSituacaoProcesso')
        
            except:
                element = status = ('Em Andamento')
        
            else:
                html_content = element.get_attribute('outerHTML')
        
                status_ = html_content.replace('<span id="labelSituacaoProcesso" class="unj-tag">','')
                status = status_.replace('</span>', '')
        
            
            finally:
                lista_rel =(proc, status, vara, executado, datamov1, mov1, datamov2, mov2)
                for x in lista_rel:
                    print(x)
        
                with open ('status.csv', 'a', newline='') as file:
                    writer = csv.writer(file, delimiter=";")
                    writer.writerow([proc, status, vara, executado, datamov1, mov1, datamov2, mov2])
        
                time.sleep(2)
        
                driver.find_element_by_css_selector('#setaVoltar').click()
        
            i += 1
            
        else:
            senha_clique = driver.find_element_by_css_selector('#botaoFecharPopupSenha')
            senha_clique.click()      
            obs = 'Pede senha'
            with open ('status.csv', 'a', newline='') as file:
                    writer = csv.writer(file, delimiter=";")
                    writer.writerow([numprocesso, obs])
            i += 1
        
        
    else:
        zerar_numproc = driver.find_element_by_css_selector('#numeroDigitoAnoUnificado')
        zerar_numproc.clear()
        #numproc_element.clear()
        erro_obs = 'Numero Invalido'
        with open ('status.csv', 'a', newline='') as file:
                    writer = csv.writer(file, delimiter=";")
                    writer.writerow([numprocesso, erro_obs])
        time.sleep(2)
        i += 1
    

#.tabelaMensagem #css selector de numero invalido
#/html/body/div[2]/div[1]/table #xpath de numero invalido



