import streamlit as st
import yfinance as yf
import pandas as pd
# pandas_ta eliminado — cálculos manuales
import numpy as np
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Macdelorean Radar v27.1",
    page_icon="🚗",
    layout="wide"
)

# --- ESTILOS VISUALES — IDENTIDAD MACDELOREAN (Negro & Dorado) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Share+Tech+Mono&display=swap');

    /* ── VARIABLES DE COLOR ── */
    :root {
        --gold:        #C9A84C;
        --gold-light:  #E8C96B;
        --gold-dark:   #8B6914;
        --gold-dim:    #6B5010;
        --black:       #0A0A0A;
        --black-mid:   #111111;
        --black-soft:  #1A1A1A;
        --black-card:  #151515;
        --text-dim:    #7A7060;
        --text-mid:    #A89060;
        --text-light:  #D4B870;
    }

    /* ── FONDO GENERAL ── */
    .stApp {
        background-color: var(--black);
        background-image:
            radial-gradient(ellipse at 20% 0%, rgba(201,168,76,0.04) 0%, transparent 55%),
            radial-gradient(ellipse at 80% 100%, rgba(201,168,76,0.03) 0%, transparent 55%);
        color: var(--text-mid);
        font-family: 'Share Tech Mono', monospace;
    }

    /* ── HEADERS ── */
    h1, h2, h3 {
        color: var(--gold) !important;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 3px;
        text-shadow: 0 0 30px rgba(201,168,76,0.25);
    }
    h4, h5 { color: var(--gold-light) !important; font-family: 'Cinzel', serif !important; }

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"] {
        background-color: var(--black-mid) !important;
        border-right: 1px solid var(--gold-dim) !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: var(--gold) !important;
        font-family: 'Cinzel', serif !important;
        font-size: 0.85rem !important;
        letter-spacing: 3px;
    }

    /* ── BOTÓN PRINCIPAL (LANZAR RADAR) ── */
    div.stButton > button {
        width: 100%;
        border: 1px solid var(--gold);
        background: linear-gradient(135deg, #0A0A0A 0%, #1A140A 50%, #0A0A0A 100%);
        color: var(--gold);
        font-weight: 700;
        font-size: 14px;
        padding: 14px 20px;
        font-family: 'Cinzel', serif;
        letter-spacing: 4px;
        transition: all 0.4s ease;
        text-transform: uppercase;
        border-radius: 2px;
        box-shadow: inset 0 0 20px rgba(201,168,76,0.05), 0 0 0 1px rgba(201,168,76,0.1);
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1A140A 0%, #2A1E08 50%, #1A140A 100%);
        color: var(--gold-light);
        box-shadow: 0 0 25px rgba(201,168,76,0.35), inset 0 0 25px rgba(201,168,76,0.08);
        border-color: var(--gold-light);
    }
    div.stButton > button:active {
        transform: scale(0.99);
    }

    /* ── CHECKBOXES ── */
    .stCheckbox label {
        color: var(--text-mid) !important;
        font-family: 'Share Tech Mono', monospace;
        font-size: 12px;
        letter-spacing: 0.5px;
    }
    .stCheckbox label:hover { color: var(--gold) !important; }

    /* ── SELECT / DROPDOWNS ── */
    .stSelectbox label { color: var(--text-mid) !important; font-family: 'Share Tech Mono', monospace; font-size: 12px; }
    .stSelectbox > div > div {
        background-color: var(--black-soft) !important;
        border: 1px solid var(--gold-dim) !important;
        color: var(--gold) !important;
        font-family: 'Share Tech Mono', monospace;
    }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--black-mid);
        border-bottom: 1px solid var(--gold-dim);
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--text-dim) !important;
        font-family: 'Cinzel', serif;
        font-size: 10px;
        letter-spacing: 2px;
        padding: 10px 16px;
        border-radius: 0 !important;
        transition: all 0.3s;
    }
    .stTabs [data-baseweb="tab"]:hover { color: var(--gold) !important; }
    .stTabs [aria-selected="true"] {
        color: var(--gold) !important;
        border-bottom: 2px solid var(--gold) !important;
        background: rgba(201,168,76,0.05) !important;
    }

    /* ── BARRA DE PROGRESO ── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--gold-dark), var(--gold), var(--gold-light));
    }

    /* ── MÉTRICAS ── */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
        color: var(--gold-light);
        font-family: 'Share Tech Mono', monospace;
    }
    div[data-testid="stMetricLabel"] {
        color: var(--text-dim);
        font-family: 'Cinzel', serif;
        font-size: 10px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    div[data-testid="stMetricDelta"] { font-family: 'Share Tech Mono', monospace; font-size: 11px; }

    /* ── TABLAS / DATAFRAMES ── */
    .stDataFrame {
        border: 1px solid var(--gold-dim) !important;
        border-radius: 2px;
    }
    .stDataFrame table { background-color: var(--black-card) !important; }
    .stDataFrame th {
        background-color: #0F0E0B !important;
        color: var(--gold) !important;
        font-family: 'Cinzel', serif !important;
        font-size: 11px !important;
        letter-spacing: 2px;
        border-bottom: 1px solid var(--gold-dim) !important;
    }
    .stDataFrame td {
        color: var(--text-mid) !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 12px !important;
        border-bottom: 1px solid rgba(201,168,76,0.08) !important;
    }
    .stDataFrame tr:hover td { background: rgba(201,168,76,0.04) !important; }

    /* ── HR / SEPARADORES ── */
    hr { border-color: var(--gold-dim) !important; opacity: 0.4; }

    /* ── ALERTS / INFO / SUCCESS ── */
    .stAlert, .stSuccess, .stInfo, .stWarning {
        border-radius: 2px !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 12px !important;
    }
    .stSuccess { border-left: 3px solid var(--gold) !important; background: rgba(201,168,76,0.06) !important; }

    /* ── EXPANDER ── */
    .streamlit-expanderHeader {
        color: var(--gold) !important;
        font-family: 'Cinzel', serif;
        font-size: 12px;
        letter-spacing: 2px;
    }

    /* ── DOWNLOAD BUTTON ── */
    div.stDownloadButton > button {
        background: transparent !important;
        border: 1px solid var(--gold-dim) !important;
        color: var(--text-dim) !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 11px !important;
        letter-spacing: 2px;
        padding: 6px 14px !important;
        transition: all 0.3s;
    }
    div.stDownloadButton > button:hover {
        border-color: var(--gold) !important;
        color: var(--gold) !important;
    }

    /* ── INPUT TEXT ── */
    .stTextInput input, .stNumberInput input {
        background: var(--black-soft) !important;
        border: 1px solid var(--gold-dim) !important;
        color: var(--gold) !important;
        font-family: 'Share Tech Mono', monospace !important;
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: var(--black); }
    ::-webkit-scrollbar-thumb { background: var(--gold-dim); border-radius: 2px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--gold); }

    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# 1. UNIVERSO DE ACTIVOS — 29 índices · 1598 tickers únicos
#    Revisado 27/09/2026: composición actual de Dow, Nasdaq-100, DAX, MDAX, IBEX, CAC, FTSE 100,
#    SMI y FTSE MIB. Fuera los valores que ya no cotizan; símbolos renombrados corregidos
#    (BK→BNY, MMC→MRSH, EQR/AVB→VMRK, PKI→RVTY, IDEX→IEX, DAQO→DQ, CHK→EXE, ROG→ROP, AXA→CS).
# ==============================================================================

