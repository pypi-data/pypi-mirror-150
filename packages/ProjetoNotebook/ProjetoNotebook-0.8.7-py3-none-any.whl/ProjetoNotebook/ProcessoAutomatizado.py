from . import Analista
from . import Gerente
import pandas as pd
import numpy as np

class ProcessarEstudante():

  def __init__(self,i_e,dir_arq_csv,filtkmeans,driver_exe_path,headless=False):

    '''Cria uma instância da classe ProcessarEstudante que tem como função agregar todos os processos
    realizados pelas classes do módulo Analista e do módulo Gerente e, a partir das informações de
    um estudante individual,
    *classificar sua solicitação como deferida ou não,
    *encontrar o notebook que lhe será fornecido caso seja aprovado, seu preço e a data estimada de entrega para o cep do
    estudante,
    *criar uma mensagem de e-mail personalizada para o estudante contendo informações sobre sua solicitação
    *enviar a mensagem criada para o estudante
    *adiconar as informações da solicitação do estudante em um arquivo .csv que serve como histórico de solicitações.


    Parâmetros:
      *i_e= dicionário contendo as informações necessárias do estudante para o processamento, que tem formato:
       {'nome':'nome_do_estudante',
        'ra':'ra_do_estudante',
        'cod_curso':'código_do_curso_do_estudante',
        'cep':'cep_do_estudante',
        'email':'email_do_estudante',
        'renda':'renda_familiar_mensal_do_estudante',
        'escola':'código_referente_a_escola_do_estudante'
        'motivação':'nota_da_motivação_do_estudante',
        'cor':'codigo_cor_do_estudante',
        'sexo':'codigo_sexo_do_estudante'}

      *dir_arq_csv= diretório local para salvar .csv referente ao histórico das solicitações.

      *filtkmeans= Instância da classe ProjetoNotebook.Analista.FiltragemKMeans.

      *driver_exe_path= Diretório no qual se encontra o arquivo executável do WebDriver que será utilizado pelo Selenium.'''

    self.nome=i_e['nome']
    self.ra=i_e['ra']
    self.cod_curso=i_e['cod_curso']
    self.cep=i_e['cep']
    self.email=i_e['email']
    self.renda=i_e['renda']
    self.escola=i_e['escola']
    self.motivacao=i_e['motivação']
    self.cor=i_e['cor']
    self.sexo=i_e['sexo']
    self.inst_HS=Gerente.HistoricoSolicitacoes(dir_arq_csv)
    self.inst_FK=filtkmeans
    self.driver_exe_path=driver_exe_path
    self.headless=headless
    self.deferido=None
    self.mp=None
    self.nn=None
    self.inst_IE=None

  def processar(self):

    '''Método da classa ProcessarEstudante que inicia o processo de classificação
    baseado nas informações do estudante, fornecidas no parâmetro de inicialização
    "i_e" da instância criada.'''

    #Calculando Nota Normalizada:
    nn_df=pd.DataFrame({'matrícula':[self.ra],'renda':[self.renda],'escola':[self.escola],
                     'motivação':[self.motivacao],'cod_curso':[self.cod_curso],'cor':[self.cor],
                    'sexo':[self.sexo]}).set_index('matrícula')

    nn= Analista.NotasNormalizadas(tbcp=nn_df).Criar()
    nn_arr=nn.to_numpy()[0]
    self.nn=nn_arr

    #Calculando Média Ponderada:
    mp=np.dot(nn_arr,self.inst_FK.inst_NP.pesos)/np.array([sum(self.inst_FK.inst_NP.pesos)])
    self.mp=mp

    #Classifcando como deferido ou não utilizando o modelo treinado da instância da classe FiltragemKMeans
    clas_def=lambda x: 1 if x==0 else 0
    clas=clas_def(self.inst_FK.classificar(mp)[0])
    if clas==1:
      self.deferido=True
    else:
      self.deferido=False

    #Criando instância da calsse InformarEstudante com as informações do estudante e se foi deferido ou não.
    d_ie={'NOME':self.nome,'RA':self.ra,'COD_CURSO':self.cod_curso,'CEP':self.cep,'EMAIL':self.email}
    self.inst_IE= Gerente.InformarEstudante('Firefox',d_ie,self.deferido,self.driver_exe_path,self.headless)

    #Utilizando a instância para encontrar o modelo de notebook,seu preço e a data estimada de entrega para o cep
    #do estudante caso o status da solicitação do estudante seja 'Aprovada'.
    if self.deferido==True:
      self.inst_IE.achar_notebook()

    #Utilizando a instância para criar uma mensagem de e-mail personalizada para o estudante para informá-lo sobre a
    #solicitação.
    self.inst_IE.criar_mensagem_email()

    #Enviando a mensagem personalizada criada utilizando a instância
    self.inst_IE.enviar_email()

    #Adicionando dados da solicitação ao histórico de solicitações utilizando a instância da classe
    #HistoricoSolicitacoes criada na inicizalização da instância da classe ProcessarEstudante
    self.inst_IE.adicionar_ao_historico(self.inst_HS)

    #Retornando o status do envio do e-mail ao estudante
    return self.inst_IE.resposta_do_envio
