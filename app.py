# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm
from sklearn.cluster import KMeans
import os
import time

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Giulia's Pink Analytics 🎀", layout="wide", page_icon="🌸")

# --- 2. CSS & ANIMAȚIE PETALE ---
st.markdown("""
<style>
    [data-testid="stSidebarNav"] span { display: none !important; }
    div.stButton > button { border-radius: 20px !important; font-weight: bold; }
    .bistro-card {
        background-color: #FCE4EC; padding: 25px; border-radius: 30px;
        border: 4px double #D81B60; text-align: center; margin-bottom: 20px;
    }
    @keyframes fall {
        0% { top: -10%; transform: translateX(0) rotate(0deg); opacity: 1; }
        100% { top: 110%; transform: translateX(20px) rotate(360deg); opacity: 0; }
    }
    .petal {
        position: fixed; z-index: 9999; font-size: 24px; pointer-events: none;
        animation: fall 12s linear infinite; color: #F48FB1;
    }
</style>
""", unsafe_allow_html=True)

# Generăm floricelele pe ecran
for i in range(12):
    st.markdown(f'<div class="petal" style="left: {i*8}%; animation-delay: {i*1}s;">🌸</div>', unsafe_allow_html=True)

# --- 3. LOGICA DE DATE ---
if 'user_name' not in st.session_state: st.session_state['user_name'] = ""

@st.cache_data
def load_data_adidas():
    if not os.path.exists('adidas.csv'): return None
    df = pd.read_csv('adidas.csv')
    df_c = df.copy()
    # 1.8 Modificarea datelor (Redenumire)
    df_c = df_c.rename(columns={'Invoice Date': 'Data_Facturare', 'Operating Margin': 'Marja_Operationala'})
    
    # Curățare date numerice (convertește $ și % în numere)
    def clean_val(x): return float(str(x).replace('$', '').replace(',', '').replace('%', ''))
    for col in ['Total Sales', 'Operating Profit', 'Price per Unit']:
        df_c[col] = df_c[col].apply(clean_val)
    
    df_c['Units Sold'] = df_c['Units Sold'].astype(str).str.replace(',', '').astype(float)
    # Conversie Marja în format numeric (0.50 în loc de 50%)
    df_c['Marja_Operationala'] = df_c['Marja_Operationala'].astype(str).str.replace('%', '').astype(float) / 100
    
    # 1.11 Ștergere coloană redundantă
    if 'Retailer ID' in df_c.columns:
        df_c = df_c.drop(columns=['Retailer ID'])
        
    return df_c

df_adidas = load_data_adidas()

# --- 4. NAVIGARE SIDEBAR ---
st.sidebar.markdown("<h2 style='text-align: center;'>Giulia Vâlcu 🌸</h2>", unsafe_allow_html=True)
pagina = st.sidebar.radio("Meniu:", ["🏠 Home", "🍴 Restaurant (Partea 1)", "👟 Adidas (Partea 2)", "🔮 AI & Final"])

# ==========================================
# PAGINA 1: HOME
# ==========================================
if pagina == "🏠 Home":
    st.markdown("<h1 style='text-align: center;'>🎀 Giulia's Pink Analytics 🎀</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Creat cu drag de Giulia Vâlcu 🌸</h3>", unsafe_allow_html=True)
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.write("### 💖 Să ne cunoaștem!")
        nume = st.text_input("Bună! Eu sunt Giulia. Pe tine cum te cheamă?", placeholder="Scrie aici...")
        if nume: st.session_state['user_name'] = nume
        
        v = st.slider("Câți ani ai?", 5, 100, 21)
        if v < 18: m = "Ești o mică stea în devenire! 🎀"
        elif 18 <= v <= 25: m = "Vârsta perfectă pentru date și stil! 🌸"
        else: m = "Înțelepciunea ta ne inspiră! 👑"
        st.success(m)

    with c2:
        st.write("### ✨ Despre Proiect")
        st.write(f"Bună, **{st.session_state['user_name'] if st.session_state['user_name'] else 'vizitatorule'}**! ✨")
        st.write("Am integrat tot codul din fișierul `proiect.py` într-o interfață modernă. Vom trece prin liste, seturi, pandas și modele de inteligență artificială.")


