import pandas as pd
import os
from time import sleep

with open('Dados\info.txt', 'r') as arquivoTxt:
    info = arquivoTxt.readlines()
print(info)
ano = int(info[0].removesuffix('\n').strip())
mes = int(info[1].removesuffix('\n').strip())
anoFinal=int(info[2].removesuffix('\n').strip())
mesFinal=int(info[3].removesuffix('\n').strip())

dfBase = pd.DataFrame() #Criando df vazio que receberá todos os dados
while ano <= anoFinal:
    while mes <= mesFinal:
        
        #Caminho do arquivo Atual
        caminhoDados = str(f'Dados\{mes:02}-{ano}.xlsx')

        #Validando se arquivo atual existe
        if os.path.exists(caminhoDados):
            # Lê o arquivo atual
            dfDados = pd.read_excel(r'' + caminhoDados)

            # Criar uma lista com as colunas de anos
            anos = dfDados.columns[4:].tolist()

            # Transforma o dataframe em um formato longo
            df_long = pd.melt(dfDados, id_vars=['MARCA', 'MODELO', 'COD_FIPE', 'COMBUS'], value_vars=anos, var_name='Ano Modelo', value_name='Valor')

            #Removendo Linhas com Valores do campo 'Valor' vazias
            df_long = df_long.dropna(subset=['Valor'])

            #Criando coluna de período
            df_long = df_long.assign(Período=str(f'{ano}-{mes:02}'))

            # Seleciona as colunas na ordem desejada
            df_long = df_long[['Período','MARCA', 'MODELO', 'COD_FIPE', 'COMBUS', 'Ano Modelo', 'Valor']]
        
            #Concatenando dados
            dfBase = pd.concat([dfBase, df_long], axis=0, ignore_index=True)

        mes += 1
    ano += 1

# Ordena o dataframe
#dfBase = dfBase.sort_values(['MARCA', 'MODELO', 'COD_FIPE', 'COMBUS', 'Ano Modelo', 'Período'])

# Escreve o novo dataframe em um arquivo csv
dfBase.to_csv(r'Dados\dataVariationMerger.csv', sep='\t', index=False)

print('Base atualizada com Sucesso')
sleep(2)