UNIVERSO = {

    '🇺🇸 DOW JONES 30': [
        "MMM","GOOGL","AXP","AMGN","AMZN","AAPL","BA","CAT","CVX","CSCO",
        "KO","DIS","GS","HD","HON","IBM","JNJ","JPM","MCD","MRK",
        "MSFT","NKE","NVDA","PG","CRM","SHW","TRV","UNH","V","WMT",
    ],

    '🚀 NASDAQ 100 COMPLETO': [
        "ADBE","AMD","ABNB","ALNY","GOOGL","GOOG","AMZN","AEP","AMGN","ADI",
        "AAPL","AMAT","APP","ARM","ASML","ALAB","ADSK","ADP","AXON","BKR",
        "BKNG","AVGO","CDNS","CTAS","CSCO","CCEP","CMCSA","CEG","CPRT","CRWV",
        "COST","CRWD","CSX","DDOG","DXCM","FANG","DASH","EXC","FAST","FER",
        "FTNT","GEHC","GILD","HON","IDXX","INTC","INTU","ISRG","KDP","KLAC",
        "KHC","LRCX","LIN","LITE","MAR","MRVL","MELI","META","MCHP","MU",
        "MSFT","MSTR","MDLZ","MPWR","MNST","NBIS","NFLX","NVDA","NXPI","ORLY",
        "ODFL","PCAR","PLTR","PANW","PAYX","PYPL","PDD","PEP","QCOM","REGN",
        "RKLB","ROP","ROST","SNDK","STX","SHOP","SBUX","SNPS","TMUS","TTWO",
        "TER","TSLA","TXN","TRI","VRTX","WMT","WBD","WDC","WDAY","XEL",
    ],

    '📈 S&P 500 — FINANCIALS & INDUSTRIALS': [
        "JPM","BAC","WFC","GS","MS","C","BNY","USB","PNC","TFC",
        "COF","AXP","SYF","ALLY","FITB","KEY","RF","HBAN","CFG","MTB",
        "ZION","FHN","WAL","EWBC","BLK","SCHW","TROW","IVZ","BEN","AMG",
        "APAM","VRTS","SEIC","FDS","ICE","CME","CBOE","NDAQ","MKTX","VIRT",
        "LPLA","RJF","SF","PIPR","MRSH","AON","AJG","WTW","HIG","MET",
        "PRU","AFL","ALL","TRV","CB","AIG","PGR","CINF","GL","LNC",
        "UNM","PFG","AIZ","EG","GE","HON","MMM","CAT","DE","EMR",
        "ETN","PH","ROK","AME","ITW","DOV","GGG","GNRC","XYL","FLS",
        "IEX","IR","TT","CARR","OTIS","RTX","LMT","NOC","GD","LHX",
        "BAH","LDOS","SAIC",
    ],

    '📈 S&P 500 — HEALTHCARE & CONSUMER': [
        "UNH","CVS","CI","HUM","CNC","MOH","ELV","JNJ","PFE","ABT",
        "MRK","LLY","BMY","GILD","AMGN","REGN","VRTX","BIIB","ALNY","MRNA",
        "BNTX","ILMN","PACB","TDOC","TMO","DHR","A","WAT","MTD","RVTY",
        "IQV","CRL","MEDP","MDT","SYK","BSX","EW","DXCM","RMD","ZBH",
        "BDX","COO","AMZN","WMT","COST","TGT","HD","LOW","TJX","ROST",
        "BURL","FIVE","MCD","SBUX","YUM","QSR","DPZ","CMG","WING","SHAK",
        "JACK","NKE","LULU","VFC","PVH","UA","CROX","DECK","WWW","PG",
        "KO","PEP","MDLZ","GIS","CPB","CAG","SJM","HRL","MKC","PM",
        "MO","BTI","MNST","KDP","CELH","FIZZ","SAM","BF-B","TAP",
    ],

    '📈 S&P 500 — ENERGY & UTILITIES': [
        "XOM","CVX","COP","EOG","DVN","APA","FANG","SLB","HAL","BKR",
        "OIS","OIH","NOV","HP","NE","PTEN","VLO","MPC","PSX","DK",
        "PBF","CLMT","PARR","KMI","WMB","ET","EPD","MPLX","PAA","TRGP",
        "OKE","LNG","FLEX","DUK","SO","NEE","AEP","EXC","XEL","D",
        "SRE","PEG","ED","WEC","ES","ETR","CNP","CMS","LNT","PNW",
        "OGE","NI","EVRG","NRG","VST","CEG","AES","BEP","CWEN","RUN",
        "SEDG","ENPH","FSLR","SPWR","CSIQ","JKS","DQ","ARRY","SHLS",
    ],

    '📈 S&P 500 — TECH & REITS': [
        "AAPL","MSFT","NVDA","GOOGL","META","TSLA","AVGO","ORCL","IBM","QCOM",
        "TXN","ADI","MCHP","LRCX","AMAT","KLAC","SNPS","CDNS","EPAM","PAYC",
        "PCTY","HUBS","VEEV","OKTA","BOX","DBX","TWLO","BAND","EGHT","MSGM",
        "ALKT","DOCU","MNDY","AMT","CCI","SBAC","UNIT","LAMR","OUT","DLR",
        "EQIX","O","WPC","NNN","VICI","GLPI","EPR","SPG","MAC","VMRK",
        "ESS","UDR","AIV","MAA","CPT","INVH","AMH","SUI","ELS","PSA",
        "EXR","CUBE","STAG","ADC","TRNO",
    ],

    '🇩🇪 DAX 40 COMPLETO': [
        "ADS.DE","AIR.DE","ALV.DE","BAS.DE","BAYN.DE","BEI.DE","BMW.DE","BNR.DE","CBK.DE","CON.DE",
        "DTG.DE","DBK.DE","DB1.DE","DHL.DE","DTE.DE","EOAN.DE","FRE.DE","FME.DE","G1A.DE","HNR1.DE",
        "HEI.DE","HEN3.DE","IFX.DE","MBG.DE","MRK.DE","MTX.DE","MUV2.DE","PAH3.DE","QIA.DE","RHM.DE",
        "RWE.DE","SAP.DE","G24.DE","SIE.DE","ENR.DE","SHL.DE","SY1.DE","VOW3.DE","VNA.DE","ZAL.DE",
    ],

    '🇩🇪 MDAX ALEMANIA (Mid Caps)': [
        "AIXA.DE","AT1.DE","NDA.DE","BC8.DE","BFSA.DE","GBF.DE","AFX.DE","EVD.DE","DHER.DE","LHA.DE",
        "EVK.DE","EVT.DE","FRA.DE","FNTN.DE","FPE3.DE","GXI.DE","HLE.DE","HFG.DE","HAG.DE","HOT.DE",
        "BOSS.DE","JEN.DE","JUN3.DE","SDF.DE","KGX.DE","KBX.DE","KRN.DE","LXS.DE","LEG.DE","NEM.DE",
        "NDX1.DE","PUM.DE","RAA.DE","RDC.DE","RRTL.DE","WAF.DE","STM.DE","SAX.DE","TEG.DE","TLX.DE",
        "TMV.DE","TKA.DE","8TRA.DE","TUI1.DE","UTDI.DE","WCH.DE",
    ],

    '🇪🇸 IBEX 35 COMPLETO': [
        "ACS.MC","ACX.MC","AMS.MC","ANA.MC","ANE.MC","BBVA.MC","BKT.MC","CABK.MC","CLNX.MC","COL.MC",
        "AENA.MC","ELE.MC","ENG.MC","FDR.MC","FER.MC","GRF.MC","IAG.MC","IBE.MC","IDR.MC","ITX.MC",
        "LOG.MC","MAP.MC","MRL.MC","MTS.MC","NTGY.MC","PUIG.MC","RED.MC","REP.MC","ROVI.MC","SAB.MC",
        "SAN.MC","SCYR.MC","SLR.MC","TEF.MC","UNI.MC",
    ],

    '🇪🇸 BME GROWTH (Small Caps España)': [
        "OHLA.MC","MDF.MC","CASH.MC","ERIZ.MC","CLNX.MC","ENAV.MC","ALNT.MC","BAIN.MC","DGRN.MC","ECR.MC",
        "ELEX.MC","FLUI.MC","HERN.MC","HGT.MC","LABE.MC","LFDS.MC","MDLN.MC","MEHR.MC","MENT.MC","MXOC.MC",
        "MYMD.MC","NMAS.MC","NRGY.MC","NTGY.MC","ORYC.MC","PBIT.MC","PCAS.MC","PRTC.MC","RLIA.MC",
    ],

    '🇫🇷 CAC 40 COMPLETO': [
        "AC.PA","AI.PA","AIR.PA","MT.AS","CS.PA","BNP.PA","EN.PA","BVI.PA","CAP.PA","CA.PA",
        "ACA.PA","BN.PA","DSY.PA","EDEN.PA","ENGI.PA","EL.PA","ERF.PA","RMS.PA","KER.PA","OR.PA",
        "LR.PA","MC.PA","ML.PA","ORA.PA","RI.PA","PUB.PA","RNO.PA","SAF.PA","SGO.PA","SAN.PA",
        "SU.PA","GLE.PA","STLAP.PA","STMPA.PA","TEP.PA","HO.PA","TTE.PA","URW.PA","VIE.PA","DG.PA",
    ],

    '🇫🇷 SBF 120 FRANCIA (Mid Caps)': [
        "ABCA.PA","ALSTOM.PA","AMUN.PA","APAM.PA","ATOS.PA","BIC.PA","BIGBEN.PA","BIM.PA","BNB.PA","CHSR.PA",
        "CNP.PA","COFA.PA","DBG.PA","DEC.PA","FNAC.PA","GAM.PA","GTT.PA","HLO.PA","IDP.PA","ILD.PA",
        "IMVD.PA","INEA.PA","IPSO.PA","JCDECAUX.PA","KOF.PA","LACR.PA","LDL.PA","LI.PA","LOUP.PA","MANU.PA",
        "MCPHY.PA","MEDCL.PA","MF.PA","MGDYN.PA","NEXANS.PA","NXI.PA","OPM.PA","OREGE.PA","PKGD.PA","PLXS.PA",
        "RBAL.PA","REMY.PA","SAFT.PA","SBMO.PA","SCOR.PA","SEB.PA","SESG.PA","SPIE.PA","TITAN.PA",
    ],

    '🇬🇧 FTSE 100 COMPLETO': [
        "III.L","ABDN.L","ADM.L","AAF.L","ALW.L","AAL.L","ANTO.L","ABF.L","AZN.L","AUTO.L",
        "AV.L","BAB.L","BA.L","BARC.L","BTRW.L","BEZ.L","BP.L","BATS.L","BLND.L","BT-A.L",
        "BNZL.L","BRBY.L","CNA.L","CCEP.L","CCH.L","CPG.L","CCC.L","CTEC.L","CRDA.L","DCC.L",
        "DGE.L","DPLM.L","EDV.L","ENT.L","EXPN.L","FCIT.L","FRES.L","GAW.L","GLEN.L","GSK.L",
        "HLN.L","HLMA.L","HSX.L","HWDN.L","HSBA.L","ICG.L","IGG.L","IHG.L","IMI.L","IMB.L",
        "INF.L","IAG.L","ITRK.L","INVP.L","JD.L","BGEO.L","KGF.L","LAND.L","LMP.L","LSEG.L",
        "MNG.L","MKS.L","MRO.L","MTLN.L","NG.L","NWG.L","NXT.L","PSON.L","PSH.L","PSN.L",
        "PCT.L","PRU.L","RKT.L","REL.L","RTO.L","RIO.L","RR.L","SGE.L","SBRY.L","SDR.L",
        "SMT.L","SGRO.L","SVT.L","SHEL.L","SMIN.L","SN.L","SPX.L","SSE.L","STAN.L","SDLF.L",
        "STJ.L","TSCO.L","BBOX.L","ULVR.L","UU.L","VOD.L","WEIR.L","WTB.L",
    ],

    '🇨🇭 SUIZA — SMI 20 + Mid Caps': [
        "NOVN.SW","ROP.SW","NESN.SW","ABBN.SW","UBSG.SW","CFR.SW","ZURN.SW","HOLN.SW","SREN.SW","LONN.SW",
        "SCMN.SW","GIVN.SW","ALC.SW","SIKA.SW","AMRZ.SW","SLHN.SW","KNIN.SW","GEBN.SW","PGHN.SW","LOGN.SW",
        "SOON.SW","UHR.SW","BAER.SW","SGSN.SW","STMN.SW","TEMN.SW","ADEN.SW","BARN.SW","BKW.SW","BCGE.SW",
        "BNR.SW","CMBN.SW","DKSH.SW","EMSN.SW","FHZN.SW","GALE.SW","GALN.SW","GAM.SW","GF.SW","HUBN.SW",
        "IMPN.SW","KOMN.SW","LHN.SW","LISN.SW","MBTN.SW","METN.SW","MOZN.SW","SAND.SW","SCHP.SW","SCHN.SW",
        "SDZ.SW","SFZN.SW","SQN.SW","SUN.SW","SWON.SW","TECN.SW","VACN.SW","VATN.SW","VONN.SW","VZN.SW",
        "ZEHN.SW","BKWB.SW",
    ],

    '🌍 EMERGING MARKETS — ETFs': [
        "EEM","VWO","IEMG","SCHE","SPEM","DEM","EMXC","EDC","FXI","MCHI",
        "ASHR","KWEB","CQQQ","YINN","CHIQ","CHIX","EWZ","EWW","EWY","EWT",
        "EWA","EWC","EWG","EWU","EWJ","EWI","EWP","EWH","EWS","EWN",
        "EWD","EWQ","EWL","EWO","EWK","EZA","INDA","INDY","SMIN","EPI",
        "PIN","INDL","EIDO","EPHE","THD","VNM","IDX","RSX","ERUS","ARGT",
        "ECH","ILF","BRZU","UBR","UAE","KSA","TUR","EGPT","NGE","AFK",
        "EMQQ","EMHY","EMLC","EMB","CEMB","PCY",
    ],

    '📊 RUSSELL 2000 — SMALL CAPS USA': [
        "IWM","IWO","IWN","IJR","VBR","VTWO","FNDA","AAOI","ABCB","ABEO",
        "ABG","ACAD","ACCO","ACEL","ACIW","ACLS","ACMR","ACT","ADMA","ADNT",
        "ADPT","ADTN","ADUS","ADV","AEIS","AEO","AGM","AGO","AGYS","AIN",
        "AIR","AIT","AKR","ALG","ALGT","ALK","ALKS","ALRM","ALV","AMBA",
        "AMC","AMN","AMPH","AMR","AMRC","AMRX","AMSF","ANDE","ANF","ANIK",
        "AOSL","APAM","APLE","APOG","APPN","APT","ARCB","ARI","ARLO","AROC",
        "ARQT","ARW","ASIX","ASB","ASO","ASPN","ASTE","ASTH","ASUR","ATEC",
        "ATEN","ATEX","ATKR","ATNI","ATR","ATRA","ATRC","AUB","AUR","AUTL",
        "AVA","AVAH","AVAV","AVNT","AVNW","AVPT","AVT","AWR","AX","AXSM",
        "AXTA","AYI","AZTA","AZZ","B","BAH","BANC","BANF","BANR","BBSI",
        "BBW","BCO","BCPC","BDC","BDN","BE","BEAM","BFAM","BFC","BFH",
        "BFS","BG","BGS","BHE","BHF","BIO","BIPC","BJ","BJRI","BKE",
        "BKH","BKU","BL","BLDR","BLFS","BLKB","BLMN","BLX","BMRC","BNL",
        "BOH","BOOM","BOOT","BOX","BRC","BRKR","BRT","BSRR","BTU","BUSE",
        "BV","BWA","BWXT","BXMT","BXP","BY","BYD","BYND","BZH","C",
        "CAC","CAKE","CAL","CALM","CALX","CAR","CARG","CARS","CART","CASH",
        "CASY","CATY","CBL","CBT","CBU","CBZ","CC","CCB","CCBG","CCCC",
        "CCK","CCO","CCOI","CCS","CDE","CDLX","CDNA","CECO","CELH","CENT",
        "CENX","CERS","CERT","CEVA","CFFN","CFR","CHCO","CHCT","CHDN","CHE",
        "CHEF","CHGG","EXE","CHWY","CIEN","CIX","CLBT","CLDT","CLF","CLH",
        "CLNE","CLNN","CLOV","CLW","CMP","CMPR","CMRE","CMTL","CNDT","CNK",
        "CNM","CNMD","CNOB","CNS","CNXC","CNXN","COFS","COHU","COKE","COLB",
        "COLM","CORT","CPF","CPK","CRC","CRGY","CRI","CRK","CRMT","CRS",
        "CRSR","CRUS","CRVL","CSGP","CSL","CSTM","CSV","CTBI","CTOS","CTRE",
        "CTRN","CTS","CUBI","CVBF","CVCO","CVGI","CVI","CWEN","CWH","CWK",
        "CWST","CWT","CXM","CXW","CYH","CYRX","CZNC","CZR","DAKT","DAN",
        "DAR","DBI","DBRG","DCO","DCOM","DDD","DDS","DEA","DEI","DGII",
        "DH","DHC","DIN","DIOD","DK","DLB","DLX","DMRC","DNLI","DNOW",
        "DOCN","DORM","DOUG","DRH","DRI","DRIO","DTI","DTM","DV","DXC",
        "DXPE","DXYN","DY","DYAI","E","EAF","EAT","EBC","ECPG","ECVT",
        "EE","EFC","EFSC","EFX","EGAN","EGBN","EGHT","EGY","EIG",
    ],

    '🌍 EUROSTOXX 50': [
        "ASML.AS","ADYEN.AS","INGA.AS","PHIA.AS","HEIA.AS","NN.AS","RAND.AS","WKL.AS","ABN.AS","UMG.AS",
        "SAP.DE","SIE.DE","ALV.DE","MBG.DE","BMW.DE","BAYN.DE","ADS.DE","BAS.DE","MUV2.DE","DTE.DE",
        "MC.PA","OR.PA","TTE.PA","SAN.PA","BNP.PA","AIR.PA","SU.PA","CS.PA","EL.PA","DG.PA",
        "ITX.MC","BBVA.MC","SAN.MC","IBE.MC","REP.MC","ENI.MI","ISP.MI","UCG.MI","ENEL.MI","TIT.MI",
        "NOKIA.HE","NESTE.HE","AD.AS","PRX.AS","ABI.BR","NDA-FI.HE","RHM.DE","ENR.DE","DBK.DE","IFX.DE",
        "DHL.DE","SAF.PA","SGO.PA","AI.PA","RMS.PA","RACE.MI","STLAM.MI",
    ],

    '🇮🇹 FTSE MIB ITALIA': [
        "A2A.MI","AMP.MI","AVIO.MI","AZM.MI","BMED.MI","BMPS.MI","BAMI.MI","BPE.MI","BC.MI","BZU.MI",
        "CPR.MI","DIA.MI","ENEL.MI","ENI.MI","RACE.MI","FCT.MI","FBK.MI","G.MI","HER.MI","ISP.MI",
        "INW.MI","IG.MI","IVG.MI","LDO.MI","LTMC.MI","MB.MI","MONC.MI","NEXI.MI","PST.MI","PRY.MI",
        "REC.MI","SPM.MI","SRG.MI","STLAM.MI","STMMI.MI","TIT.MI","TEN.MI","TRN.MI","UCG.MI","UNI.MI",
    ],

    '🇯🇵 NIKKEI 225 (ADRs disponibles en USA)': [
        "TM","HMC","SONY","NTT","NTDOY","FUJIY","KYOCY","MUFG","SMFG","MFG",
        "IX","KB","SHI","FANUY","HTHIY","ISUZY","KDDIY","KYCCF","MARUY","MSBHY",
        "NIDEC","NIPNF","NPSNY","NSANY","OTSKY","PCRFY","RICOY","SEKEY","SFUN","SGIOY",
        "SHCAY","SHNNY","SIEGY","SKLTY","SSDOY","SSUNY","STITF","STSFY","SVNDY","TCEHY",
        "TKHVY","TKOMY","TMSNY","TNABY","TOELY","TRHCY","TRYIY","TTDKY","TWTDY","TYEKF",
    ],

    '🇨🇳 CHINA — ADRs EN USA': [
        "BABA","PDD","JD","BIDU","NTES","TCOM","BILI","LI","NIO","XPEV",
        "ZTO","YUMC","TME","VIPS","BEKE","HTHT","FUTU","TAL","EDU","IQ",
        "ATHM","WB","QFIN","MNSO","GDS","KC","HUYA","DQ","YMM","TIGR",
        "BZ","LEGN","ONC","HSAI","PONY","WRD","ZLAB","JKS","VNET","GOTU",
    ],

    '🇨🇳 CHINA — HONG KONG (Hang Seng)': [
        "0700.HK","9988.HK","3690.HK","1810.HK","1211.HK","9618.HK","9999.HK","1024.HK","9888.HK","2015.HK",
        "9868.HK","9866.HK","0941.HK","0883.HK","0857.HK","0386.HK","1398.HK","0939.HK","3988.HK","1288.HK",
        "2318.HK","2628.HK","0388.HK","1299.HK","2020.HK","2331.HK","0291.HK","0960.HK","1109.HK","0688.HK",
        "2269.HK","1177.HK","0981.HK","0992.HK","0762.HK","0728.HK","6618.HK","9633.HK","6862.HK","0241.HK",
    ],

    '🇨🇳 CHINA — A-SHARES (Shanghai / Shenzhen)': [
        "600519.SS","300750.SZ","601318.SS","600036.SS","000858.SZ","002594.SZ","000333.SZ","600900.SS","601012.SS","600276.SS",
        "000651.SZ","601899.SS","600030.SS","601398.SS","600887.SS","300059.SZ","002415.SZ","600309.SS","601888.SS","688981.SS",
    ],

    '⚡ ETFs USA — SECTORES': [
        "XLK","XLF","XLV","XLE","XLC","XLY","XLP","XLI","XLB","XLRE",
        "XLU","VGT","VFH","VHT","VDE","VOX","VCR","VDC","VIS","VAW",
        "VNQ","IDU","FNCL","FHLC","FENY","FCOM","FDIS","FSTA","FIDU","FMAT",
        "FREL","FUTY",
    ],

    '⚡ ETFs USA — ÍNDICES AMPLIOS': [
        "SPY","QQQ","DIA","IWM","VTI","VOO","IVV","RSP","MDY","IJR",
        "VTV","VUG","MTUM","QUAL","VLUE","SIZE","USMV","SPHQ","SPLV","SPHB",
        "ARKK","ARKQ","ARKW","ARKG","ARKF","ARKX","PRNT","IZRL","ARKB","CTRU",
    ],

    '⚡ ETFs INTERNACIONALES': [
        "EWZ","EEM","EFA","VEA","IEFA","VWO","IEMG","FXI","MCHI","KWEB",
        "EWJ","EWY","EWT","EWA","EWC","EWG","EWQ","EWI","EWP","EWU",
        "EWH","EWS","EWM","EWN","EWD","EWL","EWO","EWK","EZU","HEDJ",
        "DBJP","DBEF","DBEU","HEFA","DXJ","HEWJ","HEZU","HSCZ","FLKR","FLJP",
    ],

    '⚡ ETFs TEMÁTICOS & APALANCADOS': [
        "SMH","SOXX","XBI","TAN","ICLN","PBW","LIT","URA","REMX","COPX",
        "BOTZ","ROBO","IRBO","AIQ","WCLD","CLOU","BUG","HACK","CIBR","IHAK",
        "SQQQ","TQQQ","SPXU","UPRO","SPXS","SDOW","UDOW","LABD","LABU","UVXY",
        "VXX","SVXY","VIXY","UVIX","SVOL","ZIVB","VIXM","VXZ","VIIX","TVIX",
        "GLD","SLV","IAU","SGOL","PHYS","PSLV","PPLT","PALL","GDX","GDXJ",
        "SIL","SILJ","NUGT","DUST","JNUG","JDST","RING","GOAU","SGDM","SGDJ",
        "USO","UNG","BNO","DBO","BOIL","KOLD","UGA","CORN","WEAT","SOYB",
        "TLT","IEF","SHY","HYG","LQD","JNK","BNDX","EMB","PCY","BWX",
        "MSTR","COIN","MARA","RIOT","CLSK","HUT","BTBT","CIFR","CORZ","WULF",
    ],

    '🎯 GROWTH & DISRUPTIVAS USA': [
        "NVDA","AMD","PLTR","CRWD","DDOG","ZS","NET","SNOW","OKTA","TWLO",
        "BILL","GTLB","HUBS","MDB","ESTC","APPN","PEGA","NOW","WDAY","VEEV",
        "PCTY","PAYC","RNG","MNDY","DOCU","BOX","DBX","DRCT","FIVN","NICE",
        "FOUR","BRZE","AMPL","ASAN","IONQ","RGTI","QUBT","QBTS","IBM","MSFT",
        "GOOGL","ORCL","ADBE","CRM","UBER","LYFT","ABNB","DASH","CART","TOST",
        "PAR","SHAK","TSLA","LCID","RIVN","WKHS","HYLN","JOBY","ACHR","AAL",
        "UAL","DAL","LUV","ALK",
    ],

    '🎯 SMALL CAPS & ESPECULATIVOS USA': [
        "SOFI","AFRM","HOOD","DKNG","GME","AMC","TLRY","SNDL","ACB","CRON",
        "OGI","TPVG","IIPR","MSOS","YOLO","MJ","CNBS","UPST","AI","OPEN",
        "SPCE","QS","CVNA","CROX","ELF","CELH","HIMS","ACMR","LAZR","LIDR",
        "INVZ","OUST","MVIS","VUZI","KOPN","KTOS","AVAV","RKLB","MNTS","ASTS",
        "LUNR","RDW","OXY","HAL","SLB","APA","DVN","COP","EOG","FANG",
        "VLO","MPC","PSX","DK","PBF","KMI","WMB","ET","EPD","MPLX",
        "AGNC","NLY","STWD","BXMT","ABR","RC","GPMT","KREF","LADR","TRTX",
        "O","WPC","NNN","VICI","GLPI","ADC","EPR","PINE",
    ],

    '💎 MEGA CAPS GLOBALES': [
        "AAPL","MSFT","NVDA","GOOGL","AMZN","META","TSLA","AVGO","LLY","V",
        "UNH","JPM","XOM","MA","JNJ","WMT","PG","HD","MRK","CVX",
        "ABBV","KO","BAC","PEP","COST","TMO","CRM","ACN","MCD","CSCO",
        "ABT","ORCL","ADBE","NKE","TXN","DHR","NEE","LIN","PM","RTX",
        "NESN.SW","ROP.SW","NOVN.SW","SHEL.L","AZN.L","HSBA.L","BP.L","GSK.L","MC.PA","OR.PA",
        "ASML.AS","SAP.DE","SIE.DE","ALV.DE","TM","SONY","MUFG",
    ],
}

