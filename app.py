import streamlit as st
import scouting_general as sg
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Maastricht Scout Terminal", layout="wide", page_icon="⚽")

# 2. Carga y Procesamiento Inicial (Solo ocurre una vez)
if 'df_2425' not in st.session_state or 'df_2526' not in st.session_state:
    with st.spinner('Procesando datos y calculando rankings...'):
        # 1. Obtener las listas
        list_2425_raw, list_2526_raw = sg.cargar_todo()
        
        # 2. Añadir posesión
        list_2526_proc, list_2425_proc = sg.cargar_posesión(list_2526_raw, list_2425_raw)
        
        # 3. Convertir a DataFrames
        df_2526 = pd.concat(list_2526_proc, ignore_index=True)
        df_2425 = pd.concat(list_2425_proc, ignore_index=True)
        
        # 4. Aplicar rankings
        # Guardamos en session_state para que no se borren al tocar filtros
        st.session_state.df_2526 = sg.rankings(df_2526)
        st.session_state.df_2425 = sg.rankings(df_2425)

# --- A partir de aquí, el código se ejecuta siempre ---

st.title("⚽ Plataforma de Scouting Profesional")
st.markdown("---")

# 3. Barra Lateral (Filtros)
st.sidebar.header("🔍 Filtros de Búsqueda")

# Selector de Temporada
temp_choice = st.sidebar.selectbox("Temporada", ["2025/2026", "2024/2025"])

# Elegimos el DataFrame basado en la temporada
if temp_choice == "2025/2026":
    df_actual = st.session_state.df_2526
else:
    df_actual = st.session_state.df_2425

# Filtro de Liga
ligas_disponibles = sorted(df_actual["Liga"].unique())
liga_select = st.sidebar.selectbox("Seleccionar Liga", ligas_disponibles)

# Filtro de Posición (Asegúrate de que la columna se llame 'Pos_Normalizada' o 'Posición')
posiciones = sorted(df_actual["Pos_Normalizada"].unique())
pos_select = st.sidebar.multiselect("Filtrar por Posición", posiciones)

# 4. Filtrado de los datos
df_display = df_actual[df_actual["Liga"] == liga_select]

if pos_select:
    df_display = df_display[df_display["Pos_Normalizada"].isin(pos_select)]

# 5. Visualización del Ranking
st.subheader(f"Top Jugadores Identificados: {liga_select} ({temp_choice})")

# IMPORTANTE: Cambia 'Final_Score' por el nombre exacto que devuelve tu función sg.rankings
col_score = "Final_Score" 

if col_score in df_display.columns:
    df_ranked = df_display.sort_values(by=col_score, ascending=False)
    
    # Selecciona las columnas que quieres mostrar (ajusta según tus Excels)
    columnas_ver = ['Jugador', 'Equipo', 'Edad', 'Pos_Normalizada', col_score]
    # Filtramos solo las que existan para evitar errores
    cols_validas = [c for c in columnas_ver if c in df_ranked.columns]
    
    st.dataframe(
        df_ranked[cols_validas].head(20),
        use_container_width=True
    )
else:
    st.warning(f"No se encontró la columna de puntuación. Revisa tu función sg.rankings.")
    st.write("Columnas disponibles:", df_display.columns.tolist())

# 6. Comparativa rápida
st.markdown("---")
if not df_display.empty:
    st.info("💡 Consejo para la demo: Al cambiar la temporada, los rankings se recalculan automáticamente usando los datos de ese año.")

import matplotlib.pyplot as plt
from mplsoccer import Radar

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "👤 Perfil Jugador", 
    "🏆 Rango en Liga", 
    "📊 Radar Evolutivo", 
    "🔍 Búsqueda", 
    "👯 Similitud", 
    "📈 Z-Score", 
    "🌍 Mercado"
])

# --- TAB 1: PERFIL RÁPIDO ---
with tab1:
    st.header("👤 Ficha Técnica del Jugador")
    temp_bio = st.radio("Temporada:", ["25/26", "24/25"], key="bio_temp", horizontal=True)
    df_bio = st.session_state.df_2526 if temp_bio == "25/26" else st.session_state.df_2425
    
    target_bio = st.selectbox("Buscar Jugador:", sorted(df_bio['Jugador'].unique()), key="bio_name")
    
    if target_bio:
        bio = sg.get_player_bio_card(df_bio, target_bio)
        if bio:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Equipo", bio['Equipo'])
            c2.metric("Liga", bio['Liga'])
            c3.metric("Edad", bio['Edad'])
            c4.metric("Score Global", bio['Puntuación'])
            
            st.subheader("⭐ Principales Virtudes")
            cv1, cv2, cv3 = st.columns(3)
            for i, (metrica, valor) in enumerate(bio['Top Virtudes']):
                [cv1, cv2, cv3][i].info(f"**{metrica}** \n\n {valor:.1f} / 100")

