import streamlit as st
import yfinance as yf
import pandas as pd
# pandas_ta eliminado — cálculos manuales
import numpy as np
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Macdelorean Radar v24",
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
# 1. UNIVERSO MASIVO DE ACTIVOS — ~1400 TICKERS
# ==============================================================================

UNIVERSO = {

    # ──────────────────────────────────────────────
    "🇺🇸 DOW JONES 30": [
        "MMM","AXP","AMGN","AAPL","BA","CAT","CVX","CSCO","KO","DIS",
        "DOW","GS","HD","HON","IBM","INTC","JNJ","JPM","MCD","MRK",
        "MSFT","NKE","PG","CRM","TRV","UNH","VZ","V","WMT","AMZN"
    ],

    # ──────────────────────────────────────────────
    "🚀 NASDAQ 100 COMPLETO": [
        "AAPL","MSFT","NVDA","AMZN","META","TSLA","GOOGL","GOOG","AVGO","COST",
        "NFLX","TMUS","AMD","CSCO","ADBE","PEP","AZN","QCOM","TXN","ISRG",
        "INTU","AMAT","HON","CMCSA","BKNG","VRTX","REGN","MU","PANW","ADI",
        "LRCX","KLAC","SNPS","CDNS","MELI","ASML","MDLZ","GILD","CTAS","ADP",
        "FTNT","MAR","ABNB","MCHP","ORLY","KDP","DXCM","WDAY","PAYX","MNST",
        "ROST","BIIB","IDXX","PCAR","EA","FAST","CTSH","ODFL","VRSK","CEG",
        "DDOG","ZS","CRWD","TEAM","NXPI","EXC","AEP","XEL","ILMN","ON",
        "GEHC","TTWO","SBUX","PDD","ALGN","ENPH","WBD","FANG","DLTR","SIRI",
        "ZM","EBAY","PYPL","LCID","RIVN","HOOD","COIN","MARA","RIOT","LULU",
        "CHTR","BKR","CSX","FISV","ANSS","CPRT","CSGP","DKNG","GFS","HTHT"
    ],

    # ──────────────────────────────────────────────
    "📈 S&P 500 — FINANCIALS & INDUSTRIALS": [
        "JPM","BAC","WFC","GS","MS","C","BK","USB","PNC","TFC",
        "COF","AXP","DFS","SYF","ALLY","FITB","KEY","RF","HBAN","CFG",
        "MTB","ZION","CMA","PBCT","FHN","SIVB","SBNY","WAL","EWBC","PACW",
        "BLK","SCHW","TROW","IVZ","BEN","AMG","APAM","VRTS","SEIC","FDS",
        "ICE","CME","CBOE","NDAQ","MKTX","VIRT","LPLA","RJF","SF","PIPR",
        "MMC","AON","AJG","WTW","HIG","MET","PRU","AFL","ALL","TRV",
        "CB","AIG","PGR","CINF","GL","LNC","UNM","PFG","AIZ","EG",
        "GE","HON","MMM","CAT","DE","EMR","ETN","PH","ROK","AME",
        "ITW","DOV","GGG","GNRC","XYL","REXNORD","FLS","IDEX","IR","TT",
        "CARR","OTIS","RTX","LMT","NOC","GD","LHX","BAH","LDOS","SAIC"
    ],

    # ──────────────────────────────────────────────
    "📈 S&P 500 — HEALTHCARE & CONSUMER": [
        "UNH","CVS","CI","HUM","CNC","MOH","ELV","WCG","OSH","ALHC",
        "JNJ","PFE","ABT","MRK","LLY","BMY","GILD","AMGN","REGN","VRTX",
        "BIIB","ALNY","MRNA","BNTX","SGEN","EXAS","ILMN","PACB","TDOC","ONEM",
        "TMO","DHR","A","WAT","MTD","PKI","IQV","CTLT","CRL","MEDP",
        "MDT","SYK","BSX","EW","DXCM","RMD","HOLX","ZBH","BDX","COO",
        "AMZN","WMT","COST","TGT","HD","LOW","TJX","ROST","BURL","FIVE",
        "MCD","SBUX","YUM","QSR","DPZ","CMG","WING","SHAK","JACK","DENN",
        "NKE","LULU","VFC","PVH","HBI","UA","SKX","CROX","DECK","WWW",
        "PG","KO","PEP","MDLZ","GIS","CPB","CAG","SJM","HRL","MKC",
        "PM","MO","BTI","MNST","KDP","CELH","FIZZ","SAM","BF-B","TAP"
    ],

    # ──────────────────────────────────────────────
    "📈 S&P 500 — ENERGY & UTILITIES": [
        "XOM","CVX","COP","EOG","PXD","DVN","MRO","APA","HES","FANG",
        "SLB","HAL","BKR","OIS","OIH","NOV","DRQ","HP","NE","PTEN",
        "VLO","MPC","PSX","DK","PBF","HFC","CLMT","PARR","CALUMET","ALJ",
        "KMI","WMB","ET","EPD","MPLX","PAA","TRGP","OKE","LNG","FLEX",
        "DUK","SO","NEE","AEP","EXC","XEL","D","SRE","PEG","ED",
        "WEC","ES","ETR","CNP","CMS","LNT","PNW","OGE","NI","EVRG",
        "NRG","VST","CEG","AES","BEP","CWEN","AMPS","NOVA","RUN","SEDG",
        "ENPH","FSLR","SPWR","CSIQ","JKS","DAQO","RUN","ARRY","NOVA","SHLS"
    ],

    # ──────────────────────────────────────────────
    "📈 S&P 500 — TECH & REITS": [
        "AAPL","MSFT","NVDA","GOOGL","META","TSLA","AVGO","ORCL","IBM","QCOM",
        "TXN","ADI","MCHP","LRCX","AMAT","KLAC","SNPS","CDNS","ANSS","EPAM",
        "PAYC","PCTY","HUBS","DOMO","COUP","VEEV","OKTA","ZI","BOX","DBX",
        "TWLO","BAND","EGHT","MSGM","CCCS","ALKT","JAMF","DOCU","SMAR","MNDY",
        "AMT","CCI","SBAC","UNIT","LAMR","OUT","DLR","EQIX","QTS","CONE",
        "O","WPC","NNN","STOR","VICI","GLPI","MGP","EPR","SPG","MAC",
        "EQR","AVB","ESS","UDR","AIV","MAA","CPT","INVH","AMH","SUI",
        "ELS","PSA","EXR","CUBE","LSI","NSA","COLD","STAG","ADC","TRNO"
    ],

    # ──────────────────────────────────────────────
    "🇩🇪 DAX 40 COMPLETO": [
        "SAP.DE","SIE.DE","AIR.DE","ALV.DE","DTE.DE","MBG.DE","VOW3.DE",
        "BMW.DE","BAS.DE","ADS.DE","IFX.DE","DHL.DE","MUV2.DE","DB1.DE",
        "BEI.DE","RWE.DE","EOAN.DE","SY1.DE","BAYN.DE","DTG.DE","HEN3.DE",
        "VNA.DE","CON.DE","PAH3.DE","MTX.DE","HEI.DE","MRK.DE","BNR.DE",
        "HNR1.DE","ZAL.DE","FRE.DE","FME.DE","QIA.DE","PUM.DE","SHL.DE",
        "ENR.DE","EVT.DE","1COV.DE","SON22.DE","SXS.DE"
    ],

    # ──────────────────────────────────────────────
    "🇩🇪 MDAX ALEMANIA (Mid Caps)": [
        "AIXA.DE","AFX.DE","BNR.DE","BOSS.DE","COP.DE","EVK.DE","FPE3.DE",
        "G1A.DE","GXI.DE","HAG.DE","HHFA.DE","HOT.DE","IFX.DE","JEN.DE",
        "K+S.DE","KGX.DE","KSB3.DE","LEG.DE","LHA.DE","MBB.DE","MDG1.DE",
        "MRCG.DE","NDX1.DE","NEM.DE","O2D.DE","PSM.DE","RAA.DE","RSL2.DE",
        "S92.DE","SDF.DE","SDAX.DE","SGL.DE","SMHN.DE","ST5.DE","STO3.DE",
        "SY1.DE","TKA.DE","TUI1.DE","VBK.DE","WAF.DE","WCH.DE","WIN.DE"
    ],

    # ──────────────────────────────────────────────
    "🇪🇸 IBEX 35 COMPLETO": [
        "ITX.MC","IBE.MC","BBVA.MC","SAN.MC","CABK.MC","TEF.MC","ACS.MC",
        "FER.MC","AENA.MC","AMS.MC","REP.MC","CLNX.MC","IAG.MC","ENG.MC",
        "ANA.MC","GRF.MC","RED.MC","MTS.MC","ACX.MC","BKT.MC","MAP.MC",
        "TL5.MC","MEL.MC","PHM.MC","SAB.MC","IDR.MC","COL.MC","LOG.MC",
        "FDR.MC","ROVI.MC","SOL.MC","UNI.MC","VIS.MC","ELE.MC","CIE.MC"
    ],

    # ──────────────────────────────────────────────
    "🇪🇸 BME GROWTH (Small Caps España)": [
        "OHLA.MC","MDF.MC","CASH.MC","ERIZ.MC","CLNX.MC","ENAV.MC",
        "ALNT.MC","BAIN.MC","DGRN.MC","ECR.MC","ELEX.MC","FLUI.MC",
        "HERN.MC","HGT.MC","LABE.MC","LFDS.MC","MDLN.MC","MEHR.MC",
        "MENT.MC","MXOC.MC","MYMD.MC","NMAS.MC","NRGY.MC","NTGY.MC",
        "OHLA.MC","ORYC.MC","PBIT.MC","PCAS.MC","PRTC.MC","RLIA.MC"
    ],

    # ──────────────────────────────────────────────
    "🇫🇷 CAC 40 COMPLETO": [
        "MC.PA","OR.PA","RMS.PA","TTE.PA","SAN.PA","AIR.PA","SU.PA",
        "BNP.PA","SAF.PA","EL.PA","AXA.PA","DG.PA","KER.PA","DSY.PA",
        "STLAP.PA","RI.PA","CAP.PA","GLE.PA","ORA.PA","BN.PA","EN.PA",
        "LR.PA","ACA.PA","CA.PA","ML.PA","VIE.PA","SGO.PA","HO.PA",
        "ATO.PA","PUB.PA","WLN.PA","URW.PA","RNO.PA","VIV.PA","ENGI.PA",
        "STM.PA","TEP.PA","BOL.PA","ERF.PA","AF.PA"
    ],

    # ──────────────────────────────────────────────
    "🇫🇷 SBF 120 FRANCIA (Mid Caps)": [
        "ABCA.PA","ALSTOM.PA","AMUN.PA","APAM.PA","ATOS.PA","BIC.PA",
        "BIGBEN.PA","BIM.PA","BNB.PA","CHSR.PA","CNP.PA","COFA.PA",
        "DBG.PA","DEC.PA","FNAC.PA","GAM.PA","GTT.PA","HLO.PA",
        "IDP.PA","ILD.PA","IMVD.PA","INEA.PA","IPSO.PA","JCDECAUX.PA",
        "KOF.PA","LACR.PA","LDL.PA","LI.PA","LOUP.PA","MANU.PA",
        "MCPHY.PA","MEDCL.PA","MF.PA","MGDYN.PA","NEXANS.PA","NXI.PA",
        "OPM.PA","OREGE.PA","PKGD.PA","PLXS.PA","RBAL.PA","REMY.PA",
        "SAFT.PA","SBMO.PA","SCOR.PA","SEB.PA","SESG.PA","SPIE.PA","TITAN.PA"
    ],

    # ──────────────────────────────────────────────
    "🇬🇧 FTSE 100 COMPLETO": [
        "SHEL.L","AZN.L","HSBA.L","ULVR.L","BP.L","GSK.L","RIO.L",
        "DGE.L","BHP.L","REL.L","NG.L","BATS.L","VOD.L","LLOY.L",
        "NWG.L","BARC.L","PRU.L","LGEN.L","AV.L","STAN.L","ABF.L",
        "ANTO.L","AUTO.L","BA.L","BNZL.L","BT-A.L","CCH.L","CPG.L",
        "CNA.L","CRDA.L","DCC.L","DPH.L","EZJ.L","FERG.L","FLTR.L",
        "GLEN.L","HLMA.L","HL.L","IHG.L","IMB.L","ITV.L","JD.L",
        "KGF.L","LAND.L","MNG.L","MRO.L","NXT.L","OCDO.L","PSN.L",
        "PSON.L","RKT.L","RR.L","RS1.L","SGE.L","SMDS.L","SMIN.L",
        "SKG.L","SPX.L","SSE.L","SBRY.L","SVT.L","TSCO.L","WPP.L",
        "WTB.L","UU.L","TUI.L","AAL.L","ADM.L","AGK.L","ANTO.L",
        "AHT.L","BME.L","BOO.L","BRBY.L","BVS.L","CCC.L","CLDN.L",
        "CNE.L","COB.L","CYBG.L","DARK.L","DLN.L","ECM.L","ENT.L",
        "EXPN.L","FCIT.L","FRES.L","GRG.L","HIK.L","HWDN.L","ICG.L",
        "III.L","IMI.L","INF.L","ITRK.L","JET.L","JET2.L","JMAT.L",
        "JUST.L","LSEG.L","LMP.L","MNDI.L","MONY.L","MTRO.L","MUT.L"
    ],

    # ──────────────────────────────────────────────
    "🌍 EUROSTOXX 50": [
        "ASML.AS","ADYEN.AS","INGA.AS","PHIA.AS","HEIA.AS","NN.AS","RAND.AS","WKL.AS","ABN.AS","UMG.AS",
        "SAP.DE","SIE.DE","ALV.DE","MBG.DE","BMW.DE","BAYN.DE","ADS.DE","BAS.DE","MUV2.DE","DTE.DE",
        "MC.PA","OR.PA","TTE.PA","SAN.PA","BNP.PA","AIR.PA","SU.PA","AXA.PA","EL.PA","DG.PA",
        "ITX.MC","BBVA.MC","SAN.MC","IBE.MC","REP.MC",
        "ENI.MI","ISP.MI","UCG.MI","ENEL.MI","TIT.MI",
        "NESN.SW","ROG.SW","NOVN.SW",
        "NOKIA.HE","NESTE.HE"
    ],

    # ──────────────────────────────────────────────
    "🇮🇹 FTSE MIB ITALIA": [
        "ENI.MI","ISP.MI","UCG.MI","ENEL.MI","TIT.MI","G.MI","MB.MI",
        "RACE.MI","LDO.MI","STM.MI","PRY.MI","BAMI.MI","MONC.MI","SRG.MI",
        "PST.MI","ORN.MI","ERG.MI","BMPS.MI","CPR.MI","FCA.MI","STLAM.MI",
        "CNH.MI","A2A.MI","AMP.MI","AZM.MI","BMED.MI","BC.MI","BZU.MI",
        "CRDI.MI","DIA.MI","DIG.MI","EXO.MI","FILA.MI","FNM.MI","GEO.MI",
        "IVG.MI","MFB.MI","MFEA.MI","MG.MI"
    ],

    # ──────────────────────────────────────────────
    "🇯🇵 NIKKEI 225 (ADRs disponibles en USA)": [
        "TM","HMC","SONY","NTT","NTDOY","FUJIY","KYOCY","MUFG","SMFG","MFG",
        "IX","KB","SHI","FANUY","HTHIY","ISUZY","KDDIY","KYCCF","MARUY","MSBHY",
        "NIDEC","NIPNF","NPSNY","NSANY","OTSKY","PCRFY","RICOY","SEKEY","SFUN","SGIOY",
        "SHCAY","SHNNY","SIEGY","SKLTY","SSDOY","SSUNY","STITF","STSFY","SVNDY","TCEHY",
        "TKHVY","TKOMY","TMSNY","TNABY","TOELY","TRHCY","TRYIY","TTDKY","TWTDY","TYEKF"
    ],

    # ──────────────────────────────────────────────
    "⚡ ETFs USA — SECTORES": [
        "XLK","XLF","XLV","XLE","XLC","XLY","XLP","XLI","XLB","XLRE","XLU",
        "VGT","VFH","VHT","VDE","VOX","VCR","VDC","VIS","VAW","VNQ","IDU",
        "FNCL","FHLC","FENY","FCOM","FDIS","FSTA","FIDU","FMAT","FREL","FUTY"
    ],

    # ──────────────────────────────────────────────
    "⚡ ETFs USA — ÍNDICES AMPLIOS": [
        "SPY","QQQ","DIA","IWM","VTI","VOO","IVV","RSP","MDY","IJR",
        "VTV","VUG","MTUM","QUAL","VLUE","SIZE","USMV","SPHQ","SPLV","SPHB",
        "ARKK","ARKQ","ARKW","ARKG","ARKF","ARKX","PRNT","IZRL","ARKB","CTRU"
    ],

    # ──────────────────────────────────────────────
    "⚡ ETFs INTERNACIONALES": [
        "EWZ","EEM","EFA","VEA","IEFA","VWO","IEMG","FXI","MCHI","KWEB",
        "EWJ","EWY","EWT","EWA","EWC","EWG","EWQ","EWI","EWP","EWU",
        "EWH","EWS","EWM","EWN","EWD","EWL","EWO","EWK","EZU","HEDJ",
        "DBJP","DBEF","DBEU","HEFA","DXJ","HEWJ","HEZU","HSCZ","FLKR","FLJP"
    ],

    # ──────────────────────────────────────────────
    "⚡ ETFs TEMÁTICOS & APALANCADOS": [
        "SMH","SOXX","XBI","TAN","ICLN","PBW","LIT","URA","REMX","COPX",
        "BOTZ","ROBO","IRBO","AIQ","WCLD","CLOU","BUG","HACK","CIBR","IHAK",
        "SQQQ","TQQQ","SPXU","UPRO","SPXS","SDOW","UDOW","LABD","LABU","UVXY",
        "VXX","SVXY","VIXY","UVIX","SVOL","ZIVB","VIXM","VXZ","VIIX","TVIX",
        "GLD","SLV","IAU","SGOL","PHYS","PSLV","PPLT","PALL","GDX","GDXJ",
        "SIL","SILJ","NUGT","DUST","JNUG","JDST","RING","GOAU","SGDM","SGDJ",
        "USO","UNG","BNO","DBO","BOIL","KOLD","UGA","CORN","WEAT","SOYB",
        "TLT","IEF","SHY","HYG","LQD","JNK","BNDX","EMB","PCY","BWX",
        "MSTR","COIN","MARA","RIOT","CLSK","HUT","BTBT","CIFR","CORZ","WULF"
    ],

    # ──────────────────────────────────────────────
    "🎯 GROWTH & DISRUPTIVAS USA": [
        "NVDA","AMD","PLTR","CRWD","DDOG","ZS","NET","SNOW","OKTA","TWLO",
        "BILL","GTLB","HUBS","CFLT","MDB","ESTC","DOMO","APPN","ALTR","PEGA",
        "NOW","WDAY","VEEV","COUP","PCTY","PAYC","RNG","SMAR","MNDY","JAMF",
        "DOCU","BOX","DBX","DRCT","FIVN","NICE","FOUR","BRZE","AMPL","ASAN",
        "IONQ","RGTI","QUBT","QBTS","IBM","MSFT","GOOGL","ORCL","ADBE","CRM",
        "UBER","LYFT","ABNB","DASH","GRUB","CART","TOST","PAR","SHAK","NURO",
        "TSLA","LCID","RIVN","FSR","GOEV","WKHS","SOLO","AYRO","NKLA","HYLN",
        "JOBY","ACHR","LILM","EVTOL","AAL","UAL","DAL","LUV","ALK","SAVE"
    ],

    # ──────────────────────────────────────────────
    "🎯 SMALL CAPS & ESPECULATIVOS USA": [
        "SOFI","AFRM","HOOD","DKNG","GME","AMC","TLRY","SNDL","ACB","HEXO",
        "CRON","OGI","VEXT","TPVG","IIPR","MSOS","YOLO","MJ","THCX","CNBS",
        "UPST","AI","SAVA","OPEN","SPCE","QS","NKLA","RIDE","XL","ATLIS",
        "CVNA","CROX","ELF","CELH","HIMS","ACMR","LAZR","LIDR","INVZ","OUST",
        "MVIS","VUZI","KOPN","KTOS","AVAV","RKLB","MNTS","ASTS","LUNR","RDW",
        "OXY","HAL","SLB","APA","DVN","MRO","HES","COP","EOG","FANG",
        "VLO","MPC","PSX","DK","PBF","KMI","WMB","ET","EPD","MPLX",
        "AGNC","NLY","STWD","BXMT","ABR","RC","GPMT","KREF","LADR","TRTX",
        "O","WPC","NNN","VICI","GLPI","STOR","ADC","EPR","SRC","PINE"
    ],

    # ──────────────────────────────────────────────
    "💎 MEGA CAPS GLOBALES": [
        "AAPL","MSFT","NVDA","GOOGL","AMZN","META","TSLA","AVGO","LLY","V",
        "UNH","JPM","XOM","MA","JNJ","WMT","PG","HD","MRK","CVX",
        "ABBV","KO","BAC","PEP","COST","TMO","CRM","ACN","MCD","CSCO",
        "ABT","ORCL","ADBE","NKE","TXN","DHR","NEE","LIN","PM","RTX",
        "NESN.SW","ROG.SW","NOVN.SW","SHEL.L","AZN.L","HSBA.L","BP.L","GSK.L",
        "MC.PA","OR.PA","ASML.AS","SAP.DE","SIE.DE","ALV.DE","TM","SONY","MUFG"
    ],
}