# Región de cada índice en el panel lateral. Un índice nuevo que no se añada aquí
# aparece igualmente en el grupo OTROS, así nunca queda oculto.
REGIONES = {
    'USA': [
        '🇺🇸 DOW JONES 30',
        '🚀 NASDAQ 100 COMPLETO',
        '📈 S&P 500 — FINANCIALS & INDUSTRIALS',
        '📈 S&P 500 — HEALTHCARE & CONSUMER',
        '📈 S&P 500 — ENERGY & UTILITIES',
        '📈 S&P 500 — TECH & REITS',
        '📊 RUSSELL 2000 — SMALL CAPS USA',
        '🎯 GROWTH & DISRUPTIVAS USA',
        '🎯 SMALL CAPS & ESPECULATIVOS USA',
        '💎 MEGA CAPS GLOBALES',
    ],
    'EUROPA': [
        '🇩🇪 DAX 40 COMPLETO',
        '🇩🇪 MDAX ALEMANIA (Mid Caps)',
        '🇪🇸 IBEX 35 COMPLETO',
        '🇪🇸 BME GROWTH (Small Caps España)',
        '🇫🇷 CAC 40 COMPLETO',
        '🇫🇷 SBF 120 FRANCIA (Mid Caps)',
        '🇬🇧 FTSE 100 COMPLETO',
        '🇨🇭 SUIZA — SMI 20 + Mid Caps',
        '🌍 EUROSTOXX 50',
        '🇮🇹 FTSE MIB ITALIA',
    ],
    'ASIA': [
        '🇯🇵 NIKKEI 225 (ADRs disponibles en USA)',
        '🇨🇳 CHINA — ADRs EN USA',
        '🇨🇳 CHINA — HONG KONG (Hang Seng)',
        '🇨🇳 CHINA — A-SHARES (Shanghai / Shenzhen)',
    ],
    'ETFs': [
        '🌍 EMERGING MARKETS — ETFs',
        '⚡ ETFs USA — SECTORES',
        '⚡ ETFs USA — ÍNDICES AMPLIOS',
        '⚡ ETFs INTERNACIONALES',
        '⚡ ETFs TEMÁTICOS & APALANCADOS',
    ],
}
_sin_region = [n for n in UNIVERSO if not any(n in g for g in REGIONES.values())]
if _sin_region:
    REGIONES['OTROS'] = _sin_region


# ==============================================================================
# 2. INTELIGENCIA TÉCNICA
# ==============================================================================

# v27: 1 petición por LOTE de tickers (antes 3 por ticker).
# Se descarga historia larga para que MACD y EMAs estén bien "calentados",
# y luego se recorta a las mismas ventanas de v25 para no descalibrar
# divergencias (rango MACD) ni Punto B.
PERIODO_HISTORIA = "8y"
VENTANA_TF = {'D': 252, 'W': 157, 'M': 60}


def _limpiar_ohlcv(raw, ticker=None):
    """Extrae OHLCV limpio de un DataFrame de yfinance (simple o multi-ticker)."""
    if raw is None or raw.empty:
        return pd.DataFrame()
    df = raw
    if isinstance(df.columns, pd.MultiIndex):
        lv0 = df.columns.get_level_values(0)
        lv1 = df.columns.get_level_values(1)
        if ticker is not None and ticker in lv0:
            df = df[ticker]
        elif ticker is not None and ticker in lv1:
            df = df.xs(ticker, axis=1, level=1)
        else:
            return pd.DataFrame()
    cols = [c for c in ['Open', 'High', 'Low', 'Close', 'Volume'] if c in df.columns]
    if 'Close' not in cols:
        return pd.DataFrame()
    df = df[cols].dropna(subset=['Close']).copy()
    if getattr(df.index, 'tz', None) is not None:
        df.index = df.index.tz_localize(None)
    return df


def descargar_lote(tickers):
    """Descarga el diario de un lote de tickers en una sola petición."""
    try:
        raw = yf.download(list(tickers), period=PERIODO_HISTORIA, interval="1d",
                          group_by="ticker", auto_adjust=True, progress=False, threads=True)
    except Exception:
        return {}
    datos = {}
    for t in tickers:
        try:
            datos[t] = _limpiar_ohlcv(raw, t)
        except Exception:
            datos[t] = pd.DataFrame()
    return datos


def _resamplear(df_base, regla):
    agg = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}
    agg = {k: v for k, v in agg.items() if k in df_base.columns}
    return df_base.resample(regla).agg(agg).dropna(subset=['Close'])


def _calcular_indicadores(df, emas=()):
    if df is None or df.empty:
        return df
    df = df.copy()
    # MACD manual
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD']   = ema12 - ema26
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    # Estocástico manual
    if len(df) > 15:
        low14  = df['Low'].rolling(window=14).min()
        high14 = df['High'].rolling(window=14).max()
        k_raw  = 100 * (df['Close'] - low14) / (high14 - low14 + 1e-10)
        df['K'] = k_raw.rolling(window=3).mean()
    # EMAs de largo plazo — solo si hay historia suficiente para que sean fiables
    for p in emas:
        if len(df) >= p + 50:
            df[f'EMA{p}'] = df['Close'].ewm(span=p, adjust=False).mean()
    return df


def procesar_datos(ticker, incluir_4h=False, df_diario=None, solo_cerradas=False):
    try:
        # Si el lote no trajo este ticker, intento individual (1 petición)
        if df_diario is None or df_diario.empty:
            raw = yf.download(ticker, period=PERIODO_HISTORIA, interval="1d",
                              progress=False, auto_adjust=True)
            df_diario = _limpiar_ohlcv(raw, ticker)
        if df_diario is None or len(df_diario) < 60:
            return None

        df_full    = df_diario
        ultimo_dia = df_full.index[-1]

        # Semanal: semana lunes-viernes
        df_w = _resamplear(df_full, 'W-FRI')
        if solo_cerradas and len(df_w) and ultimo_dia < df_w.index[-1]:
            df_w = df_w.iloc[:-1]                         # semana en curso fuera
        df_w.index = df_w.index - pd.Timedelta(days=4)    # etiqueta lunes, como Yahoo/TradingView

        # Mensual
        df_m = _resamplear(df_full, 'MS')
        if solo_cerradas and len(df_m):
            fin_mes = df_m.index[-1] + pd.offsets.BMonthEnd(0)
            if ultimo_dia < fin_mes:
                df_m = df_m.iloc[:-1]                     # mes en curso fuera

        df_d = _calcular_indicadores(df_full, emas=(40, 50, 200)).iloc[-VENTANA_TF['D']:]
        df_w = _calcular_indicadores(df_w,    emas=(40, 50, 200)).iloc[-VENTANA_TF['W']:]
        df_m = _calcular_indicadores(df_m).iloc[-VENTANA_TF['M']:]

        if df_d.empty or df_w.empty or df_m.empty:
            return None

        # 4h solo si se necesita (evita peticiones extra innecesarias)
        df_4h = pd.DataFrame()
        if incluir_4h:
            try:
                raw4  = yf.download(ticker, period="60d", interval="1h", progress=False, auto_adjust=True)
                df_1h = _limpiar_ohlcv(raw4, ticker)
                if not df_1h.empty:
                    df_4h = _calcular_indicadores(_resamplear(df_1h, '4h'))
            except Exception:
                df_4h = pd.DataFrame()

        return {'D': df_d, 'W': df_w, 'M': df_m, '4H': df_4h}
    except Exception:
        return None


def check_punto_b(df, timeframe="D"):
    """
    Detecta módulo de arranque (Punto B) en acción del precio.

    Busca la estructura A -> B -> C donde:
    - A = primer mínimo
    - B = máximo entre A y C (nivel de ruptura)
    - C = segundo mínimo
    - El precio actual ha roto o está cerca de romper B

    Tiempos válidos de formación (A a C):
    - 4H:  35 a 90 velas
    - D:   40 a 60 velas
    - W:   13 a 30 velas
    - M:   7  a 12 velas

    Buena oscilación: C < A
    Mala oscilación:  C > A

    Devuelve: (encontrado, tipo, nivel_b, tp1, tp2, info_dict)
    """
    min_velas = {"4H": 35, "D": 40, "W": 13, "M": 7}.get(timeframe, 40)
    max_velas = {"4H": 90, "D": 60, "W": 30, "M": 12}.get(timeframe, 60)
    min_bc    = 3  # mínimo de velas entre B y C en todos los TF

    if df is None or df.empty or len(df) < min_velas + 10:
        return False, "", 0, 0, 0, {}

    close = df['Close']
    high  = df['High']
    low   = df['Low']
    n     = len(df)

    ventana = min(n - 5, int(max_velas * 2.5))
    df_win  = df.iloc[-ventana:]
    c_win   = df_win['Close']
    l_win   = df_win['Low']
    h_win   = df_win['High']
    nw      = len(df_win)

    pct_min    = {"4H": 0.06, "D": 0.08, "W": 0.10, "M": 0.15}.get(timeframe, 0.08)
    max_desde_c = {"4H": 20, "D": 15, "W": 8, "M": 4}.get(timeframe, 15)

    def es_min_local(serie, i, dist=2):
        return all(serie.iloc[i] < serie.iloc[i-j] for j in range(1, dist+1)) and \
               all(serie.iloc[i] < serie.iloc[i+j] for j in range(1, dist+1))

    def es_max_local(serie, i, dist=2):
        return all(serie.iloc[i] > serie.iloc[i-j] for j in range(1, dist+1)) and \
               all(serie.iloc[i] > serie.iloc[i+j] for j in range(1, dist+1))

    # ══════════════════════════════════════════
    # ESTRUCTURA ALCISTA: A(min) -> B(max) -> C(min)
    # ══════════════════════════════════════════
    mejor = None

    for ia in range(3, nw - min_velas - 3):
        if not es_min_local(l_win, ia):
            continue
        precio_a = l_win.iloc[ia]
        fecha_a = df_win.index[ia].strftime("%d/%m/%Y") if hasattr(df_win.index[ia], "strftime") else str(df_win.index[ia])[:10]

        # Verificar que antes de A el precio venía BAJANDO en tendencia clara
        # 1. Debe haber un máximo previo al menos 15% superior a A
        # 2. La EMA de las velas previas debe estar por encima del precio de A (tendencia bajista)
        ventana_previa = min(ia, 30)
        if ventana_previa < 10:
            continue
        precios_previos = h_win.iloc[ia - ventana_previa: ia]
        max_previo = precios_previos.max()
        if max_previo < precio_a * 1.15:  # impulso previo bajista mínimo 15%
            continue
        # EMA de los últimos precios de cierre previos debe estar por encima de A
        cierres_previos = c_win.iloc[ia - ventana_previa: ia]
        ema_previa = cierres_previos.ewm(span=10, adjust=False).mean().iloc[-1]
        if ema_previa < precio_a * 1.05:  # tendencia previa no era bajista
            continue

        for ib in range(ia + 3, nw - min_bc - 5):
            if not es_max_local(h_win, ib):
                continue
            nivel_b = h_win.iloc[ib]
            fecha_b = df_win.index[ib].strftime("%d/%m/%Y") if hasattr(df_win.index[ib], "strftime") else str(df_win.index[ib])[:10]
            if nivel_b <= precio_a * 1.07:  # B debe estar al menos 7% por encima de A
                continue

            dist_ab = ib - ia  # velas de A a B

            for ic in range(ib + min_bc, nw - 2):  # mínimo min_bc velas entre B y C
                if not es_min_local(l_win, ic):
                    continue
                precio_c = l_win.iloc[ic]
                fecha_c = df_win.index[ic].strftime("%d/%m/%Y") if hasattr(df_win.index[ic], "strftime") else str(df_win.index[ic])[:10]
                if precio_c >= nivel_b * 0.93:  # C debe retroceder al menos 7% desde B
                    continue
                dist_bc    = ic - ib  # velas de B a C
                duracion_ac = ic - ia

                # 1. Tiempo total A->C dentro del rango válido
                if not (min_velas <= duracion_ac <= max_velas):
                    continue

                # 2. Simetría A->B ≈ B->C (±50%)
                if not (dist_ab * 0.33 <= dist_bc <= dist_ab * 1.75):
                    continue

                # 3. C reciente
                velas_desde_c = nw - 1 - ic
                if velas_desde_c > max_desde_c:
                    continue

                # Clasificar oscilación
                if precio_c < precio_a:
                    tipo_osc = "🟢 BUENA OSCILACIÓN"
                    min_abs  = precio_c
                else:
                    tipo_osc = "🟡 MALA OSCILACIÓN"
                    min_abs  = precio_a

                # Altura mínima
                altura = nivel_b - min_abs
                if altura < nivel_b * pct_min:
                    continue

                tp1 = round(min_abs + altura * 1.618, 2)
                tp2 = round(min_abs + altura * 2.0,   2)

                precio_actual = close.iloc[-1]
                roto_b  = precio_actual >= nivel_b
                cerca_b = precio_actual >= nivel_b * 0.98
                if not cerca_b:
                    continue

                # Madurez alcista
                velas_tras_ruptura = 0
                if roto_b:
                    for k_idx in range(ic + 1, nw):
                        if c_win.iloc[k_idx] >= nivel_b:
                            velas_tras_ruptura = nw - k_idx
                            break
                    if velas_tras_ruptura > 5:
                        continue
                    if precio_actual >= tp1:
                        continue
                    precio_minimo_tras_b = min(c_win.iloc[ic+1:].values) if ic+1 < nw else precio_actual
                    if precio_minimo_tras_b < nivel_b - (altura * 0.5):
                        continue

                # Duración real = A hasta ruptura de B
                # Si ya rompió: A->ruptura = duracion_ac + velas_tras_ruptura
                # Si no rompió: A->C como estimación
                if roto_b:
                    dur_real = duracion_ac + velas_tras_ruptura
                else:
                    dur_real = duracion_ac

                estado = "✅ ROTO" if roto_b else "⚡ CERCA"
                mejor = {
                    "tipo":           tipo_osc,
                    "nivel_b":        round(nivel_b, 2),
                    "precio_a":       round(precio_a, 2),
                    "precio_c":       round(precio_c, 2),
                    "tp1":            tp1,
                    "tp2":            tp2,
                    "estado_b":       estado,
                    "duracion_velas": dur_real,
                    "dist_ab":        dist_ab,
                    "dist_bc":        dist_bc,
                    "velas_desde_c":  velas_desde_c,
                    "velas_ruptura":  velas_tras_ruptura if roto_b else 0,
                    "fecha_a":        fecha_a,
                    "fecha_b":        fecha_b,
                    "fecha_c":        fecha_c,
                }
                break
            if mejor: break
        if mejor: break

    if mejor:
        return True, mejor["tipo"], mejor["nivel_b"], mejor["tp1"], mejor["tp2"], mejor

    # ══════════════════════════════════════════
    # ESTRUCTURA BAJISTA: A(max) -> B(min) -> C(max)
    # ══════════════════════════════════════════
    mejor = None

    for ia in range(3, nw - min_velas - 3):
        if not es_max_local(h_win, ia):
            continue

        # Verificar que antes de A el precio venía SUBIENDO en tendencia clara
        # 1. Debe haber un mínimo previo al menos 15% inferior a A
        # 2. La EMA de las velas previas debe estar por debajo del precio de A (tendencia alcista)
        ventana_previa = min(ia, 30)
        if ventana_previa < 10:
            continue
        precio_a = h_win.iloc[ia]
        fecha_a  = df_win.index[ia].strftime("%d/%m/%Y") if hasattr(df_win.index[ia], "strftime") else str(df_win.index[ia])[:10]
        precios_previos_l = l_win.iloc[ia - ventana_previa: ia]
        min_previo = precios_previos_l.min()
        if min_previo > precio_a * 0.85:  # impulso previo alcista mínimo 15%
            continue
        # EMA de los últimos precios de cierre previos debe estar por debajo de A
        cierres_previos = c_win.iloc[ia - ventana_previa: ia]
        ema_previa = cierres_previos.ewm(span=10, adjust=False).mean().iloc[-1]
        if ema_previa > precio_a * 0.95:  # tendencia previa no era alcista
            continue

        for ib in range(ia + 3, nw - min_bc - 5):
            if not es_min_local(l_win, ib):
                continue
            nivel_b = l_win.iloc[ib]
            fecha_b = df_win.index[ib].strftime("%d/%m/%Y") if hasattr(df_win.index[ib], "strftime") else str(df_win.index[ib])[:10]
            if nivel_b >= precio_a * 0.93:
                continue

            dist_ab = ib - ia

            for ic in range(ib + min_bc, nw - 2):
                if not es_max_local(h_win, ic):
                    continue
                precio_c = h_win.iloc[ic]
                fecha_c  = df_win.index[ic].strftime("%d/%m/%Y") if hasattr(df_win.index[ic], "strftime") else str(df_win.index[ic])[:10]
                if precio_c <= nivel_b * 1.07:
                    continue

                dist_bc     = ic - ib
                duracion_ac = ic - ia

                if not (min_velas <= duracion_ac <= max_velas):
                    continue
                if not (dist_ab * 0.33 <= dist_bc <= dist_ab * 1.75):
                    continue

                velas_desde_c = nw - 1 - ic
                if velas_desde_c > max_desde_c:
                    continue

                if precio_c > precio_a:
                    tipo_osc = "🟢 BUENA OSC. BAJISTA"
                    max_abs  = precio_c
                else:
                    tipo_osc = "🟡 MALA OSC. BAJISTA"
                    max_abs  = precio_a

                altura = max_abs - nivel_b
                if altura < nivel_b * pct_min:
                    continue

                tp1 = round(max_abs - altura * 1.618, 2)
                tp2 = round(max_abs - altura * 2.0,   2)

                precio_actual = close.iloc[-1]
                roto_b  = precio_actual <= nivel_b
                cerca_b = precio_actual <= nivel_b * 1.02
                if not cerca_b:
                    continue

                velas_tras_ruptura = 0
                if roto_b:
                    for k_idx in range(ic + 1, nw):
                        if c_win.iloc[k_idx] <= nivel_b:   # v27: cierre, igual que el alcista
                            velas_tras_ruptura = nw - k_idx
                            break
                    if velas_tras_ruptura > 5:
                        continue
                    if precio_actual <= tp1:
                        continue
                    precio_maximo_tras_b = max(c_win.iloc[ic+1:].values) if ic+1 < nw else precio_actual
                    if precio_maximo_tras_b > nivel_b + (altura * 0.5):
                        continue

                if roto_b:
                    dur_real = duracion_ac + velas_tras_ruptura
                else:
                    dur_real = duracion_ac

                estado = "✅ ROTO" if roto_b else "⚡ CERCA"
                mejor = {
                    "tipo":           tipo_osc,
                    "nivel_b":        round(nivel_b, 2),
                    "precio_a":       round(precio_a, 2),
                    "precio_c":       round(precio_c, 2),
                    "tp1":            tp1,
                    "tp2":            tp2,
                    "estado_b":       estado,
                    "duracion_velas": dur_real,
                    "dist_ab":        dist_ab,
                    "dist_bc":        dist_bc,
                    "velas_desde_c":  velas_desde_c,
                    "velas_ruptura":  velas_tras_ruptura if roto_b else 0,
                    "fecha_a":        fecha_a,
                    "fecha_b":        fecha_b,
                    "fecha_c":        fecha_c,
                }
                break
            if mejor: break
        if mejor: break
    if mejor:
        return True, mejor["tipo"], mejor["nivel_b"], mejor["tp1"], mejor["tp2"], mejor
    return False, "", 0, 0, 0, {}




