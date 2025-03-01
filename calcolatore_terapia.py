import streamlit as st

def classifica_ipertensione(ps, pd):
    if ps < 140 and pd < 90:
        return "VALORI NON INDICATIVI DI IPERTENSIONE", "green"
    elif ps > 159 or pd > 109:
        return "IPERTENSIONE GRAVE", "red"
    elif (140 <= ps <= 159) or (90 <= pd <= 109):
        return "IPERTENSIONE LIEVE", "orange"
    else:
        return "CONDIZIONE NON CLASSIFICATA", "gray"

def spiegazione_clinica(pam_fc_ratio):
    if pam_fc_ratio <= 1.1:
        return "I beta-bloccanti sono i farmaci adatti a questo profilo."
    elif 1.1 < pam_fc_ratio < 1.4:
        return "Per questi pazienti sono preferiti gli agonisti del recettore alfa ad azione centrale, come la metildopa che modifica l'attività simpatica centrale."
    else:
        return "Queste donne possono trarre beneficio dalla vasodilatazione indotta dai calcio-antagonisti."

def calcola_terapia(ps, pd, fc, classificazione):
    pam = (ps + (2 * pd)) / 3
    pam_fc_ratio = pam / fc

    if classificazione == "VALORI NON INDICATIVI DI IPERTENSIONE":
        return "Nessuna terapia", pam, pam_fc_ratio, "green", False

    if pam_fc_ratio <= 1.1:
        terapia = "Trandate 100 mg, una compressa ogni 8 ore"
    elif 1.1 < pam_fc_ratio < 1.4:
        terapia = "Aldomet 250 mg, una compressa ogni 8 ore"
    else:
        terapia = "Adalat crono 30 mg, una compressa al giorno"

    return terapia, pam, pam_fc_ratio, "blue", True

# -------------------- INTERFACCIA GRAFICA --------------------
st.markdown("## 🔎 **Algoritmo per la Scelta della Terapia nella Gestante Ipertesa**")

ps = st.number_input("Pressione sistolica (mmHg)", min_value=50, max_value=250, value=120)
pd = st.number_input("Pressione diastolica (mmHg)", min_value=30, max_value=150, value=80)
fc = st.number_input("Frequenza Cardiaca (bpm)", min_value=40, max_value=180, value=70)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<style>div.stButton > button:first-child {'
    'border: 3px solid red; border-radius: 10px; font-size: 16px; font-weight: bold;'
    'background-color: white; color: red; padding: 10px 20px; width: 100%;}</style>',
    unsafe_allow_html=True
)

if st.button("Calcola Terapia e Classificazione Ipertensione"):
    classificazione, colore_classificazione = classifica_ipertensione(ps, pd)
    terapia, pam, pam_fc_ratio, colore_terapia, mostra_spiegazione = calcola_terapia(ps, pd, fc, classificazione)

    # **Risultato con colori corretti**
    st.markdown(
        f'<div style="background-color:{colore_classificazione}; padding:10px; border-radius:10px; text-align:center; font-weight:bold; color:white;">'
        f'{classificazione.upper()}</div>',
        unsafe_allow_html=True,
    )

    # **Terapia consigliata**
    st.subheader("🩺 Terapia consigliata")
    st.markdown(f'<div style="background-color:#E8F5E9; padding:10px; border-radius:10px;">'
                f'🫀 <b>Farmaco consigliato:</b> {terapia}</div>', unsafe_allow_html=True)

    # **Mostra sempre PAM e PAM/FC**
    st.markdown(f"📊 **PAM (Pressione Arteriosa Media):** <span style='color:green; font-weight:bold;'>{pam:.2f}</span>", unsafe_allow_html=True)
    st.markdown(f"📈 **Rapporto PAM/FC:** <span style='color:green; font-weight:bold;'>{pam_fc_ratio:.2f}</span>", unsafe_allow_html=True)

    # **Mostra la spiegazione clinica solo se necessario**
    if mostra_spiegazione:
        st.info(spiegazione_clinica(pam_fc_ratio))

    # **Sezioni finali**
    st.subheader("🎯 Obiettivo")
    st.write("L'obiettivo è mantenere la pressione arteriosa sotto i 140/90 mmHg per prevenire complicanze materno-fetali.")

    st.subheader("⚠️ Attenzione")
    st.write("In presenza di **ipertensione grave**, proteinuria e/o sintomi neurologici, è necessaria la somministrazione di **MgSO4** per la prevenzione dell'eclampsia.")

    st.subheader("📖 Riferimento Bibliografico")
    st.write(
        "Eva Mulder et al. Protocollo di studio per il trial EVA: trattamento personalizzato dell'ipertensione lieve in gravidanza per prevenire l'ipertensione grave e la preeclampsia. **BMC Gravidanza e parto.**"
    )
