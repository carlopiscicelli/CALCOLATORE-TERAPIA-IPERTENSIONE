import streamlit as st

def classifica_ipertensione(ps, pd):
    if ps < 140 and pd < 90:
        return "VALORI NON INDICATIVI DI IPERTENSIONE"
    elif ps > 159 or pd > 109:
        return "IPERTENSIONE GRAVE"
    elif 140 <= ps <= 159 and 80 <= pd <= 109:
        return "IPERTENSIONE LIEVE"
    else:
        return "CONDIZIONE NON CLASSIFICATA"

def classifica_pam(pam):
    if pam < 97:
        return "Normale"
    else:
        return "Superiore ai limiti"

def classifica_dinamica(pam_fc_ratio):
    if pam_fc_ratio <= 1.1:
        return "Ipertensione iperdinamica con basse resistenze vascolari"
    elif 1.1 < pam_fc_ratio < 1.4:
        return "Ipertensione normodinamica con resistenze vascolari normali"
    else:
        return "Ipertensione ipodinamica con alte resistenze vascolari"

def spiegazione_clinica(pam_fc_ratio):
    if pam_fc_ratio <= 1.1:
        return "I beta-bloccanti sono i farmaci adatti a questo profilo."
    elif 1.1 < pam_fc_ratio < 1.4:
        return "Per queste pazienti sono preferiti gli agonisti del recettore alfa ad azione centrale, come la metildopa che modifica l'attività simpatica centrale."
    else:
        return "Queste donne possono trarre beneficio dalla vasodilatazione indotta dai calcio-antagonisti."

def calcola_terapia(ps, pd, fc, classificazione):
    if classificazione == "VALORI NON INDICATIVI DI IPERTENSIONE":
        return "Nessuna terapia", 0, 0
    
    pam = (ps + (2 * pd)) / 3
    pam_fc_ratio = pam / fc
    
    if pam_fc_ratio <= 1.1:
        terapia = "Trandate 100 mg, una compressa ogni 8 ore"
    elif 1.1 < pam_fc_ratio < 1.4:
        terapia = "Aldomet 250 mg, una compressa ogni 8 ore"
    else:
        terapia = "Adalat crono 30 mg, una compressa al giorno"
    
    return terapia, pam, pam_fc_ratio

st.title("📌 Algoritmo per la Scelta della Terapia nella Gestante Ipertesa")

ps = st.number_input("Pressione Sistolica (mmHg)", min_value=50, max_value=250, value=120)
pd = st.number_input("Pressione Diastolica (mmHg)", min_value=30, max_value=150, value=80)
fc = st.number_input("Frequenza Cardiaca (bpm)", min_value=40, max_value=180, value=70)

if st.button("🔍 Calcola Terapia e Classificazione Ipertensione"):
    classificazione = classifica_ipertensione(ps, pd)
    terapia, pam, pam_fc_ratio = calcola_terapia(ps, pd, fc, classificazione)
    pam_classificazione = classifica_pam(pam) if pam else "-"
    dinamica_classificazione = classifica_dinamica(pam_fc_ratio) if pam_fc_ratio else "-"
    spiegazione = spiegazione_clinica(pam_fc_ratio) if pam_fc_ratio else "-"
    
    st.markdown(f"""
    ## 📋 Risultati dell'Analisi
    
    **Pressione Sistolica:** `{ps}` mmHg  
    **Pressione Diastolica:** `{pd}` mmHg  
    **Frequenza Cardiaca:** `{fc}` bpm  
    
    **Pressione Arteriosa:** `{classificazione}`  
    **Pressione Arteriosa Media (PAM):** `{pam:.1f}` _{pam_classificazione}_  
    **PAM/FC Ratio:** `{pam_fc_ratio:.1f}` _{dinamica_classificazione}_  
    
    ## 💊 Terapia Consigliata
    **{terapia}**
    
    ## 🔬 Interpretazione
    _{spiegazione}_
    
    ## 🎯 PA Target e Adattamento della Terapia
    Il trattamento verrà aumentato se la **pressione arteriosa target di <130/80 mmHg (MAP 97 mmHg)** non viene raggiunta.  
    **Dosaggi massimi:**  
    - **800 mg** tre volte al giorno per **labetalolo**  
    - **30 mg** tre volte al giorno per **nifedipina** a lento rilascio  
    - **1000 mg** tre volte al giorno per **metildopa**  
    
    ## ⚠️ Attenzione
    In presenza di **ipertensione grave**, proteinuria e/o sintomi neurologici, è necessaria la somministrazione di **MgSO4** per la prevenzione dell'eclampsia.
    
    ---
    
    **📖 Riferimento Bibliografico**
    Eva Mulder et Al. Study protocol for the randomized controlled EVA (early vascular adjustments) trial: tailored treatment of mild hypertension in pregnancy to prevent severe hypertension and preeclampsia. **BMC Pregnancy Childbirth. 2020 Dec 12;20(1):775**
    """)