def check_vela_engano(df, idx=-1):
    if len(df) < abs(idx) + 2 or 'K' not in df.columns:
        return False, "", 0, 0
    curr = df.iloc[idx]; prev = df.iloc[idx - 1]
    mid_prev = (prev['High'] + prev['Low']) / 2
    k = curr['K']
    if (curr['Low'] < prev['Low']) and (curr['Close'] > mid_prev) and (k < 20.0):
        return True, "ALCISTA 🟢", k, min(curr['Low'], prev['Low'])
    if (curr['High'] > prev['High']) and (curr['Close'] < mid_prev) and (k > 80.0):
        return True, "BAJISTA 🔴", k, max(curr['High'], prev['High'])
    return False, "", k, 0


def encontrar_swings(serie, es_minimo=True, min_dist=3):
    """
    Detecta swing points reales en una serie.
    min_dist: velas mínimas de separación entre swings.
    """
    swings = []
    valores = serie.values
    indices = list(range(len(valores)))
    for i in range(min_dist, len(valores) - min_dist):
        ventana_izq = valores[i - min_dist:i]
        ventana_der = valores[i + 1:i + min_dist + 1]
        if es_minimo:
            if valores[i] < min(ventana_izq) and valores[i] < min(ventana_der):
                swings.append(i)
        else:
            if valores[i] > max(ventana_izq) and valores[i] > max(ventana_der):
                swings.append(i)
    return swings


def check_divergencia(df, timeframe="D"):
    """
    Divergencia real basada en swing points del MACD.
    Devuelve: (encontrada, tipo, duracion_str, antiguedad_str)
    """
    if 'MACD' not in df.columns or 'Close' not in df.columns:
        return False, "", "", ""

    min_velas = {"D": 30, "W": 26, "M": 12}.get(timeframe, 30)
    min_swing_sep = 3

    rango_macd = df['MACD'].max() - df['MACD'].min()
    if rango_macd == 0:
        return False, "", "", ""
    umbral_0 = rango_macd * 0.15

    macd_serie  = df['MACD']
    price_serie = df['Close']
    fecha_serie = df.index

    def formatear_duracion(velas, tf):
        if tf == "D":
            meses = round(velas / 21)
            return f"{meses} meses"
        elif tf == "W":
            meses = round(velas * 7 / 30)
            return f"{meses} meses"
        else:
            return f"{velas} meses"

    def formatear_antiguedad(pos_ultimo, total, tf):
        velas_atras = total - 1 - pos_ultimo
        if tf == "D":
            if velas_atras == 0: return "Hoy"
            if velas_atras < 5:  return f"Hace {velas_atras} días"
            semanas = round(velas_atras / 5)
            return f"Hace {semanas} sem"
        elif tf == "W":
            if velas_atras == 0: return "Esta semana"
            return f"Hace {velas_atras} sem"
        else:
            if velas_atras == 0: return "Este mes"
            return f"Hace {velas_atras} meses"

    total = len(df)
    low_serie  = df['Low']
    high_serie = df['High']

    # Buscar el mínimo/máximo de precio en una ventana alrededor del swing del MACD
    def min_precio_zona(pos, ventana=2):
        inicio = max(0, pos - ventana)
        fin    = min(total, pos + ventana + 1)
        return float(low_serie.iloc[inicio:fin].min())

    def max_precio_zona(pos, ventana=2):
        inicio = max(0, pos - ventana)
        fin    = min(total, pos + ventana + 1)
        return float(high_serie.iloc[inicio:fin].max())

    max_antiguedad   = {"D": 10, "W": 8, "M": 6}.get(timeframe, 8)
    MAX_SWINGS_ATRAS = 3   # v27: prueba p2 contra los 3 valles/picos anteriores

    # ── DIVERGENCIA ALCISTA ──
    # Precio hace mínimos más bajos (Low) y MACD hace mínimos más altos
    mins = encontrar_swings(macd_serie, es_minimo=True, min_dist=min_swing_sep)
    mins_validos = [i for i in mins if macd_serie.iloc[i] < -umbral_0]

    if len(mins_validos) >= 2:
        p2 = mins_validos[-1]
        precio_min_p2 = min_precio_zona(p2)
        activa  = (total - 1 - p2) <= max_antiguedad
        # Rota si después del swing el precio perfora el mínimo de la ZONA del swing
        intacta = float(low_serie.iloc[p2:].min()) >= precio_min_p2
        if activa and intacta:
            for p1 in reversed(mins_validos[-1 - MAX_SWINGS_ATRAS:-1]):
                if (p2 - p1) < min_velas:
                    continue
                # p1 tiene que ser el valle más profundo del MACD entre p1 y p2
                if macd_serie.iloc[p1:p2 + 1].min() < macd_serie.iloc[p1]:
                    continue
                precio_min_p1 = min_precio_zona(p1)
                if precio_min_p2 < precio_min_p1 and macd_serie.iloc[p2] > macd_serie.iloc[p1]:
                    fuerza = round(abs(macd_serie.iloc[p2] - macd_serie.iloc[p1]) / rango_macd * 100, 1)
                    if fuerza < 10.0:   # divergencias débiles son ruido
                        continue
                    duracion   = formatear_duracion(p2 - p1, timeframe)
                    antiguedad = formatear_antiguedad(p2, total, timeframe)
                    return True, f"DIV ALCISTA 📈 ({fuerza}%)", duracion, antiguedad

    # ── DIVERGENCIA BAJISTA ──
    # Precio hace máximos más altos (High) y MACD hace máximos más bajos
    maxs = encontrar_swings(macd_serie, es_minimo=False, min_dist=min_swing_sep)
    maxs_validos = [i for i in maxs if macd_serie.iloc[i] > umbral_0]

    if len(maxs_validos) >= 2:
        p2 = maxs_validos[-1]
        precio_max_p2 = max_precio_zona(p2)
        activa  = (total - 1 - p2) <= max_antiguedad
        intacta = float(high_serie.iloc[p2:].max()) <= precio_max_p2
        if activa and intacta:
            for p1 in reversed(maxs_validos[-1 - MAX_SWINGS_ATRAS:-1]):
                if (p2 - p1) < min_velas:
                    continue
                if macd_serie.iloc[p1:p2 + 1].max() > macd_serie.iloc[p1]:
                    continue
                precio_max_p1 = max_precio_zona(p1)
                if precio_max_p2 > precio_max_p1 and macd_serie.iloc[p2] < macd_serie.iloc[p1]:
                    fuerza = round(abs(macd_serie.iloc[p1] - macd_serie.iloc[p2]) / rango_macd * 100, 1)
                    if fuerza < 10.0:
                        continue
                    duracion   = formatear_duracion(p2 - p1, timeframe)
                    antiguedad = formatear_antiguedad(p2, total, timeframe)
                    return True, f"DIV BAJISTA 📉 ({fuerza}%)", duracion, antiguedad

    return False, "", "", ""


def super_buscador(pack):
    m = pack['M']; w = pack['W']; d = pack['D']
    if 'MACD' not in m.columns or len(m) < 2:
        return False, "", 0
    curr_m = m.iloc[-1]; prev_m = m.iloc[-2]
    m_bull = (curr_m['MACD'] > 0) and (curr_m['MACD'] > curr_m['Signal']) and (curr_m['MACD'] > prev_m['MACD'])
    m_bear = (curr_m['MACD'] < 0) and (curr_m['MACD'] < curr_m['Signal']) and (curr_m['MACD'] < prev_m['MACD'])
    w_curr = w.iloc[-1]; d_curr = d.iloc[-1]
    for i in range(5):
        idx = -1 - i
        es_vela, tipo, k, stop = check_vela_engano(w, idx=idx)
        if m_bull and (w_curr['MACD'] < w_curr['Signal']) and (d_curr['MACD'] > d_curr['Signal']) and es_vela and "ALCISTA" in tipo:
            return True, f"💎 BUY PREMIUM (Hace {i} sem)", stop
        if m_bear and (w_curr['MACD'] > w_curr['Signal']) and (d_curr['MACD'] < d_curr['Signal']) and es_vela and "BAJISTA" in tipo:
            return True, f"💀 SELL PREMIUM (Hace {i} sem)", stop
    return False, "", 0


def check_cruce_emas(df, velas=4):
    """
    Detecta cruce reciente de EMA50 con EMA200 en las últimas N velas.
    Golden Cross: EMA50 cruza por encima de EMA200 -> alcista
    Death Cross:  EMA50 cruza por debajo de EMA200 -> bajista
    v27: usa las EMAs precalculadas sobre 8 años (antes el semanal nunca tenía datos suficientes).
    """
    if 'EMA50' in df.columns and 'EMA200' in df.columns:
        if len(df) < velas + 2:
            return False, ""
        ema50, ema200 = df['EMA50'], df['EMA200']
    else:
        if len(df) < 205:
            return False, ""
        ema50  = df['Close'].ewm(span=50,  adjust=False).mean()
        ema200 = df['Close'].ewm(span=200, adjust=False).mean()

    for i in range(1, velas + 1):
        curr_diff = ema50.iloc[-i]   - ema200.iloc[-i]
        prev_diff = ema50.iloc[-i-1] - ema200.iloc[-i-1]
        if prev_diff <= 0 < curr_diff:
            return True, f"✨ GOLDEN CROSS (Hace {i-1} velas)"
        if prev_diff >= 0 > curr_diff:
            return True, f"💀 DEATH CROSS (Hace {i-1} velas)"
    return False, ""


def check_macd_estado(df):
    """
    Devuelve tupla (estado, posicion_cero)
    estado: 'alcista', 'bajista' o 'neutro'
    posicion_cero: 'encima' o 'debajo' respecto a la linea 0
    """
    if 'MACD' not in df.columns or 'Signal' not in df.columns or len(df) < 1:
        return 'neutro', 'encima'
    curr = df.iloc[-1]
    estado = 'neutro'
    if curr['MACD'] > curr['Signal']:
        estado = 'alcista'
    elif curr['MACD'] < curr['Signal']:
        estado = 'bajista'
    posicion = 'encima' if curr['MACD'] >= 0 else 'debajo'
    return estado, posicion



# ==============================================================================
# SEÑAL DE PACO PÉREZ — Motor de velas de cambio con triple confirmación
# ==============================================================================

def check_senal_paco(df, timeframe="D"):
    """
    Busca patrones de vela de cambio con triple confirmación:
    1. Patrón de vela reconocido (martillo, envolvente, harami, etc.)
    2. Estocástico en zona extrema (<20 alcista / >80 bajista)
    3. Volumen >= 2x media 20 velas Y máximo de las últimas 20 velas
    Devuelve lista de señales encontradas en las últimas 4 velas.
    """
    resultados = []

    if df is None or df.empty or len(df) < 25:
        return resultados
    if 'Volume' not in df.columns or 'K' not in df.columns:
        return resultados

    stoch_k = df['K']   # estocástico 14-3 ya calculado en _calcular_indicadores

    # Volumen institucional — media 20 velas + máximo 20 velas
    vol_media = df['Volume'].rolling(20).mean()
    vol_max20 = df['Volume'].rolling(20).max()

    macd_estado, _ = check_macd_estado(df)

    def nombre_tf(tf):
        return {"D": "días", "W": "semanas", "M": "meses"}.get(tf, "velas")

    # Buscar en las últimas 4 velas
    for vela_idx in range(1, 5):
        idx = -vela_idx
        if abs(idx) >= len(df) - 5:
            continue

        o = float(df['Open'].iloc[idx])
        h = float(df['High'].iloc[idx])
        l = float(df['Low'].iloc[idx])
        c = float(df['Close'].iloc[idx])
        v = float(df['Volume'].iloc[idx])
        o_prev = float(df['Open'].iloc[idx - 1])
        c_prev = float(df['Close'].iloc[idx - 1])
        vm   = float(vol_media.iloc[idx]) if not pd.isna(vol_media.iloc[idx]) else 0
        vmax = float(vol_max20.iloc[idx]) if not pd.isna(vol_max20.iloc[idx]) else 0
        k    = float(stoch_k.iloc[idx])   if not pd.isna(stoch_k.iloc[idx])   else 50

        if vm == 0:
            continue

        cuerpo     = abs(c - o)
        rango      = h - l + 1e-10
        mecha_inf  = min(o, c) - l
        mecha_sup  = h - max(o, c)
        es_alcista_vela = c > o
        ratio_vol  = round(v / vm, 2) if vm > 0 else 0

        # ── FILTROS OBLIGATORIOS ──
        # Volumen institucional: >2x media 20 velas Y mayor de las últimas 20 velas
        vol_ok   = (ratio_vol >= 2.0) and (v >= vmax * 0.95)
        stoch_ok_alc = k < 20
        stoch_ok_baj = k > 80

        if not vol_ok:
            continue

        patron    = None
        direccion = None

        # ─── MARTILLO (alcista) ───
        # Mecha inferior larga (>2x cuerpo), mecha superior pequeña, en zona baja
        if (stoch_ok_alc and
            mecha_inf >= cuerpo * 2.0 and
            mecha_sup <= cuerpo * 0.5 and
            cuerpo >= rango * 0.1 and
            mecha_inf >= rango * 0.55):
            patron    = "🔨 Martillo"
            direccion = "ALCISTA"

        # ─── MARTILLO INVERTIDO (alcista) ───
        elif (stoch_ok_alc and
              mecha_sup >= cuerpo * 2.0 and
              mecha_inf <= cuerpo * 0.5 and
              cuerpo >= rango * 0.1):
            patron    = "🔨 Martillo Invertido"
            direccion = "ALCISTA"

        # ─── ESTRELLA FUGAZ (bajista) ───
        elif (stoch_ok_baj and
              mecha_sup >= cuerpo * 2.0 and
              mecha_inf <= cuerpo * 0.3 and
              cuerpo >= rango * 0.1):
            patron    = "💫 Estrella Fugaz"
            direccion = "BAJISTA"

        # ─── PINBAR ALCISTA ───
        elif (stoch_ok_alc and
              mecha_inf >= rango * 0.65 and
              cuerpo <= rango * 0.25 and
              max(o, c) >= h - rango * 0.35):
            patron    = "📍 Pinbar Alcista"
            direccion = "ALCISTA"

        # ─── PINBAR BAJISTA ───
        elif (stoch_ok_baj and
              mecha_sup >= rango * 0.65 and
              cuerpo <= rango * 0.25 and
              min(o, c) <= l + rango * 0.35):
            patron    = "📍 Pinbar Bajista"
            direccion = "BAJISTA"

        # v27: la condición completa va DENTRO del elif. Antes, si la vela era verde
        # pero no envolvía, la cadena se cortaba y Harami/Doji/Marubozu nunca se evaluaban.

        # ─── ENVOLVENTE ALCISTA ───
        elif (stoch_ok_alc and es_alcista_vela and
              c_prev < o_prev and o < c_prev and c > o_prev):
            patron    = "🔁 Envolvente Alcista"
            direccion = "ALCISTA"

        # ─── ENVOLVENTE BAJISTA ───
        elif (stoch_ok_baj and not es_alcista_vela and
              c_prev > o_prev and o > c_prev and c < o_prev):
            patron    = "🔁 Envolvente Bajista"
            direccion = "BAJISTA"

        # ─── HARAMI ALCISTA ───
        elif (stoch_ok_alc and es_alcista_vela and
              c_prev < o_prev and
              o > c_prev and c < o_prev and
              cuerpo < abs(o_prev - c_prev) * 0.6):
            patron    = "🤰 Harami Alcista"
            direccion = "ALCISTA"

        # ─── HARAMI BAJISTA ───
        elif (stoch_ok_baj and not es_alcista_vela and
              c_prev > o_prev and
              o < c_prev and c > o_prev and
              cuerpo < abs(c_prev - o_prev) * 0.6):
            patron    = "🤰 Harami Bajista"
            direccion = "BAJISTA"

        # ─── DOJI DE GIRO ───
        elif (cuerpo <= rango * 0.08 and
              rango > 0 and
              (stoch_ok_alc or stoch_ok_baj)):
            direccion = "ALCISTA" if stoch_ok_alc else "BAJISTA"
            patron    = f"✝️ Doji {'Alcista' if stoch_ok_alc else 'Bajista'}"

        # ─── MARUBOZU ALCISTA (vela de fuerza) ───
        elif (stoch_ok_alc and
              es_alcista_vela and
              cuerpo >= rango * 0.85 and
              mecha_inf <= rango * 0.05 and
              mecha_sup <= rango * 0.05):
            patron    = "🟩 Marubozu Alcista"
            direccion = "ALCISTA"

        # ─── MARUBOZU BAJISTA ───
        elif (stoch_ok_baj and
              not es_alcista_vela and
              cuerpo >= rango * 0.85 and
              mecha_inf <= rango * 0.05 and
              mecha_sup <= rango * 0.05):
            patron    = "🟥 Marubozu Bajista"
            direccion = "BAJISTA"

        # ─── VELA DE ENGAÑO — usa check_vela_engano (misma lógica que buscador W/M) ───
        if patron is None:
            es_engano, tipo_engano, k_engano, _ = check_vela_engano(df, idx=idx)
            if es_engano and vol_ok:
                if "ALCISTA" in tipo_engano and stoch_ok_alc:
                    patron    = "🎭 Vela Engaño Alcista"
                    direccion = "ALCISTA"
                elif "BAJISTA" in tipo_engano and stoch_ok_baj:
                    patron    = "🎭 Vela Engaño Bajista"
                    direccion = "BAJISTA"

        if patron is None:
            continue

        # Calcular antigüedad
        unidad = nombre_tf(timeframe)
        if vela_idx == 1:
            antiguedad = f"Vela actual"
        else:
            antiguedad = f"Hace {vela_idx - 1} {unidad}"

        # Buscar patrones en las 4 velas PREVIAS a esta para contexto
        contexto_previas = []
        for prev_i in range(1, 5):
            prev_idx = idx - prev_i
            if abs(prev_idx) >= len(df) - 2:
                break
            op = float(df['Open'].iloc[prev_idx])
            hp = float(df['High'].iloc[prev_idx])
            lp = float(df['Low'].iloc[prev_idx])
            cp = float(df['Close'].iloc[prev_idx])
            cuerpo_p  = abs(cp - op)
            rango_p   = hp - lp + 1e-10
            mecha_i_p = min(op, cp) - lp
            mecha_s_p = hp - max(op, cp)
            # Solo detectar patrones más obvios para contexto
            if mecha_i_p >= cuerpo_p * 2.0 and mecha_s_p <= cuerpo_p * 0.5:
                contexto_previas.append(f"Martillo -{prev_i+vela_idx-1}{unidad[0]}")
            elif mecha_s_p >= cuerpo_p * 2.0 and mecha_i_p <= cuerpo_p * 0.5:
                contexto_previas.append(f"E.Fugaz -{prev_i+vela_idx-1}{unidad[0]}")
            elif mecha_i_p >= rango_p * 0.65 and cuerpo_p <= rango_p * 0.25:
                contexto_previas.append(f"Pinbar -{prev_i+vela_idx-1}{unidad[0]}")

        contexto_str = " · ".join(contexto_previas[:2]) if contexto_previas else "—"

        resultados.append({
            "patron":     patron,
            "direccion":  direccion,
            "antiguedad": antiguedad,
            "stoch_k":    round(k, 1),
            "vol_ratio":  ratio_vol,
            "macd":       macd_estado,
            "contexto":   contexto_str,
        })

    return resultados


