# Report de Mercado 

## "pip3 install mplcyberpunk" e "pip3 install yfinance" no terminal.

# Importação de bibliotecas
import yfinance as yf #cotações yahoo finance
import pandas as pd #manipulação e análise de dados
import matplotlib.pyplot as plt #grafico
import mplcyberpunk #estilo do grafico 


# 1. Pegar cotações últimos 5 dias
tickers = ["^BVSP", "^GSPC", "BRL=X", "BTC-USD"]

dados_mercado = yf.download(tickers, period = "5d")
dados_mercado = dados_mercado["Adj Close"] # Coluna "Adj Close" para pegar apenas a coluna que mostra o fechamento


# 2. Tratar dados coletados
dados_mercado = dados_mercado.dropna() # "Drop NA" para não carregar dados faltantes (finais de semana por exemplo)
dados_mercado.columns = ["Dolar", "Ibovespa", "S&P500", "Bitcoin"] # Renomear colunas para não aparecer o nome como ticker

'''
# 3. Gráficos de performance

#IBOV GRÁFICO
plt.style.use("cyberpunk") # Chamando o modelo cyberpunk de estilo de gráfico
plt.plot(dados_mercado["Ibovespa"]) # Criando gráfico de ibov
plt.title("IBOVESPA") # Dando título ao gráfico
plt.savefig("ibovespa.png") # Salvar a imagem do gráfico criado

plt.show() # Mostra o gráfico 


#DÓLAR GRÁFICO
plt.plot(dados_mercado["Dolar"]) 
plt.title("DÓLAR") 
plt.savefig("dolar.png") 

plt.show() 


#S&P500 GRÁFICO
plt.plot(dados_mercado["S&P500"]) 
plt.title("S&P500") 
plt.savefig("s&p500.png") 

plt.show() 

#BITCOIN GRÁFICO
plt.plot(dados_mercado["Bitcoin"]) 
plt.title("Bitcoin") 
plt.savefig("bitcoin.png") 

plt.show() 

'''

# 4. Calcular retornos diários
retornos_diarios = dados_mercado.pct_change() # "pct_change" - calculo de porcentagem 

retorno_dolar = retornos_diarios["Dolar"].iloc[-1] # porcentagem dolar do dia anterior [-1 ]
retorno_ibovespa = retornos_diarios["Ibovespa"].iloc[-1]
retorno_sp = retornos_diarios["S&P500"].iloc[-1]
retorno_bitcoin = retornos_diarios["Bitcoin"].iloc[-1]

retorno_dolar = str(round(retorno_dolar * 100, 2)) + "%" # x100 pra calcular a porcentagem e "2" (numero de casas decimais)
retorno_ibovespa = str(round(retorno_ibovespa * 100, 2)) + "%"
retorno_sp = str(round(retorno_sp * 100, 2)) + "%"
retorno_bitcoin = str(round(retorno_bitcoin * 100, 2)) + "%"


# 5. Configurar e enviar e-mail

# "pip3 install appscript" no terminal

from appscript import app, k, mactypes

mail = app('Mail')

nova_msg = mail.make(new=k.outgoing_message) # Criar nova mensagem


nova_msg.subject.set("Relatório de Mercado") 
nova_msg.content.set(f'''Segue o relatório de mercado:

Retornos de HOJE:
                     
* Ibovespa = {retorno_ibovespa}.
* Dólar = {retorno_dolar}.
* S&P500 {retorno_sp}.
* Bitcoin {retorno_bitcoin}

* Tabela últimos 5 dias:

{dados_mercado}

Att,
Nicolas Tavares

E-mail automático com Python.


''')

nova_msg.sender.set("EMAIL REMETENTE @icloud.com")  # Configurar o remetente (conta icloud)
nova_msg.make(new=k.to_recipient, with_properties={k.address: "EMAIL DESTINATARIO @..."}) # Configurar destinatario

nova_msg.send()
