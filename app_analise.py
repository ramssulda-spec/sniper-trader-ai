import streamlit as st
import google.generativeai as genai
import yfinance as yf
import mplfinance as mpf
from PIL import Image
import os
from dotenv import load_dotenv

# --- CARREGAR SENHAS ---
load_dotenv()
chave_secreta_env = os.getenv("API_KEY")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sniper AI - Hybrid", page_icon="⚔️", layout="wide")

# --- CSS PERSONALIZADO ---
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1E1E1E;
        border-radius: 5px;
        color: white;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00D100;
        color: black;
    }
    .stButton>button {
        width: 100%;
        background-color: #00D100;
        color: white;
        height: 3em;
        font-weight: bold;
        font-size: 18px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÃO: GERAR GRÁFICO AUTOMÁTICO ---
def criar_grafico(ticker, periodo, intervalo, nome_arquivo):
    try:
        dados = yf.download(ticker, period=periodo, interval=intervalo, progress=False)
        if len(dados) == 0: return None
        
        caminho_img = f"{nome_arquivo}.png"
        mc = mpf.make_marketcolors(up='#00ff00', down='#ff0000', edge='inherit', wick='inherit', volume='in')
        s  = mpf.make_mpf_style(marketcolors=mc, base_mpf_style='nightclouds')
        
        mpf.plot(dados, type='candle', style=s, mav=(9, 21), volume=False, 
                 savefig=dict(fname=caminho_img, dpi=100, bbox_inches='tight'),
                 title=f"{ticker} - {intervalo}")
        return caminho_img
    except:
        return None

# --- FUNÇÃO: CONSULTAR A IA ---
def consultar_ia(lista_imagens, prompt, api_key, temp):
    try:
        genai.configure(api_key=api_key)
        generation_config = {"temperature": temp}
        conteudo = [prompt] + lista_imagens
        
        try:
            model = genai.GenerativeModel('models/gemini-robotics-er-1.5-preview', generation_config=generation_config)
            response = model.generate_content(conteudo)
        except:
            model = genai.GenerativeModel('models/gemini-robotics-er-1.5-preview', generation_config=generation_config)
            response = model.generate_content(conteudo)
        return response.text
    except Exception as e:
        return f"Erro: {str(e)}"

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🦅 Sniper Híbrido")
    if chave_secreta_env:
        st.success("Conectado (.env)")
        api_key = chave_secreta_env
    else:
        api_key = st.text_input("API Key:", type="password")
    
    st.markdown("---")
    temperatura = st.slider("Agressividade", 0.0, 1.0, 0.4)
    estilo = st.selectbox("Modo:", ["Day Trade", "Scalping", "Swing"])

# --- INTERFACE PRINCIPAL ---
st.title("⚔️ Sniper AI: Central de Comando")
st.markdown("Escolha o método de análise abaixo:")

# CRIANDO AS ABAS
aba_auto, aba_manual = st.tabs(["🤖 MODO AUTOMÁTICO (Busca)", "📸 MODO MANUAL (Upload)"])

# ==========================================
# ABA 1: AUTOMÁTICO
# ==========================================
with aba_auto:
    st.markdown("#### 🤖 Robô de Busca de Mercado")
    ativo = st.text_input("Digite o Ativo (Ex: BTC-USD, PETR4.SA, EURUSD=X):", value="BTC-USD").upper()
    
    col_a1, col_a2, col_a3 = st.columns(3)
    ph = [col_a1.empty(), col_a2.empty(), col_a3.empty()]

    if st.button("🚀 BUSCAR E ANALISAR (AUTO)"):
        if not api_key: st.error("Sem API Key!")
        else:
            with st.spinner(f'Baixando dados de {ativo}...'):
                # Gera gráficos
                g1 = criar_grafico(ativo, "6mo", "1d", "temp_macro")
                g2 = criar_grafico(ativo, "1mo", "60m", "temp_medio")
                g3 = criar_grafico(ativo, "5d", "15m", "temp_micro")
                
                imgs_pil = []
                
                # Carrega e exibe
                if g1: 
                    img = Image.open(g1)
                    ph[0].image(img, caption="Diário")
                    imgs_pil.append(img)
                if g2: 
                    img = Image.open(g2)
                    ph[1].image(img, caption="H1")
                    imgs_pil.append(img)
                if g3: 
                    img = Image.open(g3)
                    ph[2].image(img, caption="M15")
                    imgs_pil.append(img)
                
                if len(imgs_pil) == 3:
                    prompt_auto = f"""
                    Você é um Trader Robô Autônomo ({estilo}). Analise os 3 gráficos do ativo {ativo}.
                    Os gráficos têm médias móveis (9 e 21). Use-as.
                    
                    Responda ESTRITAMENTE:
                    # 🤖 SINAL AUTOMÁTICO: {ativo}
                    **DECISÃO:** [COMPRA/VENDA/AGUARDAR]
                    **RISCO:** [🟢/🟡/🔴]
                    ---
                    🔵 **ENTRADA:** [Preço]
                    🔴 **STOP:** [Preço]
                    🟢 **ALVO:** [Preço]
                    ---
                    📝 **Análise:** [Resumo Técnico]
                    """
                    resultado = consultar_ia(imgs_pil, prompt_auto, api_key, temperatura)
                    st.markdown(resultado)
                else:
                    st.error("Erro ao baixar dados. Verifique o nome do ativo.")

# ==========================================
# ABA 2: MANUAL
# ==========================================
with aba_manual:
    st.markdown("#### 📸 Upload de Prints (TradingView)")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    imgs_manual = []
    
    with col_m1:
        u1 = st.file_uploader("Macro", type=["jpg", "png"], key="m1")
        if u1: 
            i1 = Image.open(u1)
            st.image(i1, use_container_width=True)
            imgs_manual.append(i1)
            
    with col_m2:
        u2 = st.file_uploader("Padrão", type=["jpg", "png"], key="m2")
        if u2: 
            i2 = Image.open(u2)
            st.image(i2, use_container_width=True)
            imgs_manual.append(i2)
            
    with col_m3:
        u3 = st.file_uploader("Gatilho", type=["jpg", "png"], key="m3")
        if u3: 
            i3 = Image.open(u3)
            st.image(i3, use_container_width=True)
            imgs_manual.append(i3)
            
    if st.button("🔎 ANALISAR PRINTS (MANUAL)"):
        if not api_key: st.error("Sem API Key!")
        elif not imgs_manual: st.warning("Suba pelo menos 1 imagem.")
        else:
            with st.spinner('Analisando seus prints...'):
                prompt_manual = f"""
                Você é um Trader de Elite ({estilo}). Analise os prints enviados.
                Identifique a MELHOR oportunidade AGORA.
                
                Responda ESTRITAMENTE:
                # 📸 SINAL MANUAL
                **DECISÃO:** [COMPRA/VENDA]
                **RISCO:** [🟢/🟡/🔴]
                ---
                🔵 **ENTRADA:** [Preço visual]
                🔴 **STOP:** [Preço visual]
                🟢 **ALVO:** [Preço visual]
                ---
                📝 **Tese:** [Por que entrar agora?]
                """
                resultado = consultar_ia(imgs_manual, prompt_manual, api_key, temperatura)
                st.markdown(resultado)