def check_div_stoch(df, idx, direccion):
    """
    Detecta divergencia de estocástico en las últimas 4 velas.
    Alcista: primer mínimo stoch < 20, segundo mínimo más alto.
    Bajista: primer máximo stoch > 80, segundo máximo más bajo.
    """
    if 'K' not in df.columns or len(df) < abs(idx) + 5:
        return False
    # Extraer últimas 4 velas desde idx
    vals = [float(df['K'].iloc[idx - j]) if not pd.isna(df['K'].iloc[idx - j]) else 50
            for j in range(4)]
    if direccion == 'alcista':
        # Buscar dos mínimos donde el primero esté en sobreventa < 20
        for i in range(len(vals) - 1):
            for j in range(i + 1, len(vals)):
                if vals[j] < 20 and vals[i] > vals[j]:
                    return True  # primer mínimo (más antiguo) en sobreventa, segundo más alto
        return False
    else:
        # Buscar dos máximos donde el primero esté en sobrecompra > 80
        for i in range(len(vals) - 1):
            for j in range(i + 1, len(vals)):
                if vals[j] > 80 and vals[i] < vals[j]:
                    return True  # primer máximo (más antiguo) en sobrecompra, segundo más bajo
        return False


def check_patron_vela_macdelorean(df, idx=-1):
    """
    Detecta patrones de vela de cambio clásicos del análisis técnico japonés.
    No requiere volumen — misma lógica de confirmación que Premium.
    Devuelve: (encontrado, patron, direccion, stoch_k, stop)
    """
    if len(df) < abs(idx) + 3 or 'K' not in df.columns:
        return False, "", "", 0, 0

    curr  = df.iloc[idx]
    prev  = df.iloc[idx - 1]
    prev2 = df.iloc[idx - 2] if len(df) >= abs(idx) + 3 else prev

    o = float(curr['Open'])
    h = float(curr['High'])
    l = float(curr['Low'])
    c = float(curr['Close'])
    k = float(curr['K']) if not pd.isna(curr['K']) else 50

    # Estocástico de la vela anterior (vela del medio para 3 cuerpos)
    k1 = float(prev['K']) if not pd.isna(prev['K']) else 50

    o1 = float(prev['Open']);  c1 = float(prev['Close'])
    h1 = float(prev['High']);  l1 = float(prev['Low'])
    o2 = float(prev2['Open']); c2 = float(prev2['Close'])
    h2 = float(prev2['High']); l2 = float(prev2['Low'])

    cuerpo    = abs(c - o)
    rango     = h - l + 1e-10
    mecha_inf = min(o, c) - l
    mecha_sup = h - max(o, c)
    cuerpo1   = abs(c1 - o1)
    rango1    = h1 - l1 + 1e-10
    mid_prev  = (h1 + l1) / 2

    es_alc  = c > o
    es_alc1 = c1 > o1

    stoch_alc  = k < 20
    stoch_baj  = k > 80

    # Divergencia de estocástico (segunda oportunidad si no está en extremo)
    # Solo estocástico extremo — sin divergencia de estocástico
    confirm_alc = stoch_alc
    confirm_baj = stoch_baj

    # ─── VELA DE ENGAÑO (reutiliza check_vela_engano) ───
    es_eng, tipo_eng, k_eng, stop_eng = check_vela_engano(df, idx=idx)
    if es_eng:
        if "ALCISTA" in tipo_eng and confirm_alc:
            nombre = "🎭 Vela Engaño"
            return True, nombre, "ALCISTA", k, float(min(l, l1))
        if "BAJISTA" in tipo_eng and confirm_baj:
            nombre = "🎭 Vela Engaño"
            return True, nombre, "BAJISTA", k, float(max(h, h1))

    # ─── MARTILLO (alcista) ───
    if (confirm_alc and
        mecha_inf >= cuerpo * 2.0 and
        mecha_sup <= cuerpo * 0.5 and
        cuerpo >= rango * 0.1 and
        mecha_inf >= rango * 0.55):
        nombre = "🔨 Martillo"
        return True, nombre, "ALCISTA", k, float(l)

    # ─── HOMBRE COLGADO (bajista) ───
    if (confirm_baj and
        mecha_inf >= cuerpo * 2.0 and
        mecha_sup <= cuerpo * 0.5 and
        cuerpo >= rango * 0.1 and
        mecha_inf >= rango * 0.55):
        nombre = "💀 Hombre Colgado"
        return True, nombre, "BAJISTA", k, float(h)

    # ─── MARTILLO INVERTIDO (alcista) ───
    if (confirm_alc and
        mecha_sup >= cuerpo * 2.0 and
        mecha_inf <= cuerpo * 0.5 and
        cuerpo >= rango * 0.1):
        nombre = "🔨 Martillo Invertido"
        return True, nombre, "ALCISTA", k, float(l)

    # ─── ESTRELLA FUGAZ (bajista) ───
    if (confirm_baj and
        mecha_sup >= cuerpo * 2.0 and
        mecha_inf <= cuerpo * 0.3 and
        cuerpo >= rango * 0.1):
        nombre = "💫 Estrella Fugaz"
        return True, nombre, "BAJISTA", k, float(h)

    # ─── ENVOLVENTE ALCISTA ───
    if (confirm_alc and es_alc and not es_alc1 and
        o <= c1 and c >= o1 and
        cuerpo > cuerpo1 * 0.8):
        nombre = "🔁 Envolvente Alcista"
        return True, nombre, "ALCISTA", k, float(l)

    # ─── ENVOLVENTE BAJISTA ───
    if (confirm_baj and not es_alc and es_alc1 and
        o >= c1 and c <= o1 and
        cuerpo > cuerpo1 * 0.8):
        nombre = "🔁 Envolvente Bajista"
        return True, nombre, "BAJISTA", k, float(h)

    # ─── HARAMI ALCISTA ───
    if (confirm_alc and es_alc and not es_alc1 and
        o > c1 and c < o1 and
        cuerpo < cuerpo1 * 0.6):
        nombre = "🤰 Harami Alcista"
        return True, nombre, "ALCISTA", k, float(l)

    # ─── HARAMI BAJISTA ───
    if (confirm_baj and not es_alc and es_alc1 and
        o < c1 and c > o1 and
        cuerpo < cuerpo1 * 0.6):
        nombre = "🤰 Harami Bajista"
        return True, nombre, "BAJISTA", k, float(h)

    # ─── DOJI DE GIRO ALCISTA ───
    if (confirm_alc and cuerpo <= rango * 0.08 and rango > 0):
        nombre = "✝️ Doji Alcista"
        return True, nombre, "ALCISTA", k, float(l)

    # ─── DOJI DE GIRO BAJISTA ───
    if (confirm_baj and cuerpo <= rango * 0.08 and rango > 0):
        nombre = "✝️ Doji Bajista"
        return True, nombre, "BAJISTA", k, float(h)

    # ─── MORNING STAR — estocástico medido en vela del medio (k1) ───
    es_bajista2 = o2 > c2
    stoch_mid_alc = k1 < 20
    if (stoch_mid_alc and es_alc and
        es_bajista2 and
        abs(c2 - o2) >= (h2 - l2 + 1e-10) * 0.5 and
        abs(c1 - o1) <= (h1 - l1 + 1e-10) * 0.3 and
        cuerpo >= rango * 0.45 and
        c > (o2 + c2) / 2):
        nombre = "⭐ Morning Star"
        return True, nombre, "ALCISTA", k1, float(min(l, l1, l2))

    # ─── EVENING STAR — estocástico medido en vela del medio (k1) ───
    es_alcista2 = c2 > o2
    stoch_mid_baj = k1 > 80
    if (stoch_mid_baj and not es_alc and
        es_alcista2 and
        abs(c2 - o2) >= (h2 - l2 + 1e-10) * 0.5 and
        abs(c1 - o1) <= (h1 - l1 + 1e-10) * 0.3 and
        cuerpo >= rango * 0.45 and
        c < (o2 + c2) / 2):
        nombre = "⭐ Evening Star"
        return True, nombre, "BAJISTA", k1, float(max(h, h1, h2))

    # ─── PINBAR ALCISTA ───
    if (confirm_alc and
        mecha_inf >= rango * 0.65 and
        cuerpo <= rango * 0.25):
        nombre = "📍 Pinbar Alcista"
        return True, nombre, "ALCISTA", k, float(l)

    # ─── PINBAR BAJISTA ───
    if (confirm_baj and
        mecha_sup >= rango * 0.65 and
        cuerpo <= rango * 0.25):
        nombre = "📍 Pinbar Bajista"
        return True, nombre, "BAJISTA", k, float(h)

    # ─── TRES SOLDADOS BLANCOS — patrón alcista de 3 velas consecutivas ───
    # Condiciones:
    # 1. Las 3 velas son alcistas (cierre > apertura)
    # 2. Cada vela cierra más alta que la anterior
    # 3. Cada vela abre dentro del cuerpo de la vela anterior
    # 4. Cuerpos significativos (no son dojis)
    # 5. Estocástico < 20 en la PRIMERA vela del patrón (la más antigua = vela 2 atrás)
    if len(df) >= abs(idx) + 3:
        k2 = float(prev2['K']) if not pd.isna(prev2['K']) else 50
        es_alc2 = c2 > o2
        # Las tres velas son alcistas
        if (es_alc2 and es_alc1 and es_alc and
            k2 < 20 and  # estocástico extremo en la PRIMERA vela
            c2 < c1 < c and  # cierres ascendentes
            o1 > o2 and o1 < c2 and  # vela 1 abre dentro del cuerpo de vela 2
            o > o1 and o < c1 and  # vela actual abre dentro del cuerpo de vela 1
            abs(c2 - o2) >= (h2 - l2 + 1e-10) * 0.3 and
            abs(c1 - o1) >= (h1 - l1 + 1e-10) * 0.3 and
            cuerpo >= rango * 0.3):
            return True, "🪖 Tres Soldados Blancos", "ALCISTA", k2, float(min(l, l1, l2))

    # ─── TRES CUERVOS NEGROS — patrón bajista de 3 velas consecutivas ───
    if len(df) >= abs(idx) + 3:
        k2 = float(prev2['K']) if not pd.isna(prev2['K']) else 50
        es_baj2 = c2 < o2
        es_baj1 = c1 < o1
        es_baj  = c < o
        if (es_baj2 and es_baj1 and es_baj and
            k2 > 80 and  # estocástico extremo en la PRIMERA vela
            c2 > c1 > c and  # cierres descendentes
            o1 < o2 and o1 > c2 and  # vela 1 abre dentro del cuerpo de vela 2
            o < o1 and o > c1 and  # vela actual abre dentro del cuerpo de vela 1
            abs(o2 - c2) >= (h2 - l2 + 1e-10) * 0.3 and
            abs(o1 - c1) >= (h1 - l1 + 1e-10) * 0.3 and
            cuerpo >= rango * 0.3):
            return True, "🦅 Tres Cuervos Negros", "BAJISTA", k2, float(max(h, h1, h2))

    return False, "", "", k, 0


def buscador_velas_macdelorean(pack):
    """
    Confluencia M+W+D estilo Premium con patrones ampliados:
      - MACD mensual alineado con la dirección final
      - Semanal en CORRECCIÓN (MACD contra la dirección) + patrón de cambio + estoc. extremo
      - MACD diario YA girando en la dirección final
    Alcista (BUY): M alcista + W bajista + patrón alcista semanal + D alcista
    Bajista (SELL): M bajista + W alcista + patrón bajista semanal + D bajista
    """
    m = pack['M']; w = pack['W']; d = pack['D']
    if ('MACD' not in m.columns or len(m) < 2 or
        'MACD' not in w.columns or len(w) < 1 or
        'MACD' not in d.columns or len(d) < 1):
        return False, "", "", 0, 0

    curr_m = m.iloc[-1]
    curr_w = w.iloc[-1]
    curr_d = d.iloc[-1]

    m_bull = (curr_m['MACD'] > 0) and (curr_m['MACD'] > curr_m['Signal'])
    m_bear = (curr_m['MACD'] < 0) and (curr_m['MACD'] < curr_m['Signal'])

    # Semanal correctivo: contra la tendencia mensual
    w_bull = curr_w['MACD'] > curr_w['Signal']
    w_bear = curr_w['MACD'] < curr_w['Signal']

    # Diario ya girando hacia la dirección final
    d_bull = curr_d['MACD'] > curr_d['Signal']
    d_bear = curr_d['MACD'] < curr_d['Signal']

    if not (m_bull or m_bear):
        return False, "", "", 0, 0

    # Buscar patrón de cambio en las últimas 5 semanas
    for i in range(5):
        idx = -1 - i
        es_patron, patron, direccion, k, stop = check_patron_vela_macdelorean(w, idx=idx)
        if not es_patron:
            continue
        # ALCISTA: M alcista + W correctivo bajista + patrón alcista + D alcista
        if direccion == "ALCISTA" and m_bull and w_bear and d_bull:
            return True, f"🚗 MACDELOREAN BUY — {patron} (Hace {i} sem)", direccion, k, stop
        # BAJISTA: M bajista + W correctivo alcista + patrón bajista + D bajista
        if direccion == "BAJISTA" and m_bear and w_bull and d_bear:
            return True, f"🚗 MACDELOREAN SELL — {patron} (Hace {i} sem)", direccion, k, stop

    return False, "", "", 0, 0



