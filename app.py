import streamlit as st
import scouting_general as sg
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# 1. Page Configuration
st.set_page_config(page_title="Scouting Dashboard", layout="wide", page_icon="⚽")

LEAGUE_MAP = {
    "ENGLAND": "Premier League",
    "ENGLAND 2": "EFL Championship",
    "SPAIN": "La Liga",
    "SPAIN 2": "La Liga 2",
    "FRANCE": "Ligue 1",
    "GERMANY": "Bundesliga",
    "ITALY": "Serie A",
    "PORTUGAL": "Primeira Liga",
    "NETHERLANDS": "Eredivisie",
    "DENMARK": "Superliga",
    "SWITZERLAND": "Swiss Super League",
    "BRAZIL": "Brasileirão",
    "ARGENTINA": "Primera División",
    "USA": "MLS",
    "MEXICO": "Liga MX"
}
# 2. Initial Data Loading & Session State Management
if 'df_2425' not in st.session_state or 'df_2526' not in st.session_state:
    with st.spinner('Accessing databases and calculating performance ranks...'):
        # 1. Fetch raw lists
        list_2425_raw, list_2526_raw = sg.cargar_todo()
        
        # 2. Possession Adjustments
        list_2526_proc, list_2425_proc = sg.cargar_posesión(list_2526_raw, list_2425_raw)
        
        # 3. Concatenate to DataFrames
        df_2526 = pd.concat(list_2526_proc, ignore_index=True)
        df_2425 = pd.concat(list_2425_proc, ignore_index=True)

        # --- APPLY LEAGUE MAPPING ---
        # We replace the raw names with the professional names before saving to session_state
        df_2526['Liga'] = df_2526['Liga'].map(LEAGUE_MAP).fillna(df_2526['Liga'])
        df_2425['Liga'] = df_2425['Liga'].map(LEAGUE_MAP).fillna(df_2425['Liga'])
        
        # 4. Apply Ranking Algorithms
        st.session_state.df_2526 = sg.rankings(df_2526)
        st.session_state.df_2425 = sg.rankings(df_2425)

# --- App Header ---
st.title("⚽ Scouting Platform")
st.markdown("---")

# --- METHODOLOGY SECTION ---
with st.expander("📖 READ FIRST: Methodology, Calibration & PAdj Logic", expanded=True):
    st.markdown("### 🛡️ Mitigation of Translation Risk")
    st.write("""
    A common pitfall in data scouting is the **'Translation Risk'**—the uncertainty of whether a player’s dominant stats 
    in one league will hold up in a more demanding competition. To mitigate this, we have integrated **ELO-based league ratings** into our model. By weighing a player’s MLS metrics, for instance, against the relative strength of La Liga, we can 
    'deflate' or 'inflate' specific stats to create a more realistic projection of his performance in another league. 
    
    This adjustment ensures that a player’s percentiles are not just a reflection of dominance in North America, 
    but a calculated prediction of his floor and ceiling within **another league**. Below are the power 
    rankings of the leagues used in the scouting process, established by **Opta (24-03-2026)**.
    """)
    st.image("Power Rankings 24-03-2026.png", caption="Opta League Power Rankings 2026")
    st.markdown("### ⚖️ Possession Adjustment (PAdj)")
    st.write("""
    To ensure this analysis reflects true technical quality rather than team style, all data has been 
    **Possession-Adjusted (PAdj)**. Standard 'Per 90' metrics are often misleading because they fail to account 
    for the 'opportunity' a player has to act. 
    
    For example, a defender on a team with 70% possession has significantly fewer chances to make tackles than 
    a defender on a team with only 30% possession. By adjusting for possession, we normalize the environment, 
    allowing us to compare a player’s output as if every player operated under a balanced **50% possession split**.
    """)

    st.markdown("### 📊 Percentile Calculation")
    st.write("""
    Beyond volume, these PAdj metrics are integrated with **success rates** to generate comprehensive percentiles. 
    This ensures that a high ranking is not merely a result of high activity, but of **high efficiency**. 
    For instance, a player’s crossing percentile is calculated on the marriage of his possession-adjusted volume 
    and his actual delivery accuracy. This methodology provides a much more robust 'performance ceiling' 
    than traditional raw data. The data comes from Wyscout.
    """)

st.markdown("---")

# 3. Sidebar (Global Filters)
st.sidebar.header("🔍 Global Search Filters")

