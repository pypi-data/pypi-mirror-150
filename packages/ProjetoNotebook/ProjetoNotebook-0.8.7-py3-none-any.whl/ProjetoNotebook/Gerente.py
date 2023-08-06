from . import Analista
#Bilbiotecas Necessárias
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import pandas as pd
#Incluidas no python:
import time
import re
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import csv

class HistoricoSolicitacoes():
  def __init__(self,dir_arq_csv):

    '''Inicializa uma instância da classe HistoricoSolicitacoes que tem como função armazenar novas solicitações, ler e editar
    um arquivo .csv de nome "historico_s.csv" no diretório local do usuário especificado pelo parâmetro "dir_arq_csv".
    Caso um arquivo .csv com este nome não exista no diretório local especificado pelo usuário, um novo será criado.
    Caso já exista a instância abrirá este arquivo como uma tabela do pandas e cada edição feita utilizando a instância
    terá impacto no arquivo .csv já existente.'''

    try:
      tabela_s=pd.read_csv(f'{dir_arq_csv}/historico_s.csv')
      self.tabela_s=tabela_s
      self.dir_arq_csv=dir_arq_csv
    except FileNotFoundError:
      with open(f'{dir_arq_csv}/historico_s.csv',mode='w',encoding='utf-8') as h:
        tabela_s_csv= csv.writer(h,delimiter=',')
        tabela_s_csv.writerow(['RA','Nome','Curso','CEP','Email','Deferido','Notebook','P_Notebook','Email_Enviado','DEntrega','DataEnvio'])
      tabela_s=pd.read_csv(f'{dir_arq_csv}/historico_s.csv')
      self.tabela_s=tabela_s
      self.dir_arq_csv=dir_arq_csv

  def adicionar_solicitacao(self,solicitacao):

    '''Adiciona uma, ou mais, solicitacoes ao histórico e atualiza tanto o arquivo .csv, quanto a tabela do pandas da instância.
    A solicitação deve ser passada como um dicionário no qual as chaves são os nomes das colunas do arquivo .csv (e consequentemente
    da tabela do pandas da instância) e os valores são as informações da solicitação que se deseja acrescentar.'''

    ns=pd.DataFrame(solicitacao)
    try:
      self.tabela_s=pd.concat((self.tabela_s,ns),ignore_index=True,axis=0)
      ns.to_csv(f'{self.dir_arq_csv}/historico_s.csv',mode='a',index=False,header=False)
      return 'Solicitação(oes) adicionadas.'
    except Exception as e:
      return f"Falha ao adicionar solicitação, erro: {e}"

  def deletar_solicitacao(self,RA):

    '''Deleta uma, ou mais, solicitacoes ao histórico e atualiza tanto o arquivo .csv, quanto a tabela do pandas da instância.
    Deve ser passada uma lista com os RAs dos estudantes os quais se deseja excluir as solicitacoes.'''

    tabela_nova=self.tabela_s[self.tabela_s.RA!=RA]
    tabela_nova.to_csv(f'{self.dir_arq_csv}/historico_s.csv',mode='w',index=False,header=True)
    self.tabela_s=tabela_nova