def check_sabroson(pack, periodo_ema=200, timeframe="W", margen_pct=2.0, velas_atras=3,
                   filtros_macd=None):
    """
    Busca patrón de cambio tocando una EMA con MACD configurables por timeframe.
    filtros_macd es un dict con claves 'M', 'W', 'D' y cada valor es una tupla:
        (estado, posicion_cero) donde:
            estado    ∈ {"⚪ Cualquiera", "🟢 Alcista", "🔴 Bajista"}
            posicion  ∈ {"⚪ Cualquiera", "⬆️ Por encima de 0", "⬇️ Por debajo de 0"}
    Si filtros_macd es None, no aplica filtros MACD (todos cualquiera).
    Devuelve (encontrado, direccion, patron, antiguedad, precio_ema, distancia_pct, stoch_k, stop)
    """
    df = pack[timeframe]
    col_ema = f"EMA{periodo_ema}"
    if col_ema not in df.columns and len(df) < periodo_ema + 5:
        return False, "", "", "", 0, 0, 0, 0

    if filtros_macd is None:
        filtros_macd = {
            'M': ("⚪ Cualquiera", "⚪ Cualquiera"),
            'W': ("⚪ Cualquiera", "⚪ Cualquiera"),
            'D': ("⚪ Cualquiera", "⚪ Cualquiera"),
        }

    # Verifica si la dirección candidata cumple los filtros MACD en los 3 TFs
    def macd_cumple(direccion):
        for tf_check in ('M', 'W', 'D'):
            est_sel, cer_sel = filtros_macd.get(tf_check, ("⚪ Cualquiera", "⚪ Cualquiera"))
            if est_sel == "⚪ Cualquiera" and cer_sel == "⚪ Cualquiera":
                continue
            if tf_check not in pack or 'MACD' not in pack[tf_check].columns or len(pack[tf_check]) < 1:
                return False
            est_tf, pos_tf = check_macd_estado(pack[tf_check])
            if est_sel == "🟢 Alcista" and est_tf != 'alcista': return False
            if est_sel == "🔴 Bajista" and est_tf != 'bajista': return False
            if cer_sel == "⬆️ Por encima de 0" and pos_tf != 'encima': return False
            if cer_sel == "⬇️ Por debajo de 0" and pos_tf != 'debajo': return False
        return True

    # EMA sobre el timeframe elegido
    ema_serie = df[col_ema] if col_ema in df.columns else df['Close'].ewm(span=periodo_ema, adjust=False).mean()

    unidad = {"D": "Día", "W": "Sem", "M": "Mes"}.get(timeframe, "vela")

    for j in range(velas_atras):
        idx = -1 - j
        if abs(idx) >= len(df):
            break

        vela = df.iloc[idx]
        low  = float(vela['Low'])
        high = float(vela['High'])
        close = float(vela['Close'])
        ema_vela = float(ema_serie.iloc[idx])

        if ema_vela <= 0:
            continue

        # Verificar toque en esta vela
        margen = ema_vela * (margen_pct / 100.0)
        zona_baja = ema_vela - margen
        zona_alta = ema_vela + margen
        toque_directo = (low <= ema_vela <= high)
        cerca = (zona_baja <= close <= zona_alta)
        toca = toque_directo or cerca

        if not toca:
            continue

        # Detectar patrón de vela en esta misma posición
        es_patron, patron, direccion, k, stop = check_patron_vela_macdelorean(df, idx=idx)
        if not es_patron:
            continue

        # Comprobar filtros MACD configurables en M, W, D
        if not macd_cumple(direccion):
            continue

        distancia_pct = round(abs(close - ema_vela) / ema_vela * 100, 2)
        antiguedad = "Vela actual" if j == 0 else f"Hace {j} {unidad}"

        return True, direccion, patron, antiguedad, round(ema_vela, 2), distancia_pct, round(k, 1), round(float(stop), 2)

    return False, "", "", "", 0, 0, 0, 0


# ==============================================================================
# 2b. UBICACIÓN DE LA VELA — ¿dónde aparece la señal?
#     Solo informa, no descarta nada. Cada punto a favor suma una ⭐.
#     Todo se mide con datos hasta la vela de la señal (nada del futuro).
# ==============================================================================

TF_INFERIOR = {'W': 'D', 'M': 'W', 'D': 'D'}          # la estructura se busca en la temporalidad de abajo
NOMBRE_TF   = {'D': 'diario', 'W': 'semanal', 'M': 'mensual'}
FIN_VELA    = {'D': pd.Timedelta(days=0), 'W': pd.Timedelta(days=6)}


def _atr(df, n=14):
    """Rango medio real: cuánto se mueve el valor normalmente. Sirve para medir 'cerca' sin usar %."""
    prev = df['Close'].shift(1)
    tr = pd.concat([df['High'] - df['Low'], (df['High'] - prev).abs(), (df['Low'] - prev).abs()], axis=1).max(axis=1)
    return tr.rolling(n, min_periods=5).mean()


def _abc_en_c(pack, tf, pos, alcista):
    """¿La vela de la señal es el punto C de un A-B-C en la temporalidad inferior?
    Alcista: A = mínimo, B = máximo posterior, C = mínimo de la vela de la señal, que retrocede
    al menos el 61,8 % de A→B, sin un mínimo más bajo entre B y la vela. (Bajista: al revés.)"""
    df_sig = pack[tf]
    df_inf = pack.get(TF_INFERIOR[tf])
    if df_inf is None or df_inf.empty:
        return None
    desde = df_sig.index[pos]
    if tf == 'M':
        hasta = desde + pd.offsets.MonthEnd(0)
    else:
        hasta = desde + FIN_VELA[tf]
    vela = df_inf[(df_inf.index >= desde) & (df_inf.index <= hasta)]
    previas = df_inf[df_inf.index < desde].iloc[-60:]
    if vela.empty or len(previas) < 15:
        return None
    atr = float(_atr(df_inf).loc[:vela.index[-1]].iloc[-1])
    if not atr > 0:
        return None

    ventana_b = previas.iloc[-40:]
    if alcista:
        c = float(vela['Low'].min())
        ib = ventana_b['High'].idxmax(); b = float(ventana_b['High'].max())
        antes_b = previas[previas.index < ib].iloc[-40:]
        if len(antes_b) < 3:
            return None
        ia = antes_b['Low'].idxmin(); a = float(antes_b['Low'].min())
        tramo = b - a
        entre_b_y_c = previas[previas.index > ib]['Low']
        hueco = (not entre_b_y_c.empty) and float(entre_b_y_c.min()) < c - 0.25 * atr
        buena = c < a
    else:
        c = float(vela['High'].max())
        ib = ventana_b['Low'].idxmin(); b = float(ventana_b['Low'].min())
        antes_b = previas[previas.index < ib].iloc[-40:]
        if len(antes_b) < 3:
            return None
        ia = antes_b['High'].idxmax(); a = float(antes_b['High'].max())
        tramo = a - b
        entre_b_y_c = previas[previas.index > ib]['High']
        hueco = (not entre_b_y_c.empty) and float(entre_b_y_c.max()) > c + 0.25 * atr
        buena = c > a

    if tramo < 2 * atr or hueco:                                  # oscilación pequeña o la C ya fue antes
        return None
    retroceso = (b - c) / tramo if alcista else (c - b) / tramo
    if retroceso < 0.618:                                          # no volvió lo bastante hacia A
        return None
    if abs(c - a) > max(1.5 * atr, 0.5 * tramo):                   # C demasiado lejos de A: ya no es un ABC
        return None
    n_ac = int(((df_inf.index > ia) & (df_inf.index <= vela.index[-1])).sum())
    if not (8 <= n_ac <= 80):
        return None
    return f"📍 C de ABC {NOMBRE_TF[TF_INFERIOR[tf]]} ({'buena' if buena else 'mala'} osc.)"


def _vela_previa_en_a(df, pos, alcista):
    """¿Hubo otra vela de cambio en la misma dirección 3-10 velas antes y a un precio parecido?"""
    atr = float(_atr(df).iloc[pos])
    if not atr > 0:
        return None
    extremo = float(df['Low'].iloc[pos]) if alcista else float(df['High'].iloc[pos])
    for k in range(3, 11):
        p = pos - k
        if p < 3:
            break
        idx = p - len(df)
        ok, _, direc, _, _ = check_patron_vela_macdelorean(df, idx=idx)
        if not ok:
            ok_e, tipo_e, _, _ = check_vela_engano(df, idx=idx)
            ok, direc = ok_e, ("ALCISTA" if "ALCISTA" in tipo_e else "BAJISTA")
        if ok and (direc == "ALCISTA") == alcista:
            otro = float(df['Low'].iloc[p]) if alcista else float(df['High'].iloc[p])
            if abs(otro - extremo) <= atr:
                return f"🔂 Vela de cambio en A (hace {k})"
    return None


def _pullback_a_b(df, pos, alcista):
    """¿El precio rompió un B y ha vuelto a tocarlo? La vela de cambio aparece sobre el nivel roto."""
    atr = float(_atr(df).iloc[pos])
    if not atr > 0 or pos < 15:
        return None
    lo, hi, cl = df['Low'].values, df['High'].values, df['Close'].values
    for pb in range(pos - 3, max(pos - 40, 2), -1):
        if alcista:
            if not (hi[pb] > hi[pb - 1] and hi[pb] > hi[pb - 2] and hi[pb] >= hi[pb + 1] and hi[pb] >= hi[pb + 2]):
                continue
            nivel = hi[pb]
            roto = any(cl[j] > nivel for j in range(pb + 1, pos))
            if roto and nivel - atr <= lo[pos] <= nivel + atr and cl[pos] >= nivel - 0.5 * atr:
                return "🔁 Pullback a B"
        else:
            if not (lo[pb] < lo[pb - 1] and lo[pb] < lo[pb - 2] and lo[pb] <= lo[pb + 1] and lo[pb] <= lo[pb + 2]):
                continue
            nivel = lo[pb]
            roto = any(cl[j] < nivel for j in range(pb + 1, pos))
            if roto and nivel - atr <= hi[pos] <= nivel + atr and cl[pos] <= nivel + 0.5 * atr:
                return "🔁 Pullback a B"
    return None


def _div_estocastico(df, pos, alcista):
    """Divergencia de estocástico de verdad: el precio hace un mínimo más bajo y el estocástico
    uno más alto, con el primero en sobreventa (<20). Bajista: al revés (>80)."""
    if 'K' not in df.columns or pos < 12:
        return None
    k = df['K'].values
    serie = df['Low'].values if alcista else df['High'].values
    # extremo actual: el de la zona de la señal (la vela y las 2 anteriores)
    zona = range(max(pos - 2, 0), pos + 1)
    p2 = min(zona, key=lambda i: serie[i]) if alcista else max(zona, key=lambda i: serie[i])
    for p1 in range(p2 - 5, max(p2 - 30, 2), -1):
        es_giro = (serie[p1] < serie[p1 - 1] and serie[p1] < serie[p1 + 1]) if alcista else \
                  (serie[p1] > serie[p1 - 1] and serie[p1] > serie[p1 + 1])
        if not es_giro:
            continue
        # el estocástico se compara por su extremo en cada zona (±2 velas), como se mira en el gráfico
        z1 = [x for x in k[max(p1 - 2, 0):p1 + 3] if not pd.isna(x)]
        z2 = [x for x in k[max(p2 - 2, 0):pos + 1] if not pd.isna(x)]
        if not z1 or not z2:
            continue
        entre = [x for x in k[p1 + 1:p2] if not pd.isna(x)]      # entre los dos extremos debe salir de la zona
        if not entre:
            continue
        if (alcista and serie[p2] < serie[p1] and min(z1) < 20 and max(entre) > 30
                and min(z2) >= min(z1) + 8):
            return "📐 Div. estocástico"
        if (not alcista and serie[p2] > serie[p1] and max(z1) > 80 and min(entre) < 70
                and max(z2) <= max(z1) - 8):
            return "📐 Div. estocástico"
    return None


def _div_macd(df, pos, alcista, tf):
    ok, tipo, _, _ = check_divergencia(df.iloc[:pos + 1], timeframe=tf)
    if ok and ("ALCISTA" in tipo) == alcista:
        return "📐 Div. MACD"
    return None


def _apoyo_ema(df, pos, tf):
    atr = float(_atr(df).iloc[pos])
    if not atr > 0:
        return None
    fila = df.iloc[pos]
    medias = [('EMA50', 'EMA 50'), ('EMA200', 'EMA 200')]
    if tf == 'W':
        medias.append(('EMA40', 'EMA 200 diaria'))
    tocadas = [nombre for col, nombre in medias
               if col in df.columns and not pd.isna(fila[col])
               and fila['Low'] - 0.3 * atr <= fila[col] <= fila['High'] + 0.3 * atr]
    return f"📏 Apoyo {' + '.join(tocadas)}" if tocadas else None


def ubicacion(pack, tf, idx, alcista):
    """Devuelve {'Ubicación': texto, '⭐': estrellas} para la vela idx (negativo) del timeframe tf."""
    df = pack.get(tf)
    if df is None or df.empty or tf not in ('D', 'W', 'M') or abs(idx) > len(df):
        return {"Ubicación": "—", "⭐": ""}
    pos = len(df) + idx
    etiquetas = []
    for f in (lambda: _abc_en_c(pack, tf, pos, alcista),
              lambda: _vela_previa_en_a(df, pos, alcista),
              lambda: _pullback_a_b(df, pos, alcista),
              lambda: _div_macd(df, pos, alcista, tf),
              lambda: _div_estocastico(df, pos, alcista),
              lambda: _apoyo_ema(df, pos, tf)):
        try:
            e = f()
        except Exception:
            e = None
        if e:
            etiquetas.append(e)
    return {"Ubicación": " · ".join(etiquetas) if etiquetas else "—", "⭐": "⭐" * len(etiquetas)}


def _idx_desde_texto(txt):
    """'Vela actual' → -1 · 'Hace 2 Sem' / '(Hace 2 sem)' → -3."""
    import re
    m = re.search(r"Hace (\d+)", txt or "")
    return -1 - int(m.group(1)) if m else -1


# ==============================================================================
# 3. UTILIDADES COMUNES (antes repetidas en cada escáner)
# ==============================================================================

OPC_ESTADO = ["⚪ Cualquiera", "🟢 Alcista", "🔴 Bajista"]
OPC_CERO   = ["⚪ Cualquiera", "⬆️ Por encima de 0", "⬇️ Por debajo de 0"]
SIN_FILTRO = {tf: ("⚪ Cualquiera", "⚪ Cualquiera") for tf in ('M', 'W', 'D')}
TF_NOMBRE  = {'D': 'DIARIO', 'W': 'SEMANAL', 'M': 'MENSUAL', '4H': '4 HORAS'}
TF_UNIDAD  = {'D': 'Día', 'W': 'Sem', 'M': 'Mes'}


@st.cache_resource
def _memoria_servidor():
    """Memoria que vive en el servidor, no en el móvil: sobrevive si la pantalla se bloquea
    o se cierra la pestaña. Guarda el último escaneo para poder retomarlo."""
    return {}


MEMORIA = _memoria_servidor()


def macd_pasa(df, est_sel, cer_sel):
    """Aplica el filtro MACD de un timeframe. Devuelve (cumple, estado, posicion)."""
    est, pos = check_macd_estado(df)
    ok = not ((est_sel == "🟢 Alcista" and est != 'alcista') or
              (est_sel == "🔴 Bajista" and est != 'bajista') or
              (cer_sel == "⬆️ Por encima de 0" and pos != 'encima') or
              (cer_sel == "⬇️ Por debajo de 0" and pos != 'debajo'))
    return ok, est, pos


def txt_macd(est, pos=None):
    icono = "🟢" if est == 'alcista' else ("🔴" if est == 'bajista' else "⚪")
    txt = f"{icono} {est.capitalize()}"
    if pos is not None:
        txt += " ⬆️" if pos == 'encima' else " ⬇️"
    return txt


def direccion_ok(alcista, cfg):
    return (alcista and cfg['dir_alc']) or (not alcista and cfg['dir_baj'])


def velas_a_tiempo(v, tf):
    if tf == "4H":
        horas = v * 4
        if horas < 24: return f"{horas}h"
        dias = horas // 24
        return f"{dias} dia{'s' if dias > 1 else ''}"
    if tf == "D":
        if v <= 1: return "Hoy"
        if v < 5:  return f"{v} dias"
        sem = v // 5
        return f"{sem} semana{'s' if sem > 1 else ''}"
    if tf == "W":
        if v <= 1: return "Esta semana"
        if v < 4:  return f"{v} semanas"
        mes = round(v * 7 / 30)
        return f"{mes} mes{'es' if mes > 1 else ''}"
    if tf == "M":
        if v <= 1: return "Este mes"
        return f"{v} meses"
    return f"{v} velas"