# --- SEASON FILTER HELP ---
temp_choice = st.sidebar.selectbox("Season", ["2025/2026", "2024/2025"])

# Assign current DataFrame based on choice
df_actual = st.session_state.df_2526 if temp_choice == "2025/2026" else st.session_state.df_2425

# --- LEAGUE FILTER HELP ---
ligas_disponibles = sorted(df_actual["Liga"].unique())
liga_select = st.sidebar.selectbox("Select League", ligas_disponibles)

# --- POSITION FILTER HELP ---
posiciones = sorted(df_actual["Pos_Normalizada"].unique())
pos_select = st.sidebar.multiselect("Filter by Position", posiciones)

# 4. Global Filtering Logic
df_display = df_actual[df_actual["Liga"] == liga_select]
if pos_select:
    df_display = df_display[df_display["Pos_Normalizada"].isin(pos_select)]

# 5. Main Dashboard Ranking
st.subheader(f"Identified Players: {liga_select} ({temp_choice})")

col_score = "Final_Score" 
if col_score in df_display.columns:
    df_ranked = df_display.sort_values(by=col_score, ascending=False)
    
    # Column mapping for English display
    display_cols = {
        'Jugador': 'Player', 
        'Equipo': 'Team', 
        'Edad': 'Age', 
        'Pos_Normalizada': 'Position'
    }
    
    # Filter valid columns and rename
    cols_to_show = [c for c in display_cols.keys() if c in df_ranked.columns]
    df_visible = df_ranked[cols_to_show].rename(columns=display_cols)
    
    st.dataframe(df_visible.head(20), use_container_width=True)
else:
    st.warning("Ranking columns not found. Please ensure data processing is complete.")

# 6. Navigation Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "👤 Player Profile", 
    "🏆 Rankings", 
    "📊 Radar Charts", 
    "🔍 Advanced Search", 
    "👯 Similarity", 
    "📈 Z-Score", 
    "🌍 Market Comparison"
])

# --- TAB 1: PLAYER PROFILE ---
with tab1:
    st.header("👤 Player Profile")
    with st.expander("ℹ️ How to read this card"):
        st.write("Displays general info and the Top 3 metrics where this player ranks highest.")
    
    temp_bio = st.radio("Database Season", ["25/26", "24/25"], key="bio_temp", horizontal=True)
    df_bio = st.session_state.df_2526 if temp_bio == "25/26" else st.session_state.df_2425
    
    target_bio = st.selectbox("Search Player Name:", sorted(df_bio['Jugador'].unique()), key="bio_name")
    
    if target_bio:
        bio = sg.get_player_bio_card(df_bio, target_bio)
        if bio:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Team", bio['Equipo'])
            c2.metric("League", bio['Liga'])
            c3.metric("Age", bio['Edad'])
            
            st.subheader("⭐ Standout Virtues")
            cv1, cv2, cv3 = st.columns(3)
            for i, (metrica, valor) in enumerate(bio['Top Virtudes']):
                [cv1, cv2, cv3][i].info(f"**{metrica.replace('_Rating', '')}** \n\n {valor:.1f} / 100")

# --- TAB 2: LEAGUE RANKINGS ---
with tab2:
    st.header("🏆 League Rankings")
    with st.expander("ℹ️ About League Ranking"):
        st.write("This chart shows exactly where the player sits relative to every other player in their specific league and position.")
    
    if target_bio:
        fig_rank = sg.plot_league_rank_st(df_bio, target_bio)
        if fig_rank:
            st.pyplot(fig_rank)
            st.caption("Note: The bar represents the rating; the label shows the absolute rank position.")