# --- TAB 2: RANGO EN LIGA ---
with tab2:
    st.header("🏆 Posicionamiento en su Competición")
    st.write("¿Cómo rinde este jugador comparado con los demás de su misma liga?")
    # Reutilizamos el jugador seleccionado en la Tab 1 si quieres, o ponemos otro selectbox
    if target_bio:
        fig_rank = sg.plot_league_rank_st(df_bio, target_bio)
        if fig_rank:
            st.pyplot(fig_rank)
            st.caption(f"Nota: Las barras muestran el rating y la etiqueta indica la posición real en el ranking de la liga.")

with tab3:
    st.subheader("Gráfico de Radar")
    st.info("Configura los perfiles que quieras visualizar en el radar (mínimo 1, máximo 3).")

    c1, c2, c3 = st.columns(3)
    sel_radar = []

    # --- PERFIL 1 (Siempre visible) ---
    with c1:
        st.markdown("### 🟢 Perfil 1")
        p1 = st.selectbox("Jugador", df_actual['Jugador'].unique(), key="p1_n")
        t1 = st.radio("Temporada", ["25/26", "24/25"], key="p1_t", horizontal=True)
        df_1 = st.session_state.df_2526 if t1 == "25/26" else st.session_state.df_2425
        sel_radar.append((p1, df_1, f"{p1} ({t1})"))

    # --- PERFIL 2 (Opcional) ---
    with c2:
        st.markdown("### 🔴 Perfil 2")
        activar_p2 = st.checkbox("Añadir segundo jugador", key="act_p2")
        if activar_p2:
            p2 = st.selectbox("Jugador", df_actual['Jugador'].unique(), key="p2_n")
            t2 = st.radio("Temporada", ["25/26", "24/25"], key="p2_t", horizontal=True)
            df_2 = st.session_state.df_2526 if t2 == "25/26" else st.session_state.df_2425
            sel_radar.append((p2, df_2, f"{p2} ({t2})"))

    # --- PERFIL 3 (Opcional) ---
    with c3:
        st.markdown("### 🔵 Perfil 3")
        activar_p3 = st.checkbox("Añadir tercer jugador", key="act_p3")
        if activar_p3:
            p3 = st.selectbox("Jugador", df_actual['Jugador'].unique(), key="p3_n")
            t3 = st.radio("Temporada", ["25/26", "24/25"], key="p3_t", horizontal=True)
            df_3 = st.session_state.df_2526 if t3 == "25/26" else st.session_state.df_2425
            sel_radar.append((p3, df_3, f"{p3} ({t3})"))

    st.markdown("---")
    
    # Solo generamos el radar si hay al menos una selección válida
    if st.button("📊 Generar Radar"):
        if sel_radar:
            fig = sg.plot_omni_radar_evolutivo(sel_radar)
            if fig:
                # Usamos una columna central para que el radar no ocupe todo el ancho si es solo uno
                _, col_radar, _ = st.columns([1, 5, 1])
                with col_radar:
                    st.pyplot(fig)

# --- TAB 2: SEARCH ---
with tab4:
    st.header("🔍 Buscador de Mercado Inteligente")
    st.write("Configura tus requisitos mínimos para identificar perfiles de élite.")

    # 1. Selector de Temporada Específico para Búsqueda
    c_temp, c_reset = st.columns([1, 1])
    with c_temp:
        temp_search = st.radio("Temporada de búsqueda:", ["25/26", "24/25"], key="search_temp", horizontal=True)
        df_search = st.session_state.df_2526 if temp_search == "25/26" else st.session_state.df_2425

    st.markdown("---")

    # 2. Configuración de Filtros
    metrics_search = [c for c in df_search.columns if "_Rating" in c]
    filtros_scouting = {}
    
    st.subheader("📊 Métrica por Percentil (0-100)")
    col_f1, col_f2, col_f3 = st.columns(3)
    
    for i, metrica in enumerate(metrics_search):
        target_col = [col_f1, col_f2, col_f3][i % 3]
        with target_col:
            filtros_scouting[metrica] = st.slider(
                f"{metrica.replace('_Rating', '')}", 
                0, 100, 0, 
                key=f"search_slider_{metrica}_{temp_search}" # Key única para que no choque al cambiar temp
            )

    st.markdown("---")
    
    # 3. Filtros de Perfil Físico/Contrato
    c_edad, c_min, c_liga = st.columns(3)
    with c_edad:
        max_edad_search = st.number_input("Edad Máxima", value=28, step=1)
    with c_min:
        minutos_search = st.number_input("Mínimo de Minutos", value=800, step=100)
    with c_liga:
        ligas_disp = ["Todas"] + sorted(df_search['Liga'].unique().tolist())
        liga_search = st.selectbox("Liga Específica", ligas_disp)

    # 4. EJECUCIÓN DE LA BÚSQUEDA
    # Aplicar filtros de rating
    df_res = sg.aplicar_filtros_scouting_st(df_search, filtros_scouting)
    
    # Aplicar filtros adicionales
    if not df_res.empty:
        df_res = df_res[df_res['Edad'] <= max_edad_search]
        if 'Minutos' in df_res.columns:
            df_res = df_res[df_res['Minutos'] >= minutos_search]
        if liga_search != "Todas":
            df_res = df_res[df_res['Liga'] == liga_search]

    # 5. RESULTADOS
    st.subheader(f"✅ Resultados encontrados en {temp_search}: {len(df_res)}")
    
    if not df_res.empty:
        # Mostramos solo las columnas que el usuario está filtrando + las básicas
        cols_con_filtro = [k for k, v in filtros_scouting.items() if v > 0]
        cols_ver = ['Jugador', 'Equipo', 'Liga', 'Edad', 'Final_Score'] + cols_con_filtro
        
        st.dataframe(
            df_res[cols_ver].style.format({col: "{:.1f}" for col in ['Final_Score'] + cols_con_filtro}),
            use_container_width=True
        )
        
        # Botón de exportación
        csv_data = df_res[cols_ver].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Reporte (.csv)",
            data=csv_data,
            file_name=f"scouting_report_{temp_search}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No hay jugadores que cumplan todos los criterios en esta temporada. Prueba a relajar los filtros.")