# ==============================================================================
# 2. INTELIGENCIA TÉCNICA (sin cambios respecto a v23)
# ==============================================================================

def procesar_datos(ticker, incluir_4h=False):
    try:
        df_d = yf.download(ticker, period="1y",  interval="1d",  progress=False, auto_adjust=True)
        df_w = yf.download(ticker, period="3y",  interval="1wk", progress=False, auto_adjust=True)
        df_m = yf.download(ticker, period="5y",  interval="1mo", progress=False, auto_adjust=True)

        if df_d.empty or df_w.empty or df_m.empty:
            return None

        if isinstance(df_d.columns, pd.MultiIndex): df_d = df_d.xs(ticker, axis=1, level=1)
        if isinstance(df_w.columns, pd.MultiIndex): df_w = df_w.xs(ticker, axis=1, level=1)
        if isinstance(df_m.columns, pd.MultiIndex): df_m = df_m.xs(ticker, axis=1, level=1)

        dfs = [df_d, df_w, df_m]

        # 4h solo si se necesita (evita peticiones extra innecesarias)
        df_4h = pd.DataFrame()
        if incluir_4h:
            try:
                df_4h = yf.download(ticker, period="60d", interval="1h", progress=False, auto_adjust=True)
                if isinstance(df_4h.columns, pd.MultiIndex): df_4h = df_4h.xs(ticker, axis=1, level=1)
                # Resamplear 1h a 4h
                df_4h = df_4h.resample('4h').agg({
                    'Open': 'first', 'High': 'max', 'Low': 'min',
                    'Close': 'last', 'Volume': 'sum'
                }).dropna()
                dfs.append(df_4h)
            except:
                df_4h = pd.DataFrame()

        for df in dfs:
            if df.empty: continue
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

        return {'D': df_d, 'W': df_w, 'M': df_m, '4H': df_4h}
    except:
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
                        if h_win.iloc[k_idx] <= nivel_b:
                            velas_tras_ruptura = nw - k_idx
                            break
                    if velas_tras_ruptura > 5:
                        continue
                    if precio_actual <= tp1:
                        continue
                    precio_maximo_tras_b = max(h_win.iloc[ic+1:].values) if ic+1 < nw else precio_actual
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

    # ── DIVERGENCIA ALCISTA ──
    # Precio hace mínimos más bajos (Low) y MACD hace mínimos más altos
    mins = encontrar_swings(macd_serie, es_minimo=True, min_dist=min_swing_sep)
    mins_validos = [i for i in mins if macd_serie.iloc[i] < -umbral_0]

    if len(mins_validos) >= 2:
        p1, p2 = mins_validos[-2], mins_validos[-1]
        if (p2 - p1) >= min_velas:
            precio_min_p1 = min_precio_zona(p1)
            precio_min_p2 = min_precio_zona(p2)
            # Divergencia real: precio hace mínimo MÁS BAJO, MACD hace mínimo MÁS ALTO
            if precio_min_p2 < precio_min_p1 and macd_serie.iloc[p2] > macd_serie.iloc[p1]:
                fuerza = round(abs(macd_serie.iloc[p2] - macd_serie.iloc[p1]) / rango_macd * 100, 1)
                # Filtro mínimo de fuerza — divergencias débiles son ruido
                if fuerza < 10.0:
                    return False, "", "", ""
                duracion   = formatear_duracion(p2 - p1, timeframe)
                antiguedad = formatear_antiguedad(p2, total, timeframe)
                return True, f"DIV ALCISTA 📈 ({fuerza}%)", duracion, antiguedad

    # ── DIVERGENCIA BAJISTA ──
    # Precio hace máximos más altos (High) y MACD hace máximos más bajos
    maxs = encontrar_swings(macd_serie, es_minimo=False, min_dist=min_swing_sep)
    maxs_validos = [i for i in maxs if macd_serie.iloc[i] > umbral_0]

    if len(maxs_validos) >= 2:
        p1, p2 = maxs_validos[-2], maxs_validos[-1]
        if (p2 - p1) >= min_velas:
            precio_max_p1 = max_precio_zona(p1)
            precio_max_p2 = max_precio_zona(p2)
            # Divergencia real: precio hace máximo MÁS ALTO, MACD hace máximo MÁS BAJO
            if precio_max_p2 > precio_max_p1 and macd_serie.iloc[p2] < macd_serie.iloc[p1]:
                fuerza = round(abs(macd_serie.iloc[p1] - macd_serie.iloc[p2]) / rango_macd * 100, 1)
                # Filtro mínimo de fuerza — divergencias débiles son ruido
                if fuerza < 10.0:
                    return False, "", "", ""
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
    """
    if len(df) < 205:
        return False, ""
    ema50  = df['Close'].ewm(span=50,  adjust=False).mean()
    ema200 = df['Close'].ewm(span=200, adjust=False).mean()

    # Mirar las últimas N+1 velas para detectar cruce
    for i in range(1, velas + 1):
        curr_diff = ema50.iloc[-i]   - ema200.iloc[-i]
        prev_diff = ema50.iloc[-i-1] - ema200.iloc[-i-1]
        if prev_diff < 0 and curr_diff > 0:
            return True, f"✨ GOLDEN CROSS (Hace {i-1} velas)"
        if prev_diff > 0 and curr_diff < 0:
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
    2. Estocástico en zona extrema (<25 alcista / >75 bajista)
    3. Volumen > 1.5x media 20 velas
    Devuelve lista de señales encontradas en las últimas 4 velas.
    """
    resultados = []

    if df is None or df.empty or len(df) < 25:
        return resultados
    if 'Volume' not in df.columns:
        return resultados

    # Calcular estocástico
    low14  = df['Low'].rolling(14).min()
    high14 = df['High'].rolling(14).max()
    k_raw  = 100 * (df['Close'] - low14) / (high14 - low14 + 1e-10)
    stoch_k = k_raw.rolling(3).mean()

    # Volumen institucional — media 20 velas + máximo 20 velas
    vol_media = df['Volume'].rolling(20).mean()
    vol_max20 = df['Volume'].rolling(20).max()

    # MACD
    macd_estado = 'neutro'
    if 'MACD' in df.columns and 'Signal' in df.columns:
        curr = df.iloc[-1]
        if curr['MACD'] > curr['Signal']:
            macd_estado = 'alcista'
        elif curr['MACD'] < curr['Signal']:
            macd_estado = 'bajista'

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
        stoch_ok_alc = k < 25
        stoch_ok_baj = k > 75

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

        # ─── ENVOLVENTE ALCISTA ───
        elif (stoch_ok_alc and
              vela_idx < len(df) - 1 and
              es_alcista_vela):
            o_prev = float(df['Open'].iloc[idx - 1])
            c_prev = float(df['Close'].iloc[idx - 1])
            if c_prev < o_prev and o < c_prev and c > o_prev:
                patron    = "🔁 Envolvente Alcista"
                direccion = "ALCISTA"

        # ─── ENVOLVENTE BAJISTA ───
        elif (stoch_ok_baj and
              vela_idx < len(df) - 1 and
              not es_alcista_vela):
            o_prev = float(df['Open'].iloc[idx - 1])
            c_prev = float(df['Close'].iloc[idx - 1])
            if c_prev > o_prev and o > c_prev and c < o_prev:
                patron    = "🔁 Envolvente Bajista"
                direccion = "BAJISTA"

        # ─── HARAMI ALCISTA ───
        elif (stoch_ok_alc and
              vela_idx < len(df) - 1 and
              es_alcista_vela):
            o_prev = float(df['Open'].iloc[idx - 1])
            c_prev = float(df['Close'].iloc[idx - 1])
            if (c_prev < o_prev and
                o > c_prev and c < o_prev and
                cuerpo < abs(o_prev - c_prev) * 0.6):
                patron    = "🤰 Harami Alcista"
                direccion = "ALCISTA"

        # ─── HARAMI BAJISTA ───
        elif (stoch_ok_baj and
              vela_idx < len(df) - 1 and
              not es_alcista_vela):
            o_prev = float(df['Open'].iloc[idx - 1])
            c_prev = float(df['Close'].iloc[idx - 1])
            if (c_prev > o_prev and
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
    div_stoch_alc = check_div_stoch(df, idx, 'alcista')
    div_stoch_baj = check_div_stoch(df, idx, 'bajista')

    # Suficiente confirmación alcista/bajista (estocástico extremo O divergencia)
    confirm_alc = stoch_alc or div_stoch_alc
    confirm_baj = stoch_baj or div_stoch_baj

    # Etiqueta extra si viene de divergencia sin extremo
    def etiqueta_div(patron, stoch_ok, div_ok):
        if stoch_ok:
            return patron
        return f"🔀 {patron} + Div Stoch"

    # ─── VELA DE ENGAÑO (reutiliza check_vela_engano) ───
    es_eng, tipo_eng, k_eng, stop_eng = check_vela_engano(df, idx=idx)
    if es_eng:
        if "ALCISTA" in tipo_eng and confirm_alc:
            nombre = etiqueta_div("🎭 Vela Engaño", stoch_alc, div_stoch_alc)
            return True, nombre, "ALCISTA", k, float(min(l, l1))
        if "BAJISTA" in tipo_eng and confirm_baj:
            nombre = etiqueta_div("🎭 Vela Engaño", stoch_baj, div_stoch_baj)
            return True, nombre, "BAJISTA", k, float(max(h, h1))

    # ─── MARTILLO (alcista) ───
    if (confirm_alc and
        mecha_inf >= cuerpo * 2.0 and
        mecha_sup <= cuerpo * 0.5 and
        cuerpo >= rango * 0.1 and
        mecha_inf >= rango * 0.55):
        nombre = etiqueta_div("🔨 Martillo", stoch_alc, div_stoch_alc)
        return True, nombre, "ALCISTA", k, float(l)

    # ─── HOMBRE COLGADO (bajista) ───
    if (confirm_baj and
        mecha_inf >= cuerpo * 2.0 and
        mecha_sup <= cuerpo * 0.5 and
        cuerpo >= rango * 0.1 and
        mecha_inf >= rango * 0.55):
        nombre = etiqueta_div("💀 Hombre Colgado", stoch_baj, div_stoch_baj)
        return True, nombre, "BAJISTA", k, float(h)

    # ─── MARTILLO INVERTIDO (alcista) ───
    if (confirm_alc and
        mecha_sup >= cuerpo * 2.0 and
        mecha_inf <= cuerpo * 0.5 and
        cuerpo >= rango * 0.1):
        nombre = etiqueta_div("🔨 Martillo Invertido", stoch_alc, div_stoch_alc)
        return True, nombre, "ALCISTA", k, float(l)

    # ─── ESTRELLA FUGAZ (bajista) ───
    if (confirm_baj and
        mecha_sup >= cuerpo * 2.0 and
        mecha_inf <= cuerpo * 0.3 and
        cuerpo >= rango * 0.1):
        nombre = etiqueta_div("💫 Estrella Fugaz", stoch_baj, div_stoch_baj)
        return True, nombre, "BAJISTA", k, float(h)

    # ─── ENVOLVENTE ALCISTA ───
    if (confirm_alc and es_alc and not es_alc1 and
        o <= c1 and c >= o1 and
        cuerpo > cuerpo1 * 0.8):
        nombre = etiqueta_div("🔁 Envolvente Alcista", stoch_alc, div_stoch_alc)
        return True, nombre, "ALCISTA", k, float(l)

    # ─── ENVOLVENTE BAJISTA ───
    if (confirm_baj and not es_alc and es_alc1 and
        o >= c1 and c <= o1 and
        cuerpo > cuerpo1 * 0.8):
        nombre = etiqueta_div("🔁 Envolvente Bajista", stoch_baj, div_stoch_baj)
        return True, nombre, "BAJISTA", k, float(h)

    # ─── HARAMI ALCISTA ───
    if (confirm_alc and es_alc and not es_alc1 and
        o > c1 and c < o1 and
        cuerpo < cuerpo1 * 0.6):
        nombre = etiqueta_div("🤰 Harami Alcista", stoch_alc, div_stoch_alc)
        return True, nombre, "ALCISTA", k, float(l)

    # ─── HARAMI BAJISTA ───
    if (confirm_baj and not es_alc and es_alc1 and
        o < c1 and c > o1 and
        cuerpo < cuerpo1 * 0.6):
        nombre = etiqueta_div("🤰 Harami Bajista", stoch_baj, div_stoch_baj)
        return True, nombre, "BAJISTA", k, float(h)

    # ─── DOJI DE GIRO ALCISTA ───
    if (confirm_alc and cuerpo <= rango * 0.08 and rango > 0):
        nombre = etiqueta_div("✝️ Doji Alcista", stoch_alc, div_stoch_alc)
        return True, nombre, "ALCISTA", k, float(l)

    # ─── DOJI DE GIRO BAJISTA ───
    if (confirm_baj and cuerpo <= rango * 0.08 and rango > 0):
        nombre = etiqueta_div("✝️ Doji Bajista", stoch_baj, div_stoch_baj)
        return True, nombre, "BAJISTA", k, float(h)

    # ─── MORNING STAR — estocástico medido en vela del medio (k1) ───
    es_bajista2 = o2 > c2
    stoch_mid_alc = k1 < 20
    div_mid_alc   = check_div_stoch(df, idx - 1, 'alcista')
    if ((stoch_mid_alc or div_mid_alc) and es_alc and
        es_bajista2 and
        abs(c2 - o2) >= (h2 - l2 + 1e-10) * 0.5 and
        abs(c1 - o1) <= (h1 - l1 + 1e-10) * 0.3 and
        cuerpo >= rango * 0.45 and
        c > (o2 + c2) / 2):
        nombre = etiqueta_div("⭐ Morning Star", stoch_mid_alc, div_mid_alc)
        return True, nombre, "ALCISTA", k1, float(min(l, l1, l2))

    # ─── EVENING STAR — estocástico medido en vela del medio (k1) ───
    es_alcista2 = c2 > o2
    stoch_mid_baj = k1 > 80
    div_mid_baj   = check_div_stoch(df, idx - 1, 'bajista')
    if ((stoch_mid_baj or div_mid_baj) and not es_alc and
        es_alcista2 and
        abs(c2 - o2) >= (h2 - l2 + 1e-10) * 0.5 and
        abs(c1 - o1) <= (h1 - l1 + 1e-10) * 0.3 and
        cuerpo >= rango * 0.45 and
        c < (o2 + c2) / 2):
        nombre = etiqueta_div("⭐ Evening Star", stoch_mid_baj, div_mid_baj)
        return True, nombre, "BAJISTA", k1, float(max(h, h1, h2))

    # ─── PINBAR ALCISTA ───
    if (confirm_alc and
        mecha_inf >= rango * 0.65 and
        cuerpo <= rango * 0.25):
        nombre = etiqueta_div("📍 Pinbar Alcista", stoch_alc, div_stoch_alc)
        return True, nombre, "ALCISTA", k, float(l)

    # ─── PINBAR BAJISTA ───
    if (confirm_baj and
        mecha_sup >= rango * 0.65 and
        cuerpo <= rango * 0.25):
        nombre = etiqueta_div("📍 Pinbar Bajista", stoch_baj, div_stoch_baj)
        return True, nombre, "BAJISTA", k, float(h)

    return False, "", "", k, 0


def buscador_velas_macdelorean(pack):
    """
    Mismo esquema que Premium (M+W+D) pero con todos los patrones de vela.
    Alcista: M alcista + W corrigiendo + patrón vela alcista semanal + D girando
    Bajista: M bajista + W rebotando + patrón vela bajista semanal + D girando
    """
    m = pack['M']; w = pack['W']; d = pack['D']
    if 'MACD' not in m.columns or len(m) < 2:
        return False, "", "", 0, 0

    curr_m = m.iloc[-1]; prev_m = m.iloc[-2]
    w_curr = w.iloc[-1]; d_curr = d.iloc[-1]

    m_bull = (curr_m['MACD'] > 0) and (curr_m['MACD'] > curr_m['Signal']) and (curr_m['MACD'] > prev_m['MACD'])
    m_bear = (curr_m['MACD'] < 0) and (curr_m['MACD'] < curr_m['Signal']) and (curr_m['MACD'] < prev_m['MACD'])

    for i in range(5):
        idx = -1 - i
        es_patron, patron, direccion, k, stop = check_patron_vela_macdelorean(w, idx=idx)
        if not es_patron:
            continue
        # ALCISTA: mensual alcista + semanal corrigiendo + diario girando
        if (m_bull and
            direccion == "ALCISTA" and
            w_curr['MACD'] < w_curr['Signal'] and
            d_curr['MACD'] > d_curr['Signal']):
            return True, f"🚗 MACDELOREAN BUY — {patron} (Hace {i} sem)", direccion, k, stop
        # BAJISTA: mensual bajista + semanal rebotando + diario girando
        if (m_bear and
            direccion == "BAJISTA" and
            w_curr['MACD'] > w_curr['Signal'] and
            d_curr['MACD'] < d_curr['Signal']):
            return True, f"🚗 MACDELOREAN SELL — {patron} (Hace {i} sem)", direccion, k, stop

    return False, "", "", 0, 0


# ==============================================================================
# 3. INTERFAZ
# ==============================================================================

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("file_000000005a5451f788bcd99cfd5924fa_conversation_id=67f55f0e-bd50-800d-be41-4cd7655690a8&message_id=2e76fcf1-1345-48c0-a4b1-738909da3a1c.PNG", use_container_width=True)

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

# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.image("file_000000005a5451f788bcd99cfd5924fa_conversation_id=67f55f0e-bd50-800d-be41-4cd7655690a8&message_id=2e76fcf1-1345-48c0-a4b1-738909da3a1c.PNG", use_container_width=True)
    st.markdown("""
    <div style='text-align:center; padding: 4px 0 10px 0; border-bottom: 1px solid #2A1E08;'>
        <div style='font-family: Cinzel, serif; font-size: 0.8rem; color: #C9A84C; letter-spacing: 4px; font-weight:600;'>PANEL DE CONTROL</div>
        <div style='font-family: Share Tech Mono, monospace; font-size: 0.6rem; color: #6B5010; letter-spacing: 3px; margin-top:2px;'>RADAR v24</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    st.markdown("""<div style='font-family: Cinzel, serif; font-size: 0.72rem; color: #8B6914; letter-spacing: 4px; text-transform:uppercase; padding: 6px 0 8px 0; border-bottom: 1px solid #1A1208;'>◆ &nbsp;ÍNDICES A ESCANEAR</div>""", unsafe_allow_html=True)

    # Agrupar por región — DEBE ir ANTES de los botones
    grupos = {
        "USA": [k for k in UNIVERSO if any(x in k for x in ["DOW","NASDAQ","S&P","GROWTH","SMALL","MEGA"])],
        "EUROPA": [k for k in UNIVERSO if any(x in k for x in ["DAX","MDAX","IBEX","BME","CAC","SBF","FTSE","EUROS","ITALIA"])],
        "ASIA": [k for k in UNIVERSO if "NIKKEI" in k],
        "ETFs": [k for k in UNIVERSO if "ETF" in k or "TEMAT" in k],
    }
    n_total = sum(len(keys) for keys in grupos.values())

    # Botones rápidos de selección
    col_sel1, col_sel2 = st.columns(2)
    seleccionar_todos   = col_sel1.button("✅ Todos")
    deseleccionar_todos = col_sel2.button("❌ Ninguno")

    if seleccionar_todos:
        for i in range(n_total):
            st.session_state[f"idx_{i}"] = True
    if deseleccionar_todos:
        for i in range(n_total):
            st.session_state[f"idx_{i}"] = False

    st.markdown("")

    indices_seleccionados = []
    key_counter = 0
    for grupo, keys in grupos.items():
        if not keys:
            continue
        st.markdown(f"<div style='font-family: Share Tech Mono, monospace; color: #8B6914; font-size: 10px; letter-spacing: 3px; padding: 6px 0 4px 0;'>{grupo}</div>", unsafe_allow_html=True)
        for nombre_indice in keys:
            n = len(UNIVERSO[nombre_indice])
            safe_key = f"idx_{key_counter}"
            default_val = st.session_state.get(safe_key, True)
            checked = st.checkbox(f"{nombre_indice} ({n})", value=default_val, key=safe_key)
            if checked:
                indices_seleccionados.append(nombre_indice)
            key_counter += 1
        st.markdown("")

    st.markdown("<div style='height:12px; border-top:1px solid #1A1208; margin-top:10px;'></div>", unsafe_allow_html=True)
    st.markdown("""<div style='font-family: Cinzel, serif; font-size: 0.72rem; color: #8B6914; letter-spacing: 4px; padding: 8px 0 8px 0; border-bottom: 1px solid #1A1208;'>◆ &nbsp;FILTROS DE BÚSQUEDA</div>""", unsafe_allow_html=True)
    filtro_premium   = st.checkbox("💎 Operaciones Premium (M+W+D)", value=True,  key="f1")
    filtro_velas     = st.checkbox("🕯️ Velas de Cambio (D/W/M)",     value=True,  key="f2")
    filtro_diverg    = st.checkbox("📐 Divergencias MACD",            value=False, key="f3")
    filtro_macd_combo  = st.checkbox("📡 Radar MACD por Timeframe",    value=False, key="f4")
    filtro_confluencia = st.checkbox("💥 Confluencia Div + Vela",       value=True,  key="f5")

    if filtro_velas:
        st.markdown("**Timeframes Velas de Cambio:**")
        vc_d = st.checkbox("Diario",  value=False, key="vc_d")
        vc_w = st.checkbox("Semanal", value=True,  key="vc_w")
        vc_m = st.checkbox("Mensual", value=True,  key="vc_m")
    else:
        vc_d = vc_w = vc_m = False
    filtro_emas        = st.checkbox("📈 Cruce EMA 50/200",              value=False, key="f6")
    filtro_puntob      = st.checkbox("🔵 Módulo de Arranque (Punto B)",  value=False, key="f7")
    filtro_paco        = st.checkbox("🌟 Señal de Paco Pérez",            value=False, key="f8")
    filtro_macdelorean = st.checkbox("🚗 Velas Macdelorean (M+W+D)",      value=False, key="f9")

    if filtro_puntob:
        st.markdown("**Timeframes Punto B:**")
        pb_4h = st.checkbox("4H", value=False, key="pb4h")
        pb_d  = st.checkbox("Diario",  value=True,  key="pbd")
        pb_w  = st.checkbox("Semanal", value=True,  key="pbw")
        pb_m  = st.checkbox("Mensual", value=False, key="pbm")
    else:
        pb_4h = pb_d = pb_w = pb_m = False

    if filtro_paco:
        st.markdown("**MACD — Señal Paco Pérez:**")
        opciones_paco_macd = ["⚪ Cualquiera", "🟢 Alcista", "🔴 Bajista"]
        paco_macd_filtro = st.selectbox("Estado MACD", opciones_paco_macd, index=0, key="paco_macd")
    else:
        paco_macd_filtro = "⚪ Cualquiera"

    if filtro_diverg or filtro_confluencia:
        st.markdown("**MACD — Divergencias / Confluencias:**")
        opc_estado = ["⚪ Cualquiera", "🟢 Alcista", "🔴 Bajista"]
        opc_cero   = ["⚪ Cualquiera", "⬆️ Por encima de 0", "⬇️ Por debajo de 0"]
        div_macd_m_est = st.selectbox("Mensual — Estado",   opc_estado, index=0, key="div_m_est")
        div_macd_m_cer = st.selectbox("Mensual — Línea 0",  opc_cero,   index=0, key="div_m_cer")
        div_macd_w_est = st.selectbox("Semanal — Estado",   opc_estado, index=0, key="div_w_est")
        div_macd_w_cer = st.selectbox("Semanal — Línea 0",  opc_cero,   index=0, key="div_w_cer")
        div_macd_d_est = st.selectbox("Diario — Estado",    opc_estado, index=0, key="div_d_est")
        div_macd_d_cer = st.selectbox("Diario — Línea 0",   opc_cero,   index=0, key="div_d_cer")
    else:
        div_macd_m_est = div_macd_w_est = div_macd_d_est = "⚪ Cualquiera"
        div_macd_m_cer = div_macd_w_cer = div_macd_d_cer = "⚪ Cualquiera"

    if filtro_macd_combo:
        st.markdown("**Estado MACD — selecciona cada TF:**")
        opciones_macd  = ["⚪ Cualquiera", "🟢 Alcista", "🔴 Bajista"]
        opciones_cero  = ["⚪ Cualquiera", "⬆️ Por encima de 0", "⬇️ Por debajo de 0"]
        macd_m = st.selectbox("Mensual (M)", opciones_macd, index=0, key="macd_m")
        cero_m = st.selectbox("Línea 0 — Mensual", opciones_cero, index=0, key="cero_m")
        macd_w = st.selectbox("Semanal (W)", opciones_macd, index=0, key="macd_w")
        cero_w = st.selectbox("Línea 0 — Semanal", opciones_cero, index=0, key="cero_w")
        macd_d = st.selectbox("Diario  (D)", opciones_macd, index=0, key="macd_d")
        cero_d = st.selectbox("Línea 0 — Diario", opciones_cero, index=0, key="cero_d")
    else:
        macd_m = macd_w = macd_d = "⚪ Cualquiera"
        cero_m = cero_w = cero_d = "⚪ Cualquiera"

    st.markdown("<div style='height:12px; border-top:1px solid #1A1208; margin-top:10px;'></div>", unsafe_allow_html=True)
    st.markdown("""<div style='font-family: Cinzel, serif; font-size: 0.72rem; color: #8B6914; letter-spacing: 4px; padding: 8px 0 8px 0; border-bottom: 1px solid #1A1208;'>◆ &nbsp;DIRECCIÓN</div>""", unsafe_allow_html=True)
    dir_alcista = st.checkbox("🟢 Alcistas", value=True, key="dir1")
    dir_bajista = st.checkbox("🔴 Bajistas", value=True, key="dir2")

    st.markdown("---")

    total_tickers = sum(len(UNIVERSO[i]) for i in indices_seleccionados)
    # Estimar tiempo
    seg_est = total_tickers * 0.35
    min_est = int(seg_est // 60)
    seg_r   = int(seg_est % 60)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0F0D08 0%, #181208 100%);
                border: 1px solid #3A2A0A; border-radius: 2px;
                padding: 16px 12px; text-align:center;
                box-shadow: inset 0 0 30px rgba(201,168,76,0.04);'>
        <div style='font-family: Cinzel, serif; color: #6B5010; font-size: 9px; letter-spacing: 5px; margin-bottom:8px;'>OBJETIVOS SELECCIONADOS</div>
        <div style='font-family: Share Tech Mono, monospace; color: #C9A84C; font-size: 2.2rem; font-weight:700; line-height:1; text-shadow: 0 0 20px rgba(201,168,76,0.3);'>{total_tickers}</div>
        <div style='height:1px; background: linear-gradient(90deg, transparent, #3A2A0A, transparent); margin: 8px 0;'></div>
        <div style='font-family: Share Tech Mono, monospace; color: #6B5010; font-size: 10px; letter-spacing: 2px;'>⏱ EST. {min_est}m {seg_r}s</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    lanzar = st.button("◆  LANZAR RADAR  ◆")


# ==============================================================================
# EJECUCIÓN
# ==============================================================================
if lanzar:
    if not indices_seleccionados:
        st.error("⚠️ Selecciona al menos un índice.")
        st.stop()
    if not (filtro_premium or filtro_velas or filtro_diverg or filtro_macd_combo or filtro_confluencia or filtro_emas or filtro_puntob or filtro_paco or filtro_macdelorean):
        st.error("⚠️ Activa al menos un filtro de búsqueda.")
        st.stop()

    master_list = list(dict.fromkeys(
        ticker for idx_name in indices_seleccionados for ticker in UNIVERSO[idx_name]
    ))

    st.success(f"📡 **{len(master_list)} OBJETIVOS** · **{len(indices_seleccionados)} ÍNDICES** — ESCANEO EN PROCESO...")

    res_prem   = []
    res_velas  = []
    res_diverg = []
    res_macd        = []
    res_confluencia = []
    res_emas        = []
    res_puntob      = []
    res_paco        = []
    res_macdelorean = []

    progress_bar = st.progress(0)
    status_text  = st.empty()
    col_live1, col_live2, col_live3 = st.columns(3)
    ph_prem  = col_live1.empty()
    ph_velas = col_live2.empty()
    ph_div   = col_live3.empty()

    for i, ticker in enumerate(master_list):
        progress_bar.progress((i + 1) / len(master_list))
        status_text.text(f"🔎 {ticker}  [{i+1}/{len(master_list)}]")
        time.sleep(0.05)

        pack = procesar_datos(ticker, incluir_4h=(filtro_puntob and pb_4h))
        if pack is None:
            continue

        precio = round(float(pack['D'].iloc[-1]['Close']), 2)

        if filtro_premium:
            es_sup, txt, stop = super_buscador(pack)
            if es_sup:
                if ("BUY" in txt and dir_alcista) or ("SELL" in txt and dir_bajista):
                    res_prem.append({"Ticker": ticker, "Señal": txt, "Precio": precio, "Stop Ref": round(float(stop), 2)})
                    ph_prem.dataframe(pd.DataFrame(res_prem), use_container_width=True)

        if filtro_velas:
            tfs_velas = []
            if vc_m: tfs_velas.append(('M', 'MENSUAL'))
            if vc_w: tfs_velas.append(('W', 'SEMANAL'))
            if vc_d: tfs_velas.append(('D', 'DIARIO'))
            for tf_key, tf_name in tfs_velas:
                for j in range(4):
                    es_patron, patron, direccion_p, k_p, stop_p = check_patron_vela_macdelorean(pack[tf_key], idx=-1-j)
                    if es_patron:
                        es_alc = direccion_p == "ALCISTA"
                        if (es_alc and dir_alcista) or (not es_alc and dir_bajista):
                            unidad = 'Mes' if tf_key=='M' else ('Sem' if tf_key=='W' else 'Día')
                            res_velas.append({
                                "Ticker":     ticker,
                                "TF":         tf_name,
                                "Patrón":     patron,
                                "Dirección":  direccion_p,
                                "Antigüedad": f"Hace {j} {unidad}",
                                "Stoch K":    round(k_p, 1),
                                "Precio":     precio,
                                "Stop Ref":   round(float(stop_p), 2)
                            })
                            ph_velas.dataframe(pd.DataFrame(res_velas), use_container_width=True)
                        break

        if filtro_diverg:
            for tf_key, tf_name, est_sel, cer_sel in [
                ('D', 'DIARIO',   div_macd_d_est, div_macd_d_cer),
                ('W', 'SEMANAL',  div_macd_w_est, div_macd_w_cer),
                ('M', 'MENSUAL',  div_macd_m_est, div_macd_m_cer),
            ]:
                es_div, tipo_div, duracion, antiguedad = check_divergencia(pack[tf_key], timeframe=tf_key)
                if es_div:
                    es_alc_div = "ALCISTA" in tipo_div
                    if not ((es_alc_div and dir_alcista) or (not es_alc_div and dir_bajista)):
                        continue
                    # Filtro MACD
                    est_tf, pos_tf = check_macd_estado(pack[tf_key])
                    if est_sel == "🟢 Alcista"        and est_tf != 'alcista': continue
                    if est_sel == "🔴 Bajista"        and est_tf != 'bajista': continue
                    if cer_sel == "⬆️ Por encima de 0" and pos_tf != 'encima': continue
                    if cer_sel == "⬇️ Por debajo de 0" and pos_tf != 'debajo': continue
                    macd_icon = "🟢" if est_tf=='alcista' else ("🔴" if est_tf=='bajista' else "⚪")
                    cero_icon = "⬆️" if pos_tf=='encima' else "⬇️"
                    res_diverg.append({
                        "Ticker":     ticker,
                        "TF":         tf_name,
                        "Tipo":       tipo_div,
                        "Duración":   duracion,
                        "Formada":    antiguedad,
                        "MACD":       f"{macd_icon} {est_tf.capitalize()} {cero_icon}",
                        "Precio":     precio
                    })
                    ph_div.dataframe(pd.DataFrame(res_diverg), use_container_width=True)

        if filtro_macd_combo:
            estado_m, pos_m = check_macd_estado(pack['M'])
            estado_w, pos_w = check_macd_estado(pack['W'])
            estado_d, pos_d = check_macd_estado(pack['D'])

            def cumple(sel_estado, sel_cero, estado, posicion):
                if sel_estado == "🟢 Alcista"  and estado != 'alcista': return False
                if sel_estado == "🔴 Bajista"  and estado != 'bajista': return False
                if sel_cero == "⬆️ Por encima de 0" and posicion != 'encima': return False
                if sel_cero == "⬇️ Por debajo de 0" and posicion != 'debajo': return False
                return True

            if (cumple(macd_m, cero_m, estado_m, pos_m) and
                cumple(macd_w, cero_w, estado_w, pos_w) and
                cumple(macd_d, cero_d, estado_d, pos_d)):

                def icono_estado(e): return "🟢" if e=='alcista' else ("🔴" if e=='bajista' else "⚪")
                def icono_cero(p):   return "⬆️" if p=='encima' else "⬇️"

                res_macd.append({
                    "Ticker":   ticker,
                    "Mensual":  f"{icono_estado(estado_m)} {estado_m.capitalize()} {icono_cero(pos_m)}",
                    "Semanal":  f"{icono_estado(estado_w)} {estado_w.capitalize()} {icono_cero(pos_w)}",
                    "Diario":   f"{icono_estado(estado_d)} {estado_d.capitalize()} {icono_cero(pos_d)}",
                    "Precio":   precio
                })

        # ── VELAS MACDELOREAN ──
        if filtro_macdelorean:
            es_mac, txt_mac, dir_mac, k_mac, stop_mac = buscador_velas_macdelorean(pack)
            if es_mac:
                if (dir_mac == "ALCISTA" and dir_alcista) or (dir_mac == "BAJISTA" and dir_bajista):
                    res_macdelorean.append({
                        "Ticker":    ticker,
                        "Señal":     txt_mac,
                        "Dirección": dir_mac,
                        "Stoch K":   round(k_mac, 1),
                        "Stop Ref":  round(float(stop_mac), 2),
                        "Precio":    precio
                    })

        # ── SEÑAL DE PACO PÉREZ ──
        if filtro_paco:
            for tf_key, tf_name in [('D', 'DIARIO'), ('W', 'SEMANAL'), ('M', 'MENSUAL')]:
                senales = check_senal_paco(pack[tf_key], timeframe=tf_key)
                for senal in senales:
                    dir_ok = (senal['direccion'] == 'ALCISTA' and dir_alcista) or                              (senal['direccion'] == 'BAJISTA' and dir_bajista)
                    macd_ok = (paco_macd_filtro == "⚪ Cualquiera") or                               (paco_macd_filtro == "🟢 Alcista" and senal['macd'] == 'alcista') or                               (paco_macd_filtro == "🔴 Bajista" and senal['macd'] == 'bajista')
                    if dir_ok and macd_ok:
                        macd_icon = "🟢" if senal['macd'] == 'alcista' else ("🔴" if senal['macd'] == 'bajista' else "⚪")
                        res_paco.append({
                            "Ticker":     ticker,
                            "TF":         tf_name,
                            "Patrón":     senal['patron'],
                            "Dirección":  senal['direccion'],
                            "Antigüedad": senal['antiguedad'],
                            "Stoch K":    senal['stoch_k'],
                            "Vol x media":senal['vol_ratio'],
                            "MACD":       f"{macd_icon} {senal['macd'].capitalize()}",
                            "Velas prev": senal['contexto'],
                            "Precio":     precio
                        })

        # ── CONFLUENCIA: Divergencia MACD + Patrón de Vela mismo TF ──
        if filtro_confluencia:
            for tf_key, tf_name, est_sel, cer_sel in [
                ('D', 'DIARIO',  div_macd_d_est, div_macd_d_cer),
                ('W', 'SEMANAL', div_macd_w_est, div_macd_w_cer),
                ('M', 'MENSUAL', div_macd_m_est, div_macd_m_cer),
            ]:
                # Primero verificar si hay divergencia en este TF
                es_div, tipo_div, duracion, antiguedad = check_divergencia(pack[tf_key], timeframe=tf_key)
                if not es_div:
                    continue
                div_alc = "ALCISTA" in tipo_div

                # Filtro dirección global
                if div_alc and not dir_alcista: continue
                if not div_alc and not dir_bajista: continue

                # Filtro MACD
                est_tf, pos_tf = check_macd_estado(pack[tf_key])
                if est_sel == "🟢 Alcista"         and est_tf != 'alcista': continue
                if est_sel == "🔴 Bajista"         and est_tf != 'bajista': continue
                if cer_sel == "⬆️ Por encima de 0"  and pos_tf != 'encima':  continue
                if cer_sel == "⬇️ Por debajo de 0"  and pos_tf != 'debajo':  continue

                # Buscar CUALQUIER patrón de vela en las últimas 4 velas
                patron_encontrado = None
                for j in range(4):
                    es_patron, patron, direccion_p, k_p, stop_p = check_patron_vela_macdelorean(pack[tf_key], idx=-1-j)
                    if es_patron:
                        patron_alc = direccion_p == "ALCISTA"
                        # Debe coincidir con la dirección de la divergencia
                        if patron_alc == div_alc:
                            patron_encontrado = {
                                'patron': patron,
                                'direccion': direccion_p,
                                'k': k_p,
                                'stop': stop_p,
                                'j': j
                            }
                            break

                if patron_encontrado is None:
                    continue

                macd_icon = "🟢" if est_tf=='alcista' else ("🔴" if est_tf=='bajista' else "⚪")
                cero_icon = "⬆️" if pos_tf=='encima' else "⬇️"
                icono     = "🚀" if div_alc else "💣"
                res_confluencia.append({
                    "Ticker":      ticker,
                    "TF":          tf_name,
                    "Dirección":   f"{'🟢 ALCISTA' if div_alc else '🔴 BAJISTA'}",
                    "Señal":       f"{icono} DIV + {patron_encontrado['patron']}",
                    "Div Fuerza":  tipo_div.split("(")[1].replace(")","") if "(" in tipo_div else "-",
                    "Div Dur.":    duracion,
                    "MACD":        f"{macd_icon} {est_tf.capitalize()} {cero_icon}",
                    "Vela Stoch":  round(patron_encontrado['k'], 1),
                    "Antigüedad":  f"Hace {patron_encontrado['j']} {'Mes' if tf_key=='M' else ('Sem' if tf_key=='W' else 'Día')}",
                    "Precio":      precio,
                    "Stop Ref":    round(float(patron_encontrado['stop']), 2)
                })

        # ── CRUCE EMA 50/200 ──
        if filtro_emas:
            for tf_key, tf_name in [('D', 'DIARIO'), ('W', 'SEMANAL')]:
                es_cruce, tipo_cruce = check_cruce_emas(pack[tf_key], velas=4)
                if es_cruce:
                    es_golden = "GOLDEN" in tipo_cruce
                    if (es_golden and dir_alcista) or (not es_golden and dir_bajista):
                        res_emas.append({
                            "Ticker":  ticker,
                            "TF":      tf_name,
                            "Señal":   tipo_cruce,
                            "Precio":  precio
                        })

        # ── MÓDULO DE ARRANQUE — PUNTO B ──
        if filtro_puntob:
            tfs_pb = []
            if pb_4h and not pack['4H'].empty: tfs_pb.append(('4H', '4 HORAS'))
            if pb_d:  tfs_pb.append(('D', 'DIARIO'))
            if pb_w:  tfs_pb.append(('W', 'SEMANAL'))
            if pb_m:  tfs_pb.append(('M', 'MENSUAL'))

            for tf_key, tf_name in tfs_pb:
                df_tf = pack.get(tf_key)
                if df_tf is None or (hasattr(df_tf, 'empty') and df_tf.empty):
                    continue
                es_pb, tipo_pb, nivel_b, tp1, tp2, info = check_punto_b(df_tf, timeframe=tf_key)
                if es_pb:
                    es_bajista_pb = "BAJISTA" in tipo_pb
                    if (not es_bajista_pb and dir_alcista) or (es_bajista_pb and dir_bajista):
                        def velas_a_tiempo(v, tf):
                            if tf == "4H":
                                horas = v * 4
                                if horas < 24: return f"{horas}h"
                                dias = horas // 24
                                return f"{dias} dia{'s' if dias>1 else ''}"
                            elif tf == "D":
                                if v <= 1:  return "Hoy"
                                if v < 5:   return f"{v} dias"
                                sem = v // 5
                                return f"{sem} semana{'s' if sem>1 else ''}"
                            elif tf == "W":
                                if v <= 1:  return "Esta semana"
                                if v < 4:   return f"{v} semanas"
                                mes = round(v * 7 / 30)
                                return f"{mes} mes{'es' if mes>1 else ''}"
                            elif tf == "M":
                                if v <= 1: return "Este mes"
                                return f"{v} meses"
                            return f"{v} velas"

                        duracion_txt = velas_a_tiempo(info["duracion_velas"], tf_key)
                        desde_c_txt  = velas_a_tiempo(info["velas_desde_c"],  tf_key)
                        if info["estado_b"] == "✅ ROTO" and info["velas_ruptura"] > 0:
                            roto_hace_txt = velas_a_tiempo(info["velas_ruptura"], tf_key)
                        elif info["estado_b"] == "✅ ROTO":
                            roto_hace_txt = "Hoy"
                        else:
                            roto_hace_txt = "—"

                        res_puntob.append({
                            "Ticker":        ticker,
                            "TF":            tf_name,
                            "Tipo":          tipo_pb,
                            "Estado B":      info["estado_b"],
                            "Fecha A":       info.get("fecha_a", "—"),
                            "Precio A":      info["precio_a"],
                            "Fecha B":       info.get("fecha_b", "—"),
                            "Nivel B":       info["nivel_b"],
                            "Fecha C":       info.get("fecha_c", "—"),
                            "Precio C":      info["precio_c"],
                            "TP1 (161.8%)":  tp1,
                            "TP2 (200%)":    tp2,
                            "Dur. modulo":   duracion_txt,
                            "Desde C":       desde_c_txt,
                            "Roto hace":     roto_hace_txt,
                            "Precio":        precio
                        })

    ph_prem.empty(); ph_velas.empty(); ph_div.empty()
    progress_bar.empty()
    status_text.success("✅ ESCANEO COMPLETADO.")
    st.balloons()

    st.markdown("---")
    m1, m2, m3, m4, m5, m6, m7, m8 = st.columns(8)
    m1.metric("🎯 Escaneados",       len(master_list))
    m2.metric("💎 Premium",          len(res_prem))
    m3.metric("🕯️ Velas Engaño",    len(res_velas))
    m4.metric("📐 Divergencias",     len(res_diverg))
    m5.metric("📡 MACD Combo",       len(res_macd))
    m6.metric("💥 Confluencia",      len(res_confluencia))
    m7.metric("📈 EMA Cross",        len(res_emas))
    m8.metric("🔵 Punto B",          len(res_puntob))
    st.markdown("---")

    tab_labels = []
    if filtro_premium:    tab_labels.append(f"💎 PREMIUM ({len(res_prem)})")
    if filtro_velas:      tab_labels.append(f"🕯️ VELAS CAMBIO ({len(res_velas)})")
    if filtro_diverg:     tab_labels.append(f"📐 DIVERGENCIAS ({len(res_diverg)})")
    if filtro_macd_combo:   tab_labels.append(f"📡 MACD COMBO ({len(res_macd)})")
    if filtro_confluencia:  tab_labels.append(f"💥 CONFLUENCIA ({len(res_confluencia)})")
    if filtro_emas:         tab_labels.append(f"📈 EMA CROSS ({len(res_emas)})")
    if filtro_puntob:       tab_labels.append(f"🔵 PUNTO B ({len(res_puntob)})")
    if filtro_paco:         tab_labels.append(f"🌟 PACO PÉREZ ({len(res_paco)})")
    if filtro_macdelorean:  tab_labels.append(f"🚗 MACDELOREAN ({len(res_macdelorean)})")

    tabs = st.tabs(tab_labels)
    tab_idx = 0

    if filtro_premium:
        with tabs[tab_idx]:
            if res_prem:
                df_out = pd.DataFrame(res_prem)
                st.dataframe(df_out, use_container_width=True)
                st.download_button("⬇️ Exportar CSV", df_out.to_csv(index=False).encode(), "premium.csv", "text/csv")
            else:
                st.warning("Sin entradas Premium hoy. Mantener disciplina.")
        tab_idx += 1

    if filtro_velas:
        with tabs[tab_idx]:
            if res_velas:
                df_out = pd.DataFrame(res_velas)
                alc = df_out[df_out['Dirección'] == 'ALCISTA']
                baj = df_out[df_out['Dirección'] == 'BAJISTA']
                if not alc.empty:
                    st.markdown("#### 🟢 ALCISTAS"); st.dataframe(alc.drop(columns=['Dirección']), use_container_width=True)
                if not baj.empty:
                    st.markdown("#### 🔴 BAJISTAS"); st.dataframe(baj.drop(columns=['Dirección']), use_container_width=True)
                st.download_button("⬇️ Exportar CSV", df_out.to_csv(index=False).encode(), "velas.csv", "text/csv")
            else:
                st.info("Sin velas de engaño detectadas.")
        tab_idx += 1

    if filtro_diverg:
        with tabs[tab_idx]:
            if res_diverg:
                df_out = pd.DataFrame(res_diverg)
                alc = df_out[df_out['Tipo'].str.contains("ALCISTA")]
                baj = df_out[df_out['Tipo'].str.contains("BAJISTA")]
                if not alc.empty:
                    st.markdown("#### 📈 ALCISTAS"); st.dataframe(alc, use_container_width=True)
                if not baj.empty:
                    st.markdown("#### 📉 BAJISTAS"); st.dataframe(baj, use_container_width=True)
                st.download_button("⬇️ Exportar CSV", df_out.to_csv(index=False).encode(), "divergencias.csv", "text/csv")
            else:
                st.info("Sin divergencias detectadas.")
        tab_idx += 1

    if filtro_macd_combo:
        with tabs[tab_idx]:
            if res_macd:
                df_out = pd.DataFrame(res_macd)
                st.markdown("#### 📡 RESULTADOS RADAR MACD")
                st.dataframe(df_out, use_container_width=True)
                st.download_button("⬇️ Exportar CSV", df_out.to_csv(index=False).encode(), "macd_combo.csv", "text/csv")
            else:
                st.info("Ningún activo cumple la combinación MACD seleccionada.")
        tab_idx += 1

    if filtro_confluencia:
        with tabs[tab_idx]:
            if res_confluencia:
                df_out = pd.DataFrame(res_confluencia)
                alc = df_out[df_out['Dirección'].str.contains("ALCISTA")]
                baj = df_out[df_out['Dirección'].str.contains("BAJISTA")]
                if not alc.empty:
                    st.markdown("#### 🚀 CONFLUENCIAS ALCISTAS")
                    st.dataframe(alc, use_container_width=True)
                if not baj.empty:
                    st.markdown("#### 💣 CONFLUENCIAS BAJISTAS")
                    st.dataframe(baj, use_container_width=True)
                st.download_button("⬇️ Exportar CSV", df_out.to_csv(index=False).encode(), "confluencia.csv", "text/csv")
            else:
                st.info("No se han detectado confluencias Divergencia + Vela de Engaño.")
        tab_idx += 1

    if filtro_emas:
        with tabs[tab_idx]:
            if res_emas:
                df_out = pd.DataFrame(res_emas)
                golden = df_out[df_out['Señal'].str.contains("GOLDEN")]
                death  = df_out[df_out['Señal'].str.contains("DEATH")]
                if not golden.empty:
                    st.markdown("#### ✨ GOLDEN CROSS — EMA50 cruza sobre EMA200")
                    st.dataframe(golden, use_container_width=True)
                if not death.empty:
                    st.markdown("#### 💀 DEATH CROSS — EMA50 cruza bajo EMA200")
                    st.dataframe(death, use_container_width=True)
                st.download_button("⬇️ Exportar CSV", df_out.to_csv(index=False).encode(), "ema_cross.csv", "text/csv")
            else:
                st.info("No se han detectado cruces de EMA50/200 recientes.")
        tab_idx += 1

    if filtro_puntob:
        with tabs[tab_idx]:
            if res_puntob:
                df_out = pd.DataFrame(res_puntob)
                buenas = df_out[df_out['Tipo'].str.contains("BUENA")]
                malas  = df_out[df_out['Tipo'].str.contains("MALA")]
                alc_buenas = df_out[df_out['Tipo'].str.contains("BUENA") & ~df_out['Tipo'].str.contains("BAJISTA")]
                alc_malas  = df_out[df_out['Tipo'].str.contains("MALA")  & ~df_out['Tipo'].str.contains("BAJISTA")]
                baj_buenas = df_out[df_out['Tipo'].str.contains("BUENA OSCILACIÓN BAJISTA|BUENA OSC. BAJISTA")]
                baj_malas  = df_out[df_out['Tipo'].str.contains("MALA OSCILACIÓN BAJISTA|MALA OSC. BAJISTA")]

                if not alc_buenas.empty:
                    st.markdown("#### 🟢 BUENA OSCILACIÓN ALCISTA — C < A")
                    st.dataframe(alc_buenas, use_container_width=True)
                if not alc_malas.empty:
                    st.markdown("#### 🟡 MALA OSCILACIÓN ALCISTA — C > A")
                    st.dataframe(alc_malas, use_container_width=True)
                if not baj_buenas.empty:
                    st.markdown("#### 🔴 BUENA OSCILACIÓN BAJISTA — C > A")
                    st.dataframe(baj_buenas, use_container_width=True)
                if not baj_malas.empty:
                    st.markdown("#### 🟠 MALA OSCILACIÓN BAJISTA — C < A")
                    st.dataframe(baj_malas, use_container_width=True)
                st.download_button("⬇️ Exportar CSV", df_out.to_csv(index=False).encode(), "punto_b.csv", "text/csv")
            else:
                st.info("No se han detectado módulos de arranque válidos.")
        tab_idx += 1

    if filtro_paco:
        with tabs[tab_idx]:
            if res_paco:
                df_out = pd.DataFrame(res_paco)
                alc = df_out[df_out['Dirección'] == 'ALCISTA']
                baj = df_out[df_out['Dirección'] == 'BAJISTA']
                if not alc.empty:
                    st.markdown("#### 🟢 SEÑALES ALCISTAS — PACO PÉREZ")
                    st.dataframe(alc.drop(columns=['Dirección']), use_container_width=True)
                if not baj.empty:
                    st.markdown("#### 🔴 SEÑALES BAJISTAS — PACO PÉREZ")
                    st.dataframe(baj.drop(columns=['Dirección']), use_container_width=True)
                st.download_button("⬇️ Exportar CSV", df_out.to_csv(index=False).encode(), "paco_perez.csv", "text/csv")
            else:
                st.info("Sin señales Paco Pérez detectadas. El mercado no presenta configuraciones de alta calidad ahora mismo.")
        tab_idx += 1

    if filtro_macdelorean:
        with tabs[tab_idx]:
            if res_macdelorean:
                df_out = pd.DataFrame(res_macdelorean)
                alc = df_out[df_out['Dirección'] == 'ALCISTA']
                baj = df_out[df_out['Dirección'] == 'BAJISTA']
                if not alc.empty:
                    st.markdown("#### 🚗🟢 VELAS MACDELOREAN — BUY")
                    st.dataframe(alc.drop(columns=['Dirección']), use_container_width=True)
                if not baj.empty:
                    st.markdown("#### 🚗🔴 VELAS MACDELOREAN — SELL")
                    st.dataframe(baj.drop(columns=['Dirección']), use_container_width=True)
                st.download_button("⬇️ Exportar CSV", df_out.to_csv(index=False).encode(), "macdelorean_velas.csv", "text/csv")
            else:
                st.info("Sin señales Velas Macdelorean. Espera la confluencia perfecta M+W+D.")

else:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        ("📊", "ÍNDICES", "17 mercados"),
        ("🎯", "TICKERS", f"~{sum(len(v) for v in UNIVERSO.values())} activos"),
        ("🌍", "COBERTURA", "USA · EU · UK · JP"),
        ("⚡", "ETFs", "Sectores · Temáticos · Apalancados"),
    ]
    for col, (icon, label, val) in zip([c1,c2,c3,c4], stats):
        col.markdown(f"""
        <div style='background: linear-gradient(160deg, #111008 0%, #0D0C08 100%);
                    border: 1px solid #2A1E08;
                    border-top: 1px solid #3A2A0A;
                    border-radius: 2px; padding:20px 12px; text-align:center;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.5), inset 0 1px 0 rgba(201,168,76,0.08);
                    transition: all 0.3s;'>
            <div style='font-size:1.5rem; margin-bottom:8px; opacity:0.7;'>{icon}</div>
            <div style='font-family: Cinzel, serif; color: #8B6914; font-size: 8px;
                        letter-spacing: 4px; margin-bottom:6px; text-transform:uppercase;'>{label}</div>
            <div style='font-family: Share Tech Mono, monospace; color: #C9A84C;
                        font-size: 13px; letter-spacing: 1px;'>{val}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    bloques = [
        ("💎 PREMIUM", "Confluencia M + W + D\nMACD estricto multi-timeframe\n+ Vela de engaño semanal"),
        ("🕯️ VELAS ENGAÑO", "Barrido de mínimos/máximos\nRecuperación > 50% vela\nEstocástico extremo (<20 / >80)"),
        ("📐 DIVERGENCIAS", "Precio vs Momentum MACD\nVentana de 10 velas\nDisponible en D / W / M"),
    ]
    for col, (titulo, desc) in zip([c1,c2,c3], bloques):
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

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; padding: 10px 0;'>
        <div style='display:inline-block; height:1px; width:60px;
                    background: linear-gradient(90deg, transparent, #3A2A0A); vertical-align:middle; margin-right:14px;'></div>
        <span style='font-family: Cinzel, serif; color: #3A2A0A; font-size: 10px; letter-spacing: 5px;'>
            SELECCIONA ÍNDICES · ACTIVA FILTROS · LANZA EL RADAR
        </span>
        <div style='display:inline-block; height:1px; width:60px;
                    background: linear-gradient(90deg, #3A2A0A, transparent); vertical-align:middle; margin-left:14px;'></div>
    </div>
    """, unsafe_allow_html=True)
