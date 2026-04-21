import pandas as pd
import os
import re
import streamlit as st

def cargar_todo():


# ==========================================
# 1. CONFIGURACIÓN DE CARGA (Aquí pones tus rutas)
# ==========================================
# El orden importa: el primero será 'Primera' y el segundo 'Segunda'
    archivos = [
        "RB ENGLAND 2526 24-03-26.xlsx",  
        "RB FRANCE 2526 24-03-26.xlsx",   
        "RB GERMANY 2526 24-03-26.xlsx",   
        "RB ITALY 2526 24-03-26.xlsx",   
        "RB SPAIN 2526 24-03-26.xlsx",   
        
        "RB ENGLAND 2425.xlsx",   
        "RB FRANCE 2425.xlsx",   
        "RB GERMANY 2425.xlsx",   
        "RB ITALY 2425.xlsx",   
        "RB SPAIN 2425.xlsx",     
    ]
    
    
    # ==========================================
    # 1. CONFIGURACIÓN
    # ==========================================
    MIN_MINUTES = 0
    
    # Contenedores para guardar los DataFrames INDIVIDUALES
    # Cada elemento de estas listas será un DataFrame de UNA liga específica
    list_2425 = []  
    list_2526 = []  
    
    def limpiar_nombre_liga(ruta):
        # 'RB SPAIN 2 2526.xlsx' -> 'SPAIN 2'
        nombre = os.path.basename(ruta).replace(".xlsx", "").upper()
        nombre = re.sub(r'^RB\s+', '', nombre)
        nombre = re.sub(r'\s+\d{2}-\d{2}-\d{2}', '', nombre) 
        nombre = re.sub(r'\s+(2425|2526|2025)', '', nombre) 
        return nombre.strip()
    
    # ==========================================
    # 2. PROCESAMIENTO LIGA POR LIGA
    # ==========================================
    # ==========================================
    # 2. PROCESAMIENTO LIGA POR LIGA
    # ==========================================
    for ruta_original in archivos:
        try:
            # CLAVE: Extraemos solo el nombre del archivo (ej: 'RB SPAIN 2526.xlsx')
            # Esto ignora si antes decía C:/Users/juanf/...
            nombre_archivo = os.path.basename(ruta_original)
            
            # Intentamos leer el archivo desde la carpeta raíz del repositorio
            if os.path.exists(nombre_archivo):
                df_temp = pd.read_excel(nombre_archivo)
                
                # Extraemos el nombre literal del país/liga usando tu función
                liga_nombre = limpiar_nombre_liga(nombre_archivo)
                df_temp["Liga"] = liga_nombre
                
                # Filtro de minutos
                if "Minutos jugados" in df_temp.columns:
                    df_temp = df_temp[df_temp["Minutos jugados"] >= MIN_MINUTES].copy()
                
                # --- CLASIFICACIÓN POR TEMPORADA ---
                if "2526" in nombre_archivo:
                    df_temp["Temporada"] = "25/26"
                    list_2526.append(df_temp)
                    st.toast(f"✅ Cargado: {liga_nombre} (25/26)") # Feedback visual en Streamlit
        
                elif "2425" in nombre_archivo or "2025" in nombre_archivo:
                    df_temp["Temporada"] = "24/25_2025"
                    list_2425.append(df_temp)
                    st.toast(f"✅ Cargado: {liga_nombre} (24/25)")

            else:
                # Si no existe en el repo, te avisará en rojo en la web
                st.error(f"❌ No se encontró en GitHub: {nombre_archivo}")
    
        except Exception as e:
            st.error(f"❌ Error procesando {nombre_archivo}: {e}")
    
    # ==========================================
    # 3. VERIFICACIÓN
    # ==========================================
    print("\n" + "="*30)
    print(f"PROCESAMIENTO COMPLETADO")
    print(f"Ligas listas para procesar en 24/25: {len(list_2425)}")
    print(f"Ligas listas para procesar en 25/26: {len(list_2526)}")
    return list_2425, list_2526