class InformarEstudante():

  def __init__(self,navWeb,info_estudante,deferido,driver_exe_path,headless=True):
    '''Inicializa uma instância da classe InformarEstudante que possui todas as informações necessárias,
     de um estudante individual, para:

     1-Caso a solicitação do estudante seja deferida:

       *defenir o notebook que será comprado, o seu preço e sua data de entrega prevista,
        utilizando:
          *A informação sobre o curso do estudante para definir o modelo do notebook;
          *A biblioteca 'selenium' para acessar o site da Dell, encontrar o modelo do notebook ,
           coletar o preço do modelo, inserir o cep do estudante na página de 'Data de entrega estimada' e
           coletar a data de entrega estimada para o cep inserido.

       *Criar uma mensagem personalizada sobre as informações da solicitação com o nome,ra,notebook que será recebido,
        e data de entrega estimada deste para ser enviada ao estudante. Utilizando a biblioteca 'email' inclusa no python.

       *Enviar um e-mail para o e-mail do estudante fornecido a partir da conta 'projetonotebookcdia@gmail.com' com a mensagem
        personalizada criada. Utilizando a biblioteca 'smtp' e 'ssl' inclusas no python.

      2-Caso a solicitação do estudante não seja deferida:

       *Criar uma mensagem personalizada sobre as informações da solicitação com o nome e ra
        para ser enviada ao estudante. Utilizando a biblioteca 'email' inclusa no python.

       *Enviar um e-mail para o e-mail do estudante fornecido a partir da conta 'projetonotebookcdia@gmail.com' com a mensagem
        personalizada criada neste caso informando sobre o não deferimento.
        Utilizando a biblioteca 'smtp' e 'ssl' inclusas no python.

    Parâmetros de incialização de uma instância:

    navweb= Navegador que será utilizado pela bilbioteca 'selenium' para realizar o WebScraping em forma de string

    info_estudantes= dicionário contendo informações do estudante cujo formato é:
    {'NOME':'nome_estudante',
     'RA':'RA_Estudante',
     'COD_CURSO':cod_curso_estudante,
     'CEP':'cep_estudante',
     'EMAIL':email_estudante}

    deferido= Valor booleano (True ou False) indicando se a solicitação do aluno foi deferida ou não.

    driver_exe_path= Diretório onde se encontra o arquivo executável do WebDriver que será utilizado pelo Selenium.

    headless= Valor booleano (True ou False) indicando se deseja que o Selenium abra uma janela do navegador ou não.
     '''

    self.navw=navWeb
    self.nome=info_estudante['NOME']
    self.ra=info_estudante['RA']
    self.curso=info_estudante['COD_CURSO']
    self.cep=info_estudante['CEP']
    self.email=info_estudante['EMAIL']
    self.deferido=deferido
    self.driver_exe_path=driver_exe_path
    self.headless=headless
    #Valor armazenado após executar o método 'achar_notebook' da instância se o parâmetro de
    #inicialização deferido for igual a True
    self.notebook=None
    self.data_de_entrega=None
    self.preco_notebook=None
    #Valor armazenado após executar o método 'criar_mensagem_email' da instância
    self.mensagem_personalizada=None
    #Valor armazenado após executar o método 'enviar_email' da instância caso tenha sido feito
    #a execução prévia do método 'criar_mensagem_email'
    self.resposta_do_envio=None
  def achar_notebook(self):

    '''Método 'achar_notebook' da instância que tem a função de:
    defenir o notebook que será comprado, o seu preço e sua data de entrega prevista,
    utilizando:
      *A informação sobre o curso do estudante para definir o modelo do notebook;
      *A biblioteca 'selenium' para acessar o site da Dell, encontrar o modelo do notebook ,
       coletar o preço do modelo, inserir o cep do estudante na página de 'Data de entrega estimada' e
       coletar a data de entrega estimada para o cep inserido.
    Não será executada caso o parâmetro de incialização 'deferido' da instância tenha o valor False.
    '''


    if self.deferido==False:
      return 'Aluno não deferido -Não receberá notebook'
    if self.navw=='Firefox':
      #Criando a instância do WebDriver utilizando a biblioteca Selenium , a partir de um arquivo executável que lida com
      #a conexão entre o script e os comandos passados ao navegador.
      if self.headless==True:
        options=FirefoxOptions()
        options.add_argument('--headless')
        driver= webdriver.Firefox(executable_path=self.driver_exe_path,options=options)
      else:
        driver= webdriver.Firefox(executable_path=self.driver_exe_path)
      #Realizando comando de espera ao driver para permitir a inicialização correta antes de realizar uma chamada.
      driver.implicitly_wait(0.5)
    else:
      return f'Não Implementado para navegador {self.navw}'

    #Definindo o notebook baseado no curso:
    if self.curso==1 or self.curso==8 or self.curso==7:
      self.notebook='latitude'
    elif self.curso==6 or self.curso==3 or self.curso==2:
      self.notebook='vostro'
    elif self.curso==9 or self.curso==5 or self.curso==4:
      self.notebook='inspiron'
    else:
      driver.close()
      return f'Curso {self.curso} Não é válido.'

    #Acessando o site da dell atarvés do driver e colocando a janela em tela-cheia.
    driver.get('https://www.dell.com/pt-br/shop/notebooks-dell/sc/laptops')
    driver.maximize_window()

    #Pausando a execução do código para permitir a abertura e expansão da janela.
    time.sleep(1)

    #Utilizando métodos do driver para encontrar os elementos da página que correspondem aos preços dos 3
    #Notebooks escolhidos para os diferentes cursos, convertendo as strings retornadas para dados do tipo
    #float e armazenando nas variáveis com nome dos modelos.
    pp=re.compile(' *\d*\S*,')
    precos=driver.find_element(by=By.CLASS_NAME,value='starting-at-price').text
    precos_float=[float(i.strip().replace('.','').replace(',','.')) for i in pp.findall(precos)]
    p_inspiron,p_vostro,p_latitude=precos_float

    #Utilizando o driver para localizar os botões de Link para as páginas de compra de cada notebook.
    compre_inspiron=driver.find_element(by=By.LINK_TEXT,value='Compre o Inspiron')
    compre_vostro=driver.find_element(by=By.LINK_TEXT,value='Compre o Vostro')
    compre_latitude=driver.find_element(by=By.LINK_TEXT,value='Compre o Latitude')

    #Filtrando qual página de compra acessar através do parâmetro fornecido.
    if self.notebook=='inspiron':

      #Utilizando o driver para clicar no link de compra do modelo Inspiron e pausando a execução do
      #código para a abertura correta da página.
      compre_inspiron.click()
      time.sleep(1)

      #Clicando no botão de 'Aceitar' do pop-up referente a cookies.
      driver.find_element(by=By.CSS_SELECTOR,value='a.cc-btn:nth-child(2)').click()

      #Lidando com erros relacionados a outro tipo de pop-up que ocasionalmente aparace quando
      #tentando acessar o site.
      try:

        #Pausar a execução do código por 5 segundos para dar tempo do pop-up tornar-se visível na tela
        time.sleep(5)
        #Caso pop-up apareça:
        #Mudar foco do WebDriver para a janela do pop-up, encontrar e clicar no botão que fecha o pop-up.
        driver.switch_to.frame(driver.find_element(by=By.ID,value='iframeSurvey'))
        driver.find_element(by=By.CSS_SELECTOR,value='#noButtonIPDell').click()
        #Voltar o foco do WebDriver para a página principal do site.
        driver.switch_to.default_content()

      except NoSuchElementException:

        #Caso pop-up não apareça: Continuar com a execução normalmente
        pass

      #Encontrar e clicar no botão 'Data estimada de entrega' disponível sob o modelo do notebook que
      #abre um novo pop-up na página requisitando a inserção do cep.
      driver.find_element(by=By.CLASS_NAME,value='cf-view-dates').click()

      #Utilizando o Driver para encontrar a caixa de texto onde deve-se digitar o cep e inserindo
      #O cep passado como parâmetro na caixa.
      cep_input=driver.find_element(by=By.CLASS_NAME,value='zip-code')
      cep_input.send_keys(self.cep)

      #Pausando execução do código para esperar a inserção do cep.
      time.sleep(1)

      #Encontrando e clicando no botão que envia o cep inserido e começa o cálculo da data estimada de
      #entrega na página.
      driver.find_element(by=By.CSS_SELECTOR,value='.btn').click()

      #Pausando a execução do código para esperar o cálculo da data estimada de entrega.
      time.sleep(1)

      #Encontrando e armazenando a data calculada disponibilizada no site a partir do cep inserido na variável data_de_entrega
      #e fechando o driver.
      data_de_entrega=driver.find_element(by=By.CSS_SELECTOR,value='p.cf-delivery-options:nth-child(5) > b:nth-child(1)').text
      self.data_de_entrega=data_de_entrega
      self.preco_notebook=p_inspiron
      driver.close()

      return (p_inspiron,data_de_entrega)

    elif self.notebook=='vostro':

      #Mesma Implementação porém é necesário lidar com as especificidades das páginas acessadas sendo elas diferentes para cada
      #notebook.
      compre_vostro.click()
      time.sleep(1)

      driver.find_element(by=By.CSS_SELECTOR,value='a.cc-btn:nth-child(2)').click()

      try:

        time.sleep(5)
        driver.switch_to.frame(driver.find_element(by=By.ID,value='iframeSurvey'))
        driver.find_element(by=By.CSS_SELECTOR,value='#noButtonIPDell').click()
        driver.switch_to.default_content()

      except NoSuchElementException:

        pass

      driver.find_element(by=By.CSS_SELECTOR,value='#v3510w7012w > section:nth-child(1) > div:nth-child(7) > div:nth-child(2) > div:nth-child(2)').click()

      cep_input=driver.find_element(by=By.CLASS_NAME,value='zip-code')
      cep_input.send_keys(self.cep)

      time.sleep(1)

      driver.find_element(by=By.CSS_SELECTOR,value='.btn').click()

      time.sleep(1)

      data_de_entrega=driver.find_element(by=By.CSS_SELECTOR,value='p.cf-delivery-options:nth-child(5) > b:nth-child(1)').text
      self.data_de_entrega=data_de_entrega
      self.preco_notebook=p_vostro
      driver.close()

      return (p_vostro,data_de_entrega)

    elif self.notebook=='latitude':
      #Mesma Implementação porém é necesário lidar com as especificidades das páginas acessadas sendo elas diferentes para cada
      #notebook.
      compre_latitude.click()
      time.sleep(1)

      driver.find_element(by=By.CSS_SELECTOR,value='a.cc-btn:nth-child(2)').click()

      try:

        time.sleep(5)
        driver.switch_to.frame(driver.find_element(by=By.ID,value='iframeSurvey'))
        driver.find_element(by=By.CSS_SELECTOR,value='#noButtonIPDell').click()
        driver.switch_to.default_content()

      except NoSuchElementException:

        pass

      driver.find_element(by=By.CLASS_NAME,value='cf-view-dates').click()

      cep_input=driver.find_element(by=By.CLASS_NAME,value='zip-code')
      cep_input.send_keys(self.cep)

      time.sleep(1)

      driver.find_element(by=By.CSS_SELECTOR,value='.btn').click()

      time.sleep(3)

      data_de_entrega=driver.find_element(by=By.CSS_SELECTOR,value='p.cf-delivery-options:nth-child(5) > b:nth-child(1)').text
      self.data_de_entrega=data_de_entrega
      self.preco_notebook=p_latitude
      driver.close()
      return (p_latitude,data_de_entrega)
    else:
      return "Não Implementado para Outros Modelos"

  def criar_mensagem_email(self):

    '''Método 'criar_mensagem_email' da instância que tem a fução de:

    Criar uma mensagem personalizada sobre as informações da solicitação com o nome,ra,notebook que será recebido,
    e data de entrega estimada deste para ser enviada ao estudante. Utilizando a biblioteca 'email' inclusa no python.

    Não será executada caso o parâmetro de inicialização "deferido" da classe tiver o valor True e o método "achar_notebook"
    ainda não tiver sido executado.
    '''

    sender_email = "projetonotebookcdia@gmail.com"
    receiver_email= self.email
    message=MIMEMultipart('alternative')
    message['Subject']='Resposta Referente a sua Solicitação de Compra de Notebook'
    message['From']= sender_email
    message['To']= receiver_email

    if self.deferido==True:

      if self.notebook==None:
        return "Execute o método achar_notebook da instância para coletar as informações do notebook já que o aluno foi deferido"

      MensagemDoEmailTxt=f"""\
      Olá {self.nome}, Tudo bem?
      A universidade PUC-SP manda este e-mail com felicidade para informá-lo que a sua solicitação de compra de notebook foi deferida!
      Queremos oferecer a nossos estudantes todas as oportunidades e ferramentas necessárias para seu sucesso
      e por isso já realizamos a compra do seu notebook de modelo {self.notebook} da marca Dell que será enviado ao seu endereço fornecido
      na matrícula.
      A data estimada de entrega, de acordo com o site da Dell no qual foi relizada a compra, é {self.data_de_entrega}.

      Mensagem Enviada Automaticamente por: ProjetoNotebook, para o aluno de RA: {self.ra}."""

      MensagemDoEmailHtml=f"""\
      <html>
        <body>
          <h1>Olá <strong>{self.nome}</strong>,Tudo Bem?</h1><br>
          <h2>A Universidade <strong><a href="https://www.pucsp.br/home">PUC-SP</a></strong> manda este e-mail com felicidade para informá-lo<br>
          que a sua solicitação de compra de notebook foi <strong>Deferida!</strong><br></h2>
          <h3>Queremos oferecer a nossos estudantes todas as oportunidades e ferramentas necessárias para seu sucesso<br>
          e por isso <strong>Já realizamos a compra do seu notebook</strong><br></h3>
          <h3><strong>Modelo:</strong> <em>{self.notebook}</em><br>
          <strong>Da Marca:</strong> <em><a href="https://www.dell.com/pt-br">DELL</a></em><br>
          Que será enviado ao seu endereço fornecido na matrícula.<br></h3>
          <h3>A <strong>data estimada de entrega</strong>, de acordo com o site no qual foi relizada a compra, é <em>{self.data_de_entrega}</em>.<br>
          <h3>Mensagem Enviada Automáticamente<br>
          <strong>Por:</strong> <em>ProjetoNotebook</em><br>
          <strong>Para:</strong> Aluno de RA: <em>{self.ra}</em></h3>
        </body>
      </html>
      """

    else:

      MensagemDoEmailTxt=f"""\
      Olá {self.nome}, Tudo bem?
      A universidade PUC-SP manda este e-mail para informá-lo que a sua solicitação de compra de notebook não
      foi deferida.
      Sentimos muito por não ser possível atender a sua solicitação no momento.

      Mensagem Enviada Automaticamente por: ProjetoNotebook, para o aluno de RA: {self.ra}."""

      MensagemDoEmailHtml=f"""\
      <html>
        <body>
          <h1>Olá <strong>{self.nome}</strong>,Tudo Bem?</h1><br>
          <h2>A Universidade <strong><a href="https://www.pucsp.br/home">PUC-SP</a></strong> manda este e-mail para informá-lo<br>
          que a sua solicitação de compra de notebook <strong>Não Foi Deferida.</strong><br></h2>
          <h3>Sentimos Muito por não ser possível atender sua solicitação no momento.</h3><br>
          <h3>Mensagem Enviada Automáticamente<br>
          <strong>Por:</strong> <em>ProjetoNotebook</em><br>
          <strong>Para:</strong> Aluno de RA: <em>{self.ra}</em></h3>
        </body>
      </html>
      """
    part1=MIMEText(MensagemDoEmailTxt,'plain')
    part2=MIMEText(MensagemDoEmailHtml,'html')
    message.attach(part1)
    message.attach(part2)
    self.mensagem_personalizada=message
    return message

  def enviar_email(self):
    '''método "enviar_email" da instância que tem a função de:

    Enviar um e-mail para o e-mail do estudante fornecido a partir da conta 'projetonotebookcdia@gmail.com' com a mensagem
    personalizada criada. Utilizando a biblioteca 'smtp' e 'ssl' inclusas no python.

    Não será executado caso o método "criar_mensagem_email" da instância ainda não tiver sido executado.
    '''
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "projetonotebookcdia@gmail.com"
    password = "a3sQ2pw3C1#Rz"
    receiver_email= self.email
    if self.mensagem_personalizada==None:
      return "O método criar_mensagem_email da instância deve ser executado primeiro para gerar a mensagem que será mandada."
    context = ssl.create_default_context()
    try:
      server = smtplib.SMTP(smtp_server,port)
      server.starttls(context=context)
      server.login(sender_email, password)
      message=self.mensagem_personalizada.as_string()
      server.sendmail(sender_email,receiver_email,message)
      resp='E-mail Enviado!'
    except Exception as e:
      resp=f"Erro ao enviar e-mail: {e}"
    finally:
      server.quit()
      self.resposta_do_envio=resp
      return resp
  def adicionar_ao_historico(self,historico):

    '''Método da instância que tem como função adicionar as informações da solicitação
    do estudante à um arquivo .csv utilizando a classe HistoricoSolicitacoes.'''

    data_atual=f'{datetime.datetime.today().day}/{datetime.datetime.today().month}/{datetime.datetime.today().year}'
    solicitacao={'RA':[self.ra],'Nome':[self.nome],'Curso':[self.curso],'CEP':[self.cep],'Email':[self.email],'Deferido':[self.deferido],
                "Notebook":[self.notebook],'P_Notebook':[self.preco_notebook],'Email_Enviado':[self.resposta_do_envio],
                 'DEntrega':[self.data_de_entrega],'DataEnvio':[data_atual]}
    return historico.adicionar_solicitacao(solicitacao)
