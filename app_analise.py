import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# --- CARREGAR SENHAS ---
load_dotenv()
chave_secreta_env = os.getenv("API_KEY")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sniper SMC - Ultimate", page_icon="🧬", layout="wide")

# --- CSS (VISUAL INSTITUCIONAL) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #2962FF; /* Azul Royal SMC */
        color: white;
        height: 4em;
        font-weight: bold;
        font-size: 20px;
        border-radius: 6px;
        border: none;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background-color: #0039CB;
    }
    [data-testid='stFileUploader'] {
        background-color: #1a1a1a;
        padding: 15px;
        border: 1px solid #444;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🧬 Sniper Ultimate")
    
    if chave_secreta_env:
        st.success("✅ Terminal Ativo")
        api_key = chave_secreta_env
    else:
        api_key = st.text_input("API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 🧠 Seleção de Inteligência")
    
    # AQUI ESTÃO TODOS OS MODELOS AVANÇADOS NOVAMENTE
    modelo_selecionado = st.selectbox(
        "Motor de IA:",
        [
            # GERAÇÃO 3 (Experimental / Mais Potente)
            "models/gemini-3-pro-preview",
            "models/gemini-3-flash-preview",
            
            # GERAÇÃO 2.5 (Intermediária Avançada)
            "models/gemini-2.5-pro",
            "models/gemini-2.5-flash",
            
            # GERAÇÃO 2.0 (Padrão Ouro Atual)
            "models/gemini-2.0-flash",
            "models/gemini-2.0-flash-lite",
            
            # GERAÇÃO 1.5 (Estável / Backup)
            "models/gemini-1.5-pro",
            "models/gemini-1.5-flash"
        ]
    )
    
    st.caption(f"Motor: {modelo_selecionado.split('/')[-1]}")
    
    st.markdown("---")
    # SMC precisa de precisão (temperatura baixa)
    temperatura = st.slider("Precisão (0.0 = Máxima)", 0.0, 1.0, 0.1)
    
    ativo_tipo = st.selectbox(
        "Mercado:",
        ["Synthetic Indices (Crash/Boom/Vol)", "Forex (Major Pairs)", "Crypto (BTC/ETH)", "XAUUSD (Gold)"]
    )

# --- FUNÇÃO DE ANÁLISE ---
def analisar_grafico(lista_imagens, prompt, api_key, temp, modelo_nome):
    try:
        genai.configure(api_key=api_key)
        generation_config = {"temperature": temp}
        conteudo = [prompt] + lista_imagens
        
        model = genai.GenerativeModel(modelo_nome, generation_config=generation_config)
        response = model.generate_content(conteudo)
        return response.text

    except Exception as e:
        erro = str(e)
        if "429" in erro:
            return f"⏳ Cota excedida para {modelo_nome}. Tente um modelo 'Flash' ou 'Lite' na lista."
        elif "404" in erro:
            return f"⚠️ Modelo não encontrado. Verifique o requirements.txt."
        else:
            return f"⛔ Erro Técnico: {erro}"

# --- INTERFACE ---
st.title(f"🧬 Sniper SMC: {modelo_selecionado.split('/')[-1]}")
st.markdown("##### Framework Smart Money Concepts com IA de Última Geração")

col1, col2, col3 = st.columns(3)
imagens_para_analise = []

with col1:
    st.caption("1. HTF (Macro Structure)")
    img1 = st.file_uploader("Ex: H4 / Daily", type=["jpg", "png", "jpeg"], key="img1")
    if img1:
        pil_img1 = Image.open(img1)
        st.image(pil_img1, use_container_width=True)
        imagens_para_analise.append(pil_img1)

with col2:
    st.caption("2. Medium TF (Liquidity/POI)")
    img2 = st.file_uploader("Ex: H1 / M30", type=["jpg", "png", "jpeg"], key="img2")
    if img2:
        pil_img2 = Image.open(img2)
        st.image(pil_img2, use_container_width=True)
        imagens_para_analise.append(pil_img2)

with col3:
    st.caption("3. LTF (Entry Confirmation)")
    img3 = st.file_uploader("Ex: M5 / M1", type=["jpg", "png", "jpeg"], key="img3")
    if img3:
        pil_img3 = Image.open(img3)
        st.image(pil_img3, use_container_width=True)
        imagens_para_analise.append(pil_img3)

if st.button("🔎 EXECUTAR ANÁLISE SMC (GEN 3)"):
    if not api_key:
        st.error("🔒 Sem API Key.")
    elif len(imagens_para_analise) == 0:
        st.warning("⚠️ O framework SMC exige pelo menos 1 imagem.")
    else:
        with st.spinner(f'Mapeando Liquidez com {modelo_selecionado}...'):
            
            # --- PROMPT SMC PROFISSIONAL (MANTIDO) ---
            prompt = f"""
            Act as a Senior Institutional Analyst specializing in {ativo_tipo}.
            Analyze the provided images (Image 1 = Macro, Image 2 = Structure, Image 3 = Entry).
            
            Please perform the analysis using the following 'Smart Money' framework:

            1. **Macro Market Structure:** Determine the dominant trend on this timeframe (Bullish, Bearish, or Ranging). Look for major Breaks of Structure (BOS) or Changes of Character (CHoCH) that indicate a long-term directional shift.
            2. **Key Swing Levels:** Identify significant Higher Timeframe (HTF) Points of Interest (POIs), such as major Order Blocks, Breakers, or weekly/daily Support & Resistance zones.
            3. **Liquidity Sweeps:** Highlight any obvious liquidity pools (previous swing highs/lows) that the price has recently swept or is targeting as a draw on liquidity.
            4. **Confluence:** Confirm if the price is in a 'Premium' or 'Discount' zone relative to the swing range.

            Based on the visual data, generate a Precise Swing Signal in this exact format:

            # 🧬 SMC INSTITUTIONAL SETUP

            **Market Bias:** [LONG / SHORT]
            
            ---
            **ENTRY ZONE:** [Specific Price Range for a limit order]
            **STOP LOSS (SL):** [Precise Price - Must be structural, below/above the key swing low/high to survive volatility]
            **TAKE PROFIT 1 (Conservative):** [Price - Key structural resistance/support]
            **TAKE PROFIT 2 (Swing Target):** [Price - The ultimate target based on the macro leg extension]
            ---

            **Risk-to-Reward Ratio:** [Must be at least 1:3 for Swing Trading]
            
            **Trade Rationale:** [Briefly explain the BOS, POI, and Liquidity logic]

            CRITICAL: If the market is currently in 'No Man's Land' (middle of a range) or the structure is unclear for a Swing Trade, explicitly state: 
            ### 🚫 NO VALID SWING SETUP AVAILABLE (Wait for Price Action)
            """
            
            resultado = analisar_grafico(imagens_para_analise, prompt, api_key, temperatura, modelo_selecionado)
            
            if "NO VALID SWING SETUP" in resultado:
                st.warning("Sem setup claro no momento.")
                st.markdown(resultado)
            else:
                st.success(f"Análise SMC Concluída ({modelo_selecionado})")
                st.markdown(resultado)