import json
def cargar_posesión(list_2526, list_2425):
    
    def convertir_a_mapeo(texto_json):
        """Convierte el texto sucio con 'null' en un diccionario de Python"""
        datos = json.loads(texto_json)
        return {team['name']: team['statValue']['value'] for team in datos}
    
    team_possession_laliga = """[{"id":8634,"teamId":8634,"name":"Barcelona","position":null,"substatValue":{"value":71,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":69.2,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":8633,"teamId":8633,"name":"Real Madrid","position":null,"substatValue":{"value":54,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":59.7,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":10268,"teamId":10268,"name":"Elche","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":58.8,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":9906,"teamId":9906,"name":"Atletico Madrid","position":null,"substatValue":{"value":43,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.1,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":8302,"teamId":8302,"name":"Sevilla","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.2,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":8370,"teamId":8370,"name":"Rayo Vallecano","position":null,"substatValue":{"value":26,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.6,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":9910,"teamId":9910,"name":"Celta Vigo","position":null,"substatValue":{"value":36,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.1,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":9866,"teamId":9866,"name":"Deportivo Alaves","position":null,"substatValue":{"value":23,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.9,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":8560,"teamId":8560,"name":"Real Sociedad","position":null,"substatValue":{"value":38,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.8,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8315,"teamId":8315,"name":"Athletic Club","position":null,"substatValue":{"value":30,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.5,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":7732,"teamId":7732,"name":"Girona","position":null,"substatValue":{"value":27,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.2,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":8603,"teamId":8603,"name":"Real Betis","position":null,"substatValue":{"value":42,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":10267,"teamId":10267,"name":"Valencia","position":null,"substatValue":{"value":27,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.7,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":8371,"teamId":8371,"name":"Osasuna","position":null,"substatValue":{"value":30,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.8,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":8670,"teamId":8670,"name":"Real Oviedo","position":null,"substatValue":{"value":16,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.1,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":10205,"teamId":10205,"name":"Villarreal","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.8,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":8661,"teamId":8661,"name":"Mallorca","position":null,"substatValue":{"value":29,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.7,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":8581,"teamId":8581,"name":"Levante","position":null,"substatValue":{"value":28,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.1,"format":"percent","fractions":1},"rank":18,"type":"teams"},{"id":8558,"teamId":8558,"name":"Espanyol","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":41.9,"format":"percent","fractions":1},"rank":19,"type":"teams"},{"id":8305,"teamId":8305,"name":"Getafe","position":null,"substatValue":{"value":21,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":40.7,"format":"percent","fractions":1},"rank":20,"type":"teams"}]"""
    
    
    team_possession_laliga_2425 = """[{"id":8634,"teamId":8634,"name":"Barcelona","position":null,"substatValue":{"value":102,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":69.1,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":8633,"teamId":8633,"name":"Real Madrid","position":null,"substatValue":{"value":78,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":60.5,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":7732,"teamId":7732,"name":"Girona","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.3,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":8560,"teamId":8560,"name":"Real Sociedad","position":null,"substatValue":{"value":35,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":9910,"teamId":9910,"name":"Celta Vigo","position":null,"substatValue":{"value":59,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.7,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":9906,"teamId":9906,"name":"Atletico Madrid","position":null,"substatValue":{"value":68,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.6,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":8603,"teamId":8603,"name":"Real Betis","position":null,"substatValue":{"value":57,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.6,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":8370,"teamId":8370,"name":"Rayo Vallecano","position":null,"substatValue":{"value":41,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.7,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":8306,"teamId":8306,"name":"Las Palmas","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.9,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8302,"teamId":8302,"name":"Sevilla","position":null,"substatValue":{"value":42,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.6,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":8315,"teamId":8315,"name":"Athletic Club","position":null,"substatValue":{"value":54,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.4,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":10267,"teamId":10267,"name":"Valencia","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.4,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":10205,"teamId":10205,"name":"Villarreal","position":null,"substatValue":{"value":71,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.5,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":8661,"teamId":8661,"name":"Mallorca","position":null,"substatValue":{"value":35,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.6,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":8371,"teamId":8371,"name":"Osasuna","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":9866,"teamId":9866,"name":"Deportivo Alaves","position":null,"substatValue":{"value":38,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.3,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":10281,"teamId":10281,"name":"Real Valladolid","position":null,"substatValue":{"value":26,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.7,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":7854,"teamId":7854,"name":"Leganes","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.5,"format":"percent","fractions":1},"rank":18,"type":"teams"},{"id":8305,"teamId":8305,"name":"Getafe","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":41.2,"format":"percent","fractions":1},"rank":19,"type":"teams"},{"id":8558,"teamId":8558,"name":"Espanyol","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":39.6,"format":"percent","fractions":1},"rank":20,"type":"teams"}]"""
    
    
    
    
    team_possession_premierl = """[{"id":8650,"teamId":8650,"name":"Liverpool","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":60.2,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":8456,"teamId":8456,"name":"Manchester City","position":null,"substatValue":{"value":59,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":59.6,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":8455,"teamId":8455,"name":"Chelsea","position":null,"substatValue":{"value":53,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":58.6,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":9825,"teamId":9825,"name":"Arsenal","position":null,"substatValue":{"value":59,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.4,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":10252,"teamId":10252,"name":"Aston Villa","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.6,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":10260,"teamId":10260,"name":"Manchester United","position":null,"substatValue":{"value":51,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.5,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":10261,"teamId":10261,"name":"Newcastle United","position":null,"substatValue":{"value":42,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.1,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":10204,"teamId":10204,"name":"Brighton & Hove Albion","position":null,"substatValue":{"value":38,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":9879,"teamId":9879,"name":"Fulham","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.7,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8586,"teamId":8586,"name":"Tottenham Hotspur","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":8678,"teamId":8678,"name":"AFC Bournemouth","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.8,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":10203,"teamId":10203,"name":"Nottingham Forest","position":null,"substatValue":{"value":28,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.7,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":9937,"teamId":9937,"name":"Brentford","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.2,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":8463,"teamId":8463,"name":"Leeds United","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.7,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":9826,"teamId":9826,"name":"Crystal Palace","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.5,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":8668,"teamId":8668,"name":"Everton","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.1,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":8472,"teamId":8472,"name":"Sunderland","position":null,"substatValue":{"value":30,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.6,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":8602,"teamId":8602,"name":"Wolverhampton Wanderers","position":null,"substatValue":{"value":22,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.9,"format":"percent","fractions":1},"rank":18,"type":"teams"},{"id":8654,"teamId":8654,"name":"West Ham United","position":null,"substatValue":{"value":35,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.6,"format":"percent","fractions":1},"rank":19,"type":"teams"},{"id":8191,"teamId":8191,"name":"Burnley","position":null,"substatValue":{"value":32,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":41.3,"format":"percent","fractions":1},"rank":20,"type":"teams"}]"""
    
    
    team_possession_premierl_2425 = """[{"id":8650,"teamId":8650,"name":"Liverpool","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":60.2,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":8456,"teamId":8456,"name":"Manchester City","position":null,"substatValue":{"value":59,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":59.6,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":8455,"teamId":8455,"name":"Chelsea","position":null,"substatValue":{"value":53,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":58.6,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":9825,"teamId":9825,"name":"Arsenal","position":null,"substatValue":{"value":59,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.4,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":10252,"teamId":10252,"name":"Aston Villa","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.6,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":10260,"teamId":10260,"name":"Manchester United","position":null,"substatValue":{"value":51,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.5,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":10261,"teamId":10261,"name":"Newcastle United","position":null,"substatValue":{"value":42,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.1,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":10204,"teamId":10204,"name":"Brighton & Hove Albion","position":null,"substatValue":{"value":38,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":9879,"teamId":9879,"name":"Fulham","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.7,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8586,"teamId":8586,"name":"Tottenham Hotspur","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":8678,"teamId":8678,"name":"AFC Bournemouth","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.8,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":10203,"teamId":10203,"name":"Nottingham Forest","position":null,"substatValue":{"value":28,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.7,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":9937,"teamId":9937,"name":"Brentford","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.2,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":8463,"teamId":8463,"name":"Leeds United","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.7,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":9826,"teamId":9826,"name":"Crystal Palace","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.5,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":8668,"teamId":8668,"name":"Everton","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.1,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":8472,"teamId":8472,"name":"Sunderland","position":null,"substatValue":{"value":30,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.6,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":8602,"teamId":8602,"name":"Wolverhampton Wanderers","position":null,"substatValue":{"value":22,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.9,"format":"percent","fractions":1},"rank":18,"type":"teams"},{"id":8654,"teamId":8654,"name":"West Ham United","position":null,"substatValue":{"value":35,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.6,"format":"percent","fractions":1},"rank":19,"type":"teams"},{"id":8191,"teamId":8191,"name":"Burnley","position":null,"substatValue":{"value":32,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":41.3,"format":"percent","fractions":1},"rank":20,"type":"teams"}]"""
    
    
    
    
    
    team_possession_seriea = """[{"id":10171,"teamId":10171,"name":"Como","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":61.3,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":8636,"teamId":8636,"name":"Inter","position":null,"substatValue":{"value":64,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":60.3,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":9875,"teamId":9875,"name":"Napoli","position":null,"substatValue":{"value":41,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":57.3,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":9885,"teamId":9885,"name":"Juventus","position":null,"substatValue":{"value":46,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.9,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":8686,"teamId":8686,"name":"Roma","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.8,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":8524,"teamId":8524,"name":"Atalanta","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":9857,"teamId":9857,"name":"Bologna","position":null,"substatValue":{"value":36,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.8,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":8535,"teamId":8535,"name":"Fiorentina","position":null,"substatValue":{"value":30,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":8564,"teamId":8564,"name":"Milan","position":null,"substatValue":{"value":43,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.4,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8543,"teamId":8543,"name":"Lazio","position":null,"substatValue":{"value":26,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.7,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":10233,"teamId":10233,"name":"Genoa","position":null,"substatValue":{"value":32,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.7,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":8600,"teamId":8600,"name":"Udinese","position":null,"substatValue":{"value":31,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.9,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":8529,"teamId":8529,"name":"Cagliari","position":null,"substatValue":{"value":29,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.6,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":7801,"teamId":7801,"name":"Cremonese","position":null,"substatValue":{"value":21,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.9,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":10167,"teamId":10167,"name":"Parma","position":null,"substatValue":{"value":20,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.7,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":7943,"teamId":7943,"name":"Sassuolo","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.6,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":9804,"teamId":9804,"name":"Torino","position":null,"substatValue":{"value":27,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.2,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":9888,"teamId":9888,"name":"Lecce","position":null,"substatValue":{"value":18,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.8,"format":"percent","fractions":1},"rank":18,"type":"teams"},{"id":9876,"teamId":9876,"name":"Hellas Verona","position":null,"substatValue":{"value":20,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":40.6,"format":"percent","fractions":1},"rank":19,"type":"teams"},{"id":6479,"teamId":6479,"name":"Pisa","position":null,"substatValue":{"value":20,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":40.4,"format":"percent","fractions":1},"rank":20,"type":"teams"}]"""
    
    
    team_possession_seriea_2425 = """[{"id":8636,"teamId":8636,"name":"Inter","position":null,"substatValue":{"value":79,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":59.8,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":9857,"teamId":9857,"name":"Bologna","position":null,"substatValue":{"value":57,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":58.5,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":9885,"teamId":9885,"name":"Juventus","position":null,"substatValue":{"value":58,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":57.5,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":8524,"teamId":8524,"name":"Atalanta","position":null,"substatValue":{"value":78,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.3,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":8543,"teamId":8543,"name":"Lazio","position":null,"substatValue":{"value":61,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.1,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":10171,"teamId":10171,"name":"Como","position":null,"substatValue":{"value":49,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.8,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":9875,"teamId":9875,"name":"Napoli","position":null,"substatValue":{"value":59,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.6,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":8564,"teamId":8564,"name":"Milan","position":null,"substatValue":{"value":61,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.1,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":8686,"teamId":8686,"name":"Roma","position":null,"substatValue":{"value":56,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.9,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8535,"teamId":8535,"name":"Fiorentina","position":null,"substatValue":{"value":60,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.5,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":6504,"teamId":6504,"name":"Monza","position":null,"substatValue":{"value":28,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.6,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":9804,"teamId":9804,"name":"Torino","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.5,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":8600,"teamId":8600,"name":"Udinese","position":null,"substatValue":{"value":41,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.2,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":10233,"teamId":10233,"name":"Genoa","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.6,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":7881,"teamId":7881,"name":"Venezia","position":null,"substatValue":{"value":32,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.8,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":8529,"teamId":8529,"name":"Cagliari","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.7,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":10167,"teamId":10167,"name":"Parma","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.2,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":9888,"teamId":9888,"name":"Lecce","position":null,"substatValue":{"value":27,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.5,"format":"percent","fractions":1},"rank":18,"type":"teams"},{"id":8534,"teamId":8534,"name":"Empoli","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":41.3,"format":"percent","fractions":1},"rank":19,"type":"teams"},{"id":9876,"teamId":9876,"name":"Hellas Verona","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":38.4,"format":"percent","fractions":1},"rank":20,"type":"teams"}]"""
    
    
    
    
    
    
    
    team_possession_bundes = """[{"id":9823,"teamId":9823,"name":"Bayern München","position":null,"substatValue":{"value":88,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":66.5,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":8178,"teamId":8178,"name":"Bayer Leverkusen","position":null,"substatValue":{"value":45,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":60.1,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":10269,"teamId":10269,"name":"VfB Stuttgart","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":58.5,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":8226,"teamId":8226,"name":"Hoffenheim","position":null,"substatValue":{"value":49,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.1,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":178475,"teamId":178475,"name":"RB Leipzig","position":null,"substatValue":{"value":46,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.8,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":9810,"teamId":9810,"name":"Eintracht Frankfurt","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.8,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":9789,"teamId":9789,"name":"Borussia Dortmund","position":null,"substatValue":{"value":51,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.7,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":8697,"teamId":8697,"name":"Werder Bremen","position":null,"substatValue":{"value":25,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":8358,"teamId":8358,"name":"Freiburg","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.6,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8722,"teamId":8722,"name":"1. FC Köln","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.1,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":9790,"teamId":9790,"name":"Hamburger SV","position":null,"substatValue":{"value":26,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.8,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":9788,"teamId":9788,"name":"Borussia Mönchengladbach","position":null,"substatValue":{"value":27,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.5,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":8406,"teamId":8406,"name":"Augsburg","position":null,"substatValue":{"value":30,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.1,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":8721,"teamId":8721,"name":"Wolfsburg","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.9,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":8152,"teamId":8152,"name":"St. Pauli","position":null,"substatValue":{"value":23,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.6,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":9905,"teamId":9905,"name":"Mainz 05","position":null,"substatValue":{"value":27,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.3,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":94937,"teamId":94937,"name":"FC Heidenheim","position":null,"substatValue":{"value":22,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.3,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":8149,"teamId":8149,"name":"Union Berlin","position":null,"substatValue":{"value":29,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":39.1,"format":"percent","fractions":1},"rank":18,"type":"teams"}]"""
    
    
    team_possession_bundes_2425 = """[{"id":9823,"teamId":9823,"name":"Bayern München","position":null,"substatValue":{"value":99,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":68.3,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":8178,"teamId":8178,"name":"Bayer Leverkusen","position":null,"substatValue":{"value":72,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":59.4,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":9789,"teamId":9789,"name":"Borussia Dortmund","position":null,"substatValue":{"value":71,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":59.2,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":10269,"teamId":10269,"name":"VfB Stuttgart","position":null,"substatValue":{"value":64,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":57.5,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":178475,"teamId":178475,"name":"RB Leipzig","position":null,"substatValue":{"value":53,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.3,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":9905,"teamId":9905,"name":"Mainz 05","position":null,"substatValue":{"value":55,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.3,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":9810,"teamId":9810,"name":"Eintracht Frankfurt","position":null,"substatValue":{"value":68,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.9,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":8697,"teamId":8697,"name":"Werder Bremen","position":null,"substatValue":{"value":54,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.9,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":9788,"teamId":9788,"name":"Borussia Mönchengladbach","position":null,"substatValue":{"value":55,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.8,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8358,"teamId":8358,"name":"Freiburg","position":null,"substatValue":{"value":49,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.7,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":8226,"teamId":8226,"name":"Hoffenheim","position":null,"substatValue":{"value":46,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.6,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":8721,"teamId":8721,"name":"Wolfsburg","position":null,"substatValue":{"value":56,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":9911,"teamId":9911,"name":"Bochum","position":null,"substatValue":{"value":31,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.2,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":8406,"teamId":8406,"name":"Augsburg","position":null,"substatValue":{"value":35,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":8152,"teamId":8152,"name":"St. Pauli","position":null,"substatValue":{"value":28,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":8150,"teamId":8150,"name":"Holstein Kiel","position":null,"substatValue":{"value":49,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.7,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":94937,"teamId":94937,"name":"FC Heidenheim","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.2,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":8149,"teamId":8149,"name":"Union Berlin","position":null,"substatValue":{"value":35,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":39.6,"format":"percent","fractions":1},"rank":18,"type":"teams"}]"""
    
    
    
    
    
    
    team_possession_ligue1 = """[{"id":9847,"teamId":9847,"name":"Paris Saint-Germain","position":null,"substatValue":{"value":53,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":68.5,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":8592,"teamId":8592,"name":"Marseille","position":null,"substatValue":{"value":51,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":57.8,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":8639,"teamId":8639,"name":"Lille","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.7,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":9748,"teamId":9748,"name":"Lyon","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.5,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":9829,"teamId":9829,"name":"Monaco","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.6,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":6379,"teamId":6379,"name":"Paris FC","position":null,"substatValue":{"value":28,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.2,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":9851,"teamId":9851,"name":"Rennes","position":null,"substatValue":{"value":38,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":9848,"teamId":9848,"name":"Strasbourg","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.8,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":8550,"teamId":8550,"name":"Metz","position":null,"substatValue":{"value":22,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.1,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8588,"teamId":8588,"name":"Lens","position":null,"substatValue":{"value":45,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":9831,"teamId":9831,"name":"Nice","position":null,"substatValue":{"value":30,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.1,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":9746,"teamId":9746,"name":"Le Havre","position":null,"substatValue":{"value":20,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.1,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":8689,"teamId":8689,"name":"Lorient","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.5,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":8583,"teamId":8583,"name":"Auxerre","position":null,"substatValue":{"value":19,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.4,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":9830,"teamId":9830,"name":"Nantes","position":null,"substatValue":{"value":22,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.1,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":9941,"teamId":9941,"name":"Toulouse","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.9,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":8121,"teamId":8121,"name":"Angers","position":null,"substatValue":{"value":22,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.5,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":8521,"teamId":8521,"name":"Brest","position":null,"substatValue":{"value":32,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.3,"format":"percent","fractions":1},"rank":18,"type":"teams"}]"""
    
    
    team_possession_ligue1_2425 = """[{"id":9847,"teamId":9847,"name":"Paris Saint-Germain","position":null,"substatValue":{"value":92,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":68.4,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":8592,"teamId":8592,"name":"Marseille","position":null,"substatValue":{"value":74,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":63.6,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":8639,"teamId":8639,"name":"Lille","position":null,"substatValue":{"value":52,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":57.9,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":9748,"teamId":9748,"name":"Lyon","position":null,"substatValue":{"value":65,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.6,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":9829,"teamId":9829,"name":"Monaco","position":null,"substatValue":{"value":63,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.1,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":8588,"teamId":8588,"name":"Lens","position":null,"substatValue":{"value":42,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.1,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":9851,"teamId":9851,"name":"Rennes","position":null,"substatValue":{"value":51,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.1,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":9848,"teamId":9848,"name":"Strasbourg","position":null,"substatValue":{"value":56,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.2,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":8521,"teamId":8521,"name":"Brest","position":null,"substatValue":{"value":52,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.4,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":9831,"teamId":9831,"name":"Nice","position":null,"substatValue":{"value":66,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.5,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":9853,"teamId":9853,"name":"Saint-Etienne","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.3,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":10249,"teamId":10249,"name":"Montpellier","position":null,"substatValue":{"value":23,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":9941,"teamId":9941,"name":"Toulouse","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.7,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":9837,"teamId":9837,"name":"Reims","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.9,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":9746,"teamId":9746,"name":"Le Havre","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":8583,"teamId":8583,"name":"Auxerre","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.5,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":8121,"teamId":8121,"name":"Angers","position":null,"substatValue":{"value":32,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":40.8,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":9830,"teamId":9830,"name":"Nantes","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":40,"format":"percent","fractions":1},"rank":18,"type":"teams"}]"""
    
    
    
    
    
    team_possession_championship = """[{"id":8549,"teamId":8549,"name":"Middlesbrough","position":null,"substatValue":{"value":54,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":58.3,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":8466,"teamId":8466,"name":"Southampton","position":null,"substatValue":{"value":57,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":57.2,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":9902,"teamId":9902,"name":"Ipswich Town","position":null,"substatValue":{"value":60,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":10003,"teamId":10003,"name":"Swansea City","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.3,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":8669,"teamId":8669,"name":"Coventry City","position":null,"substatValue":{"value":72,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.2,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":8658,"teamId":8658,"name":"Birmingham City","position":null,"substatValue":{"value":46,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":10194,"teamId":10194,"name":"Stoke City","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.2,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":9850,"teamId":9850,"name":"Norwich City","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.2,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":8659,"teamId":8659,"name":"West Bromwich Albion","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.8,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8657,"teamId":8657,"name":"Sheffield United","position":null,"substatValue":{"value":50,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.6,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":8197,"teamId":8197,"name":"Leicester City","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.6,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":8462,"teamId":8462,"name":"Portsmouth","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.2,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":9817,"teamId":9817,"name":"Watford","position":null,"substatValue":{"value":45,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.9,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":8655,"teamId":8655,"name":"Blackburn Rovers","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.7,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":8427,"teamId":8427,"name":"Bristol City","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.1,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":9841,"teamId":9841,"name":"Wrexham","position":null,"substatValue":{"value":54,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.5,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":10004,"teamId":10004,"name":"Millwall","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.8,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":10172,"teamId":10172,"name":"Queens Park Rangers","position":null,"substatValue":{"value":46,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.2,"format":"percent","fractions":1},"rank":18,"type":"teams"},{"id":10163,"teamId":10163,"name":"Sheffield Wednesday","position":null,"substatValue":{"value":21,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.6,"format":"percent","fractions":1},"rank":19,"type":"teams"},{"id":8667,"teamId":8667,"name":"Hull City","position":null,"substatValue":{"value":56,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.5,"format":"percent","fractions":1},"rank":20,"type":"teams"},{"id":8411,"teamId":8411,"name":"Preston North End","position":null,"substatValue":{"value":41,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.3,"format":"percent","fractions":1},"rank":21,"type":"teams"},{"id":8451,"teamId":8451,"name":"Charlton Athletic","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.3,"format":"percent","fractions":1},"rank":22,"type":"teams"},{"id":10170,"teamId":10170,"name":"Derby County","position":null,"substatValue":{"value":52,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.2,"format":"percent","fractions":1},"rank":23,"type":"teams"},{"id":8653,"teamId":8653,"name":"Oxford United","position":null,"substatValue":{"value":31,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":40.6,"format":"percent","fractions":1},"rank":24,"type":"teams"}]"""
    
    
    team_possession_championship_2425 = """[{"id":8463,"teamId":8463,"name":"Leeds United","position":null,"substatValue":{"value":95,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":61.6,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":9850,"teamId":9850,"name":"Norwich City","position":null,"substatValue":{"value":71,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":58.2,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":10003,"teamId":10003,"name":"Swansea City","position":null,"substatValue":{"value":51,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":58.1,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":8191,"teamId":8191,"name":"Burnley","position":null,"substatValue":{"value":69,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.9,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":8549,"teamId":8549,"name":"Middlesbrough","position":null,"substatValue":{"value":64,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.6,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":8669,"teamId":8669,"name":"Coventry City","position":null,"substatValue":{"value":64,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.6,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":8659,"teamId":8659,"name":"West Bromwich Albion","position":null,"substatValue":{"value":57,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.4,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":9817,"teamId":9817,"name":"Watford","position":null,"substatValue":{"value":53,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.7,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":8657,"teamId":8657,"name":"Sheffield United","position":null,"substatValue":{"value":63,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.5,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8427,"teamId":8427,"name":"Bristol City","position":null,"substatValue":{"value":59,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.1,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":8667,"teamId":8667,"name":"Hull City","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.9,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":8472,"teamId":8472,"name":"Sunderland","position":null,"substatValue":{"value":58,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.1,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":8655,"teamId":8655,"name":"Blackburn Rovers","position":null,"substatValue":{"value":53,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.1,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":8411,"teamId":8411,"name":"Preston North End","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.2,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":10163,"teamId":10163,"name":"Sheffield Wednesday","position":null,"substatValue":{"value":60,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":10194,"teamId":10194,"name":"Stoke City","position":null,"substatValue":{"value":45,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.7,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":10172,"teamId":10172,"name":"Queens Park Rangers","position":null,"substatValue":{"value":53,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.6,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":8344,"teamId":8344,"name":"Cardiff City","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.6,"format":"percent","fractions":1},"rank":18,"type":"teams"},{"id":8346,"teamId":8346,"name":"Luton Town","position":null,"substatValue":{"value":45,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45,"format":"percent","fractions":1},"rank":19,"type":"teams"},{"id":8462,"teamId":8462,"name":"Portsmouth","position":null,"substatValue":{"value":58,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.8,"format":"percent","fractions":1},"rank":20,"type":"teams"},{"id":10170,"teamId":10170,"name":"Derby County","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.4,"format":"percent","fractions":1},"rank":21,"type":"teams"},{"id":8653,"teamId":8653,"name":"Oxford United","position":null,"substatValue":{"value":49,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.2,"format":"percent","fractions":1},"rank":22,"type":"teams"},{"id":10004,"teamId":10004,"name":"Millwall","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.5,"format":"percent","fractions":1},"rank":23,"type":"teams"},{"id":8401,"teamId":8401,"name":"Plymouth Argyle","position":null,"substatValue":{"value":51,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.3,"format":"percent","fractions":1},"rank":24,"type":"teams"}]"""
    
    
    
    
    
    team_possession_proleague = """[{"id":8342,"teamId":8342,"name":"Club Brugge","position":null,"substatValue":{"value":51,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":62.9,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":9987,"teamId":9987,"name":"Genk","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":61.5,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":9997,"teamId":9997,"name":"St.Truiden","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.3,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":7978,"teamId":7978,"name":"Union St.Gilloise","position":null,"substatValue":{"value":43,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.3,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":8635,"teamId":8635,"name":"Anderlecht","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.9,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":9991,"teamId":9991,"name":"Gent","position":null,"substatValue":{"value":41,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.2,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":8203,"teamId":8203,"name":"KV Mechelen","position":null,"substatValue":{"value":36,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.9,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":10001,"teamId":10001,"name":"Westerlo","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":9986,"teamId":9986,"name":"Sporting Charleroi","position":null,"substatValue":{"value":36,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.3,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":9988,"teamId":9988,"name":"Royal Antwerp","position":null,"substatValue":{"value":30,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.9,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":10000,"teamId":10000,"name":"Zulte Waregem","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.8,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":9984,"teamId":9984,"name":"Cercle Brugge","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.3,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":7947,"teamId":7947,"name":"FCV Dender EH","position":null,"substatValue":{"value":21,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.2,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":1773,"teamId":1773,"name":"OH Leuven","position":null,"substatValue":{"value":29,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.8,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":9985,"teamId":9985,"name":"Standard Liege","position":null,"substatValue":{"value":25,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.5,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":1218969,"teamId":1218969,"name":"RAAL La Louviere","position":null,"substatValue":{"value":22,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":36.2,"format":"percent","fractions":1},"rank":16,"type":"teams"}]"""
    
    
    team_possession_proleague_2425 = """[{"id":8342,"teamId":8342,"name":"Club Brugge","position":null,"substatValue":{"value":86,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":58.7,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":9987,"teamId":9987,"name":"Genk","position":null,"substatValue":{"value":69,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":57.9,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":8635,"teamId":8635,"name":"Anderlecht","position":null,"substatValue":{"value":62,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.1,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":8203,"teamId":8203,"name":"KV Mechelen","position":null,"substatValue":{"value":62,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.4,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":9986,"teamId":9986,"name":"Sporting Charleroi","position":null,"substatValue":{"value":57,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.7,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":9988,"teamId":9988,"name":"Royal Antwerp","position":null,"substatValue":{"value":53,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.7,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":9991,"teamId":9991,"name":"Gent","position":null,"substatValue":{"value":45,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.2,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":1773,"teamId":1773,"name":"OH Leuven","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.8,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":583877,"teamId":583877,"name":"Beerschot","position":null,"substatValue":{"value":36,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.1,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":7978,"teamId":7978,"name":"Union St.Gilloise","position":null,"substatValue":{"value":71,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":10001,"teamId":10001,"name":"Westerlo","position":null,"substatValue":{"value":69,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.9,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":9997,"teamId":9997,"name":"St.Truiden","position":null,"substatValue":{"value":50,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.6,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":9984,"teamId":9984,"name":"Cercle Brugge","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.1,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":8571,"teamId":8571,"name":"Kortrijk","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.6,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":7947,"teamId":7947,"name":"FCV Dender EH","position":null,"substatValue":{"value":53,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.3,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":9985,"teamId":9985,"name":"Standard Liege","position":null,"substatValue":{"value":27,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":41.4,"format":"percent","fractions":1},"rank":16,"type":"teams"}]"""
    
    
    
    
    team_possession_brazil_2025 = """[{"id":9770,"teamId":9770,"name":"Flamengo","position":null,"substatValue":{"value":78,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":62,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":9808,"teamId":9808,"name":"Corinthians","position":null,"substatValue":{"value":42,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.8,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":7877,"teamId":7877,"name":"Bahia","position":null,"substatValue":{"value":50,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.2,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":10276,"teamId":10276,"name":"Vasco da Gama","position":null,"substatValue":{"value":55,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.5,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":10272,"teamId":10272,"name":"Atletico MG","position":null,"substatValue":{"value":43,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.1,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":9863,"teamId":9863,"name":"Fluminense","position":null,"substatValue":{"value":50,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.9,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":10283,"teamId":10283,"name":"Palmeiras","position":null,"substatValue":{"value":66,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.3,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":10277,"teamId":10277,"name":"Sao Paulo","position":null,"substatValue":{"value":43,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.1,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":8517,"teamId":8517,"name":"Botafogo RJ","position":null,"substatValue":{"value":58,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.7,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8702,"teamId":8702,"name":"Internacional","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.2,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":163782,"teamId":163782,"name":"Mirassol","position":null,"substatValue":{"value":63,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":8514,"teamId":8514,"name":"Santos FC","position":null,"substatValue":{"value":45,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.7,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":9781,"teamId":9781,"name":"Cruzeiro","position":null,"substatValue":{"value":55,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.8,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":109705,"teamId":109705,"name":"Red Bull Bragantino","position":null,"substatValue":{"value":45,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.7,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":6305,"teamId":6305,"name":"Sport Recife","position":null,"substatValue":{"value":28,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.3,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":9769,"teamId":9769,"name":"Gremio","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.2,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":8287,"teamId":8287,"name":"Fortaleza","position":null,"substatValue":{"value":43,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.3,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":10274,"teamId":10274,"name":"Juventude","position":null,"substatValue":{"value":35,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.8,"format":"percent","fractions":1},"rank":18,"type":"teams"},{"id":172341,"teamId":172341,"name":"Ceara","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42,"format":"percent","fractions":1},"rank":19,"type":"teams"},{"id":7733,"teamId":7733,"name":"Vitoria","position":null,"substatValue":{"value":35,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":41.3,"format":"percent","fractions":1},"rank":20,"type":"teams"}]"""
    
    
    
    
    
    
    team_possession_argentina_2025 = """[{"id":10086,"teamId":10086,"name":"Argentinos Juniors","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":63,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":10076,"teamId":10076,"name":"River Plate","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":62.9,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":10078,"teamId":10078,"name":"Independiente","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":58.6,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":10101,"teamId":10101,"name":"Talleres","position":null,"substatValue":{"value":20,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.1,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":10077,"teamId":10077,"name":"Boca Juniors","position":null,"substatValue":{"value":55,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.4,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":161730,"teamId":161730,"name":"Defensa y Justicia","position":null,"substatValue":{"value":32,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.3,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":10080,"teamId":10080,"name":"Racing Club","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.1,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":10094,"teamId":10094,"name":"Estudiantes","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.6,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":10079,"teamId":10079,"name":"Velez Sarsfield","position":null,"substatValue":{"value":26,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.3,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":10084,"teamId":10084,"name":"Rosario Central","position":null,"substatValue":{"value":42,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.2,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":10082,"teamId":10082,"name":"Lanus","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.7,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":10227,"teamId":10227,"name":"Godoy Cruz","position":null,"substatValue":{"value":19,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.6,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":10096,"teamId":10096,"name":"Union","position":null,"substatValue":{"value":32,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.3,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":213596,"teamId":213596,"name":"Central Cordoba de Santiago","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.1,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":10081,"teamId":10081,"name":"Huracan","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.8,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":10092,"teamId":10092,"name":"Belgrano","position":null,"substatValue":{"value":26,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.1,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":10090,"teamId":10090,"name":"Instituto","position":null,"substatValue":{"value":26,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.6,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":161727,"teamId":161727,"name":"Atletico Tucuman","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.9,"format":"percent","fractions":1},"rank":18,"type":"teams"},{"id":10083,"teamId":10083,"name":"San Lorenzo","position":null,"substatValue":{"value":31,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.7,"format":"percent","fractions":1},"rank":19,"type":"teams"},{"id":10103,"teamId":10103,"name":"Gimnasia LP","position":null,"substatValue":{"value":27,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.8,"format":"percent","fractions":1},"rank":20,"type":"teams"},{"id":202757,"teamId":202757,"name":"Sarmiento","position":null,"substatValue":{"value":24,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.6,"format":"percent","fractions":1},"rank":21,"type":"teams"},{"id":161729,"teamId":161729,"name":"Independiente Rivadavia","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.5,"format":"percent","fractions":1},"rank":22,"type":"teams"},{"id":161728,"teamId":161728,"name":"Aldosivi","position":null,"substatValue":{"value":31,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.5,"format":"percent","fractions":1},"rank":23,"type":"teams"},{"id":10089,"teamId":10089,"name":"Club Atletico Platense","position":null,"substatValue":{"value":29,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.5,"format":"percent","fractions":1},"rank":24,"type":"teams"},{"id":89396,"teamId":89396,"name":"Tigre","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.7,"format":"percent","fractions":1},"rank":25,"type":"teams"},{"id":89395,"teamId":89395,"name":"San Martin San Juan","position":null,"substatValue":{"value":18,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.6,"format":"percent","fractions":1},"rank":26,"type":"teams"},{"id":10087,"teamId":10087,"name":"Banfield","position":null,"substatValue":{"value":29,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.9,"format":"percent","fractions":1},"rank":27,"type":"teams"},{"id":10201,"teamId":10201,"name":"Newell's Old Boys","position":null,"substatValue":{"value":25,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.7,"format":"percent","fractions":1},"rank":28,"type":"teams"},{"id":213534,"teamId":213534,"name":"Barracas Central","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":40.6,"format":"percent","fractions":1},"rank":29,"type":"teams"},{"id":298629,"teamId":298629,"name":"Deportivo Riestra","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":32.3,"format":"percent","fractions":1},"rank":30,"type":"teams"}]"""
    
    
    
    
    
    
    
    team_possession_portugal = """[{"id":10264,"teamId":10264,"name":"Braga","position":null,"substatValue":{"value":50,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":63.1,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":9768,"teamId":9768,"name":"Sporting CP","position":null,"substatValue":{"value":62,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":61.8,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":9772,"teamId":9772,"name":"Benfica","position":null,"substatValue":{"value":51,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":58.9,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":9773,"teamId":9773,"name":"FC Porto","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.2,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":7842,"teamId":7842,"name":"Estoril","position":null,"substatValue":{"value":46,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.1,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":1634,"teamId":1634,"name":"Famalicao","position":null,"substatValue":{"value":29,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.2,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":158085,"teamId":158085,"name":"Arouca","position":null,"substatValue":{"value":32,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.7,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":8348,"teamId":8348,"name":"Moreirense","position":null,"substatValue":{"value":30,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.7,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":7844,"teamId":7844,"name":"Vitoria de Guimaraes","position":null,"substatValue":{"value":28,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.6,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":9764,"teamId":9764,"name":"Gil Vicente","position":null,"substatValue":{"value":35,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.5,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":1567,"teamId":1567,"name":"Santa Clara","position":null,"substatValue":{"value":20,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.2,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":1074320,"teamId":1074320,"name":"Estrela da Amadora","position":null,"substatValue":{"value":26,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.2,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":7841,"teamId":7841,"name":"Rio Ave","position":null,"substatValue":{"value":23,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.2,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":10214,"teamId":10214,"name":"Nacional","position":null,"substatValue":{"value":28,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.6,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":9780,"teamId":9780,"name":"Alverca","position":null,"substatValue":{"value":24,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.6,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":212821,"teamId":212821,"name":"Casa Pia AC","position":null,"substatValue":{"value":26,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":188163,"teamId":188163,"name":"Tondela","position":null,"substatValue":{"value":19,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":41.6,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":1889,"teamId":1889,"name":"AVS Futebol SAD","position":null,"substatValue":{"value":18,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":40.9,"format":"percent","fractions":1},"rank":18,"type":"teams"}]"""
    
    
    team_possession_portugal_2425 = """[{"id":9773,"teamId":9773,"name":"FC Porto","position":null,"substatValue":{"value":65,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":62,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":9768,"teamId":9768,"name":"Sporting CP","position":null,"substatValue":{"value":88,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":60.5,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":9772,"teamId":9772,"name":"Benfica","position":null,"substatValue":{"value":84,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":58.3,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":10264,"teamId":10264,"name":"Braga","position":null,"substatValue":{"value":55,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":57.1,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":7844,"teamId":7844,"name":"Vitoria de Guimaraes","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.9,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":158085,"teamId":158085,"name":"Arouca","position":null,"substatValue":{"value":35,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.4,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":9764,"teamId":9764,"name":"Gil Vicente","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.8,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":1634,"teamId":1634,"name":"Famalicao","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.6,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":7842,"teamId":7842,"name":"Estoril","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.1,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":7841,"teamId":7841,"name":"Rio Ave","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.7,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":8348,"teamId":8348,"name":"Moreirense","position":null,"substatValue":{"value":42,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.5,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":10214,"teamId":10214,"name":"Nacional","position":null,"substatValue":{"value":32,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.3,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":212821,"teamId":212821,"name":"Casa Pia AC","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.6,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":1074320,"teamId":1074320,"name":"Estrela da Amadora","position":null,"substatValue":{"value":24,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.6,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":1567,"teamId":1567,"name":"Santa Clara","position":null,"substatValue":{"value":36,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.5,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":1889,"teamId":1889,"name":"AVS Futebol SAD","position":null,"substatValue":{"value":25,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.6,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":6004,"teamId":6004,"name":"Farense","position":null,"substatValue":{"value":25,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":40.8,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":8613,"teamId":8613,"name":"Boavista","position":null,"substatValue":{"value":24,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":39.9,"format":"percent","fractions":1},"rank":18,"type":"teams"}]"""
    
    
    
    
    team_possession_denmark = """[{"id":10202,"teamId":10202,"name":"Nordsjælland","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":57.9,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":8391,"teamId":8391,"name":"FC København","position":null,"substatValue":{"value":35,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.1,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":8113,"teamId":8113,"name":"FC Midtjylland","position":null,"substatValue":{"value":58,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.6,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":8071,"teamId":8071,"name":"AGF","position":null,"substatValue":{"value":46,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.5,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":8595,"teamId":8595,"name":"Brøndby IF","position":null,"substatValue":{"value":31,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.2,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":8415,"teamId":8415,"name":"Silkeborg","position":null,"substatValue":{"value":24,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.1,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":8414,"teamId":8414,"name":"OB","position":null,"substatValue":{"value":36,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.7,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":8410,"teamId":8410,"name":"Randers FC","position":null,"substatValue":{"value":22,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.4,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":9939,"teamId":9939,"name":"Viborg","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.7,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8487,"teamId":8487,"name":"Sønderjyske","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.8,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":8231,"teamId":8231,"name":"Vejle Boldklub","position":null,"substatValue":{"value":26,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.7,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":8454,"teamId":8454,"name":"Fredericia","position":null,"substatValue":{"value":30,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.4,"format":"percent","fractions":1},"rank":12,"type":"teams"}]"""
    
    
    team_possession_denmark_2425 = """[{"id":10202,"teamId":10202,"name":"Nordsjælland","position":null,"substatValue":{"value":53,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":60.9,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":8595,"teamId":8595,"name":"Brøndby IF","position":null,"substatValue":{"value":58,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.2,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":8415,"teamId":8415,"name":"Silkeborg","position":null,"substatValue":{"value":56,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":8391,"teamId":8391,"name":"FC København","position":null,"substatValue":{"value":60,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.4,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":8071,"teamId":8071,"name":"AGF","position":null,"substatValue":{"value":53,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.8,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":9939,"teamId":9939,"name":"Viborg","position":null,"substatValue":{"value":57,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.8,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":8113,"teamId":8113,"name":"FC Midtjylland","position":null,"substatValue":{"value":64,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.9,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":8487,"teamId":8487,"name":"Sønderjyske","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.9,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":8470,"teamId":8470,"name":"AaB","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.9,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":9907,"teamId":9907,"name":"Lyngby","position":null,"substatValue":{"value":26,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.6,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":8410,"teamId":8410,"name":"Randers FC","position":null,"substatValue":{"value":57,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.4,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":8231,"teamId":8231,"name":"Vejle Boldklub","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.4,"format":"percent","fractions":1},"rank":12,"type":"teams"}]"""
    
    
    
    
    team_possession_mls_2025 = """[{"id":1701119,"teamId":1701119,"name":"San Diego FC","position":null,"substatValue":{"value":74,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":61.6,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":6001,"teamId":6001,"name":"Columbus Crew","position":null,"substatValue":{"value":60,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":58.9,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":960720,"teamId":960720,"name":"Inter Miami CF","position":null,"substatValue":{"value":101,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.9,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":6637,"teamId":6637,"name":"LA Galaxy","position":null,"substatValue":{"value":46,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.3,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":130394,"teamId":130394,"name":"Seattle Sounders FC","position":null,"substatValue":{"value":65,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.2,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":307691,"teamId":307691,"name":"Vancouver Whitecaps","position":null,"substatValue":{"value":76,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.9,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":546238,"teamId":546238,"name":"New York City FC","position":null,"substatValue":{"value":56,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.9,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":6606,"teamId":6606,"name":"Real Salt Lake","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.1,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":867280,"teamId":867280,"name":"Los Angeles FC","position":null,"substatValue":{"value":73,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.9,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":6514,"teamId":6514,"name":"New York Red Bulls","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.6,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":6603,"teamId":6603,"name":"San Jose Earthquakes","position":null,"substatValue":{"value":60,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.7,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":8259,"teamId":8259,"name":"Houston Dynamo FC","position":null,"substatValue":{"value":43,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.5,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":915807,"teamId":915807,"name":"Nashville SC","position":null,"substatValue":{"value":61,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.4,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":773958,"teamId":773958,"name":"Atlanta United","position":null,"substatValue":{"value":38,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.3,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":6580,"teamId":6580,"name":"New England Revolution","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.7,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":6397,"teamId":6397,"name":"Chicago Fire FC","position":null,"substatValue":{"value":73,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.6,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":307690,"teamId":307690,"name":"Portland Timbers","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.8,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":161195,"teamId":161195,"name":"CF Montreal","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.7,"format":"percent","fractions":1},"rank":18,"type":"teams"},{"id":722265,"teamId":722265,"name":"FC Cincinnati","position":null,"substatValue":{"value":55,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.3,"format":"percent","fractions":1},"rank":19,"type":"teams"},{"id":191716,"teamId":191716,"name":"Philadelphia Union","position":null,"substatValue":{"value":62,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.2,"format":"percent","fractions":1},"rank":20,"type":"teams"},{"id":1323940,"teamId":1323940,"name":"Charlotte FC","position":null,"substatValue":{"value":56,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.9,"format":"percent","fractions":1},"rank":21,"type":"teams"},{"id":6604,"teamId":6604,"name":"Sporting Kansas City","position":null,"substatValue":{"value":46,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.9,"format":"percent","fractions":1},"rank":22,"type":"teams"},{"id":267810,"teamId":267810,"name":"Orlando City","position":null,"substatValue":{"value":64,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.6,"format":"percent","fractions":1},"rank":23,"type":"teams"},{"id":1218886,"teamId":1218886,"name":"Austin FC","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.5,"format":"percent","fractions":1},"rank":24,"type":"teams"},{"id":1427963,"teamId":1427963,"name":"St. Louis City","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.2,"format":"percent","fractions":1},"rank":25,"type":"teams"},{"id":56453,"teamId":56453,"name":"Toronto FC","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46,"format":"percent","fractions":1},"rank":26,"type":"teams"},{"id":8314,"teamId":8314,"name":"Colorado Rapids","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.4,"format":"percent","fractions":1},"rank":27,"type":"teams"},{"id":6602,"teamId":6602,"name":"DC United","position":null,"substatValue":{"value":30,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45,"format":"percent","fractions":1},"rank":28,"type":"teams"},{"id":6399,"teamId":6399,"name":"FC Dallas","position":null,"substatValue":{"value":53,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":40.6,"format":"percent","fractions":1},"rank":29,"type":"teams"},{"id":207242,"teamId":207242,"name":"Minnesota United","position":null,"substatValue":{"value":61,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":38.9,"format":"percent","fractions":1},"rank":30,"type":"teams"}]"""
    
    
    
    team_possession_netherlands = """[{"id":8640,"teamId":8640,"name":"PSV Eindhoven","position":null,"substatValue":{"value":78,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":61.3,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":8593,"teamId":8593,"name":"Ajax","position":null,"substatValue":{"value":53,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.8,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":8464,"teamId":8464,"name":"NEC Nijmegen","position":null,"substatValue":{"value":69,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.5,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":8611,"teamId":8611,"name":"FC Twente","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.9,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":10235,"teamId":10235,"name":"Feyenoord","position":null,"substatValue":{"value":61,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.2,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":10229,"teamId":10229,"name":"AZ Alkmaar","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.5,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":8674,"teamId":8674,"name":"FC Groningen","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.6,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":10228,"teamId":10228,"name":"SC Heerenveen","position":null,"substatValue":{"value":49,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.3,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":6433,"teamId":6433,"name":"Go Ahead Eagles","position":null,"substatValue":{"value":45,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.9,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":9761,"teamId":9761,"name":"NAC Breda","position":null,"substatValue":{"value":29,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.8,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":8614,"teamId":8614,"name":"Sparta Rotterdam","position":null,"substatValue":{"value":35,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.3,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":9908,"teamId":9908,"name":"FC Utrecht","position":null,"substatValue":{"value":42,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.1,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":10218,"teamId":10218,"name":"Excelsior","position":null,"substatValue":{"value":29,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.6,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":6601,"teamId":6601,"name":"FC Volendam","position":null,"substatValue":{"value":30,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.2,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":6422,"teamId":6422,"name":"Fortuna Sittard","position":null,"substatValue":{"value":43,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.9,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":6413,"teamId":6413,"name":"PEC Zwolle","position":null,"substatValue":{"value":38,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.6,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":6414,"teamId":6414,"name":"Telstar","position":null,"substatValue":{"value":38,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.6,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":9791,"teamId":9791,"name":"Heracles","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.9,"format":"percent","fractions":1},"rank":18,"type":"teams"}]"""
    
    
    team_possession_netherlands_2425 = """[{"id":8640,"teamId":8640,"name":"PSV Eindhoven","position":null,"substatValue":{"value":103,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":68,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":8593,"teamId":8593,"name":"Ajax","position":null,"substatValue":{"value":67,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":57.8,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":10235,"teamId":10235,"name":"Feyenoord","position":null,"substatValue":{"value":76,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":57.6,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":8611,"teamId":8611,"name":"FC Twente","position":null,"substatValue":{"value":62,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.5,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":10228,"teamId":10228,"name":"SC Heerenveen","position":null,"substatValue":{"value":42,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.3,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":10229,"teamId":10229,"name":"AZ Alkmaar","position":null,"substatValue":{"value":58,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.8,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":6433,"teamId":6433,"name":"Go Ahead Eagles","position":null,"substatValue":{"value":57,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.4,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":6413,"teamId":6413,"name":"PEC Zwolle","position":null,"substatValue":{"value":43,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.4,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":8614,"teamId":8614,"name":"Sparta Rotterdam","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8464,"teamId":8464,"name":"NEC Nijmegen","position":null,"substatValue":{"value":51,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.4,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":8674,"teamId":8674,"name":"FC Groningen","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.8,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":9908,"teamId":9908,"name":"FC Utrecht","position":null,"substatValue":{"value":62,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.5,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":9791,"teamId":9791,"name":"Heracles","position":null,"substatValue":{"value":42,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.2,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":9761,"teamId":9761,"name":"NAC Breda","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.9,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":6422,"teamId":6422,"name":"Fortuna Sittard","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.3,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":10219,"teamId":10219,"name":"RKC Waalwijk","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.8,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":8525,"teamId":8525,"name":"Willem II","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.8,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":4116,"teamId":4116,"name":"Almere City FC","position":null,"substatValue":{"value":23,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.5,"format":"percent","fractions":1},"rank":18,"type":"teams"}]"""
    
    
    
    
    team_possession_segunda = """[{"id":494050,"teamId":494050,"name":"FC Andorra","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":60.1,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":7869,"teamId":7869,"name":"Cordoba","position":null,"substatValue":{"value":41,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":57.9,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":8306,"teamId":8306,"name":"Las Palmas","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.5,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":10279,"teamId":10279,"name":"Castellon","position":null,"substatValue":{"value":49,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.3,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":9865,"teamId":9865,"name":"Almeria","position":null,"substatValue":{"value":59,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":8696,"teamId":8696,"name":"Racing Santander","position":null,"substatValue":{"value":62,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.6,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":9864,"teamId":9864,"name":"Malaga","position":null,"substatValue":{"value":52,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.5,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":7854,"teamId":7854,"name":"Leganes","position":null,"substatValue":{"value":36,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.4,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":9783,"teamId":9783,"name":"Deportivo La Coruna","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.4,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":357259,"teamId":357259,"name":"AD Ceuta FC","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.6,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":8372,"teamId":8372,"name":"Eibar","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":10281,"teamId":10281,"name":"Real Valladolid","position":null,"substatValue":{"value":36,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.6,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":7878,"teamId":7878,"name":"Granada","position":null,"substatValue":{"value":37,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.3,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":8394,"teamId":8394,"name":"Real Zaragoza","position":null,"substatValue":{"value":27,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.2,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":1753,"teamId":1753,"name":"Cultural Leonesa","position":null,"substatValue":{"value":28,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.6,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":7876,"teamId":7876,"name":"Burgos CF","position":null,"substatValue":{"value":36,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":8385,"teamId":8385,"name":"Cadiz","position":null,"substatValue":{"value":31,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.5,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":96925,"teamId":96925,"name":"SD Huesca","position":null,"substatValue":{"value":30,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.1,"format":"percent","fractions":1},"rank":18,"type":"teams"},{"id":9869,"teamId":9869,"name":"Sporting Gijon","position":null,"substatValue":{"value":42,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.9,"format":"percent","fractions":1},"rank":19,"type":"teams"},{"id":8393,"teamId":8393,"name":"Albacete","position":null,"substatValue":{"value":39,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.1,"format":"percent","fractions":1},"rank":20,"type":"teams"},{"id":161744,"teamId":161744,"name":"Real Sociedad B","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.9,"format":"percent","fractions":1},"rank":21,"type":"teams"},{"id":4032,"teamId":4032,"name":"CD Mirandes","position":null,"substatValue":{"value":30,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.4,"format":"percent","fractions":1},"rank":22,"type":"teams"}]"""
    
    
    team_possession_segunda_2425 = """[{"id":10268,"teamId":10268,"name":"Elche","position":null,"substatValue":{"value":59,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":61.7,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":10279,"teamId":10279,"name":"Castellon","position":null,"substatValue":{"value":65,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.8,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":7869,"teamId":7869,"name":"Cordoba","position":null,"substatValue":{"value":59,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.4,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":9783,"teamId":9783,"name":"Deportivo La Coruna","position":null,"substatValue":{"value":56,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.8,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":9865,"teamId":9865,"name":"Almeria","position":null,"substatValue":{"value":72,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":53.2,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":9864,"teamId":9864,"name":"Malaga","position":null,"substatValue":{"value":42,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.4,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":8696,"teamId":8696,"name":"Racing Santander","position":null,"substatValue":{"value":65,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.8,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":8670,"teamId":8670,"name":"Real Oviedo","position":null,"substatValue":{"value":56,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.7,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":7878,"teamId":7878,"name":"Granada","position":null,"substatValue":{"value":65,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.3,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":8394,"teamId":8394,"name":"Real Zaragoza","position":null,"substatValue":{"value":56,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.1,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":9869,"teamId":9869,"name":"Sporting Gijon","position":null,"substatValue":{"value":57,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.9,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":8372,"teamId":8372,"name":"Eibar","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.9,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":8581,"teamId":8581,"name":"Levante","position":null,"substatValue":{"value":69,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.1,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":7876,"teamId":7876,"name":"Burgos CF","position":null,"substatValue":{"value":41,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.5,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":8385,"teamId":8385,"name":"Cadiz","position":null,"substatValue":{"value":55,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.3,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":9867,"teamId":9867,"name":"Tenerife","position":null,"substatValue":{"value":35,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.3,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":8474,"teamId":8474,"name":"Racing de Ferrol","position":null,"substatValue":{"value":22,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.8,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":8288,"teamId":8288,"name":"Eldense","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.6,"format":"percent","fractions":1},"rank":18,"type":"teams"},{"id":4032,"teamId":4032,"name":"CD Mirandes","position":null,"substatValue":{"value":59,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.4,"format":"percent","fractions":1},"rank":19,"type":"teams"},{"id":96925,"teamId":96925,"name":"SD Huesca","position":null,"substatValue":{"value":58,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.8,"format":"percent","fractions":1},"rank":20,"type":"teams"},{"id":8393,"teamId":8393,"name":"Albacete","position":null,"substatValue":{"value":57,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":43.3,"format":"percent","fractions":1},"rank":21,"type":"teams"},{"id":8554,"teamId":8554,"name":"Cartagena","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":39.9,"format":"percent","fractions":1},"rank":22,"type":"teams"}]"""
    
    
    
    team_possession_switzerland = """[{"id":7896,"teamId":7896,"name":"Lugano","position":null,"substatValue":{"value":48,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":56.8,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":9931,"teamId":9931,"name":"Basel","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.7,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":10192,"teamId":10192,"name":"Young Boys","position":null,"substatValue":{"value":61,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":9777,"teamId":9777,"name":"Servette","position":null,"substatValue":{"value":53,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":10243,"teamId":10243,"name":"FC Zürich","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.7,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":10179,"teamId":10179,"name":"Sion","position":null,"substatValue":{"value":44,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.6,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":7730,"teamId":7730,"name":"Lausanne","position":null,"substatValue":{"value":45,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.3,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":10199,"teamId":10199,"name":"Luzern","position":null,"substatValue":{"value":62,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.8,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":10191,"teamId":10191,"name":"Thun","position":null,"substatValue":{"value":72,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.8,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":9956,"teamId":9956,"name":"Grasshopper","position":null,"substatValue":{"value":38,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.6,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":10190,"teamId":10190,"name":"St. Gallen","position":null,"substatValue":{"value":60,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.5,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":7894,"teamId":7894,"name":"Winterthur","position":null,"substatValue":{"value":34,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":42.3,"format":"percent","fractions":1},"rank":12,"type":"teams"}]"""
    
    
    team_possession_switzerland_2425 = """[{"id":7896,"teamId":7896,"name":"Lugano","position":null,"substatValue":{"value":55,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":59.6,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":10243,"teamId":10243,"name":"FC Zürich","position":null,"substatValue":{"value":56,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.4,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":9931,"teamId":9931,"name":"Basel","position":null,"substatValue":{"value":91,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":10192,"teamId":10192,"name":"Young Boys","position":null,"substatValue":{"value":60,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.2,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":10190,"teamId":10190,"name":"St. Gallen","position":null,"substatValue":{"value":52,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.1,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":9777,"teamId":9777,"name":"Servette","position":null,"substatValue":{"value":64,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.7,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":7730,"teamId":7730,"name":"Lausanne","position":null,"substatValue":{"value":62,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.3,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":10199,"teamId":10199,"name":"Luzern","position":null,"substatValue":{"value":66,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":47.9,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":10179,"teamId":10179,"name":"Sion","position":null,"substatValue":{"value":47,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.7,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":9956,"teamId":9956,"name":"Grasshopper","position":null,"substatValue":{"value":43,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.1,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":7894,"teamId":7894,"name":"Winterthur","position":null,"substatValue":{"value":43,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.3,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":6447,"teamId":6447,"name":"Yverdon","position":null,"substatValue":{"value":40,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":44.5,"format":"percent","fractions":1},"rank":12,"type":"teams"}]"""
    
    
    
    
    team_possession_mexico_2425 = """[{"id":7849,"teamId":7849,"name":"Monterrey","position":null,"substatValue":{"value":36,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":57.2,"format":"percent","fractions":1},"rank":1,"type":"teams"},{"id":6576,"teamId":6576,"name":"CF America","position":null,"substatValue":{"value":38,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":57,"format":"percent","fractions":1},"rank":2,"type":"teams"},{"id":162418,"teamId":162418,"name":"Tijuana","position":null,"substatValue":{"value":29,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.3,"format":"percent","fractions":1},"rank":3,"type":"teams"},{"id":8561,"teamId":8561,"name":"Tigres","position":null,"substatValue":{"value":27,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":55.3,"format":"percent","fractions":1},"rank":4,"type":"teams"},{"id":6358,"teamId":6358,"name":"Atletico de San Luis","position":null,"substatValue":{"value":20,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":54.5,"format":"percent","fractions":1},"rank":5,"type":"teams"},{"id":6578,"teamId":6578,"name":"Cruz Azul","position":null,"substatValue":{"value":33,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.8,"format":"percent","fractions":1},"rank":6,"type":"teams"},{"id":6618,"teamId":6618,"name":"Toluca","position":null,"substatValue":{"value":51,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":52.3,"format":"percent","fractions":1},"rank":7,"type":"teams"},{"id":7848,"teamId":7848,"name":"Pachuca","position":null,"substatValue":{"value":29,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":51.6,"format":"percent","fractions":1},"rank":8,"type":"teams"},{"id":7807,"teamId":7807,"name":"Chivas","position":null,"substatValue":{"value":18,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":50.2,"format":"percent","fractions":1},"rank":9,"type":"teams"},{"id":1946,"teamId":1946,"name":"Pumas","position":null,"substatValue":{"value":23,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":49.1,"format":"percent","fractions":1},"rank":10,"type":"teams"},{"id":1842,"teamId":1842,"name":"Necaxa","position":null,"substatValue":{"value":38,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.9,"format":"percent","fractions":1},"rank":11,"type":"teams"},{"id":1841,"teamId":1841,"name":"Leon","position":null,"substatValue":{"value":27,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.1,"format":"percent","fractions":1},"rank":12,"type":"teams"},{"id":7857,"teamId":7857,"name":"Santos Laguna","position":null,"substatValue":{"value":15,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":48.1,"format":"percent","fractions":1},"rank":13,"type":"teams"},{"id":649424,"teamId":649424,"name":"FC Juarez","position":null,"substatValue":{"value":16,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":46.8,"format":"percent","fractions":1},"rank":14,"type":"teams"},{"id":6577,"teamId":6577,"name":"Atlas","position":null,"substatValue":{"value":25,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.2,"format":"percent","fractions":1},"rank":15,"type":"teams"},{"id":1170234,"teamId":1170234,"name":"Mazatlan FC","position":null,"substatValue":{"value":16,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":45.1,"format":"percent","fractions":1},"rank":16,"type":"teams"},{"id":7847,"teamId":7847,"name":"Puebla","position":null,"substatValue":{"value":12,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":39.4,"format":"percent","fractions":1},"rank":17,"type":"teams"},{"id":1943,"teamId":1943,"name":"Queretaro FC","position":null,"substatValue":{"value":17,"format":"number","fractions":0},"statValue":{"name":"possession_percentage_team","value":37.2,"format":"percent","fractions":1},"rank":18,"type":"teams"}]"""
    
    
    
    
        
    # Unificamos todos tus diccionarios en uno solo para acceso rápido
    master_possession = {
        "25/26": {
            "Spain": convertir_a_mapeo(team_possession_laliga),
            "England": convertir_a_mapeo(team_possession_premierl),
            "Italy": convertir_a_mapeo(team_possession_seriea),
            "Germany": convertir_a_mapeo(team_possession_bundes),
            "France": convertir_a_mapeo(team_possession_ligue1),
            "Belgium": convertir_a_mapeo(team_possession_proleague),
            "Portugal": convertir_a_mapeo(team_possession_portugal),
            "England 2": convertir_a_mapeo(team_possession_championship),
            "Switzerland": convertir_a_mapeo(team_possession_switzerland),
            "Denmark": convertir_a_mapeo(team_possession_denmark),
            "Netherlands": convertir_a_mapeo(team_possession_netherlands),
            "Spain 2": convertir_a_mapeo(team_possession_segunda)
    
            # Añade aquí el resto de ligas 2526
        },
        "24/25_2025": {
            "Spain": convertir_a_mapeo(team_possession_laliga_2425),
            "England": convertir_a_mapeo(team_possession_premierl_2425),
            "Italy": convertir_a_mapeo(team_possession_seriea_2425),
            "Germany": convertir_a_mapeo(team_possession_bundes_2425),
            "France": convertir_a_mapeo(team_possession_ligue1_2425),
            "Belgium": convertir_a_mapeo(team_possession_proleague_2425),
            "Portugal": convertir_a_mapeo(team_possession_portugal_2425),
            "England 2": convertir_a_mapeo(team_possession_championship_2425),
            "Switzerland": convertir_a_mapeo(team_possession_switzerland_2425),
            "Denmark": convertir_a_mapeo(team_possession_denmark_2425),
            "Netherlands": convertir_a_mapeo(team_possession_netherlands_2425),
            "Spain 2": convertir_a_mapeo(team_possession_segunda_2425),
            "Mexico": convertir_a_mapeo(team_possession_mexico_2425),
            "USA": convertir_a_mapeo(team_possession_mls_2025),
            "Brazil": convertir_a_mapeo(team_possession_brazil_2025),
            "Italy": convertir_a_mapeo(team_possession_argentina_2025)
    
    
            # "Brazil": possession_mapping_brazil, etc.
        }
    }
    
    # Aplicar posesión a cada archivo individual de tus listas
    for df in list_2526:
        liga = df['Liga'].iloc[0]
        mapa = master_possession["25/26"].get(liga, {})
        df['team_possession'] = df['Equipo'].map(mapa).fillna(50.0)
    
    for df in list_2425:
        liga = df['Liga'].iloc[0]
        mapa = master_possession["24/25_2025"].get(liga, {})
        df['team_possession'] = df['Equipo'].map(mapa).fillna(50.0)
    
    print("✅ Columna 'team_possession' añadida a cada archivo individualmente.")

    return list_2526, list_2425
    
    
