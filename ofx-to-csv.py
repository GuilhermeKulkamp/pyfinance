import ofxparse
import pandas as pd
import os
from datetime import datetime

# Inicializando um DataFrame vazio
df = pd.DataFrame()

# Define o diretório em que serão lidos os arquivos
diretorio = "extratos"

# Percorrendo todos os arquivos na pasta 'extratos'
for extrato in os.listdir(diretorio):
    # Verificando o tipo de arquivo
    tipo = os.path.splitext(f'{diretorio}/{extrato}')
    
    # Filtrando apenas arquivos com extensão .ofx
    if tipo[1] == '.ofx':
        # Abrindo o arquivo OFX para leitura
        with open(f"{diretorio}/{extrato}", encoding='ascii') as ofx_file:
            # Fazendo o parse do arquivo OFX para obter os dados
            ofx = ofxparse.OfxParser.parse(ofx_file)
        
        # Lista temporária para armazenar os dados das transações
        transactions_data = []
        
        # Percorrendo as contas do arquivo OFX
        for account in ofx.accounts:
            # Percorrendo as transações de cada conta
            for transaction in account.statement.transactions:
                # Adicionando cada transação à lista de dados
                transactions_data.append({
                    "conta_ID": account.account_id,
                    "ID": transaction.id,
                    "Data": transaction.date,
                    "Valor": transaction.amount,
                    "Descrição": transaction.memo,
                    "Categoria": '',

                })
        
        # Criando um DataFrame temporário a partir das transações do arquivo atual
        df_temp = pd.DataFrame(transactions_data)
        
        # Convertendo a coluna "Valor" para o tipo float (caso necessário)
        df_temp["Valor"] = df_temp["Valor"].astype(float)
        
        # Convertendo a coluna "Data" para apenas o componente de data (sem hora)
        df_temp["Data"] = df_temp["Data"].apply(lambda x: x.date())
        
        # Concatenando os dados do DataFrame temporário com o DataFrame principal
        df = pd.concat([df, df_temp])


# Salvando o DataFrame 'df' em um arquivo CSV
# O método 'to_csv' salva o DataFrame em um arquivo CSV (.csv)
# Argumento 'index=False' para evitar a inclusão do índice no arquivo CSV
# ATENÇÃO: Caso o arquivo já exista ele será sobrescrito

df.to_csv(f'{diretorio}/transacoes_extratos.csv', index=False, sep=';')

# Comentários adicionais:
# No CSV, o argumento 'sep=";"' define que o separador de colunas será o ponto e vírgula, 
# que é comum em locais onde a vírgula é usada como separador decimal (por exemplo, no Brasil).