# --- TAB 3: RADAR CHARTS ---
with tab3:
    st.header("📊 Multi-Player Radar Comparison")
    with st.expander("ℹ️ How to use Radar Charts"):
        st.write("Select up to 3 players (or the same player in different seasons) to visualize their rankings.")

    c1, c2, c3 = st.columns(3)
    sel_radar = []

    with c1:
        st.markdown("### 🟢 Primary Profile")
        p1 = st.selectbox("Player", df_actual['Jugador'].unique(), key="p1_n")
        t1 = st.radio("Season", ["25/26", "24/25"], key="p1_t", horizontal=True)
        df_1 = st.session_state.df_2526 if t1 == "25/26" else st.session_state.df_2425
        sel_radar.append((p1, df_1, f"{p1} ({t1})"))

    with c2:
        st.markdown("### 🔴 Secondary Profile")
        activar_p2 = st.checkbox("Add second player", key="act_p2")
        if activar_p2:
            p2 = st.selectbox("Player", df_actual['Jugador'].unique(), key="p2_n")
            t2 = st.radio("Season", ["25/26", "24/25"], key="p2_t", horizontal=True)
            df_2 = st.session_state.df_2526 if t2 == "25/26" else st.session_state.df_2425
            sel_radar.append((p2, df_2, f"{p2} ({t2})"))

    with c3:
        st.markdown("### 🔵 Comparison Profile")
        activar_p3 = st.checkbox("Add third player", key="act_p3")
        if activar_p3:
            p3 = st.selectbox("Player", df_actual['Jugador'].unique(), key="p3_n")
            t3 = st.radio("Season", ["25/26", "24/25"], key="p3_t", horizontal=True)
            df_3 = st.session_state.df_2526 if t3 == "25/26" else st.session_state.df_2425
            sel_radar.append((p3, df_3, f"{p3} ({t3})"))

    if st.button("📊 Generate Visual Radar"):
        if sel_radar:
            fig = sg.plot_omni_radar_evolutivo(sel_radar)
            if fig:
                _, col_radar, _ = st.columns([1, 5, 1])
                with col_radar:
                    st.pyplot(fig)

# --- TAB 4: ADVANCED SEARCH ---
# --- TAB 4: ADVANCED SEARCH ---
with tab4:
    st.header("🔍 Advanced Search")
    with st.expander("ℹ️ About the Search Engine"):
        st.write("Set minimum requirements. The sliders represent **Percentiles (0-100)**. A value of 80 means the player must be in the top 20% for that metric.")

    c_temp, _ = st.columns([1, 1])
    with c_temp:
        temp_search = st.radio("Season to Search:", ["25/26", "24/25"], key="search_temp", horizontal=True)
        df_search = st.session_state.df_2526 if temp_search == "25/26" else st.session_state.df_2425

    st.markdown("---")
    metrics_search = [c for c in df_search.columns if "_Rating" in c]
    filtros_scouting = {}
    
    st.subheader("📊 Metric Percentile Requirements")
    col_f1, col_f2, col_f3 = st.columns(3)
    
    for i, metrica in enumerate(metrics_search):
        target_col = [col_f1, col_f2, col_f3][i % 3]
        with target_col:
            filtros_scouting[metrica] = st.slider(
                f"{metrica.replace('_Rating', '')}", 
                0, 100, 0, 
                key=f"search_slider_{metrica}_{temp_search}"
            )

    st.markdown("---")
    c_edad, c_min, c_liga = st.columns(3)
    with c_edad:
        max_edad_search = st.number_input("Maximum Age", value=28, step=1)
    with c_min:
        minutos_search = st.number_input("Minimum Minutes Played", value=800, step=100)
    with c_liga:
        ligas_disp = ["All Leagues"] + sorted(df_search['Liga'].unique().tolist())
        liga_search = st.selectbox("Search Specific League", ligas_disp)

    # --- SEARCH EXECUTION ---
    df_res = sg.aplicar_filtros_scouting_st(df_search, filtros_scouting)
    
    if not df_res.empty:
        # Additional static filters
        df_res = df_res[df_res['Edad'] <= max_edad_search]
        if 'Minutos' in df_res.columns:
            df_res = df_res[df_res['Minutos'] >= minutos_search]
        if liga_search != "All Leagues":
            df_res = df_res[df_res['Liga'] == liga_search]

    st.subheader(f"✅ Results Found: {len(df_res)}")

    if not df_res.empty:
        # --- DYNAMIC SORTING & VIEW ---
        st.markdown("### 🏆 Ranking Strategy")
        col_sort_search = st.selectbox(
            "Sort players by specific talent:", 
            options=metrics_search, 
            format_func=lambda x: x.replace('_Rating', ''),
            key="sort_selector_search"
        )

        # Prepare columns for the view (excluding Final_Score)
        # We show the basics + all the ratings to compare
        cols_ver = ['Jugador', 'Equipo', 'Liga', 'Edad'] + metrics_search
        
        # Sort and limit to top 50
        df_final_view = df_res[cols_ver].sort_values(by=col_sort_search, ascending=False).head(50)

        # Render with Heatmap Styling
        st.dataframe(
            df_final_view.style.background_gradient(subset=metrics_search, cmap="YlGn")
            .format({col: "{:.1f}" for col in metrics_search}),
            use_container_width=True,
            height=500
        )
        
        # Download Button
        csv_data = df_final_view.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Scouting Report (.csv)", 
            data=csv_data, 
            file_name=f"scouting_report_{temp_search}.csv", 
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.warning("No players found with these exact requirements. Try lowering the sliders.")