def limpieza_posiciones():
    # ==========================================
# LIMPIEZA DE POSICIONES MÚLTIPLES
# ==========================================

# ==========================================
# 1. LIMPIEZA DE POSICIONES PRINCIPALES
# ==========================================

    print("Limpiando posiciones en Temporada 25/26...")
    for df in list_2526:
        # 1. Quitamos espacios en blanco extra (ej: " RB, RWB")
        df['Posición específica'] = df['Posición específica'].str.strip()
        
        # 2. Extraemos la primera posición (la principal)
        # Ejemplo: "RB, RWB" -> "RB"
        df['Posición_Principal'] = df['Posición específica'].str.split(',').str[0].str.strip()
        
        # (Opcional) Verificación rápida de la liga procesada
        liga = df['Liga'].iloc[0] if 'Liga' in df.columns else "Desconocida"
        print(f"  ✅ Posiciones normalizadas en: {liga}")
    
    print("\nLimpiando posiciones en Temporada 24/25...")
    for df in list_2425:
        df['Posición específica'] = df['Posición específica'].str.strip()
        df['Posición_Principal'] = df['Posición específica'].str.split(',').str[0].str.strip()
        
        liga = df['Liga'].iloc[0] if 'Liga' in df.columns else "Desconocida"
        print(f"  ✅ Posiciones normalizadas en: {liga}")
    
    # ==========================================
    # 2. VERIFICACIÓN DE RESULTADOS
    # ==========================================
    # Vamos a ver cómo ha quedado un ejemplo (si hay datos)
    if list_2526:
        print("\nEjemplo de las posiciones creadas (Top 5 jugadores del primer archivo):")
        cols_verificar = ['Jugador', 'Posición específica', 'Posición_Principal']
        # Buscamos las columnas que existan para no dar error
        cols_presentes = [c for c in cols_verificar if c in list_2526[0].columns]
        print(list_2526[0][cols_presentes].head())

    return list_2425, list_2526


