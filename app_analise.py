import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# --- CARREGAR SENHAS ---
load_dotenv()
chave_secreta_env = os.getenv("API_KEY")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IPDA Decoder - V21", page_icon="🧩", layout="wide")

# --- CSS (VISUAL MATRIX / ALGORÍTMICO) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #00E676; /* Verde Matrix */
        color: black;
        height: 4em;
        font-weight: bold;
        font-size: 20px;
        border-radius: 2px;
        border: 1px solid #00E676;
        text-transform: uppercase;
        font-family: 'Courier New', monospace;
    }
    .stButton>button:hover {
        background-color: #00C853;
        box-shadow: 0px 0px 15px #00E676;
    }
    [data-testid='stFileUploader'] {
        background-color: #0d0d0d;
        border: 1px dashed #00E676;
    }
    h1, h2, h3 {
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🧩 IPDA Control Center")
    
    if chave_secreta_env:
        st.success("✅ Algorithm Connected")
        api_key = chave_secreta_env
    else:
        api_key = st.text_input("API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 🧠 AI Core Selector")
    
    modelo_selecionado = st.selectbox(
        "Decryption Engine:",
        [
            "models/gemini-3-pro-preview",      # Recomendado para IPDA (Raciocínio Profundo)
            "models/gemini-2.0-flash",          # Rápido e Eficiente
            "models/gemini-2.5-pro",            # Alta Precisão
            "models/gemini-1.5-pro"             # Backup
        ]
    )
    
    st.caption(f"Engine: {modelo_selecionado.split('/')[-1]}")
    
    st.markdown("---")
    # IPDA exige precisão cirúrgica. Temperatura baixa é obrigatória.
    temperatura = st.slider("Algorithm Variance (Temp)", 0.0, 1.0, 0.1)
    
    ativo_tipo = st.selectbox(
        "Target Asset:",
        ["Synthetic Indices (V75, Crash, Boom)", "Forex (IPDA Standard)", "XAUUSD (Gold Algo)", "Crypto"]
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
            return f"⏳ Rate Limit Hit on {modelo_nome}. Switch to a 'Flash' model."
        elif "404" in erro:
            return f"⚠️ Model Not Found. Update requirements.txt."
        else:
            return f"⛔ System Error: {erro}"

# --- INTERFACE ---
st.title(f"🧩 IPDA Decoder: {modelo_selecionado.split('/')[-1]}")
st.markdown("##### Interbank Price Delivery Algorithm - Surgical Strike System")

col1, col2, col3 = st.columns(3)
imagens_para_analise = []

with col1:
    st.caption("1. Macro Narrative (DNA)")
    img1 = st.file_uploader("HTF (H4/Daily)", type=["jpg", "png", "jpeg"], key="img1")
    if img1:
        pil_img1 = Image.open(img1)
        st.image(pil_img1, use_container_width=True)
        imagens_para_analise.append(pil_img1)

with col2:
    st.caption("2. Fractal Alignment (Flow)")
    img2 = st.file_uploader("MTF (H1/M30)", type=["jpg", "png", "jpeg"], key="img2")
    if img2:
        pil_img2 = Image.open(img2)
        st.image(pil_img2, use_container_width=True)
        imagens_para_analise.append(pil_img2)

with col3:
    st.caption("3. Execution Trigger (Micro)")
    img3 = st.file_uploader("LTF (M5/M1)", type=["jpg", "png", "jpeg"], key="img3")
    if img3:
        pil_img3 = Image.open(img3)
        st.image(pil_img3, use_container_width=True)
        imagens_para_analise.append(pil_img3)

if st.button("RUN ALGORITHMIC SIMULATION"):
    if not api_key:
        st.error("🔒 Access Denied: Missing API Key.")
    elif len(imagens_para_analise) == 0:
        st.warning("⚠️ Data Missing: Upload charts to decode the algorithm.")
    else:
        with st.spinner(f'Decoding Market Maker Script with {modelo_selecionado}...'):
            
            # --- SEU NOVO PROMPT IPDA (COMPLETO) ---
            prompt = f"""
            Role: You are the Interbank Price Delivery Algorithm (IPDA) Specialist & Senior Quantitative Engineer. 
            Your purpose is to deconstruct {ativo_tipo} by identifying the underlying "Market Maker Script." 
            You do not predict; you decode the algorithm's next high-probability draw on liquidity.

            Objective: Analyze the provided chart images (Image 1=Macro, Image 2=Flow, Image 3=Trigger) and cross-reference them with real-time algorithmic behavioral patterns to deliver a Surgical Strike Entry.

            1. Advanced Algorithmic Investigation (Real-Time Simulation)
            - Signature Analysis: Investigate the specific "Asset DNA." (e.g., If V75, look for high-frequency stop runs. If Boom 1000, analyze the "Base Consolidation" preceding the spike).
            - Time-Price Distortion: Analyze the current price action relative to the "Look-back Period" (20, 40, 60 periods). Is the algorithm currently seeking Market Efficiency or Liquidity Expansion?
            - Volume Proxy: Since there is no centralized volume, you must analyze "Candle Displacement." Large, impulsive candles (displacement) indicate Institutional Sponsorship. Small, overlapping candles indicate Retail Noise.

            2. Deep-Dive Analytical Layers (No-Gap Protocol)
            - Fractal Convergence: You must verify that the H4 Market Structure, the H1 Order Flow, and the M15 Execution Trigger are all aligned. If there is a "Fractal Divergence," the setup is discarded.
            - The Invalidation Hard-Point: Identify the exact micro-pip where the "Institutional Narrative" fails. This is your Stop Loss—it must be non-negotiable and mathematically sound.
            - Inducement vs. True Break: Differentiate between a "Fake-out" (Liquidity Grab) and a "Break of Structure" (BOS). You are strictly forbidden from entering before a Liquidity Sweep has occurred.

            3. Surgical Execution Report (Ultra-Professional)
            
            [I. ALGORITHMIC STATE DIAGNOSIS]
            Asset DNA: [e.g., V100 - High Momentum / Low Mean Reversion]
            IPDA Phase: [Expansion / Retracement / Reversal / Consolidation]
            Liquidity Draw: [Where is the algorithm "programmed" to go next? Identify BSL/SSL]

            [II. HIGH-PRECISION ENTRY ARCHITECTURE]
            The Killzone Entry: [Exact Price or Narrow Range]
            The "Insurance" Stop Loss: [Price + Technical Justification]
            Take Profit 1 (Liquidity Hunt): [First structural target]
            Take Profit 2 (Algorithmic Extension): [Final projection target]
            Risk-to-Reward Ratio: [Must be 1:5 or higher for A+ setups]

            [III. CONFLUENCE MATRIX (The "Why")]
            Structure: [Confirmed BOS/MSS with Body Close]
            Efficiency: [FVG / Order Block / Mitigation Block identified]
            Liquidity: [Previous "Retail Trap" successfully swept]
            Momentum: [RSI/Price Divergence or Displacement confirmed]

            [IV. REAL-TIME WARNINGS]
            "No-Trade" Conditions: [e.g., Price is in "Equilibrium," Choppy PA, or Inducement not yet taken]
            Probability Score: [X/10] - Only 9/10 or 10/10 should be executed.

            4. Execution Commands for the AI (The "Enforcer"):
            - "Run a simulated backtest of the last 5 similar patterns on this asset before confirming the entry."
            - "Identify if the current price is inside a 'Premium Array' seeking 'Discount' or vice versa."
            - "If the setup is 100% precise, provide the 'Sniper Entry.' If it is 99% precise, explain what is missing."
            """
            
            resultado = analisar_grafico(imagens_para_analise, prompt, api_key, temperatura, modelo_selecionado)
            
            if "No-Trade" in resultado and "Conditions: Active" in resultado:
                 st.warning("⚠️ Algoritmo detectou condições adversas. Aguarde.")
            
            st.success("Algorithmic Pattern Decoded")
            st.markdown(resultado)