# --- TAB 5: SIMILARITY ---

# --- TAB 5: SIMILARITY ---
with tab5:
    st.header("👯‍♂️ Similarity")
    with st.expander("ℹ️ How Similarity works"):
        st.write("Calculates the cosine similarity between players. This finds players who share a similar profile regardless of league or age.")

    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        st.markdown("### 🎯 Benchmark Player")
        temp_origen = st.radio("Season of Profile:", ["25/26", "24/25"], key="sim_temp_org")
        df_org = st.session_state.df_2526 if temp_origen == "25/26" else st.session_state.df_2425
        target_sim = st.selectbox("Select Benchmark Player:", sorted(df_org['Jugador'].unique()))
        
        st.markdown("---")
        st.markdown("### 🔎 Search Target")
        temp_destino = st.radio("Search Twins in Season:", ["25/26", "24/25"], index=0, key="sim_temp_dest")
        df_dest = st.session_state.df_2526 if temp_destino == "25/26" else st.session_state.df_2425
        n_sim = st.slider("Number of Results:", 5, 15, 10)
        
        # --- THE GENERATE BUTTON ---
        run_sim = st.button("🚀 Find Similar Players", use_container_width=True)

    with col_s2:
        if run_sim:
            if target_sim:
                with st.spinner(f"Analyzing statistical DNA for {target_sim}..."):
                    fig_sim = sg.plot_similar_players_cross_st(target_sim, df_org, df_dest, top_n=n_sim)
                    
                    if fig_sim:
                        st.pyplot(fig_sim)
                    else:
                        st.error("Could not generate similarity chart. Check if metrics are available for this player.")
            else:
                st.warning("Please select a benchmark player first.")
        else:
            # Placeholder message before the user clicks the button
            st.info("Configure the filters on the left and click the button to generate the twin analysis.")

# --- TAB 6: Z-SCORE ---
with tab6:
    st.header("📈 Z-Score Analysis")
    with st.expander("ℹ️ Understanding Z-Score"):
        st.write("Shows standard deviations from the mean. 0 is average. +1.0 is the top 16%. +2.0 is world class. (-1.0 and -2.0 are the opposite). It helps identify how 'unique' a player's trait is.")
    cz1, cz2 = st.columns(2)
    sel_z = []
    for i, col in enumerate([cz1, cz2]):
        with col:
            p = st.selectbox(f"Select Player {i+1}", df_actual['Jugador'].unique(), key=f"zn{i}")
            t = st.radio(f"Player {i+1} Season", ["25/26", "24/25"], key=f"zt{i}", horizontal=True)
            df_sel = st.session_state.df_2526 if t == "25/26" else st.session_state.df_2425
            sel_z.append((p, df_sel))
    if st.button("Calculate Z-Scores"):
        st.pyplot(sg.plot_zscore_st(sel_z))

# --- TAB 7: MARKET ---
with tab7:
    st.header("🌍 Market Benchmarking")
    with st.expander("ℹ️ How to use the Market Plot"):
        st.write("Compares your player (Yellow Star) against others in his position in those specific metrics. It helps determine how good a player is in the combination of a number of metrics.")

    temp_market = st.radio("Database for Market Analysis:", ["25/26", "24/25"], key="mkt_temp_uni", horizontal=True)
    df_mkt_base = st.session_state.df_2526 if temp_market == "25/26" else st.session_state.df_2425

    st.markdown("---")
    col_m1, col_m2 = st.columns([1, 2])
    with col_m1:
        st.markdown(f"### ⚙️ Analysis Settings")
        target_m = st.selectbox("Analyze Prospect:", sorted(df_mkt_base['Jugador'].unique()))
        all_ratings = [c for c in df_mkt_base.columns if "_Rating" in c]
        selected_m = st.multiselect("Metrics for Y-Axis:", options=all_ratings, default=all_ratings[:3])
        st.info(f"Comparing **{target_m}** against others in the ({temp_market}) season.")
    
    with col_m2:
        if target_m and selected_m:
            fig_mkt = sg.plot_market_analysis_st(df_mkt_base, target_m, selected_m)
            st.pyplot(fig_mkt)