from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
def rankings(df):
        
    
    # ==========================================
    # 1. SELECTOR DE POSICIÓN
    # ==========================================
    TARGET_POS = "RB"
    
    mapeo_grupos = {
        "RCMF": "CMF", "LCMF": "CMF",
        "RAMF": "RW", "LAMF": "LW",
        "LWF" : "LW",
        "LDMF" : "DMF", "RDMF" : "DMF",
        "RWB" : "RB", "LWB" : "LB",
        "LCB" : "CB", "RCB" : "CB"
    }
    
    config_posiciones = {
        "CB": {
            "defensivas": ['Interceptaciones/90', 'Entradas/90', "Duelos defensivos/90", 
                        "Duelos aéreos en los 90", "Faltas/90"],
            "ofensivas": ['Pases progresivos/90', 'Carreras en progresión/90', 
                        'Pases largos/90'],
            "pilares": {
                "Aggressiveness": ["Faltas/90_PAdj", "Entradas/90_PAdj"],
                "Aerial": ["Duelos aéreos en los 90_PAdj", "Duelos aéreos ganados, %"],
                "Duels": ["Duelos defensivos ganados, %", "Duelos defensivos/90_PAdj"],
                "Reading" : ["Interceptaciones/90_PAdj"],
                "Verticality": ["Pases progresivos/90_OPAdj", "Precisión pases progresivos, %"],
                "Long_Ball": ["Pases largos/90_OPAdj", "Precisión pases largos, %"],
                "Carrying": ["Carreras en progresión/90_OPAdj"]
            }
        },
        "RB": {
            "defensivas": ['Interceptaciones/90', 'Entradas/90', "Duelos defensivos/90", 
                        "Faltas/90", "Duelos aéreos en los 90"],
            "ofensivas": ['Pases progresivos/90', 'Carreras en progresión/90', 
                        'Pases largos/90', "Centros/90", 
                        "Regates/90", "xA/90", "Desmarques/90", "xG/90"],
            "pilares": {
                "Aggressiveness": ["Faltas/90_PAdj", "Entradas/90_PAdj"],
                "Defensive Duels": ["Duelos defensivos ganados, %", "Duelos defensivos/90_PAdj"],
                "Interceptions" : ["Interceptaciones/90_PAdj"],
                "Progressive Passing": ["Pases progresivos/90_OPAdj", "Precisión pases progresivos, %"],
                "Long Passing": ["Pases largos/90_OPAdj", "Precisión pases largos, %"],
                "Carrying": ["Carreras en progresión/90_OPAdj"],
                "Dribbling" : ["Regates/90_OPAdj", "Regates realizados, %"],
                "Crossing" : ["Crossing/90_OPAdj", "Precisión centros, %"],
                "Creativity" : ["xA/90_OPAdj"],
                "Runs in Behind" : ["Desmarques/90_OPAdj", "Precisión desmarques, %"],
                "Goal Threat" : ["xG/90_OPAdj"],
                "Aerial Duels": ["Duelos aéreos en los 90_PAdj", "Duelos aéreos ganados, %"],
    
            }
        },
        "LB": {
            "defensivas": ['Interceptaciones/90', 'Entradas/90', "Duelos defensivos/90", 
                        "Faltas/90"],
            "ofensivas": ['Pases progresivos/90', 'Carreras en progresión/90', 
                        'Pases largos/90', "Pases/90", "Centros/90", 
                        "Regates/90", "xA/90", "Desmarques/90"],
            "pilares": {
                "Aggressiveness": ["Faltas/90_PAdj", "Entradas/90_PAdj"],
                "Duels": ["Duelos defensivos ganados, %", "Duelos defensivos/90_PAdj"],
                "Reading" : ["Interceptaciones/90_PAdj"],
                "Passing_Volume": ["Pases/90_OPAdj", "Precisión pases, %"],
                "Verticality": ["Pases progresivos/90_OPAdj", "Precisión pases progresivos, %"],
                "Long_Ball": ["Pases largos/90_OPAdj", "Precisión pases largos, %"],
                "Carrying": ["Carreras en progresión/90_OPAdj"],
                "Dribbling" : ["Regates/90_OPAdj", "Regates realizados, %"],
                "Crossing" : ["Crossing/90_OPAdj", "Precisión centros, %"],
                "Assists" : ["xA/90_OPAdj"],
                "Desmarques" : ["Desmarques/90_OPAdj", "Precisión desmarques, %"]
    
            }
        },
        "DM": {
            "defensivas": ['Interceptaciones/90', 'Entradas/90', "Duelos defensivos/90", 
                        "Duelos aéreos en los 90", "Faltas/90"],
            "ofensivas": ['Pases progresivos/90', 'Carreras en progresión/90', 
                        'Pases largos/90', "Pases/90"],
            "pilares": {
                "Aggressiveness": ["Faltas/90_PAdj", "Entradas/90_PAdj"],
                "Aerial": ["Duelos aéreos en los 90_PAdj", "Duelos aéreos ganados, %"],
                "Duels": ["Duelos defensivos ganados, %", "Duelos defensivos/90_PAdj"],
                "Reading" : ["Interceptaciones/90_PAdj"],
                "Passing_Volume": ["Pases/90_OPAdj", "Precisión pases, %"],
                "Verticality": ["Pases progresivos/90_OPAdj", "Precisión pases progresivos, %"],
                "Long_Ball": ["Pases largos/90_OPAdj", "Precisión pases largos, %"],
                "Dribbling": ["Carreras en progresión/90_OPAdj"]
            }
        },
        "CMF": {
            "defensivas": ['Interceptaciones/90', 'Entradas/90', "Duelos defensivos/90", 
                        "Duelos aéreos en los 90", "Faltas/90"],
            "ofensivas": ['Pases progresivos/90', 'Carreras en progresión/90', 
                        'Pases largos/90', "xG/90", "Regates/90", "xA/90", "Pases en profunidad/90"],
            "pilares": {
                "Aggressiveness": ["Faltas/90_PAdj", "Entradas/90_PAdj"],
                "Duels": ["Duelos defensivos ganados, %", "Duelos defensivos/90_PAdj"],
                "Reading" : ["Interceptaciones/90_PAdj"],
                "Verticality": ["Pases progresivos/90_OPAdj", "Precisión pases progresivos, %"],
                "Long_Ball": ["Pases largos/90_OPAdj", "Precisión pases largos, %"],
                "Carrying": ["Carreras en progresión/90_OPAdj"],
                "Profundidad" : ["Pases en profundidad/90_OPAdj", "Precisión pases en profundidad, %"],
                "Dribbling" : ["Regates/90_OPAdj", "Regates realizados, %"],
                "Assists" : ["xA/90_OPAdj"],
                "Goals" : ["xG/90_OPAdj"]
            }
        },
        "AMF": {
            "defensivas": [],
            "ofensivas": ['Pases progresivos/90', 'Carreras en progresión/90', 
                        'Pases largos/90', "xG/90", "Regates/90", "xA/90", "Pases en profunidad/90", "Desmarques/90"],
            "pilares": {
                "Verticality": ["Pases progresivos/90_OPAdj", "Precisión pases progresivos, %"],
                "Long_Ball": ["Pases largos/90_OPAdj", "Precisión pases largos, %"],
                "Carrying": ["Carreras en progresión/90_OPAdj"],
                "Dribbling" : ["Regates/90_OPAdj", "Regates realizados, %"],
                "Assists" : ["xA/90_OPAdj"],
                "Goals" : ["xG/90_OPAdj"],
                "Profundidad" : ["Pases en profundidad/90_OPAdj", "Precisión pases en profundidad, %"],
                "Desmarques" : ["Desmarques/90_OPAdj", "Precisión desmarques, %"]
    
    
            }
        },
        "LW": {
            "defensivas": [],
            "ofensivas": ["Pases progresivos/90", "Carreras en progresión/90", 
                          "xG/90", "Regates/90", "xA/90", "Centros/90", "Pases en profunidad/90", "Desmarques/90"],
            "pilares": {
                "Progressive Passing": ["Pases progresivos/90_OPAdj", "Precisión pases progresivos, %"],
                "Carrying": ["Carreras en progresión/90_OPAdj"],
                "Dribbling" : ["Regates/90_OPAdj", "Regates realizados, %"],
                "Creativity" : ["xA/90_OPAdj"],
                "Goal Threat" : ["xG/90_OPAdj"],
                "Crossing" : ["Crossing/90_OPAdj", "Precisión centros, %"],
                "Passes in Behind" : ["Pases en profundidad/90_OPAdj", "Precisión pases en profundidad, %"],
                "Runs in Behind" : ["Desmarques/90_OPAdj", "Precisión desmarques, %"]
            }
        },
        "RW": {
            "defensivas": [],
            "ofensivas": ["Pases progresivos/90", "Carreras en progresión/90", 
                          "xG/90", "Regates/90", "xA/90", "Centros/90", "Pases en profunidad/90", "Desmarques/90"],
            "pilares": {
                "Progressive Passing": ["Pases progresivos/90_OPAdj", "Precisión pases progresivos, %"],
                "Carrying": ["Carreras en progresión/90_OPAdj"],
                "Dribbling" : ["Regates/90_OPAdj", "Regates realizados, %"],
                "Creativity" : ["xA/90_OPAdj"],
                "Goal Threat" : ["xG/90_OPAdj"],
                "Crossing" : ["Crossing/90_OPAdj", "Precisión centros, %"],
                "Passes in Behind" : ["Pases en profundidad/90_OPAdj", "Precisión pases en profundidad, %"],
                "Runs in Behind" : ["Desmarques/90_OPAdj", "Precisión desmarques, %"]
            }
        },
        "CF": {
            "defensivas": [],
            "ofensivas": ["Pases progresivos/90", "Carreras en progresión/90", 
                          "xG/90", "Regates/90", "xA/90", "Pases en profunidad/90", "Desmarques/90"],
            "pilares": {
                "Verticality": ["Pases progresivos/90_OPAdj", "Precisión pases progresivos, %"],
                "Carrying": ["Carreras en progresión/90_OPAdj"],
                "Dribbling" : ["Regates/90_OPAdj", "Regates realizados, %"],
                "Assists" : ["xA/90_OPAdj"],
                "Goals" : ["xG/90_OPAdj"],
                "Profundidad" : ["Pases en profundidad/90_OPAdj", "Precisión pases en profundidad, %"],
                "Desmarques" : ["Desmarques/90_OPAdj", "Precisión desmarques, %"]
            }
        },
        
    }
    elo_map = {
        "Spain": 1.0, "USA": 0.904, "England": 1.053, "Italy": 0.986, 
        "Germany": 0.985, "France": 0.976, "Belgium": 0.932, "Portugal": 0.928, 
        "Argentina": 0.927, "Brazil": 0.927, "England 2": 0.924, "Denmark": 0.914, 
        "Netherlands": 0.896, "Spain 2": 0.892, "Switzerland": 0.882, "Mexico": 0.878
    }
    # ==========================================
    # 2. FUNCIÓN DE PROCESAMIENTO POR TEMPORADA
    # ==========================================
    df = df.copy()
    
    # Normalización de Posiciones
    df['Posición específica'] = df['Posición específica'].str.strip()
    df['Posición_Principal'] = df['Posición específica'].str.split(',').str[0]
    df['Pos_Normalizada'] = df['Posición_Principal'].map(mapeo_grupos).fillna(df['Posición_Principal'])
    
    grupo_buscado = mapeo_grupos.get(TARGET_POS, TARGET_POS)
    conf = config_posiciones.get(grupo_buscado)

    if not conf:
        print(f"⚠️ No hay configuración para: {grupo_buscado}")
        return df

    # Filtramos por posición
    df = df[df['Pos_Normalizada'] == TARGET_POS].copy()
    if df.empty:
        return df

    # --- CÁLCULOS PADJ ---
    # Usamos la columna 'team_possession' que ya viene en el DF desde la función anterior
    for stat in conf["defensivas"]:
        if stat in df.columns:
            df[f'{stat}_PAdj'] = df[stat] * (50 / (100 - df['team_possession']))
    
    for stat in conf["ofensivas"]:
        if stat in df.columns:
            df[f'{stat}_OPAdj'] = df[stat] * (50 / df['team_possession'])

    # --- RANKING POR LIGA + ELO ---
    all_results = []
    for liga, df_liga in df.groupby('Liga'):
        df_liga = df_liga.copy()
        factor = elo_map.get(liga, 1.0)
        rating_cols = []
        
        for pilar, metrics in conf["pilares"].items():
            valid_m = [m for m in metrics if m in df_liga.columns]
            if valid_m:
                # Rank local (percentil 0-100)
                temp_pcts = [df_liga[m].rank(pct=True) * 100 for m in valid_m]
                pilar_pct_avg = pd.concat(temp_pcts, axis=1).mean(axis=1)
                
                col_name = f"{pilar}_Rating"
                df_liga[col_name] = pilar_pct_avg * factor
                rating_cols.append(col_name)
        
        if rating_cols:
            df_liga['Final_Score'] = df_liga[rating_cols].mean(axis=1)
            all_results.append(df_liga)

    return pd.concat(all_results, ignore_index=True) if all_results else df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Radar
