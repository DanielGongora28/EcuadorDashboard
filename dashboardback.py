# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 20:13:33 2022

@author: PC
"""

import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import base64
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout = 'wide')

st.markdown("<h1 style ='text-align: center; color:#1687CE;'>✈🌎💰 IMPORTACIONES Y EXPORTACIONES DE ECUADOR ✈🌎💰</h1>", unsafe_allow_html =True)

@st.cache(persist=True, allow_output_mutation=True)
def load_data(url):
    df = pd.read_csv(url)
    return df
exp=pd.read_csv('Bases/ExportacionesEcuador.csv',encoding='unicode_escape')
exportaciones=load_data('Bases/Exportaciones.csv')
importaciones=load_data('Bases/03._Export._o_Import._por_Subpartida_y_País_BK.csv')
#####################
c1,c2,c3,c4=st.columns((1,1,1,1))
c1.markdown("<h3 style ='text-align: center; color:black;'>Principal Importador</h3>", unsafe_allow_html =True)
top_imp=exportaciones['País Origen'].value_counts().index[0]
c1.text('Pais: '+ str(top_imp))
################################
c2.markdown("<h3 style ='text-align: center; color:black;'>Principal Exportador</h3>", unsafe_allow_html =True)
top_exp=importaciones['País Origen'].value_counts().index[0]
c2.text('Pais: '+ str(top_exp))
################################
c3.markdown("<h3 style ='text-align: center; color:black;'>Producto Estrella</h3>", unsafe_allow_html =True)
prodest=exportaciones['Descripción Nandina'].value_counts().index[0]
c3.text('⭐: '+ str(prodest))
#################################
c4.markdown("<h3 style ='text-align: center; color:black;'>Producto mas demandado</h3>", unsafe_allow_html =True)
proddem=importaciones['Descripción Nandina'].value_counts().index[0]
c4.text('📦: '+str(proddem))
#################################
#Hacer las pestañas#
#Pais#
c1, c2 = st.columns((1,1))
c1.markdown("<h3 style ='text-align: center; color:black;'>¿Cuales son los paises que mas le venden productos a ecuador?</h3>", unsafe_allow_html =True)
importaciones2=importaciones[['Trimestre','Día','Cantidad Unidades Físicas','Descripción Nandina','Año','Num Mes','Nombre Mes','Valor Peso Neto en miles','País Origen','Valor FOB Dólar bajo Selección','Valor CIF dólar bajo Selección']]
importaciones2['Trimestre']=importaciones2.Trimestre.replace({'2019/T1':1,'2019/T2':2,'2019/T3':3,'2019/T4':4,'2020/T1':1,'2020/T2':2,'2020/T3':3,'2020/T4':4})
#importaciones2=importaciones2#
importaciones2=importaciones2.rename(columns={'Día':'Fecha','Cantidad Unidades Físicas': 'Unidades','Descripción Nandina':'Producto','Num Mes':'Codigomes','Valor Peso Neto en miles':'PesoNeto','País Origen':'Pais','Valor FOB Dólar bajo Selección': 'ValorFOB','Valor CIF dólar bajo Selección':'ValorCIB'})
importaciones2['PesoNeto']=importaciones2.PesoNeto.replace(',','.', regex=True)
importaciones2['PesoNeto']=importaciones2['PesoNeto'].astype('float')
importaciones3=importaciones2[['Pais','PesoNeto']]
importaciones3=importaciones3.groupby(['Pais'])[['PesoNeto']].sum().sort_values('PesoNeto',ascending=False).reset_index()
importacionesG=importaciones3.head(10)

importacionesG=importacionesG.sort_values(by='PesoNeto', ascending=False)
fig = px.bar(importacionesG, x = 'Pais', y='PesoNeto',
             title= '<b>Paises que mas le importan a Ecuador<b>',
             color_discrete_sequence=px.colors.qualitative.G10)


fig.update_layout(
    xaxis_title = 'Pais',
    yaxis_title = 'PesoNeto',
    template = 'simple_white',
    title_x = 0.5)

c1.plotly_chart(fig)
########################
########################
importacionesmes=importaciones2[['Pais','PesoNeto','Codigomes']]
importacionesmes=importacionesmes.groupby(['Pais','Codigomes'])[['PesoNeto']].sum().sort_values('PesoNeto',ascending=False).reset_index()
mes=pd.DataFrame()
trim=pd.DataFrame()
for i in range(1,13):
    b=importacionesmes[importacionesmes.Codigomes==i].sort_values('PesoNeto', ascending=False).head(5)[['Pais','Codigomes','PesoNeto']]
    mes=pd.concat([mes,b])
importacionestrim=importaciones2[['Pais','PesoNeto','Trimestre']]
importacionestrim=importacionestrim.groupby(['Pais','Trimestre'])[['PesoNeto']].sum().sort_values('PesoNeto',ascending=False).reset_index()

for i in range(1,5):
    a=importacionestrim[importacionestrim.Trimestre==str(i)].sort_values('PesoNeto', ascending=False).head(5)[['Pais','Trimestre','PesoNeto']]
    trim=pd.concat([trim,a])
  ##########################
c2.markdown("<h3 style ='text-align: center; color:black;'>Variaciones mensuales y trimestrales</h3>", unsafe_allow_html =True)
  #Crear un slider que las slecciones sean por mes y trimestre y depende de lo que elijan mostrar mes o trim#
option = c2.selectbox('Elija la periodicidad: ',
                        ('Mes','Trimestre'))
if option=='Mes':
    c2.dataframe(mes)
else:
    c2.dataframe(trim)
    
##########################
c3, c4 = st.columns((1,1))
c3.markdown("<h3 style ='text-align: center; color:black;'>¿Cuales son los paises que mas le compran productos a ecuador?</h3>", unsafe_allow_html =True)
exportaciones2=exportaciones[['Trimestre','Día','Cantidad Unidades Físicas','Descripción Nandina','Año','Num Mes','Nombre Mes','Valor Peso Neto en miles','País Origen','Valor FOB Dólar bajo Selección','Valor CIF dólar bajo Selección']]
exportaciones2['Trimestre']=exportaciones2.Trimestre.replace({'2019/T1':1,'2019/T2':2,'2019/T3':3,'2019/T4':4,'2020/T1':1,'2020/T2':2,'2020/T3':3,'2020/T4':4})
exportaciones2=exportaciones2.rename(columns={'Día':'Fecha','Cantidad Unidades Físicas': 'Unidades','Descripción Nandina':'Producto','Num Mes':'Codigomes','Valor Peso Neto en miles':'PesoNeto','País Origen':'Pais','Valor FOB Dólar bajo Selección': 'ValorFOB','Valor CIF dólar bajo Selección':'ValorCIB'})
exportaciones2['PesoNeto']=exportaciones2.PesoNeto.replace(',','.', regex=True)
exportaciones2['PesoNeto']=exportaciones2['PesoNeto'].astype('float')
exportaciones3=exportaciones2[['Pais','PesoNeto']]
exportaciones3=exportaciones3.groupby(['Pais'])[['PesoNeto']].sum().sort_values('PesoNeto',ascending=False).reset_index()
exportacionesG=exportaciones3.head(10)
exportacionesG=exportacionesG.sort_values(by='PesoNeto', ascending=False)

fig2 = px.bar(exportacionesG, x = 'Pais', y='PesoNeto',
             title= '<b>Paises a los que Ecuador mas exporta<b>',
             color_discrete_sequence=px.colors.qualitative.Vivid)


fig2.update_layout(
    xaxis_title = 'Pais',
    yaxis_title = 'PesoNeto',
    template = 'simple_white',
    title_x = 0.5)        

c3.plotly_chart(fig2)
########################
#No muestra el segundo label#####
##########################
exportacionestabla=exportaciones2[['Pais','PesoNeto','Codigomes']]
exportacionestabla=exportacionestabla.groupby(['Pais','Codigomes'])[['PesoNeto']].sum().sort_values('PesoNeto',ascending=False).reset_index()
expmes=pd.DataFrame()
exptrim=pd.DataFrame()
for i in range(1,13):
    c=exportacionestabla[exportacionestabla.Codigomes==i].sort_values('PesoNeto', ascending=False).head(5)[['Pais','Codigomes','PesoNeto']]
    expmes=pd.concat([expmes,c])
exportacionestabla2=exportaciones2[['Pais','PesoNeto','Trimestre']]
exportacionestabla2=exportacionestabla2.groupby(['Pais','Trimestre'])[['PesoNeto']].sum().sort_values('PesoNeto',ascending=False).reset_index()
for i in range(1,5):
    d=exportacionestabla2[exportacionestabla2.Trimestre==str(i)].sort_values('PesoNeto', ascending=False).head(5)[['Pais','Trimestre','PesoNeto']]
    exptrim=pd.concat([exptrim,d])
############################
########################
c4.markdown("<h3 style ='text-align: center; color:black;'>Variaciones mensuales y trimestrales</h3>", unsafe_allow_html =True)
  #Crear un slider que las slecciones sean por mes y trimestre y depende de lo que elijan mostrar mes o trim#
option2 = c4.selectbox('Elija la periodicidad:',
                        ('Mensual','Trimestral'))
if option2=='Mensual':
    c4.dataframe(expmes)
elif option2=='Trimestral':
    c4.dataframe(exptrim)
##########################

st.markdown("<h3 style ='text-align: center; color:black;'>¿Cómo ha sido la evolución del CIF por exportaciones e importaciones?</h3>", unsafe_allow_html =True)

exp4=exportaciones.copy()
exp4['Valor CIF dólar bajo Selección']=exp4['Valor CIF dólar bajo Selección'].replace(',','.',regex=True).astype('float')
exp4=exp4.groupby(['Día'])[['Valor CIF dólar bajo Selección']].sum().reset_index()


imp4=importaciones.copy()
imp4['Valor CIF dólar bajo Selección']=imp4['Valor CIF dólar bajo Selección'].replace(',','.',regex=True).astype('float')
imp4=imp4.groupby(['Día'])[['Valor CIF dólar bajo Selección']].sum().reset_index()


evo5=pd.merge(exp4,imp4,how='left',on='Día')

evo5['ValorCIF-Exportaciones_0']=evo5['Valor CIF dólar bajo Selección_x'].cumsum()
evo5['ValorCIF-Importaciones_0']=evo5['Valor CIF dólar bajo Selección_y'].cumsum()
#st.write(evo5)
##Parece que el cumsum no se hiciera en importaciones###
fig3 = px.line(evo5, x='Día', y =['ValorCIF-Exportaciones_0','ValorCIF-Importaciones_0'], title = '<b>Evolucion CIF<b>',
              color_discrete_sequence=px.colors.qualitative.G10,width=1600, height=450)

# agregar detalles
fig3.update_layout(
    template = 'simple_white',
    title_x = 0.5,
    legend_title = 'Serie de tiempo Importaciones y Exportaciones :',
    xaxis_title = '<b>Fecha<b>',
    yaxis_title = '<b>ValorCIF<b>',
)  

st.plotly_chart(fig3)
##############################   
st.markdown("<h3 style ='text-align: center; color:black;'>¿Como son las exportaciones con los paises de LATAM?</h3>", unsafe_allow_html =True)
exportaciones['Valor CIF dólar bajo Selección']=exportaciones['Valor CIF dólar bajo Selección'].replace(',','.',regex=True)
exportaciones['Valor CIF dólar bajo Selección']=exportaciones['Valor CIF dólar bajo Selección'].astype('float')
exportaciones_v = exportaciones.groupby(['País Procedencia / Destino'])[['Valor CIF dólar bajo Selección']].sum().reset_index()
exportaciones_ve = exportaciones_v.sort_values(by=['Valor CIF dólar bajo Selección'], ascending = False)
exportaciones_vec = exportaciones_ve.loc[(exportaciones_ve['País Procedencia / Destino'] == 'COLOMBIA') | (exportaciones_ve['País Procedencia / Destino'] == 'PERÚ') | (exportaciones_ve['País Procedencia / Destino'] == 'BRASIL')
                    | (exportaciones_ve['País Procedencia / Destino'] == 'VENEZUELA')| (exportaciones_ve['País Procedencia / Destino'] == 'MÉXICO')| (exportaciones_ve['País Procedencia / Destino'] == 'PANAMÁ')
                    | (exportaciones_ve['País Procedencia / Destino'] == 'CHILE') | (exportaciones_ve['País Procedencia / Destino'] == 'BOLIVIA')| (exportaciones_ve['País Procedencia / Destino'] == 'ARGENTINA')
                    | (exportaciones_ve['País Procedencia / Destino'] == 'URUGUAY')| (exportaciones_ve['País Procedencia / Destino'] == 'PARAGUAY')] 
figlatam = px.bar(exportaciones_vec, x = 'País Procedencia / Destino', y='Valor CIF dólar bajo Selección', title= '<b> Exportaciones a paises de LATAM <b>',
                  width=1600, height=450)
figlatam.update_layout(
    xaxis_title = 'Países',
    yaxis_title = 'CIF',
    template = 'simple_white',
    title_x = 0.5)

st.plotly_chart(figlatam)
##############################
st.markdown("<h1 style ='text-align: center; color:#1687CE;'>📦✈🌎 PRODUCTOS DESTACADOS PARA ECUADOR 📦✈🌎</h1>", unsafe_allow_html =True)
c1, c2 = st.columns((1,1))
c1.markdown("<h3 style ='text-align: center; color:black;'>¿Cual es el tipo de mercancia que mas ingresos le da a ecuador?</h3>", unsafe_allow_html =True)
exp_sample=exportaciones[['Código de Unidades Fisicas','Descripción Nandina','Valor CIF dólar bajo Selección']]
exp_sample['Descripción Nandina']=exp_sample['Descripción Nandina'].str.replace('Las demás','Los demás')
exp_sample['Valor CIF dólar bajo Selección']=exp_sample['Valor CIF dólar bajo Selección'].astype('float')
exp_gb=exp_sample.groupby(['Descripción Nandina'])[['Valor CIF dólar bajo Selección']].sum().sort_values('Valor CIF dólar bajo Selección', ascending=False).reset_index()
grafexp=exp_gb.head(10)
sum10=grafexp['Valor CIF dólar bajo Selección'].sum()
sumall=exp_gb['Valor CIF dólar bajo Selección'].sum()
suma=sumall-sum10
dic3={'Descripción Nandina':['2041 registros restantes'],'Valor CIF dólar bajo Selección':[suma]}
dfn=pd.DataFrame(dic3, columns = ['Descripción Nandina' , 'Valor CIF dólar bajo Selección'])
grafexp=grafexp.append(dfn)
# crear gráfica
figpie = px.pie(grafexp, values = 'Valor CIF dólar bajo Selección', names ='Descripción Nandina',
             title= '<b>% Productos mejor vendidos<b>',
             color_discrete_sequence=px.colors.qualitative.G10)

# agregar detalles a la gráfica
figpie.update_layout(
    template = 'simple_white',
    legend_title = '<b>Descripcion<b>',
    title_x = 0.5)
c1.plotly_chart(figpie)

c2.markdown("<h3 style ='text-align: center; color:black;'>¿Cuáles son los productos de mayor demanda internacional provenientes de Ecuador?</h3>", unsafe_allow_html =True)

importaciones["Descripción Nandina"] = importaciones["Descripción Nandina"].replace("Los demas", "Los demás")
importaciones["Descripción Nandina"] = importaciones["Descripción Nandina"].replace("Las demás", "Los demás")
importaciones["Trimestre"] = importaciones["Trimestre"].replace("2019/T1", "1")
importaciones["Trimestre"] = importaciones["Trimestre"].replace("2019/T2", "2")
importaciones["Trimestre"] = importaciones["Trimestre"].replace("2019/T3", "3")
importaciones["Trimestre"] = importaciones["Trimestre"].replace("2019/T4", "4")
importaciones["Trimestre"] = importaciones["Trimestre"].replace("2020/T1", "1")
importaciones["Trimestre"] = importaciones["Trimestre"].replace("2020/T2", "2")
importaciones["Trimestre"] = importaciones["Trimestre"].replace("2020/T3", "3")
importaciones["Trimestre"] = importaciones["Trimestre"].replace("2020/T4", "4")
importaciones["Valor Peso Neto en miles"] = importaciones["Valor Peso Neto en miles"].replace(",", ".")
importaciones["Valor FOB Dólar bajo Selección"] = importaciones["Valor FOB Dólar bajo Selección"].replace(",", ".")
importaciones["Valor CIF dólar bajo Selección"] = importaciones["Valor CIF dólar bajo Selección"].replace(",", ".")
importaciones['Día'] = pd.to_datetime(importaciones['Día'])
importaciones["Valor Peso Neto en miles"] = pd.to_numeric(importaciones["Valor Peso Neto en miles"], errors='coerce')
importaciones["Valor FOB Dólar bajo Selección"] = pd.to_numeric(importaciones["Valor FOB Dólar bajo Selección"], errors='coerce')
importaciones["Valor CIF dólar bajo Selección"] = pd.to_numeric(importaciones["Valor CIF dólar bajo Selección"], errors='coerce')
importaciones["Cantidad Unidades Físicas"] = pd.to_numeric(importaciones["Cantidad Unidades Físicas"], errors='coerce') 

exportaciones["Descripción Nandina"] = exportaciones["Descripción Nandina"].replace("Los demas", "Los demás")
exportaciones["Descripción Nandina"] = exportaciones["Descripción Nandina"].replace("Las demás", "Los demás")
exportaciones["Trimestre"] = exportaciones["Trimestre"].replace("2019/T1", "1")
exportaciones["Trimestre"] = exportaciones["Trimestre"].replace("2019/T2", "2")
exportaciones["Trimestre"] = exportaciones["Trimestre"].replace("2019/T3", "3")
exportaciones["Trimestre"] = exportaciones["Trimestre"].replace("2019/T4", "4")
exportaciones["Trimestre"] = exportaciones["Trimestre"].replace("2020/T1", "1")
exportaciones["Trimestre"] = exportaciones["Trimestre"].replace("2020/T2", "2")
exportaciones["Trimestre"] = exportaciones["Trimestre"].replace("2020/T3", "3")
exportaciones["Trimestre"] = exportaciones["Trimestre"].replace("2020/T4", "4")
exportaciones["Valor Peso Neto en miles"] = exportaciones["Valor Peso Neto en miles"].replace(",", ".")
exportaciones["Valor FOB Dólar bajo Selección"] = exportaciones["Valor FOB Dólar bajo Selección"].replace(",", ".")
exportaciones["Valor CIF dólar bajo Selección"] = exportaciones["Valor CIF dólar bajo Selección"].replace(",", ".")
exportaciones['Día'] = pd.to_datetime(exportaciones['Día'])
exportaciones["Valor Peso Neto en miles"] = pd.to_numeric(exportaciones["Valor Peso Neto en miles"], errors='coerce')
exportaciones["Valor FOB Dólar bajo Selección"] = pd.to_numeric(exportaciones["Valor FOB Dólar bajo Selección"], errors='coerce')
exportaciones["Valor CIF dólar bajo Selección"] = pd.to_numeric(exportaciones["Valor CIF dólar bajo Selección"], errors='coerce')
exportaciones["Cantidad Unidades Físicas"] = pd.to_numeric(exportaciones["Cantidad Unidades Físicas"], errors='coerce')  
    
exportaciones = exportaciones.replace(np.nan, 0)
exportaciones2 = exportaciones.groupby(['Descripción Nandina'])[['Cantidad Unidades Físicas']].sum().reset_index()
exportaciones3 = exportaciones2.sort_values(by=['Cantidad Unidades Físicas'], ascending = False)  
exportaciones3['Descripción Nandina'] = exportaciones3['Descripción Nandina'].str[:12]
exportaciones4 = exportaciones3.head(10)


figexp = px.pie(exportaciones4, values = 'Cantidad Unidades Físicas', names ='Descripción Nandina',
             title= '<b>% Productos de mayor demanda internacional provenientes de Ecuador<b>',
             color_discrete_sequence=px.colors.qualitative.G10)

# agregar detalles a la gráfica
figexp.update_layout(
    template = 'simple_white',
    legend_title = '<b>Descripción Nandina<b>',
    title_x = 0.5)
c2.plotly_chart(figexp)
###############################
c3, c4 = st.columns((1,1))
dicindex={'Con un contenido de azufre menor o igual a 50':'S% < 50%',
     'Tortas y demás residuos sólidos de la extracción del aceite de soja (soya), incluso molidos o en «pellets».': 'Residuos Soja',
     'Máquinas automáticas para tratamiento o procesamiento de datos, portátiles, de peso inferior o igual a 10 kg, que estén constituidas, al menos, por una unidad central de proceso, un teclado y un visualizador': 'Maquinas automaticas',
     'Paquetes por correos rápidos (mensajería acelerada o courier)':'Mensajeria',
     'Aparatos de telecomunicación por corriente portadora o telecomunicación digital': 'Telecomunicaciones',
     'Reactivos de laboratorio o de diagnóstico que no se empleen en el paciente': 'Reactivos',
     'Con un porcentaje de nitrógeno superior o igual a 45% pero inferior o igual a 46% en peso (calidad fertilizante)': 'Fertilizantes nitrogenados',
     'Máquinas de capacidad unitaria, expresada en peso de ropa seca, superior a 10 kg':'Secadoras',
     'Atunes de aleta amarilla (rabiles) (thunnus albacares)': 'Atunes',
     'Con un contenido de carbono superior o igual a 0,12% en peso': '0.12% -> C',
     'Unidades de proceso, excepto las de las subpartidas 8471.41 u 8471.49, aunque incluyan en la misma envoltura uno o dos de los tipos siguientes de unidades: unidad de memoria, unidad de entrada y unidad de salida':'Unidades de procesamiento',
     'Tubería para revestimiento y producción con extremos roscados, terminados o con coupling': 'Tuberia',
     'Con equipo de enfriamiento inferior o igual a 30.000 btu/hora': 'Enfriamiento',
     'Máquinas que efectúan dos o más de las siguientes funciones : impresión, copia o fax, aptas para ser conectadas a una máquina automática para tratamiento o procesamiento de datos o a una red': 'Impresoras',
     'Los demás, simplemente laminados en caliente, enrollados':'Enrollados',
     'Preparaciones acondicionadas para la venta al por menor':'Preparaciones',
     'Con un contenido de dióxido de titanio superior o igual al 80% en peso, calculado sobre materia seca':'TiO2 >= 80%',
     'Máquinas para tratamiento de aguas residuales':'Maquinas PTAR',
     'Con un contenido de potasio superior o igual o superior al 58% pero inferior o igual al 63.1% en peso expresado en óxido de potasio':'58<=KO<=63.1%',
     'Aparatos de diagnóstico de visualización por resonancia magnética': 'Ap. de diagnostico'
     }
c3.markdown("<h3 style ='text-align: center; color:black;'>¿Cuáles son los productos en los que mas gasta ecuador?</h3>", unsafe_allow_html =True)
########################################
import plotly.graph_objects as go 
imp_sample=importaciones[['Código de Unidades Fisicas','Descripción Nandina','Valor CIF dólar bajo Selección']]
imp_sample['Descripción Nandina']=imp_sample['Descripción Nandina'].str.replace('Las demás','Los demás')
imp_sample['Valor CIF dólar bajo Selección']=imp_sample['Valor CIF dólar bajo Selección'].replace(',','.',regex=True)
imp_sample['Valor CIF dólar bajo Selección']=imp_sample['Valor CIF dólar bajo Selección'].astype('float')
imp_gb=imp_sample.groupby(['Descripción Nandina'])[['Valor CIF dólar bajo Selección']].sum().sort_values('Valor CIF dólar bajo Selección', ascending=False).reset_index()
grafimp=imp_gb.head(50)
sum100=grafimp['Valor CIF dólar bajo Selección'].sum()
sumall=imp_gb['Valor CIF dólar bajo Selección'].sum()
suma=sumall-sum100
dic3={'Descripción Nandina':['3650 restantes'],'Valor CIF dólar bajo Selección':[suma]}
dfn=pd.DataFrame(dic3, columns = ['Descripción Nandina' , 'Valor CIF dólar bajo Selección'])
grafimp=grafimp.append(dfn)
grafimp=grafimp.sort_values(by='Valor CIF dólar bajo Selección',ascending=False).reset_index()
# crear base
df0 = grafimp.rename(columns={'Valor CIF dólar bajo Selección':'counts'})
df0=df0.set_index('Descripción Nandina')
a=pd.Series(df0.index)
a=a.replace(dicindex)
df0=df0.set_index(a)
df0=df0.drop(columns='index')

df0['ratio'] = df0.apply(lambda x: x.cumsum()/df0['counts'].sum()) 

# definir figura
pareto = go.Figure([go.Bar(x=df0.index, y=df0['counts'], yaxis='y1', name='sessions id'),
                 go.Scatter(x=df0.index, y=df0['ratio'], yaxis='y2', name='CIF', hovertemplate='%{y:.1%}', marker={'color': '#000000'})])

# agregar detalles
pareto.update_layout(template='plotly_white', showlegend=False, hovermode='x', bargap=.3,
                  title={'text': '<b>Pareto accidentes de Gastos en mercancia<b>', 'x': .5}, 
                  yaxis={'title': 'CIF'},
                  yaxis2={'rangemode': "tozero", 'overlaying': 'y', 'position': 1, 'side': 'right', 'title': 'ratio', 'tickvals': np.arange(0, 1.1, .2), 'tickmode': 'array', 'ticktext': [str(i) + '%' for i in range(0, 101, 20)]},
                  width=800, height=900)

c3.plotly_chart(pareto)
    
#################
c4.markdown("<h3 style ='text-align: center; color:black;'>¿Cuáles son los productos que mas importa Ecuador?</h3>", unsafe_allow_html =True)

importaciones5 = importaciones2[['Producto','Unidades']]
importaciones5 = importaciones5.replace(np.nan, 0)
importaciones5 = importaciones5.groupby(['Producto'])[['Unidades']].sum().reset_index()
importaciones5 = importaciones5.sort_values(by=['Unidades'], ascending = False)
importaciones5['Producto'] = importaciones5['Producto'].str[:12]
figarmas = px.pie(importaciones5.head(10), values = 'Unidades', names ='Producto',
             title= '<b>% Productos de mayor necesidad en el mercado ecuatoriano<b>',
             color_discrete_sequence=px.colors.qualitative.G10)

# agregar detalles a la gráfica
figarmas.update_layout(
    template = 'simple_white',
    legend_title = '<b>Producto<b>',
    title_x = 0.5)

c4.plotly_chart(figarmas)
################################
st.markdown("<h1 style ='text-align: center; color:#1687CE;'>🌎 Impacto geografico 🌎</h1>", unsafe_allow_html =True)

st.markdown("<h3 style ='text-align: center; color:black;'>¿Cuales son las provincias mercantiles de ecuador?</h3>", unsafe_allow_html =True)

dic={'ESMERALDAS':'ESMERALDAS',
     'GUAYAQUIL': 'GUAYAS',
     'HUAQUILLAS': 'EL ORO',
     'QUITO':'PICHINCHA',
     'MACHALA': 'EL ORO',
     'MANTA': 'MANABI',
     'TULCAN': 'CARCHI'}

dic2={'distrito':['AZUAY','BOLIVAR','CAÑAR','CHIMBORAZO','COTOPAXI', 'GALAPAGOS', 'BAQUERIZO','IMBABURA','LOJA','LOS RIOS',
      'MANABI', 'MORONA SANTIAGO','NAPO', 'ORELLANA', 'PASTAZA', 'SANTA ELENA','SUCUMBIOS','ZAMORA CHINCHIPE',],
      'cantidad':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}


dfNew=pd.DataFrame(dic2, columns = ['distrito' , 'cantidad'])

df=exp[['SUBPARTIDA','DISTRITO']]
df=df.rename(columns={'SUBPARTIDA':'cantidad','DISTRITO':'distrito'})
df.distrito=df.distrito.apply(lambda x: x[4:])
df.distrito=df.distrito.apply(lambda x: 'GUAYAQUIL' if x=='GUAYAQUIL - AEREO' else x)
df.distrito=df.distrito.apply(lambda x: 'GUAYAQUIL' if x=='GUAYAQUIL - MARITIMO' else x)
df.distrito=df.distrito.apply(lambda x: 'MACHALA' if x=='PUERTO BOLIVAR' else x)
df.distrito=df.distrito.replace(dic)
df=df.groupby(['distrito'])[['cantidad']].count().reset_index()
df=df.append(dfNew)

import geojson
with open('Bases/provincias.geojson') as f :
    gj_com=geojson.load(f)

mn=df.cantidad.max()
mx=df.cantidad.min()
mapec = px.choropleth_mapbox( df, # dataframe que tiene el indicador
              geojson = gj_com, # archivo json con el shape
              color = 'cantidad', # columna que contiene el indicador: valor sobre el cual se va dar la tonalidad del color
              locations = 'distrito', # llave del dataframe para hacer el join con el shape
              featureidkey = 'properties.dpa_despro', # llave del shape para hacer el join con el dataframe
              color_continuous_scale = 'dense', # escala de color que se va usar
              range_color =(mx, mn), # rangos entre los cuales va variar el color
              hover_name = 'distrito', # información que se va a observar cuando se pase el cursor por el poligono
              center = {'lat':	-1.831239, 'lon':-78.183406}, # centro en el cual se va ubicar el mapa, ubicado a conveniencia
              zoom = 2.2, # zoom de la imagen
              mapbox_style="carto-positron") # estilo del mapa
mapec.update_layout(width=1600, height=850)
mapec.update_geos(fitbounds = 'locations', visible = False) # ajustar a los limites del shape
st.plotly_chart(mapec)

























