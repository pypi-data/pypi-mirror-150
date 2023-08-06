from setuptools import setup,find_packages,Extension

def long_description():
  with open('README.md',encoding='utf-8') as f:
    desc=f.read()
  return desc
VERSION = '0.8.7'
DESCRIPTION = 'Automação do processo de classificação de solicitações de compra de Notebooks à faculdade -Trabalho Acadêmico Hipotético'
LONG_DESCRIPTION = long_description()

# Setting up
setup(
    name="ProjetoNotebook",
    version=VERSION,
    author="Lucas Almeida",
    author_email="ra00319146@pucsp.edu.br",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy','pandas','plotly','matplotlib','bs4','requests','sklearn','lxml','Selenium==3.141.0'],
    keywords=['python','pucsp','cdia'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
   include_package_data=True,
   package_data={'': ['Dados/*.tsv','Dados/Processamentos_Feitos/*.csv']},
   url='https://github.com/lc1a/ProjetoNotebook',
   entry_points={'ProjetoNotebook.Analista':'Analista=ProjetoNotebook:Analista',
                 'ProjetoNotebook.Gerente':'Gerente=ProjetoNotebook:Gerente',
                 'ProjetoNotebook.ProcessoAutomatizado':'ProcessoAutomatizado=ProjetoNotebook:ProcessoAutomatizado'}
)