from sklearn.metrics.pairwise import cosine_similarity

from mplsoccer import Radar
import matplotlib.pyplot as plt
import numpy as np

def plot_omni_radar_evolutivo(players_list):
    """
    Versión Final: Sigue estrictamente el diseño de referencia para 1, 2 o 3 jugadores.
    """
    extracted_data, labels = [], []
    
    # 1. Extraer datos (maneja hasta 3 jugadores)
    for name, df, label in players_list:
        try:
            row = df[df['Jugador'] == name].iloc[0]
            extracted_data.append(row)
            labels.append(label)
        except (IndexError, KeyError):
            continue
            
    if not extracted_data:
        return None

    # 2. Configurar Pilares
    pilares_cols = [c for c in extracted_data[0].index if '_Rating' in c]
    params = [c.replace('_Rating', '') for c in pilares_cols]
    values = [p[pilares_cols].values.flatten().tolist() for p in extracted_data]
    
    low = [0] * len(params)
    high = [100] * len(params)
    
    # Colores profesionales del diseño de referencia
    colors = ['#77BA99', '#E84855', '#F3E03B'] # Verde, Rojo, Amarillo
    edge_colors = ['#225533', '#991122', '#C2B11B']

    # 3. Inicializar Radar
    try:
        radar = Radar(params, low, high, round_int=[False]*len(params), num_rings=5, center_circle_radius=1)
    except TypeError:
        radar = Radar(params, low, high, num_rings=5, center_circle_radius=1)

    fig, ax = radar.setup_axis()
    radar.draw_circles(ax=ax, facecolor='#f5f5f5', edgecolor='#dddddd', zorder=1)

    # 4. Dibujar Radares (con el estilo exacto de kwargs)
    for i, (val, color, edge) in enumerate(zip(values, colors, edge_colors)):
        radar.draw_radar(ax=ax, values=val, 
                         kwargs_radar={'facecolor': color, 'alpha': 0.4, 'edgecolor': edge, 'lw': 2},
                         kwargs_rings={'facecolor': color, 'alpha': 0.1})
    
    # Etiquetas con tipografía monospace
    radar.draw_range_labels(ax=ax, fontsize=9, fontproperties="monospace", zorder=12)
    radar.draw_param_labels(ax=ax, fontsize=11, fontproperties="monospace", fontweight='bold', zorder=12)

    # 5. Título Dinámico con el espaciado solicitado
    # Usamos las etiquetas (labels) que vienen del app.py
    if len(labels) == 1:
        fig.text(0.5, 0.95, labels[0], size=14, color=colors[0], ha="center", fontweight='bold')
    elif len(labels) == 2:
        fig.text(0.45, 0.95, labels[0], size=14, color=colors[0], ha="right", fontweight='bold')
        fig.text(0.5, 0.95, " vs", size=14, color="black", ha="center")
        fig.text(0.55, 0.95, labels[1], size=14, color=colors[1], ha="left", fontweight='bold')
    elif len(labels) >= 3:
        fig.text(0.35, 0.95, labels[0], size=14, color=colors[0], ha="right", fontweight='bold')
        fig.text(0.4, 0.95, " vs", size=14, color="black", ha="center")
        fig.text(0.50, 0.95, labels[1], size=14, color=colors[1], ha="center", fontweight='bold')
        fig.text(0.6, 0.95, " vs ", size=14, color="black", ha="center")
        fig.text(0.65, 0.95, labels[2], size=14, color=colors[2], ha="left", fontweight='bold')

    # Créditos y nota metodológica inferior
    ax.text(0.0, -0.1, 
            'Ratings: Percentile-based (0-100)\nAdjusted by Team Possession & League ELO', 
            fontsize=9, ha='left', va='center', transform=ax.transAxes, fontfamily='monospace', color='#555555')

    return fig