# ==============================================================================
# 4. ESCÁNERES — cada uno recibe (ticker, pack, precio, cfg) y devuelve filas
# ==============================================================================

def esc_premium(t, pack, precio, cfg):
    ok, txt, stop = super_buscador(pack)
    if ok and (("BUY" in txt and cfg['dir_alc']) or ("SELL" in txt and cfg['dir_baj'])):
        return [{"Ticker": t, "Señal": txt, "Precio": precio, "Stop Ref": round(float(stop), 2),
                 **ubicacion(pack, 'W', _idx_desde_texto(txt), "BUY" in txt)}]
    return []


def esc_velas(t, pack, precio, cfg):
    filas = []
    for tf in cfg['vc_tfs']:
        est_sel, cer_sel = cfg['vc_macd'][tf]
        for j in range(4):
            ok, patron, dir_p, k_p, stop_p = check_patron_vela_macdelorean(pack[tf], idx=-1 - j)
            if not ok:
                continue
            if not direccion_ok(dir_p == "ALCISTA", cfg):
                continue          # mirar velas más antiguas en la dirección pedida
            pasa, est, pos = macd_pasa(pack[tf], est_sel, cer_sel)
            if pasa:
                filas.append({"Ticker": t, "TF": TF_NOMBRE[tf], "Patrón": patron, "Dirección": dir_p,
                              "Antigüedad": f"Hace {j} {TF_UNIDAD[tf]}", "Stoch K": round(k_p, 1),
                              "MACD": txt_macd(est, pos), "Precio": precio, "Stop Ref": round(float(stop_p), 2),
                              **ubicacion(pack, tf, -1 - j, dir_p == "ALCISTA")})
            break
    return filas


def _divergencias_filtradas(pack, cfg):
    """Divergencias válidas en D/W/M que pasan dirección y filtro MACD (compartido por 3 escáneres)."""
    for tf in ('D', 'W', 'M'):
        es_div, tipo, dur, antig = check_divergencia(pack[tf], timeframe=tf)
        if not es_div:
            continue
        alc = "ALCISTA" in tipo
        if not direccion_ok(alc, cfg):
            continue
        pasa, est, pos = macd_pasa(pack[tf], *cfg['div_macd'][tf])
        if pasa:
            yield tf, tipo, dur, antig, alc, est, pos


def _fuerza(tipo):
    return tipo.split("(")[1].replace(")", "") if "(" in tipo else "-"


def esc_diverg(t, pack, precio, cfg):
    return [{"Ticker": t, "TF": TF_NOMBRE[tf], "Tipo": tipo, "Duración": dur, "Formada": antig,
             "MACD": txt_macd(est, pos), "Precio": precio}
            for tf, tipo, dur, antig, alc, est, pos in _divergencias_filtradas(pack, cfg)]


def esc_confluencia(t, pack, precio, cfg):
    filas = []
    for tf, tipo, dur, antig, alc, est, pos in _divergencias_filtradas(pack, cfg):
        for j in range(4):
            ok, patron, dir_p, k_p, stop_p = check_patron_vela_macdelorean(pack[tf], idx=-1 - j)
            if ok and (dir_p == "ALCISTA") == alc:
                filas.append({"Ticker": t, "TF": TF_NOMBRE[tf],
                              "Dirección": '🟢 ALCISTA' if alc else '🔴 BAJISTA',
                              "Señal": f"{'🚀' if alc else '💣'} DIV + {patron}",
                              "Div Fuerza": _fuerza(tipo), "Div Dur.": dur, "MACD": txt_macd(est, pos),
                              "Vela Stoch": round(k_p, 1), "Antigüedad": f"Hace {j} {TF_UNIDAD[tf]}",
                              "Precio": precio, "Stop Ref": round(float(stop_p), 2),
                              **ubicacion(pack, tf, -1 - j, alc)})
                break
    return filas


def esc_conf_master(t, pack, precio, cfg):
    filas = []
    for tf, tipo, dur, antig, alc, est, pos in _divergencias_filtradas(pack, cfg):
        for j in range(4):
            ok, tipo_v, k_v, stop_v = check_vela_engano(pack[tf], idx=-1 - j)
            if ok and ("ALCISTA" in tipo_v) == alc:
                filas.append({"Ticker": t, "TF": TF_NOMBRE[tf], "Dirección": "ALCISTA" if alc else "BAJISTA",
                              "Señal": f"{'🚀' if alc else '💣'} DIV + VELA ENGAÑO",
                              "Div Fuerza": _fuerza(tipo), "Div Dur.": dur, "MACD": txt_macd(est, pos),
                              "Vela Stoch": round(k_v, 1), "Antigüedad": f"Hace {j} {TF_UNIDAD[tf]}",
                              "Precio": precio, "Stop Ref": round(float(stop_v), 2),
                              **ubicacion(pack, tf, -1 - j, alc)})
                break
    return filas


def esc_macd_combo(t, pack, precio, cfg):
    estados = {}
    for tf in ('M', 'W', 'D'):
        pasa, est, pos = macd_pasa(pack[tf], *cfg['combo_macd'][tf])
        if not pasa:
            return []
        estados[tf] = txt_macd(est, pos)
    return [{"Ticker": t, "Mensual": estados['M'], "Semanal": estados['W'], "Diario": estados['D'],
             "Precio": precio}]


def esc_macdelorean(t, pack, precio, cfg):
    ok, txt, dir_m, k, stop = buscador_velas_macdelorean(pack)
    if ok and direccion_ok(dir_m == "ALCISTA", cfg):
        return [{"Ticker": t, "Señal": txt, "Dirección": dir_m, "Stoch K": round(k, 1),
                 "Stop Ref": round(float(stop), 2), "Precio": precio,
                 **ubicacion(pack, 'W', _idx_desde_texto(txt), dir_m == "ALCISTA")}]
    return []


def _esc_sabroson(t, pack, precio, cfg, periodo, tf, filtros, col_ema):
    ok, dir_s, patron, antig, p_ema, dist, k, stop = check_sabroson(
        pack, periodo_ema=periodo, timeframe=tf, margen_pct=2.0, velas_atras=3, filtros_macd=filtros)
    if ok and direccion_ok(dir_s == "ALCISTA", cfg):
        return [{"Ticker": t, "Dirección": dir_s, "Patrón": patron, "Antigüedad": antig, col_ema: p_ema,
                 "Distancia %": dist, "Stoch K": k, "Stop Ref": stop, "Precio": precio,
                 **ubicacion(pack, tf, _idx_desde_texto(antig), dir_s == "ALCISTA")}]
    return []


def esc_sabroson200(t, pack, precio, cfg):
    return _esc_sabroson(t, pack, precio, cfg, 40, "W", cfg['s200_macd'], "EMA 200D/40W")


def esc_sabroson50(t, pack, precio, cfg):
    return _esc_sabroson(t, pack, precio, cfg, 50, "D", cfg['s50_macd'], "EMA 50 (D)")


def esc_paco(t, pack, precio, cfg):
    filas = []
    sel = cfg['paco_macd']
    for tf in ('D', 'W', 'M'):
        for s in check_senal_paco(pack[tf], timeframe=tf):
            macd_ok = (sel == "⚪ Cualquiera" or (sel == "🟢 Alcista" and s['macd'] == 'alcista') or
                       (sel == "🔴 Bajista" and s['macd'] == 'bajista'))
            if direccion_ok(s['direccion'] == 'ALCISTA', cfg) and macd_ok:
                filas.append({"Ticker": t, "TF": TF_NOMBRE[tf], "Patrón": s['patron'], "Dirección": s['direccion'],
                              "Antigüedad": s['antiguedad'], "Stoch K": s['stoch_k'], "Vol x media": s['vol_ratio'],
                              "MACD": txt_macd(s['macd']), "Velas prev": s['contexto'], "Precio": precio,
                              **ubicacion(pack, tf, _idx_desde_texto(s['antiguedad']), s['direccion'] == 'ALCISTA')})
    return filas


def esc_emas(t, pack, precio, cfg):
    filas = []
    for tf in ('D', 'W'):
        ok, tipo = check_cruce_emas(pack[tf], velas=4)
        if ok and direccion_ok("GOLDEN" in tipo, cfg):
            filas.append({"Ticker": t, "TF": TF_NOMBRE[tf], "Señal": tipo, "Precio": precio})
    return filas


def esc_puntob(t, pack, precio, cfg):
    filas = []
    for tf in cfg['pb_tfs']:
        df_tf = pack.get(tf)
        if df_tf is None or df_tf.empty:
            continue
        ok, tipo, nivel_b, tp1, tp2, info = check_punto_b(df_tf, timeframe=tf)
        if not ok or not direccion_ok("BAJISTA" not in tipo, cfg):
            continue
        if info["estado_b"] == "✅ ROTO":
            roto = velas_a_tiempo(info["velas_ruptura"], tf) if info["velas_ruptura"] > 0 else "Hoy"
        else:
            roto = "—"
        filas.append({"Ticker": t, "TF": TF_NOMBRE[tf], "Tipo": tipo, "Estado B": info["estado_b"],
                      "Fecha A": info.get("fecha_a", "—"), "Precio A": info["precio_a"],
                      "Fecha B": info.get("fecha_b", "—"), "Nivel B": info["nivel_b"],
                      "Fecha C": info.get("fecha_c", "—"), "Precio C": info["precio_c"],
                      "TP1 (161.8%)": tp1, "TP2 (200%)": tp2,
                      "Dur. modulo": velas_a_tiempo(info["duracion_velas"], tf),
                      "Desde C": velas_a_tiempo(info["velas_desde_c"], tf),
                      "Roto hace": roto, "Precio": precio})
    return filas


# ── Cómo separar cada tabla en la pestaña de resultados ──
def _por_direccion(tit_alc, tit_baj, quitar=True):
    def f(df):
        out = []
        for valor, tit in (('ALCISTA', tit_alc), ('BAJISTA', tit_baj)):
            sub = df[df['Dirección'] == valor]
            out.append((tit, sub.drop(columns=['Dirección']) if quitar else sub))
        return out
    return f


def _por_texto(col, grupos):
    return lambda df: [(tit, df[df[col].str.contains(patron)]) for patron, tit in grupos]


def _split_puntob(df):
    t = df['Tipo']
    return [("#### 🟢 BUENA OSCILACIÓN ALCISTA — C < A", df[t.str.contains("BUENA") & ~t.str.contains("BAJISTA")]),
            ("#### 🟡 MALA OSCILACIÓN ALCISTA — C > A",  df[t.str.contains("MALA") & ~t.str.contains("BAJISTA")]),
            ("#### 🔴 BUENA OSCILACIÓN BAJISTA — C > A", df[t.str.contains("BUENA OSC. BAJISTA")]),
            ("#### 🟠 MALA OSCILACIÓN BAJISTA — C < A",  df[t.str.contains("MALA OSC. BAJISTA")])]


# ── Registro único de escáneres: nombre, sidebar, función, métricas, pestaña ──
# (clave, casilla del panel, por defecto, función, métrica, pestaña, csv, separar, mensaje si vacío)
ESCANERES = [
    ("premium", "💎 Operaciones Premium (M+W+D)", True, esc_premium, "💎 Premium", "💎 PREMIUM", "premium.csv",
     None, "Sin entradas Premium hoy. Mantener disciplina."),
    ("velas", "🕯️ Velas de Cambio (D/W/M)", True, esc_velas, "🕯️ Velas Cambio", "🕯️ VELAS CAMBIO", "velas.csv",
     _por_direccion("#### 🟢 VELAS DE CAMBIO — ALCISTAS", "#### 🔴 VELAS DE CAMBIO — BAJISTAS"),
     "Sin velas de cambio detectadas."),
    ("diverg", "📐 Divergencias MACD", False, esc_diverg, "📐 Divergencias", "📐 DIVERGENCIAS", "divergencias.csv",
     _por_texto('Tipo', [("ALCISTA", "#### 📈 ALCISTAS"), ("BAJISTA", "#### 📉 BAJISTAS")]),
     "Sin divergencias detectadas."),
    ("macd_combo", "📡 Radar MACD por Timeframe", False, esc_macd_combo, "📡 MACD Combo", "📡 MACD COMBO",
     "macd_combo.csv", lambda df: [("#### 📡 RESULTADOS RADAR MACD", df)],
     "Ningún activo cumple la combinación MACD seleccionada."),
    ("confluencia", "💥 Confluencia Div + Vela", True, esc_confluencia, "💥 Confluencia", "💥 CONFLUENCIA",
     "confluencia.csv",
     _por_texto('Dirección', [("ALCISTA", "#### 🚀 CONFLUENCIAS ALCISTAS"), ("BAJISTA", "#### 💣 CONFLUENCIAS BAJISTAS")]),
     "No se han detectado confluencias Divergencia + Vela."),
    ("emas", "📈 Cruce EMA 50/200", False, esc_emas, "📈 EMA Cross", "📈 EMA CROSS", "ema_cross.csv",
     _por_texto('Señal', [("GOLDEN", "#### ✨ GOLDEN CROSS — EMA50 cruza sobre EMA200"),
                          ("DEATH", "#### 💀 DEATH CROSS — EMA50 cruza bajo EMA200")]),
     "No se han detectado cruces de EMA50/200 recientes."),
    ("puntob", "🔵 Módulo de Arranque (Punto B)", False, esc_puntob, "🔵 Punto B", "🔵 PUNTO B", "punto_b.csv",
     _split_puntob, "No se han detectado módulos de arranque válidos."),
    ("paco", "🌟 Señal de Paco Pérez", False, esc_paco, "🌟 Paco Pérez", "🌟 PACO PÉREZ", "paco_perez.csv",
     _por_direccion("#### 🟢 SEÑALES ALCISTAS — PACO PÉREZ", "#### 🔴 SEÑALES BAJISTAS — PACO PÉREZ"),
     "Sin señales Paco Pérez detectadas. El mercado no presenta configuraciones de alta calidad ahora mismo."),
    ("macdelorean", "🚗 Velas Macdelorean (M+W+D)", False, esc_macdelorean, "🚗 Macdelorean", "🚗 MACDELOREAN",
     "macdelorean_velas.csv",
     _por_direccion("#### 🚗🟢 VELAS MACDELOREAN — BUY", "#### 🚗🔴 VELAS MACDELOREAN — SELL"),
     "Sin señales Velas Macdelorean. Espera la confluencia perfecta M+W+D."),
    ("sabroson200", "🌮 Operaciones Sabrosón 200", False, esc_sabroson200, "🌮 Sabrosón 200", "🌮 SABROSÓN 200",
     "sabroson_200.csv",
     _por_direccion("#### 🌮🟢 SABROSÓN 200 — ALCISTAS", "#### 🌮🔴 SABROSÓN 200 — BAJISTAS"),
     "Sin activos tocando la EMA 200 con los filtros MACD elegidos."),
    ("sabroson50", "🌯 Operaciones Sabrosón 50", False, esc_sabroson50, "🌯 Sabrosón 50", "🌯 SABROSÓN 50",
     "sabroson_50.csv",
     _por_direccion("#### 🌯🟢 SABROSÓN 50 — ALCISTAS", "#### 🌯🔴 SABROSÓN 50 — BAJISTAS"),
     "Sin activos tocando la EMA 50 con los filtros MACD elegidos."),
    ("conf_master", "💎 Confluencias Master", False, esc_conf_master, "💎 Conf Master", "💎 CONF MASTER",
     "confluencias_master.csv",
     _por_direccion("#### 💎🟢 CONFLUENCIAS MASTER — ALCISTAS", "#### 💎🔴 CONFLUENCIAS MASTER — BAJISTAS"),
     "Sin confluencias master. Las mejores señales llegan a quien espera."),
]
FUNCION = {e[0]: e[3] for e in ESCANERES}


# ==============================================================================
# 5. INTERFAZ — CABECERA
# ==============================================================================

LOGO = "file_000000005a5451f788bcd99cfd5924fa_conversation_id=67f55f0e-bd50-800d-be41-4cd7655690a8&message_id=2e76fcf1-1345-48c0-a4b1-738909da3a1c.PNG"

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(LOGO, use_container_width=True)