# --- TAB 3: SIMILARITY ---
with tab5:
    st.header("👯‍♂️ Buscador de Gemelos: Filtro de Reemplazo")
    st.write("Usa un perfil histórico como 'molde' para encontrar jugadores similares hoy.")

    col_s1, col_s2 = st.columns([1, 2])
    
    with col_s1:
        st.markdown("### 🎯 Definir Objetivo")
        
        # Eliges la temporada de donde quieres sacar al jugador que te gusta
        temp_origen = st.radio("Temporada del jugador 'molde':", ["25/26", "24/25"], key="sim_temp_org")
        df_org = st.session_state.df_2526 if temp_origen == "25/26" else st.session_state.df_2425
        
        target_sim = st.selectbox("Seleccionar jugador (Cualquier Liga):", sorted(df_org['Jugador'].unique()))
        
        st.markdown("---")
        st.markdown("### 🔎 Buscar En")
        
        # Aquí eliges en qué base de datos quieres buscar al gemelo (normalmente será la actual)
        temp_destino = st.radio("Buscar gemelos en la temporada:", ["25/26", "24/25"], index=0, key="sim_temp_dest")
        df_dest = st.session_state.df_2526 if temp_destino == "25/26" else st.session_state.df_2425
        
        n_sim = st.slider("Resultados:", 5, 15, 10)

    with col_s2:
        if target_sim:
            # Llamamos a la nueva función de cruce
            fig_sim = sg.plot_similar_players_cross_st(target_sim, df_org, df_dest)
            if fig_sim:
                st.pyplot(fig_sim)
                st.success(f"Mostrando jugadores de la temporada {temp_destino} que más se parecen al perfil de {target_sim} ({temp_origen})")

# --- TAB 4: Z-SCORE ---
with tab6:
    st.subheader("Comparativa de Calidad Relativa")
    cz1, cz2 = st.columns(2)
    sel_z = []
    for i, col in enumerate([cz1, cz2]):
        with col:
            p = st.selectbox(f"Jugador {i+1}", df_actual['Jugador'].unique(), key=f"zn{i}")
            t = st.radio(f"Temp {i+1}", ["25/26", "24/25"], key=f"zt{i}", horizontal=True)
            df_sel = st.session_state.df_2526 if t == "25/26" else st.session_state.df_2425
            sel_z.append((p, df_sel))
    if st.button("Calcular Z-Score"):
        st.pyplot(sg.plot_zscore_st(sel_z))

# --- TAB 5: MARKET ---
with tab7:
    st.header("🌍 Market Analysis: Contexto Cerrado")
    st.write("Analiza a un jugador frente a la élite europea dentro de una temporada específica.")

    # 1. Selector de Temporada (Controla toda la pestaña)
    temp_market = st.radio("Seleccionar base de datos para el análisis:", ["25/26", "24/25"], key="mkt_temp_uni", horizontal=True)
    
    # Cargamos el DF correspondiente
    df_mkt_base = st.session_state.df_2526 if temp_market == "25/26" else st.session_state.df_2425

    st.markdown("---")
    
    col_m1, col_m2 = st.columns([1, 2])
    
    with col_m1:
        st.markdown(f"### ⚙️ Configuración ({temp_market})")
        
        # El buscador solo muestra jugadores de la temporada elegida arriba
        target_m = st.selectbox("Analizar prospecto:", sorted(df_mkt_base['Jugador'].unique()))
        
        
        # Filtros de métricas
        all_ratings = [c for c in df_mkt_base.columns if "_Rating" in c]
        selected_m = st.multiselect(
            "Métricas para el eje Y:", 
            options=all_ratings,
            default=all_ratings[:3] # O tus métricas por defecto
        )
        
        st.info(f"Estás comparando a **{target_m}** contra toda la élite europea de la temporada **{temp_market}**.")
    
    with col_m2:
        if target_m and selected_m:
            # Enviamos el DataFrame completo de esa temporada para que la comparativa sea justa
            fig_mkt = sg.plot_market_analysis_st(df_mkt_base, target_m, selected_m)
            st.pyplot(fig_mkt)


