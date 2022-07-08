from matplotlib.pyplot import figimage
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import seaborn as sns
import numpy as np
from plotly import express as px
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import matplotlib.pyplot as plt






with st.sidebar:
    selected = option_menu("Main Menu", ["Proyecto", 'Graficos', 'Mapa'], 
        icons=['plus', 'plus', 'plus'], menu_icon="cast", default_index=1)
    selected

if selected == "Proyecto":

    st.text('Este proyecto se realizo por Juan Sebastian Cabuya Sotelo, dando como solucion la visualizacion de los datos de una base de datos, respectivamnte de inmuebles')

    st.title('House sales in King County, USA')
    data = pd.read_csv('basededatos/data.csv')
    
    st.text('columnas de la base de datos')
    data.columns
########################################################################################################################
    st.text('¿Cuál es el número de inmuebles por año de construcción?')
    data['yr_built'] = pd.to_datetime(data['yr_built'], format='%Y').dt.year
    anho = st.slider('seleccione el rango', 1900, 2015)
    st.write('las casas construidas son: ', data[data['yr_built']==anho].shape[0])
#######################################################################################################################

    st.write(data)
    st.text('numero de casas con vista al mar seleccionando las habitaciones y seleccionando los banhos')
    habitaciones2 = st.selectbox(
    'numero de habitaciones',
    list(set(data['bedrooms'])),
    )

    banhos2 = st.selectbox(
    'numero de baños',
    list(set(data['bathrooms']))
    )

    resultado = data[(data['waterfront'] ==1) & (data['bedrooms'] == habitaciones2) & (data['bathrooms'] == banhos2)].shape[0]
    st.write('las casas con vista al mar son: ', resultado)

#########################################################################################################################

    data['date'] = pd.to_datetime(data['date'], format = '%Y-%m-%d')

    data['yr_built'] = pd.to_datetime(data['yr_built'], format ='%Y').dt.year

    #llenar la columna anterior con new_house para fechas anteriores a 2015-01-01
    data['house_age'] = 'NA'
    #llenar la columna anterior con new_house para fechas anteriores a 2015-01-01
    data.loc[data['yr_built']>1990,'house_age'] = 'new_house' 
    #llenar la columna anterior con old_house para fechas anteriores a 2015-01-01
    data.loc[data['yr_built']<1990,'house_age'] = 'old_house'

    st.text('numero de casas viejas o nuevas')
    genre = st.radio(
    "Escoja tipo de casa",
    ('casa nueva', 'casa vieja'))

    if genre == 'casa nueva':
     resultado = data[data['house_age'] == 'new_house'].shape[0]
     st.write('El numero de casas nuevas son: ', resultado)
    else:
     resultado = data[data['house_age'] == 'old_house'].shape[0]
     st.write('El numero de casas viejas son: ', resultado)

#########################################################################################################################    

if selected == "Graficos":

    data = pd.read_csv('basededatos/data.csv')

    st.title('Cual es el tamaño promedio de las habitaciones de los inmuebles por año de construccion')

    habitaciones = st.multiselect(
    'cuantas habitaciones',
    list(set(data['bedrooms'])),
    [1,2,3]
    )

    banhos = st.multiselect(
    'cuantas bañoss',
    list(set(data['bathrooms'])),
    [1,2,3]
    )

    sns.set(style="darkgrid")
    sns.axes_style("whitegrid")

    aux = data[data['bedrooms'].isin(habitaciones) &(data['bathrooms'].isin(banhos))]

    df = aux[['sqft_living','yr_built']].groupby('yr_built').mean().reset_index()
    fig = sns.lineplot(x= 'yr_built', y='sqft_living', data = df)
    fig.set_xlabel('Año de Construcción')
    fig.set_ylabel('Precio (USD)')
    st.pyplot(fig.figure)

########################################################################################################################
        
    data2 = pd.read_csv('basededatos/data2.csv')
    
    st.title('numero de plantas en casas por precio')

    casas = st.multiselect(
    'numero de habitaciones',
    list(set(data2['floors'])),
    [1,2,3]
    )
   
    
    df2 = data2[data2['floors'].isin(casas)]
    aux2 = df2[['floors','yr_built']].groupby('yr_built').mean().reset_index()
    fig2 = sns.lineplot(x= 'yr_built', y='floors', data = df2)
    fig2.set_xlabel('Año de Construcción')
    fig2.set_ylabel('plantas')
    st.pyplot(fig2.figure)