# --- PARTEA 2: VIBE CHECK & INSPIRAȚIE ---
    c3, c4 = st.columns(2)
    with c3:
        st.write("### 💅 Vibe Check")
        stare = st.radio("Cum te simți astăzi?", ["🌸 Super inspirată", "🚀 Gata de acțiune", "☕ Îmi trebuie o cafea", "🎀 Într-o stare total roz"])
        
        if "cafea" in stare:
            st.warning("☕ Îți pregătesc un espresso virtual! Acum ești gata să analizezi date!")
        elif "inspirată" in stare:
            st.success("🌸 Perfect! Vei adora graficele noastre din secțiunea Adidas.")
        elif "acțiune" in stare:
            st.info("🚀 Asta e atitudinea! Treci direct la Machine Learning!")
        else:
            st.markdown("<div style='background-color: #F8BBD0; padding: 10px; border-radius: 8px;'>🎀 Rozul nu e o culoare, e o stare de spirit!</div>", unsafe_allow_html=True)

    with c4:
        st.write("### 📖 Inspirația Zilei")
        import random
        citate = [
            "„Bucură-te de viață, e mult prea scurtă să porți pantofi plictisitori.” 👠",
            "„Datele sunt noul aur, dar tu strălucești mult mai tare!” ✨",
            "„Programarea este ca magia, doar că folosești tastatura în loc de baghetă.” 🪄",
            "„Păstrează-ți standardele ridicate, la fel ca graficele tale de profit.” 📈",
            "„O fată trebuie să fie două lucruri: cine și ce vrea ea.” — Coco Chanel 👗"
        ]
        st.write("Ai nevoie de un mic impuls? Apasă butonul de mai jos:")
        if st.button("💖 Generează un citat"):
            st.markdown(f"<div style='background-color: #FCE4EC; padding: 15px; border-radius: 10px; border: 2px dashed #D81B60; text-align: center; font-style: italic;'><b>{random.choice(citate)}</b></div>", unsafe_allow_html=True)

    st.divider()

    # --- PARTEA 3: HARTA CĂLĂTORIEI ---
    st.write("### 🗺️ Harta Călătoriei (Ce urmează să descoperi?)")
    st.write("Apasă pe săgeți pentru a vedea ce surprize ascunde fiecare secțiune:")
    
    with st.expander("🍴 Partea 1: Giulia's Bistro (Python de bază)"):
        st.write("Vom simula un sistem de restaurant folosind **Liste, Dicționare, Seturi și Tupluri**. Vei putea să îți adaugi mâncarea preferată în meniu și vom calcula nota de plată cu TVA folosind o **Funcție** creată de noi.")
        
    with st.expander("👟 Partea 2: Adidas (Data Science & Pandas)"):
        st.write("Vom importa un set real de date cu vânzările Adidas. Îl vom curăța, vom repara **Valorile Lipsă (Missing Values)** și vom desena grafice roz superbe ca să vedem ce produse aduc cel mai mare profit.")
        
    with st.expander("🔮 Partea 3: Magic AI (Scikit-Learn & Statsmodels)"):
        st.write("Aici devine serios! Un algoritm va grupa produsele automat (**K-Means Clustering**), iar un model matematic avansat (**Regresie Liniară**) îți va prezice exact câți bani vei face dacă vinzi X unități la prețul Y.")