import pandas as pd

def aplicar_filtros_scouting_st(df_temporada, filtros):
    """
    Filtra un DataFrame de temporada basado en un diccionario de métricas y valores mínimos.
    
    Args:
        df_temporada (pd.DataFrame): El DataFrame de la temporada seleccionada (24/25 o 25/26).
        filtros (dict): Diccionario donde la clave es el nombre de la métrica (_Rating) 
                        y el valor es el mínimo (0-100).
    
    Returns:
        pd.DataFrame: DataFrame filtrado y ordenado por Final_Score.
    """
    if df_temporada is None or df_temporada.empty:
        return pd.DataFrame()

    # Hacemos una copia para no alterar los datos originales en el Session State
    df_res = df_temporada.copy()

    # Aplicamos los filtros de métricas dinámicamente
    for columna, valor_minimo in filtros.items():
        if valor_minimo > 0: # Solo aplicamos el filtro si el usuario movió el slider
            if columna in df_res.columns:
                df_res = df_res[df_res[columna] >= valor_minimo]
            else:
                # Si por alguna razón la métrica no existe en esa temporada, la saltamos
                continue

    # Ordenamos por la puntuación final de mayor a menor
    if 'Final_Score' in df_res.columns:
        df_res = df_res.sort_values(by='Final_Score', ascending=False)
    
    return df_res