############################################################################################################################

    st.title('Precio vs Años')
    
    data['dormitory_type'] = 'NA'

    figure = plt.figure(figsize = (24,12))
    df = data[['price', 'yr_built', 'dormitory_type']].groupby(['yr_built', 'dormitory_type']).mean().reset_index()
    st.write(sns.lineplot(data = df, 
    x = 'yr_built', 
    y = 'price', 
    hue= 'dormitory_type'))
    
    fig = figure
    st.pyplot(fig)


###########################################################################################################################
    st.title('habitaciones en las casas')
   
    showPyplotGlobalUse = False

    labels=['cero', 'una', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez', 'once', 'treintaytres']
    size = [13, 199, 2760, 9824, 6882, 1601, 272, 38, 13, 6, 3,1,1]
    colors = ['cyan', 'blue', 'gray', 'orange', 'green', 'pink', 'brown', 'purple', 'red', 'white', 'yellow', 'gold', 'coral']
    explode = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

    plt.pie(size, labels = labels, colors = colors, explode = explode, shadow = True, autopct = '%.2f%%')
    plt.title('habitaciones en casas', fontsize = 10)
    plt.axis('off')
    plt.legend(loc = 'best')
    img = plt.show()

    #img = imagen
    st.pyplot(img)

    st.set_option('deprecation.showPyplotGlobalUse', False)
##########################################################################################################################
    
    st.title('Distribucion de variables numericas')

    fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(12, 5))
    axes = axes.flat
    columnas_numeric = data.select_dtypes(include=['float64', 'int']).columns
    columnas_numeric = columnas_numeric.drop('id')
    columnas_numeric = columnas_numeric.drop('sqft_basement')
    columnas_numeric = columnas_numeric.drop('yr_renovated')
    columnas_numeric = columnas_numeric.drop('zipcode')
    columnas_numeric = columnas_numeric.drop('lat')
    columnas_numeric = columnas_numeric.drop('long')
    columnas_numeric = columnas_numeric.drop('sqft_living15')
    columnas_numeric = columnas_numeric.drop('sqft_lot15')

    for i, colum in enumerate(columnas_numeric):
     sns.histplot(
        data    = data,
        x       = colum,
        stat    = "count",
        kde     = True,
        color   = (list(plt.rcParams['axes.prop_cycle'])*2)[i]["color"],
        line_kws= {'linewidth': 2},
        alpha   = 0.3,
        ax      = axes[i]
    )
    axes[i].set_title(colum, fontsize = 7, fontweight = "bold")
    axes[i].tick_params(labelsize = 6)
    axes[i].set_xlabel("")
    
    
    fig.tight_layout()
    plt.subplots_adjust(top = 0.9)
    fig.suptitle('Distribución variables numéricas', fontsize = 10, fontweight = "bold")
    fig = fig.figure
    st.pyplot(fig)

###########################################################################################################################


###########################################################################################################################

if selected == "Mapa":

    st.title('Mapa de las Casas')

    data = pd.read_csv('basededatos/data.csv')
    df_test = data.head(100)

    casas = folium.Map(location=[df_test['lat'].mean(), df_test['long'].mean()], zoom_start=9)
    marker_cluster = MarkerCluster().add_to(casas)

    for nombre, fila in df_test.iterrows():
                 folium.Marker([fila['lat'],fila['long']],
                 popup = 'Propiedad Vendida en ${}, en {}.Características: {} habitaciones, {} baños, constuida en {}, área de {}'.format(
                 fila['price'],
                 fila['date'],
                 fila['bedrooms'],
                 fila['bathrooms'],
                 fila['yr_built'], 
                 fila['sqft_living'])
     ).add_to(marker_cluster)
    folium_static(casas)
#############################################################################################################################
# data['hause_age'] = 'NA'
# #llenar la columna anterior con new_house para fechas anteriores a 2015-01-01
# data.loc[data['yr_built'].dt.year>1990,'hause_age'] = 'new_hause' 
# #llenar la columna anterior con old_house para fechas anteriores a 2015-01-01
# data.loc[data['yr_built'].dt.year<1990,'hause_age'] = 'old_hause'
# data

# st.text('¿Cuál es la mayor cantidad de cuartos que tiene una propiedad old_hause y new_hause?')
# options = st.multiselect(
#      'Tipo de propiedad',
#      ['old_use','new_hause'],
#      ['Yellow', 'Red'])

# st.write('You selected:', options)


#st.text('¿Cuál es el menor número de cuartos por año de construcción de las propiedades?')
#nombres = {'yr_built':'Año Construcción','bedrooms':'Mínimo No. Cuartos'}
#st.text(data[['bedrooms','yr_built']].groupby('yr_built').min().reset_index().rename(columns = nombres))

#st.text('¿Cuál es la suma de todos los precios de compra por cada número de habitaciones?')
#st.text(data[['price', 'bedrooms']].groupby('bedrooms').mean().reset_index())