# ==========================================
# PAGINA 2: RESTAURANT (BONUS: TIMP DE AȘTEPTARE)
# ==========================================
elif pagina == "🍴 Restaurant (Partea 1)":
    st.markdown('<div class="bistro-card"><h1 style="font-family: cursive; margin:0;">Giulia\'s Bistro 🎀</h1><p style="margin:0; font-weight:bold;">Gătim cu pasiune și cod Python</p></div>', unsafe_allow_html=True)

    # --- INITIALIZARE MEMORIE ---
    import random # Avem nevoie pentru timpul de așteptare random

    if 'incasari_live' not in st.session_state:
        st.session_state['incasari_live'] = [120, 45, 0, 310, 0, 85, 200, 0]

    if 'date_recenzii' not in st.session_state:
        st.session_state['date_recenzii'] = [
            {"nume": "Andreea M.", "comentariu": "Cea mai bună limonadă roz din oraș! Recomand cu drag. ✨", "nota": 5},
            {"nume": "Cristian D.", "comentariu": "Friptura de vită a fost gătită perfect. Atmosferă foarte primitoare.", "nota": 5},
            {"nume": "Elena P.", "comentariu": "Desertul Tiramisu este divin, dar am așteptat cam mult nota.", "nota": 4},
            {"nume": "Mihai T.", "comentariu": "Designul locației este superb, totul este roz și instagramabil! 🌸", "nota": 5},
        ]
        
    # Memorie NOUĂ pentru sistemul de așteptare
    if 'stadiu_comanda' not in st.session_state:
        st.session_state['stadiu_comanda'] = 'selectare'
    if 'total_curent' not in st.session_state:
        st.session_state['total_curent'] = 0
    if 'timp_estimat' not in st.session_state:
        st.session_state['timp_estimat'] = 0

    st.write(f"### ✨ Bun venit la masă, {st.session_state['user_name']}!")
    
    # --- 1. MENIU & COMANDĂ ---
    preturi_meniu = {
        'Bruschete cu roșii': 25, 
        'Ciorbă de burtă': 30, 
        'Friptură de vită': 75, 
        'Paste Carbonara': 50, 
        'Risotto cu creveți': 65,       
        'Sushi Pink Roll': 55,         
        'Tiramisu': 35, 
        'Cheesecake cu zmeură': 40, 
        'Limonadă roz': 20, 
        'Cocktail Pink Lady': 45,       
        'Vin rose': 55
    }
    
    col_m1, col_m2 = st.columns([1, 1.5])
    with col_m1:
        st.write("### 📖 Meniul Nostru")
        meniu_html = "<ul style='color: #4A0E2E; font-size: 16px; list-style-type: none; padding: 0;'>"
        for produs, pret in preturi_meniu.items():
            meniu_html += f"<li style='margin-bottom: 5px;'><b>{produs}</b> <span style='float: right; color: #D81B60;'>{pret} RON</span></li>"
        meniu_html += "</ul>"
        st.markdown(f"<div style='background-color: #FFF5F8; padding: 15px; border-radius: 15px; border: 1px solid #F8BBD0;'>{meniu_html}</div>", unsafe_allow_html=True)

    with col_m2:
        st.write("### 🛒 Comanda ta interactivă")
        
        # PASUL 1: ALEGEREA PRODUSELOR
        if st.session_state['stadiu_comanda'] == 'selectare':
            comanda = st.multiselect("Bifează ce dorești să comanzi azi:", list(preturi_meniu.keys()))
            
            if comanda:
                subtotal = sum([preturi_meniu[item] for item in comanda])
                procent_tva = 0.19 if 'Vin rose' in comanda else 0.09
                valoare_tva = subtotal * procent_tva
                total_intermediar = subtotal + valoare_tva
                
                discount = 0
                if total_intermediar > 200:
                    discount = total_intermediar * 0.10
                    
                total_final = total_intermediar - discount
                
                # CONSTRUIREA BONULUI (SIGUR - Fără spații care strică designul!)
                html_bon = "<div style='background-color: #FCE4EC; padding: 20px; border-radius: 15px; border: 2px dashed #D81B60;'>"
                html_bon += "<h4 style='color: #4A0E2E; margin-top:0; text-align: center;'>Nota de plată</h4>"
                html_bon += f"<div style='display: flex; justify-content: space-between; margin-bottom: 5px;'><span>Subtotal:</span> <b>{subtotal:.2f} RON</b></div>"
                html_bon += f"<div style='display: flex; justify-content: space-between; margin-bottom: 5px;'><span>TVA ({int(procent_tva*100)}%):</span> <b>+ {valoare_tva:.2f} RON</b></div>"
                
                if discount > 0:
                    html_bon += f"<div style='display: flex; justify-content: space-between; color: #D81B60;'><span>💖 Discount:</span> <b>- {discount:.2f} RON</b></div>"
                
                html_bon += "<hr style='border: 0.5px solid #D81B60; margin: 10px 0;'>"
                html_bon += f"<h3 style='color: #D81B60; margin-bottom:0; text-align: center;'>Total de plată: {total_final:.2f} RON</h3>"
                html_bon += "</div>"
                
                # Afișăm bonul curat
                st.markdown(html_bon, unsafe_allow_html=True)
                
                if st.button("💖 Trimite Comanda către Bucătărie"):
                    # Salvăm totalul și generăm un timp random, apoi trecem la Pasul 2
                    st.session_state['timp_estimat'] = random.choice([15, 25, 35, 45, 60])
                    st.session_state['total_curent'] = round(total_final, 2)
                    st.session_state['stadiu_comanda'] = 'confirmare'
                    st.rerun() 
            else:
                st.info("Alege ceva bun din meniu pentru a vedea nota de plată!")
                
        # PASUL 2: CONFIRMARE SAU ANULARE
        elif st.session_state['stadiu_comanda'] == 'confirmare':
            st.markdown(f"""
            <div style='background-color: #FFF3E0; padding: 20px; border-radius: 15px; border: 2px solid #FF9800; text-align: center;'>
                <h3 style='color: #E65100; margin-top:0;'>⏳ Bucătăria evaluează comanda...</h3>
                <p style='font-size: 18px;'>Timpul estimat de așteptare este de <b>{st.session_state['timp_estimat']} minute</b>.</p>
                <p style='color: #4A0E2E;'>Valoare comandă: <b>{st.session_state['total_curent']:.2f} RON</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("✅ Accept și aștept", use_container_width=True):
                    # ADAUGĂ BANII
                    st.session_state['incasari_live'].append(st.session_state['total_curent'])
                    st.session_state['stadiu_comanda'] = 'selectare'
                    st.balloons()
                    st.success("Mulțumim! Comanda este în preparare.")
                    time.sleep(1.5)
                    st.rerun()
            with col_btn2:
                if st.button("❌ E prea mult, anulez", use_container_width=True):
                    # ADAUGĂ 0 RON (COMANDĂ ANULATĂ)
                    st.session_state['incasari_live'].append(0) 
                    st.session_state['stadiu_comanda'] = 'selectare'
                    st.error("Comanda a fost anulată (S-a trimis 0 RON în sistem).")
                    time.sleep(1.5)
                    st.rerun()

    # --- 2. ALERGENI ---
    st.divider()
    st.write("### ⚠️ Sistem Alergeni (Seturi)")
    a_friptura, a_tiramisu = {'Gluten', 'Soia', 'Muștar'}, {'Ouă', 'Lactate', 'Gluten'}
    comuni = a_friptura.intersection(a_tiramisu)
    c_a1, c_a2 = st.columns(2)
    c_a1.write(f"Alergeni friptură: `{a_friptura}`")
    c_a1.write(f"Alergeni tiramisu: `{a_tiramisu}`")
    c_a2.warning(f"Alergeni comuni identificați: **{comuni}**")

    # --- 3. RECENZII ---
    st.divider()
    st.write("### ⭐ Recenzii Live (Tupluri)")
    toate_notele = tuple([r['nota'] for r in st.session_state['date_recenzii']])
    
    col_r1, col_r2 = st.columns(2)
    for i, r in enumerate(st.session_state['date_recenzii']):
        t_col = col_r1 if i % 2 == 0 else col_r2
        with t_col:
            st.markdown(f"<div style='background-color: white; padding: 12px; border-radius: 12px; border: 1px solid #F8BBD0; margin-bottom: 10px;'><b>{r['nume']}</b><br><i style='font-size: 13px;'>\"{r['comentariu']}\"</i><br>{'⭐' * r['nota']}</div>", unsafe_allow_html=True)
    
    with st.expander("💖 Lasă și tu o recenzie"):
        f_n = st.text_input("Nume:")
        f_not = st.selectbox("Nota:", [5,4,3,2,1])
        f_c = st.text_area("Mesaj:")
        if st.button("Postează"):
            st.session_state['date_recenzii'].append({"nume": f_n, "comentariu": f_c, "nota": f_not})
            st.rerun()

    # --- 4. MONITORIZARE INCASARI (PANOU ELEGANT) ---
    st.divider()
    st.write("### 📉 Monitorizare Încasări (Logica for + continue)")
    
    date_tabel = []
    valide = 0
    for i, v in enumerate(st.session_state['incasari_live']):
        if v == 0:
            date_tabel.append({"Masa": f"Masa {i+1}", "Sumă": "0 RON", "Status": "❌ Anulat"})
            continue
        valide += v
        date_tabel.append({"Masa": f"Masa {i+1}", "Sumă": f"{v:.2f} RON", "Status": "✅ Încasat"})

    c_tab, c_log = st.columns([1.2, 1])
    with c_tab:
        # Importăm pandas doar pentru a face tabelul superb
        import pandas as pd
        
        # Transformăm lista într-un DataFrame
        df_tabel = pd.DataFrame(date_tabel)
        
        # Setăm coloana 'Masa' ca index principal (scăpăm de 0, 1, 2)
        if not df_tabel.empty:
            df_tabel.set_index('Masa', inplace=True)
            
        # Afișăm noul tabel
        st.table(df_tabel)
        
    with c_log:
        mese_total = len(st.session_state['incasari_live'])
        mese_anulate = st.session_state['incasari_live'].count(0)
        mese_valide = mese_total - mese_anulate
        
        st.markdown(f"""
        <div style='background-color: #FCE4EC; color: #4A0E2E; padding: 25px; border-radius: 20px; border: 2px solid #D81B60; text-align: center; box-shadow: 2px 2px 10px rgba(216, 27, 96, 0.1);'>
            <h3 style='color: #D81B60; margin-top: 0;'>📊 Raport Încasări</h3>
            <p style='font-size: 16px; margin: 5px 0;'>Total comenzi plasate: <b>{mese_total}</b></p>
            <p style='font-size: 16px; margin: 5px 0; color: #FF5252;'>Comenzi anulate (0 RON): <b>{mese_anulate}</b></p>
            <p style='font-size: 16px; margin: 5px 0; color: #2E7D32;'>Comenzi încasate: <b>{mese_valide}</b></p>
            <hr style='border: 0.5px solid #D81B60; margin: 15px 0;'>
            <p style='margin:0; font-size: 14px; text-transform: uppercase;'>Venit Total Validat</p>
            <h2 style='margin:0; color: #D81B60; font-size: 32px;'>{valide:.2f} RON</h2>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 **Notă tehnică:** Algoritmul folosește `for` și `continue` pentru a detecta și ignora automat comenzile anulate (0) din tabelul de alături.")



# ==========================================
# PAGINA 3: ADIDAS (DASHBOARD FINAL CU EXPORT)
# ==========================================
elif pagina == "👟 Adidas (Partea 2)":
    # Header personalizat
    st.markdown("""
    <div style='background-color: #FCE4EC; padding: 20px; border-radius: 15px; border: 2px solid #D81B60; display: flex; align-items: center; gap: 20px; margin-bottom: 20px;'>
        <img src="https://cdn-icons-png.flaticon.com/512/731/731962.png" width="80">
        <div>
            <h1 style='color: #4A0E2E; margin: 0;'>Analiză Date: Adidas Group 👟</h1>
            <p style='color: #D81B60; margin: 0; font-weight: bold;'>Data Science & Analytics cu Pandas</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if df_adidas is not None:
        st.write(f"### 👩‍💻 Bun venit în centrul de control, **{st.session_state['user_name']}**!")
        
        # --- QUIZ INTERACTIV DESPRE GARDEROBA UTILIZATORULUI ---
        st.divider()
        st.write("### 💖 Cât de mare fan Adidas ești?")
        
        col_quiz1, col_quiz2 = st.columns([1.5, 1])
        with col_quiz1:
            st.write("Înainte să analizăm vânzările globale, hai să vedem ce conține garderoba ta!")
            garderoba = st.multiselect(
                "Ce piese de la Adidas deții în acest moment?",
                ["👟 Sneakers (Stan Smith, Superstar, Ozweego, etc.)", 
                 "👕 Haine (Treninguri, Hanorace, Colanți)", 
                 "🎒 Accesorii (Rucsacuri, Șepci, Borsete)", 
                 "🧦 Echipament sportiv (Mingi, Șosete, etc.)"]
            )
            
            buget = st.slider("Câți bani cheltui în medie pe an pe branduri sport? (RON)", 0, 5000, 500)
            
        with col_quiz2:
            st.write("") 
            st.write("")
            if st.button("✨ Calculează-mi Profilul de Client", use_container_width=True):
                if len(garderoba) == 0:
                    st.info("Ești genul care preferă alte branduri? Nu-i nimic, datele noastre te vor convinge! 😉")
                elif len(garderoba) <= 2:
                    st.success(f"**Profil: Fan Casual!** Ai {len(garderoba)} categorii de produse. Ești clientul nostru de bază! 🎀")
                    st.balloons()
                else:
                    st.error(f"**Profil: ADIDAS VIP! 🌟** Ai aproape toată colecția și un buget de {buget} RON! Analiza de mai jos se bazează fix pe clienți de top ca tine!")
                    st.balloons()

        st.divider()

        # Tab-uri cu iconițe drăguțe (ACUM SUNT 4 TAB-URI)
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Vizualizări (Plotly)", "🧹 Curățare Date (NaN)", "🤝 Merge Data (Join)", "🏆 Top Performanțe (Nou)"])
        
        # ----------------------------------------
        # TAB 1: GRAFICE MULT MAI INTERACTIVE
        # ----------------------------------------
        with tab1:
            st.markdown("<h3 style='color: #D81B60;'>📈 Performanța Vânzărilor pe Regiuni</h3>", unsafe_allow_html=True)
            
            c_filtru1, c_filtru2 = st.columns(2)
            with c_filtru1:
                metric = st.selectbox("1️⃣ Alege ce măsurăm (Axa Y):", ['Total Sales', 'Units Sold', 'Operating Profit'])
            with c_filtru2:
                if 'Retailer' in df_adidas.columns:
                    lista_retaileri = df_adidas['Retailer'].unique()
                    retaileri_selectati = st.multiselect("2️⃣ Filtrează după Magazin (Retailer):", lista_retaileri, default=lista_retaileri)
                else:
                    retaileri_selectati = [] 
            
            if 'Retailer' in df_adidas.columns and retaileri_selectati:
                df_filtrat = df_adidas[df_adidas['Retailer'].isin(retaileri_selectati)]
            else:
                df_filtrat = df_adidas
                
            df_grafic = df_filtrat.groupby('Region')[metric].sum().reset_index()
            
            if not df_grafic.empty:
                fig = px.bar(df_grafic, 
                             x='Region', y=metric, color=metric,
                             color_continuous_scale=['#F8BBD0', '#D81B60', '#880E4F'],
                             title=f"Analiză interactivă: {metric} per Regiune")
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ Nu există date pentru filtrele selectate.")
            
            st.divider()
            st.markdown("<h3 style='color: #D81B60;'>🔍 Audit Tranzacții (Logica iloc)</h3>", unsafe_allow_html=True)
            col_iloc, col_text = st.columns([1, 1])
            with col_iloc:
                st.write("Folosind `df.iloc[0:1]`, am extras exact **prima tranzacție** din istoric.")
                st.dataframe(df_filtrat.iloc[0:1]) 
            with col_text:
                st.info("💡 **Ce am demonstrat?** `iloc` accesează rândurile după poziția lor fizică (0 = primul rând). E perfect pentru a lua rapid un 'sample' din setul masiv de date Adidas.")

        # ----------------------------------------
        # TAB 2: CURĂȚARE DATE (NaN)
        # ----------------------------------------
        with tab2:
            st.markdown("<h3 style='color: #D81B60;'>🛠️ Tratarea Valorilor Lipsă (fillna)</h3>", unsafe_allow_html=True)
            st.write("În viața reală, bazele de date au erori sau câmpuri goale (`NaN`). Aici simulăm o eroare și o reparăm algoritmic.")
            
            df_null = df_adidas[['Retailer', 'Region', 'Total Sales']].head(5).copy()
            df_null.loc[0, 'Total Sales'] = np.nan 
            
            col_inainte, col_dupa = st.columns(2)
            
            with col_inainte:
                st.error("❌ **Bază de date cu erori (NaN):**")
                st.dataframe(df_null)
            
            with col_dupa:
                if st.button("✨ Rulează Curățarea (fillna)"):
                    st.balloons()
                    media = df_adidas['Total Sales'].mean()
                    df_null['Total Sales'] = df_null['Total Sales'].fillna(media)
                    
                    st.success(f"✅ Reparat! Valoarea lipsă a fost înlocuită cu media: **{media:,.2f}**.")
                    st.dataframe(df_null)
                else:
                    st.info("👆 Apasă butonul pentru a curăța datele folosind media coloanei.")

        # ----------------------------------------
        # TAB 3: MERGE DATA
        # ----------------------------------------
        with tab3:
            st.markdown("<h3 style='color: #D81B60;'>🔗 Unire Tabele (Merge/Join)</h3>", unsafe_allow_html=True)
            st.write("Legăm datele despre vânzări de o bază de date HR cu **Managerii Zonali**.")
            
            date_m = {'Region': ['Northeast', 'South', 'West', 'Midwest', 'Southeast'],
                      'Manager': ['Popescu Ion', 'Ionescu Maria', 'Stan Andrei', 'Dumitrescu Elena', 'Radu Mihai']}
            df_m = pd.DataFrame(date_m)
            
            c_merge1, c_merge2 = st.columns([1, 1])
            with c_merge1:
                st.write("**Tabel 1: Date Adidas (Extras)**")
                st.dataframe(df_adidas[['Retailer', 'Region', 'Total Sales']].head(4))
            with c_merge2:
                st.write("**Tabel 2: Manageri (Sursă HR)**")
                st.dataframe(df_m)
                
            st.divider()
            
            st.write("🎉 **Tabel Combinat (Lipit pe coloana 'Region'):**")
            df_merged = pd.merge(df_adidas, df_m, on='Region', how='left')
            st.dataframe(df_merged[['Retailer', 'Region', 'Manager', 'Total Sales']].head(8), use_container_width=True)
            
            st.info("💡 **Cod:** `pd.merge(df_adidas, df_m, on='Region', how='left')` păstrează toate vânzările și aduce numele managerului potrivit pentru fiecare regiune.")

        # ----------------------------------------
        # TAB 4: FILTRARE, SORTARE & DOWNLOAD (NOU)
        # ----------------------------------------
        with tab4:
            st.markdown("<h3 style='color: #D81B60;'>🏆 Top Vânzări & Export Date</h3>", unsafe_allow_html=True)
            st.write("Să zicem că șeful îți cere urgent un raport doar cu cele mai mari tranzacții. Iată cum folosim logica de **filtrare** și **sortare** din Pandas pentru a-l genera instant!")
            
            col_filtru, col_rezultat = st.columns([1, 2])
            
            with col_filtru:
                # Slider pentru filtrare (valoarea maximă se adaptează automat la datele tale)
                max_sales = float(df_adidas['Total Sales'].max())
                prag_minim = st.slider("💰 Setare prag minim vânzare (RON):", 0.0, max_sales, max_sales * 0.5)
                
            with col_rezultat:
                # 1. FILTRARE: Alegem doar tranzactiile peste prag
                df_top = df_adidas[df_adidas['Total Sales'] >= prag_minim]
                
                # 2. SORTARE: Ordonăm descrescător (cele mai mari primele)
                df_top = df_top.sort_values(by='Total Sales', ascending=False)
                
                st.success(f"Am găsit **{len(df_top)} tranzacții** care depășesc pragul setat de tine.")
                st.dataframe(df_top[['Retailer', 'Region', 'Total Sales']].head(10), use_container_width=True)
                
                st.info("💡 **Concepte tehnice bifate:** Filtrare condițională `df[df['Col'] > x]` și sortare cu `df.sort_values(ascending=False)`.")
            
            st.divider()
            
            # BUTONUL DE DOWNLOAD MAGNIFIC
            st.write("### 💾 Exportă Raportul pentru Management")
            st.write("Acum că am curățat și sortat datele, le putem descărca direct într-un fișier compatibil cu Excel!")
            
            # Transformăm datele în format CSV pentru a fi descărcate
            csv = df_top.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Descarcă Raportul Premium (CSV)",
                data=csv,
                file_name='raport_vanzari_adidas.csv',
                mime='text/csv',
                help="Apasă pentru a salva fișierul pe calculatorul tău."
            )

    else:
        st.warning("⚠️ Baza de date Adidas nu a putut fi încărcată. Verifică fișierul Excel.")

# ==========================================
# PAGINA 4: AI & FINAL (VERSION PINK & PRO)
# ==========================================
elif pagina == "🔮 AI & Final":
    # Header Premium
    st.markdown("""
    <div style='background-color: #FCE4EC; padding: 20px; border-radius: 15px; border: 2px solid #D81B60; display: flex; align-items: center; gap: 20px; margin-bottom: 20px;'>
        <h1 style='font-size: 40px; margin: 0;'>🧠</h1>
        <div>
            <h1 style='color: #4A0E2E; margin: 0;'>Laborator AI & Machine Learning</h1>
            <p style='color: #D81B60; margin: 0; font-weight: bold;'>Scikit-Learn & Statsmodels</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if df_adidas is not None:
        st.write(f"### Bine ai venit în viitor, **{st.session_state['user_name']}**! 🚀")
        
        tab_ml1, tab_ml2 = st.tabs(["🧩 Segmentare (K-Means)", "📈 Predicție Vânzări (Regresie)"])
        
        # ----------------------------------------
        # TAB 1: CLUSTERIZARE (PINK THEME)
        # ----------------------------------------
        with tab_ml1:
            st.markdown("<h3 style='color: #D81B60;'>🧩 Segmentarea Produselor (Scikit-Learn)</h3>", unsafe_allow_html=True)
            
            c_clust1, c_clust2 = st.columns([1, 2])
            with c_clust1:
                st.write("**Setări AI:**")
                nr_clustere = st.slider("Câte grupuri vrei să formeze AI-ul?", min_value=2, max_value=5, value=3)
                st.info(f"💡 AI-ul împarte acum produsele în **{nr_clustere}** categorii de performanță.")
            
            with c_clust2:
                X = df_adidas[['Units Sold', 'Operating Profit']].dropna()
                kmeans = KMeans(n_clusters=nr_clustere, random_state=42, n_init=10).fit(X)
                
                # Adăugăm Grupurile (începând de la 1)
                X['Grup'] = ["Grup " + str(i + 1) for i in kmeans.labels_]
                
                # Paleta de culori ROZ personalizată
                pink_shades = ['#F8BBD0', '#F06292', '#D81B60', '#AD1457', '#880E4F']
                
                fig_cl = px.scatter(X, x='Units Sold', y='Operating Profit', 
                                    color='Grup', 
                                    color_discrete_sequence=pink_shades,
                                    title="Analiza Grupurilor de Produse")
                
                fig_cl.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_cl, use_container_width=True)

            st.markdown("""
            <div style='background-color: #FFF5F8; padding: 15px; border-radius: 10px; border: 1px solid #F8BBD0;'>
                <p style='margin:0; color: #4A0E2E;'>💡 <b>Interpretare AI:</b> Produsele din grupurile situate în <b>dreapta-sus</b> sunt 'vedetele' portofoliului (vânzări mari + profit mare), în timp ce cele din <b>stânga-jos</b> reprezintă produse de nișă sau aflate la început.</p>
            </div>
            """, unsafe_allow_html=True)

        # ----------------------------------------
        # TAB 2: REGRESIE MULTIPLĂ
        # ----------------------------------------
        with tab_ml2:
            st.markdown("<h3 style='color: #D81B60;'>🔮 Oracolul Financiar (Regresie Multiplă)</h3>", unsafe_allow_html=True)
            
            df_reg = df_adidas[['Total Sales', 'Units Sold', 'Price per Unit']].dropna()
            Y = df_reg['Total Sales']
            X_reg = sm.add_constant(df_reg[['Units Sold', 'Price per Unit']])
            model = sm.OLS(Y, X_reg).fit()
            acuratete = model.rsquared * 100
            
            st.success(f"✅ Model antrenat! Acuratețe: **{acuratete:.2f}%**.")
            
            st.write("#### 🕹️ Simulator de Business")
            col_x, col_y, col_rez = st.columns([1, 1, 1.5])
            with col_x:
                u = st.number_input("📦 Unități estimate:", min_value=0, max_value=50000, value=2500)
            with col_y:
                p = st.number_input("💸 Preț dorit (RON):", min_value=0, max_value=1000, value=60)
                
            with col_rez:
                pred = model.params['const'] + (model.params['Units Sold'] * u) + (model.params['Price per Unit'] * p)
                pred_final = max(0, pred)
                
                st.markdown(f"""
                <div style='background-color: #2D2D2D; color: white; padding: 20px; border-radius: 15px; text-align: center; border: 2px solid #D81B60;'>
                    <p style='margin: 0; color: #F8BBD0; font-size: 14px;'>VÂNZĂRI ESTIMATE PRIN AI:</p>
                    <h2 style='margin: 0; color: #D81B60;'>{pred_final:,.2f} RON</h2>
                </div>
                """, unsafe_allow_html=True)

    # ----------------------------------------
    # FINALUL APLICAȚIEI
    # ----------------------------------------
    st.write("<br><br>", unsafe_allow_html=True)
    st.divider()
    st.markdown(f"<h2 style='text-align: center; color: #4A0E2E;'>✨ Felicitări, {st.session_state.get('user_name', 'Giulia')}! ✨</h2>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("💖 SĂRBĂTOREȘTE FINALUL! 💖", use_container_width=True):
            st.balloons()
            st.snow()
            st.success("Aplicația a fost finalizată cu succes! 🎀")
    
    st.markdown("<br><h4 style='text-align: center; color: #D81B60; font-family: cursive;'>Made with ❤️ by Giulia Vâlcu</h4>", unsafe_allow_html=True)
   
   
   
   
   
   
   
   
   
   
   
   
    # python -m streamlit run app.py