from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

def plot_similar_players_cross_st(player_name, df_origen, df_destino, top_n=10):
    # 1. Definir características
    features = [c for c in df_origen.columns if "_Rating" in c]
    features = [f for f in features if f in df_destino.columns]
    
    if player_name not in df_origen['Jugador'].values:
        return None

    # 2. Filtrar Destino (Top 5 Ligas)
    top_5 = ['La Liga', 'Premier League', 'Bundesliga', 'Serie A', 'Ligue 1']
    df_destino_filt = df_destino[df_destino['Liga'].isin(top_5)].copy()

    if df_destino_filt.empty:
        df_destino_filt = df_destino.copy()

    # 3. ADN del jugador objetivo
    target_vector = df_origen[df_origen['Jugador'] == player_name][features].fillna(0).values
    
    # 4. Matriz de candidatos
    candidatos_matrix = df_destino_filt[features].fillna(0).values
    
    # 5. Cálculo de Similitud
    try:
        sim_scores_array = cosine_similarity(target_vector, candidatos_matrix)[0]
        sim_scores = sorted(list(enumerate(sim_scores_array)), key=lambda x: x[1], reverse=True)
        
        final_sim_scores = []
        for i, score in sim_scores:
            nombre_candidato = df_destino_filt.iloc[i]['Jugador']
            if nombre_candidato == player_name and score > 0.99:
                continue
            final_sim_scores.append((i, score))
            if len(final_sim_scores) >= top_n:
                break

        # 6. Crear Gráfico con NOMBRES + EQUIPOS
        # Ajustamos esta parte para sacar el equipo (asumiendo que la columna se llama 'Equipo')
        names = []
        for i, _ in final_sim_scores:
            p_name = df_destino_filt.iloc[i]['Jugador']
            p_team = df_destino_filt.iloc[i]['Equipo'] # <--- Cambia 'Equipo' si tu columna se llama distinto
            names.append(f"{p_name} ({p_team})")

        similarities = [score * 100 for _, score in final_sim_scores]

        if not names: return None

        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#ffffff')
        bars = ax.barh(names, similarities, color='#D4AF37', edgecolor='black', alpha=0.8)
        ax.invert_yaxis()
        
        # Ajustamos el límite para que se vean bien los nombres largos
        ax.set_xlim(max(0, min(similarities)-10), 105)
        ax.set_title(f"Statistical Twins: Players similar to {player_name}", fontweight='bold', pad=20)
        
        for bar in bars:
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                    f'{bar.get_width():.1f}%', va='center', fontweight='bold')
        
        plt.tight_layout()
        return fig
    except Exception as e:
        print(f"Error en similitud: {e}")
        return None