st.markdown("""
<style>
.header-line {
    width: 100%; height: 1px;
    background: linear-gradient(90deg, transparent 0%, #C9A84C 30%, #E8C96B 50%, #C9A84C 70%, transparent 100%);
    margin: 8px 0;
}
.header-diamond {
    display: inline-block; width: 6px; height: 6px;
    background: #C9A84C; transform: rotate(45deg);
    margin: 0 10px; vertical-align: middle;
}
.sb-titulo { font-family: Cinzel, serif; font-size: 0.72rem; color: #8B6914; letter-spacing: 4px;
             text-transform: uppercase; padding: 8px 0 8px 0; border-bottom: 1px solid #1A1208; }
.sb-grupo  { font-family: Share Tech Mono, monospace; color: #8B6914; font-size: 10px;
             letter-spacing: 3px; padding: 6px 0 4px 0; }
.sb-sep    { height: 12px; border-top: 1px solid #1A1208; margin-top: 10px; }
</style>
<div style="text-align:center; padding: 4px 0 8px 0;">
    <div style="margin-top:4px;">
        <span style="font-family: Cinzel, serif; font-size: 1.75rem; font-weight: 700;
                     color: #C9A84C; letter-spacing: 8px;
                     text-shadow: 0 0 40px rgba(201,168,76,0.30);">
            THE MACDELOREAN
        </span>
    </div>
    <div style="margin-top:2px;">
        <span style="font-family: Cinzel, serif; font-size: 0.78rem; font-weight: 400;
                     color: #8B6914; letter-spacing: 10px; text-transform: uppercase;">
            Investment Group
        </span>
    </div>
    <div class="header-line" style="margin: 10px auto; max-width: 480px;"></div>
    <div>
        <span class="header-diamond"></span>
        <span style="font-family: Share Tech Mono, monospace; font-size: 0.68rem;
                     color: #6B5010; letter-spacing: 5px; text-transform: uppercase;">
            Radar de Inteligencia Estructural &nbsp;&#183;&nbsp; Universo Máximo
        </span>
        <span class="header-diamond"></span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:1px; background: linear-gradient(90deg, transparent, #6B5010, transparent); margin-bottom:20px;'></div>", unsafe_allow_html=True)


def titulo_sidebar(texto):
    st.markdown(f"<div class='sb-sep'></div><div class='sb-titulo'>◆ &nbsp;{texto}</div>", unsafe_allow_html=True)


def selector_macd(titulo, prefijo):
    """Seis desplegables (estado + línea 0 para M/W/D). Devuelve {'M': (est, cer), ...}."""
    st.markdown(f"**{titulo}**")
    out = {}
    for tf, nombre in (('M', 'Mensual'), ('W', 'Semanal'), ('D', 'Diario')):
        est = st.selectbox(f"{nombre} — Estado",  OPC_ESTADO, index=0, key=f"{prefijo}_{tf.lower()}_est")
        cer = st.selectbox(f"{nombre} — Línea 0", OPC_CERO,   index=0, key=f"{prefijo}_{tf.lower()}_cer")
        out[tf] = (est, cer)
    return out


def elegir_tfs(titulo, opciones, prefijo):
    """Casillas de timeframes. opciones = [(tf, etiqueta, por_defecto), ...]."""
    st.markdown(f"**{titulo}**")
    return [tf for tf, etiqueta, defecto in opciones
            if st.checkbox(etiqueta, value=defecto, key=f"{prefijo}{tf.lower()}")]


# ==============================================================================
# 6. SIDEBAR
# ==============================================================================
with st.sidebar:
    st.image(LOGO, use_container_width=True)
    st.markdown("""
    <div style='text-align:center; padding: 4px 0 10px 0; border-bottom: 1px solid #2A1E08;'>
        <div style='font-family: Cinzel, serif; font-size: 0.8rem; color: #C9A84C; letter-spacing: 4px; font-weight:600;'>PANEL DE CONTROL</div>
        <div style='font-family: Share Tech Mono, monospace; font-size: 0.6rem; color: #6B5010; letter-spacing: 3px; margin-top:2px;'>RADAR v27.1</div>
    </div>
    """, unsafe_allow_html=True)

    titulo_sidebar("ÍNDICES A ESCANEAR")
    lista_indices = [n for grupo in REGIONES.values() for n in grupo]

    col_sel1, col_sel2 = st.columns(2)
    if col_sel1.button("✅ Todos"):
        for n in lista_indices:
            st.session_state[f"idx_{n}"] = True
    if col_sel2.button("❌ Ninguno"):
        for n in lista_indices:
            st.session_state[f"idx_{n}"] = False

    indices_seleccionados = []
    for grupo, nombres in REGIONES.items():
        if not nombres:
            continue
        st.markdown(f"<div class='sb-grupo'>{grupo}</div>", unsafe_allow_html=True)
        for nombre in nombres:
            if st.checkbox(f"{nombre} ({len(UNIVERSO[nombre])})",
                           value=st.session_state.get(f"idx_{nombre}", True), key=f"idx_{nombre}"):
                indices_seleccionados.append(nombre)

    titulo_sidebar("FILTROS DE BÚSQUEDA")
    activos = {}
    for n, (clave, etiqueta, defecto, *_ ) in enumerate(ESCANERES, start=1):
        activos[clave] = st.checkbox(etiqueta, value=defecto, key=f"f{n}")

    # Opciones extra de cada escáner (solo aparecen si está activado)
    cfg = {'vc_tfs': [], 'vc_macd': SIN_FILTRO, 's200_macd': SIN_FILTRO, 's50_macd': SIN_FILTRO,
           'pb_tfs': [], 'paco_macd': "⚪ Cualquiera", 'div_macd': SIN_FILTRO, 'combo_macd': SIN_FILTRO}
    if activos['velas']:
        cfg['vc_tfs'] = elegir_tfs("Timeframes Velas de Cambio:",
                                   [('M', "Mensual", True), ('W', "Semanal", True), ('D', "Diario", False)], "vc_")
        cfg['vc_macd'] = selector_macd("MACD — Velas de Cambio:", "vc_macd")
    if activos['sabroson200']:
        cfg['s200_macd'] = selector_macd("MACD — Sabrosón 200:", "s200")
    if activos['sabroson50']:
        cfg['s50_macd'] = selector_macd("MACD — Sabrosón 50:", "s50")
    if activos['puntob']:
        cfg['pb_tfs'] = elegir_tfs("Timeframes Punto B:",
                                   [('4H', "4H", False), ('D', "Diario", True), ('W', "Semanal", True),
                                    ('M', "Mensual", False)], "pb")
    if activos['paco']:
        st.markdown("**MACD — Señal Paco Pérez:**")
        cfg['paco_macd'] = st.selectbox("Estado MACD", OPC_ESTADO, index=0, key="paco_macd")
    if activos['diverg'] or activos['confluencia'] or activos['conf_master']:
        cfg['div_macd'] = selector_macd("MACD — Divergencias / Confluencias:", "div")
    if activos['macd_combo']:
        cfg['combo_macd'] = selector_macd("Estado MACD — selecciona cada TF:", "combo")

    titulo_sidebar("DIRECCIÓN")
    cfg['dir_alc'] = st.checkbox("🟢 Alcistas", value=True, key="dir1")
    cfg['dir_baj'] = st.checkbox("🔴 Bajistas", value=True, key="dir2")
    solo_cerradas = st.checkbox("🔒 Solo velas cerradas (W/M)", value=False, key="solo_cerradas",
                                help="Ignora la semana y el mes en curso: menos señales, pero no repintan.")

    st.markdown("---")
    total_tickers = len(set(t for n in indices_seleccionados for t in UNIVERSO[n]))
    seg_est = total_tickers * 0.15
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0F0D08 0%, #181208 100%);
                border: 1px solid #3A2A0A; border-radius: 2px;
                padding: 16px 12px; text-align:center; margin-top:14px;
                box-shadow: inset 0 0 30px rgba(201,168,76,0.04);'>
        <div style='font-family: Cinzel, serif; color: #6B5010; font-size: 9px; letter-spacing: 5px; margin-bottom:8px;'>OBJETIVOS SELECCIONADOS</div>
        <div style='font-family: Share Tech Mono, monospace; color: #C9A84C; font-size: 2.2rem; font-weight:700; line-height:1; text-shadow: 0 0 20px rgba(201,168,76,0.3);'>{total_tickers}</div>
        <div style='height:1px; background: linear-gradient(90deg, transparent, #3A2A0A, transparent); margin: 8px 0;'></div>
        <div style='font-family: Share Tech Mono, monospace; color: #6B5010; font-size: 10px; letter-spacing: 2px;'>⏱ EST. {int(seg_est // 60)}m {int(seg_est % 60)}s</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    lanzar = st.button("◆  LANZAR RADAR  ◆")

    # Escaneo a medias (móvil bloqueado, pestaña cerrada...): se puede retomar
    pendiente = MEMORIA.get('escaneo')
    continuar = False
    if pendiente and not pendiente['completo']:
        hechos, total = pendiente['hechos'], len(pendiente['master_list'])
        st.caption(f"⏸️ Hay un escaneo interrumpido del {pendiente['hora']} ({hechos}/{total}). "
                   "Se retoma con los filtros de entonces.")
        continuar = st.button(f"▶️  CONTINUAR ESCANEO  ({hechos}/{total})")


# ==============================================================================
# 7. EJECUCIÓN
# ==============================================================================
if lanzar or continuar:
    if continuar and not lanzar:
        esc = pendiente                                   # retoma el escaneo guardado
    else:
        if not indices_seleccionados:
            st.error("⚠️ Selecciona al menos un índice.")
            st.stop()
        if not any(activos.values()):
            st.error("⚠️ Activa al menos un filtro de búsqueda.")
            st.stop()
        esc = {'master_list': list(dict.fromkeys(t for n in indices_seleccionados for t in UNIVERSO[n])),
               'n_indices': len(indices_seleccionados), 'activos': dict(activos), 'cfg': cfg,
               'solo_cerradas': solo_cerradas, 'hora': time.strftime('%d/%m/%Y %H:%M'),
               'resultados': {clave: [] for clave, *_ in ESCANERES}, 'fallos': [],
               'hechos': 0, 'completo': False}
        MEMORIA['escaneo'] = esc

    master_list, activos, cfg = esc['master_list'], esc['activos'], esc['cfg']
    resultados, fallos, inicio = esc['resultados'], esc['fallos'], esc['hechos']
    claves_activas = [clave for clave, act in activos.items() if act]
    st.success(f"📡 **{len(master_list)} OBJETIVOS** · **{esc['n_indices']} ÍNDICES** — "
               + (f"CONTINUANDO DESDE {inicio}..." if inicio else "ESCANEO EN PROCESO..."))

    progress_bar = st.progress(inicio / len(master_list))
    status_text  = st.empty()
    vivos        = [(clave, ph) for clave, ph in zip(['premium', 'velas', 'diverg'], st.columns(3))]
    vivos        = [(clave, ph.empty()) for clave, ph in vivos if activos[clave]]

    TAM_LOTE   = 50
    n_lotes    = (len(master_list) + TAM_LOTE - 1) // TAM_LOTE
    datos_lote = {}
    incluir_4h = activos['puntob'] and '4H' in cfg['pb_tfs']

    for i in range(inicio, len(master_list)):
        ticker = master_list[i]
        if i % TAM_LOTE == 0 or i == inicio:
            fin_lote = (i // TAM_LOTE + 1) * TAM_LOTE
            status_text.text(f"📥 Descargando lote {i // TAM_LOTE + 1}/{n_lotes}...")
            datos_lote = descargar_lote(master_list[i:fin_lote])
        progress_bar.progress((i + 1) / len(master_list))
        status_text.text(f"🔎 {ticker}  [{i + 1}/{len(master_list)}]")

        pack = procesar_datos(ticker, incluir_4h=incluir_4h,
                              df_diario=datos_lote.get(ticker), solo_cerradas=esc['solo_cerradas'])
        if pack is None:
            fallos.append(ticker)
            esc['hechos'] = i + 1
            continue
        precio = round(float(pack['D'].iloc[-1]['Close']), 2)

        # Se calcula todo el ticker y se guarda de golpe: si se corta a mitad, no quedan filas duplicadas
        nuevas = {clave: FUNCION[clave](ticker, pack, precio, cfg) for clave in claves_activas}
        for clave, filas in nuevas.items():
            resultados[clave].extend(filas)
        esc['hechos'] = i + 1
        for clave_v, ph in vivos:
            if nuevas.get(clave_v):
                ph.dataframe(pd.DataFrame(resultados[clave_v]), use_container_width=True)

    esc['completo'] = True
    for _, ph in vivos:
        ph.empty()
    progress_bar.empty()
    status_text.success("✅ ESCANEO COMPLETADO.")
    st.balloons()

    # Guardar en sesión → pulsar "Exportar CSV" no borra el escaneo
    st.session_state['radar'] = {
        'hora':         esc['hora'],
        'n_escaneados': len(master_list),
        'fallos':       fallos,
        'res':          resultados,
        'activos':      dict(activos),
    }

# Si el escaneo terminó mientras el móvil estaba bloqueado, sus resultados aparecen al volver
elif not st.session_state.get('radar') and pendiente and pendiente['completo']:
    st.session_state['radar'] = {'hora': pendiente['hora'], 'n_escaneados': len(pendiente['master_list']),
                                 'fallos': pendiente['fallos'], 'res': pendiente['resultados'],
                                 'activos': pendiente['activos']}


# ==============================================================================
# 8. RESULTADOS
# ==============================================================================
if st.session_state.get('radar'):
    _R = st.session_state['radar']
    res, act = _R['res'], _R['activos']

    st.caption(f"📅 Resultados del escaneo del {_R['hora']} · {_R['n_escaneados']} tickers")
    if _R['fallos']:
        with st.expander(f"⚠️ {len(_R['fallos'])} tickers sin datos (dejaron de cotizar o cambiaron de símbolo)"):
            st.write(", ".join(_R['fallos']))

    st.markdown("---")
    metricas = [("🎯 Escaneados", _R['n_escaneados'])] + [(e[4], len(res[e[0]])) for e in ESCANERES]
    columnas = list(st.columns(7)) + list(st.columns(6))
    for col, (etiqueta, valor) in zip(columnas, metricas):
        col.metric(etiqueta, valor)
    st.markdown("---")

    mostrados = [e for e in ESCANERES if act.get(e[0])]
    tabs = st.tabs([f"{e[5]} ({len(res[e[0]])})" for e in mostrados])
    for tab, (clave, _, _, _, _, _, csv, separar, vacio) in zip(tabs, mostrados):
        with tab:
            if not res[clave]:
                (st.warning if clave == 'premium' else st.info)(vacio)
                continue
            df_out = pd.DataFrame(res[clave])
            if '⭐' in df_out.columns:                     # las mejor ubicadas, arriba
                df_out = df_out.iloc[df_out['⭐'].str.len().sort_values(ascending=False, kind='stable').index]
            if separar is None:
                st.dataframe(df_out, use_container_width=True)
            else:
                for titulo, sub in separar(df_out):
                    if not sub.empty:
                        st.markdown(titulo)
                        st.dataframe(sub, use_container_width=True)
            st.download_button("⬇️ Exportar CSV", df_out.to_csv(index=False).encode(), csv, "text/csv",
                               key=f"csv_{clave}")

else:
    st.markdown("<br>", unsafe_allow_html=True)
    n_unicos = len(set(t for v in UNIVERSO.values() for t in v))
    stats = [("📊", "ÍNDICES", f"{len(UNIVERSO)} mercados"),
             ("🎯", "TICKERS", f"~{n_unicos} activos"),
             ("🌍", "COBERTURA", "USA · EU · UK · JP · CN"),
             ("⚡", "ETFs", "Sectores · Temáticos · Apalancados")]
    for col, (icon, label, val) in zip(st.columns(4), stats):
        col.markdown(f"""
        <div style='background: linear-gradient(160deg, #111008 0%, #0D0C08 100%);
                    border: 1px solid #2A1E08; border-top: 1px solid #3A2A0A;
                    border-radius: 2px; padding:20px 12px; text-align:center;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.5), inset 0 1px 0 rgba(201,168,76,0.08);'>
            <div style='font-size:1.5rem; margin-bottom:8px; opacity:0.7;'>{icon}</div>
            <div style='font-family: Cinzel, serif; color: #8B6914; font-size: 8px;
                        letter-spacing: 4px; margin-bottom:6px; text-transform:uppercase;'>{label}</div>
            <div style='font-family: Share Tech Mono, monospace; color: #C9A84C;
                        font-size: 13px; letter-spacing: 1px;'>{val}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    bloques = [
        ("💎 PREMIUM", "Confluencia M + W + D\nMACD estricto multi-timeframe\n+ Vela de engaño semanal"),
        ("🕯️ VELAS ENGAÑO", "Barrido de mínimos/máximos\nRecuperación > 50% vela\nEstocástico extremo (<20 / >80)"),
        ("📐 DIVERGENCIAS", "Precio vs Momentum MACD\nSwings reales del MACD\nDisponible en D / W / M")]
    for col, (titulo, desc) in zip(st.columns(3), bloques):
        col.markdown(f"""
        <div style='background: linear-gradient(160deg, #0F0D08 0%, #0A0908 100%);
                    border: 1px solid #1A1208; border-left: 2px solid #3A2A0A;
                    border-radius: 2px; padding:18px 16px;
                    box-shadow: 0 2px 12px rgba(0,0,0,0.4);'>
            <div style='font-family: Cinzel, serif; color: #C9A84C; font-size: 11px;
                        margin-bottom:12px; letter-spacing: 3px; text-transform:uppercase;
                        padding-bottom: 8px; border-bottom: 1px solid #1A1208;'>{titulo}</div>
            <div style='font-family: Share Tech Mono, monospace; color: #6B5010; font-size: 11px;
                        line-height: 2.0; white-space: pre-line; letter-spacing: 0.5px;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; padding: 30px 0 10px 0;'>
        <span style='font-family: Cinzel, serif; color: #3A2A0A; font-size: 10px; letter-spacing: 5px;'>
            SELECCIONA ÍNDICES · ACTIVA FILTROS · LANZA EL RADAR
        </span>
    </div>
    """, unsafe_allow_html=True)