def plot_zscore_st(lista_jugadores, titulo="Comparativa Z-Score"):
    player_data_list, pilares_cols = [], []
    for nombre, df_origen in lista_jugadores:
        if df_origen.empty: continue
        if not pilares_cols: pilares_cols = [c for c in df_origen.columns if '_Rating' in c]
        df_z = df_origen.copy()
        for col in pilares_cols:
            df_z[f'z_{col}'] = (df_z[col] - df_z.groupby('Liga')[col].transform('mean')) / (df_z.groupby('Liga')[col].transform('std') + 1e-6)
        try:
            player_data_list.append(df_z[df_z['Jugador'] == nombre].iloc[0])
        except: continue
    
    if not player_data_list: return None
    params = [c.replace('_Rating', '') for c in pilares_cols]
    fig, ax = plt.subplots(figsize=(10, 7))
    y = np.arange(len(params))
    height = 0.8 / len(player_data_list)
    colors = ['#77BA99', '#E84855', '#3182CE']
    for i, data in enumerate(player_data_list):
        z_vals = [data[f'z_{col}'] for col in pilares_cols]
        ax.barh(y + (i - (len(player_data_list)-1)/2) * height, z_vals, height, label=data['Jugador'], color=colors[i%3])
    ax.axvline(0, color='black', lw=1)
    ax.set_yticks(y)
    ax.set_yticklabels(params, fontweight='bold')
    ax.legend()
    return fig

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_market_analysis_st(df_temporada, target_player, metrics, titulo_temp=""):
    """
    Gráfico de dispersión blindado para que siempre muestre la nube de puntos referencia,
    usando la estética de la imagen de ejemplo.
    """
    if df_temporada is None or df_temporada.empty: return None

    df_plot = df_temporada.copy()
    col_age = 'Edad' if 'Edad' in df_temporada.columns else 'Age'
    col_name = 'Jugador' if 'Jugador' in df_temporada.columns else 'Name'
    col_liga = 'Liga' if 'Liga' in df_temporada.columns else 'League'

    # 1. Crear métrica combinada
    # Usamos .fillna(0) para que no haya errores si falta un rating
    df_plot['Combined'] = df_plot[metrics].mean(axis=1).fillna(0)

    # 2. DEFINIR POBLACIÓN DE REFERENCIA (TOP 5 LIGAS)
    # Lógica Blindada: Intentamos detectar automáticamente los nombres de ligas Top 5
    top_5_posibles = [
        ['Spain', 'England', 'Germany', 'Italy', 'France'],  # Inglés (Estándar)
        ['ESPAÑA', 'INGLATERRA', 'ALEMANIA', 'ITALIA', 'FRANCIA'], # Español (Mayús)
        ['España', 'Inglaterra', 'Alemania', 'Italia', 'Francia'] # Español (Minús)
    ]
    
    df_poblacion = pd.DataFrame() # Vacío inicialmente
    found_top_5 = False
    
    # Probamos cada lista de nombres hasta encontrar una que devuelva datos
    for lista in top_5_posibles:
        df_temp_filt = df_plot[df_plot[col_liga].isin(lista)].copy()
        if not df_temp_filt.empty:
            df_poblacion = df_temp_filt
            found_top_5 = True
            break # Paramos en la primera que funcione

    # PLAN B: Si no detectamos Top 5, usamos TODO el DataFrame para que no salga vacío
    if df_poblacion.empty:
        df_poblacion = df_plot.copy()
        found_top_5 = False

    # 3. EXTRAER TARGET
    df_target = df_plot[df_plot[col_name] == target_player].copy()
    
    # 4. CREAR EL GRÁFICO (Estética de image_0.png)
    # Usamos el color de fondo de la imagen de ejemplo
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='#FCF9F0')
    ax.set_facecolor('#FCF9F0')
    
    # Separar Veteranos de U23 (Población de referencia)
    u23_ref = df_poblacion[df_poblacion[col_age] <= 23]
    vets_ref = df_poblacion[df_poblacion[col_age] > 23]
    
    # --- Dibujar Puntos de Fondo ---
    # Veteranos (Puntos grises de image_0.png)
    ax.scatter(vets_ref[col_age], vets_ref['Combined'], 
               color='#d3d3d3', alpha=0.4, s=60, label='Veterans')
    
    # U23 / Prospects (Puntos azules con borde de image_0.png)
    ax.scatter(u23_ref[col_age], u23_ref['Combined'], 
               color='#5DA5DA', alpha=0.8, s=120, edgecolor='black', lw=1.2, label='U23')

    # --- Resaltar TARGET (Estrella Amarilla de image_0.png) ---
    if not df_target.empty:
        p = df_target.iloc[0]
        # Dibujamos la estrella gigante
        ax.scatter(p[col_age], p['Combined'], 
                   color='#FDD835', s=600, marker='*', edgecolor='black', zorder=15, label=f'TARGET: {target_player}')
        
        # Etiquetas de los jugadores más cercanos (Benchmarks)
        # Calculamos distancia euclidiana
        df_poblacion['dist'] = np.sqrt((df_poblacion[col_age] - p[col_age])**2 + (df_poblacion['Combined'] - p['Combined'])**2)
        closest = df_poblacion[df_poblacion[col_name] != target_player].sort_values('dist').head(6)
        
        # Usamos ajuste dinámico para que no se pisen las etiquetas si es posible
        from matplotlib import text
        for _, row in closest.iterrows():
            ax.text(row[col_age], row['Combined'] + 1.8, row[col_name], 
                    fontsize=8.5, ha='center', fontweight='bold', color='#333333',
                    bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))

    # --- Líneas de Referencia (Estilo image_0.png) ---
    mean_combined = df_poblacion['Combined'].mean()
    # Línea punteada horizontal (Media Élite)
    ax.axhline(mean_combined, color='gray', linestyle=(0, (1, 10)), lw=1.5, alpha=0.6, label='Mean')
    # Línea discontinua vertical (División Edad U23/Vets)
    ax.axvline(23.5, color='#F8BBD0', linestyle=(0, (5, 5)), lw=1.5, alpha=0.8)
    
    # --- Estética Final ---
    ax.set_title(f'Market Positioning {titulo_temp}: {target_player}', fontsize=16, fontweight='bold', pad=30)
    ax.set_xlabel('Age', fontsize=11, labelpad=10)
    # Nombre dinámico para el eje Y según las métricas elegidas
    nombre_metrica_y = 'Combined Rating (Ratings)'
    if len(metrics) > 0:
        nombres_c = [m.replace('_Rating','') for m in metrics]
        nombre_metrica_y = f'{" + ".join(nombres_c)}'
    ax.set_ylabel(f'Combined Rating ({nombre_metrica_y})', fontsize=11, labelpad=10)
    
    ax.legend(loc='lower right', facecolor='white', frameon=True, fontsize=10)
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    
    return fig

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_player_bio_card(df, player_name):
    try:
        row = df[df['Jugador'] == player_name].iloc[0]
        # Extraer ratings para sacar las mejores virtudes
        ratings = {c.replace('_Rating', ''): row[c] for c in df.columns if '_Rating' in c}
        top_3 = sorted(ratings.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "Equipo": row['Equipo'],
            "Liga": row['Liga'],
            "Edad": int(row['Edad']),
            "Puntuación": round(row['Final_Score'], 1),
            "Top Virtudes": top_3
        }
    except:
        return None

def plot_league_rank_st(df, player_name):
    try:
        row_target = df[df['Jugador'] == player_name].iloc[0]
        liga_target = row_target['Liga']
        
        # Filtramos solo su liga
        df_liga = df[df['Liga'] == liga_target].copy()
        metrics = [c for c in df.columns if '_Rating' in c]
        
        # Calculamos el rango (ej: 1º de 40 jugadores en Dribbling)
        ranks = []
        for m in metrics:
            df_liga[f'rank_{m}'] = df_liga[m].rank(ascending=False)
            pos = int(df_liga[df_liga['Jugador'] == player_name][f'rank_{m}'].iloc[0])
            total = len(df_liga)
            percentile = (row_target[m]) # Usamos el rating directamente para la barra
            ranks.append({'Metrica': m.replace('_Rating',''), 'Posicion': pos, 'Total': total, 'Valor': percentile})
        
        df_rank = pd.DataFrame(ranks).sort_values('Valor', ascending=True)

        # Gráfico de barras horizontales
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = plt.cm.RdYlGn(np.array(df_rank['Valor'])/100)
        bars = ax.barh(df_rank['Metrica'], df_rank['Valor'], color=colors, edgecolor='black', alpha=0.7)
        
        # Añadir texto de posición (ej: "1º / 45")
        for i, bar in enumerate(bars):
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                    f"Pos: {df_rank.iloc[i]['Posicion']}º de {df_rank.iloc[i]['Total']}", 
                    va='center', fontweight='bold', fontsize=9)

        ax.set_xlim(0, 115)
        ax.set_title(f"Performance vs {liga_target}", fontsize=12, fontweight='bold')
        sns.despine(left=True, bottom=True)
        return fig
    except:
        return None
