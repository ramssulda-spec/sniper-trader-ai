import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# --- CARREGAR SENHAS ---
load_dotenv()
chave_secreta_env = os.getenv("API_KEY")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sniper Pro - Manual", page_icon="🎯", layout="wide")

# --- CSS (ESTILO DARK PRO) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #00D100; /* Verde Profit */
        color: white;
        height: 4em;
        font-weight: bold;
        font-size: 20px;
        border-radius: 8px;
        border: none;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background-color: #00a800;
        box-shadow: 0px 0px 15px #00ff00;
    }
    /* Deixa a área de upload mais visível */
    [data-testid='stFileUploader'] {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🦅 Sniper Pro Manual")
    
    if chave_secreta_env:
        st.success("✅ Sistema Conectado")
        api_key = chave_secreta_env
    else:
        api_key = st.text_input("Cole sua API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 🎚️ Calibragem")
    
    # 0.4 é o ponto ideal entre criatividade e precisão para o modelo "Hunter"
    temperatura = st.slider("Agressividade", 0.0, 1.0, 0.4)
    
    estilo = st.selectbox(
        "Modo Operacional:",
        ["Day Trade (Intraday)", "Scalping (Rápido)", "Swing Trade (Longo)"]
    )
    
    st.info("ℹ️ Sistema focado em análise visual pura. Suba seus prints do TradingView.")

# --- FUNÇÃO DE ANÁLISE ---
def analisar_grafico(lista_imagens, prompt, api_key, temp):
    try:
        genai.configure(api_key=api_key)
        generation_config = {"temperature": temp}
        conteudo = [prompt] + lista_imagens
        
        # Tenta o modelo PRO (Melhor raciocínio visual)
        try:
            model = genai.GenerativeModel('models/gemini-robotics-er-1.5-preview', generation_config=generation_config)
            response = model.generate_content(conteudo)
        except:
            # Se falhar, usa o Flash (Backup rápido)
            model = genai.GenerativeModel('models/gemini-robotics-er-1.5-preview', generation_config=generation_config)
            response = model.generate_content(conteudo)
            
        return response.text
    except Exception as e:
        return f"Erro de Conexão: {str(e)}"

# --- INTERFACE PRINCIPAL ---
st.title("🎯 Sniper Pro: Análise Visual")
st.markdown("##### Envie os prints dos tempos gráficos para triangulação de sinal.")

col1, col2, col3 = st.columns(3)
imagens_para_analise = []

# COLUNA 1 - MACRO
with col1:
    st.markdown("### 1️⃣ Tendência (Macro)")
    st.caption("Ex: Diário ou H4")
    img1 = st.file_uploader("Upload Macro", type=["jpg", "png", "jpeg"], key="img1")
    if img1:
        pil_img1 = Image.open(img1)
        st.image(pil_img1, use_container_width=True)
        imagens_para_analise.append(pil_img1)

# COLUNA 2 - ESTRUTURA
with col2:
    st.markdown("### 2️⃣ Padrão (Médio)")
    st.caption("Ex: H1 ou M15")
    img2 = st.file_uploader("Upload Padrão", type=["jpg", "png", "jpeg"], key="img2")
    if img2:
        pil_img2 = Image.open(img2)
        st.image(pil_img2, use_container_width=True)
        imagens_para_analise.append(pil_img2)

# COLUNA 3 - GATILHO
with col3:
    st.markdown("### 3️⃣ Gatilho (Micro)")
    st.caption("Ex: M5 ou M1")
    img3 = st.file_uploader("Upload Gatilho", type=["jpg", "png", "jpeg"], key="img3")
    if img3:
        pil_img3 = Image.open(img3)
        st.image(pil_img3, use_container_width=True)
        imagens_para_analise.append(pil_img3)

# --- BOTÃO DE AÇÃO ---
st.markdown("---")
if st.button("🔎 ANALISAR OPORTUNIDADE"):
    if not api_key:
        st.error("🔒 API Key não encontrada na barra lateral ou .env")
    elif len(imagens_para_analise) == 0:
        st.warning("⚠️ Você precisa subir pelo menos 1 imagem para análise.")
    else:
        with st.spinner('O Sniper está analisando a confluência dos gráficos...'):
            
            # --- PROMPT V10: O ESPECÍFICO ---
            prompt = f"""
            Aja como um Trader Profissional de Elite ({estilo}).
            Analise as imagens fornecidas. Use a lógica "Top-Down" (Do tempo maior para o menor).
            
            Sua tarefa é encontrar a MELHOR oportunidade de trade presente AGORA.
            Não quero explicações longas. Quero os dados para a boleta.
            
            Responda ESTRITAMENTE neste formato:
            
            # ⚡ SINAL DETECTADO
            
            **AÇÃO:** [COMPRA 🐂 / VENDA 🐻]
            
            **RISCO TÉCNICO:** [ESCOLHA UM:]
            - 🟢 **BAIXO** (Confluência total)
            - 🟡 **MÉDIO** (Contra tendência macro ou sem pullback)
            - 🔴 **ALTO** (Trade de risco/contra fluxo)
            
            ---
            🔵 **ENTRADA:** [Preço Exato ou Região Visual]
            🔴 **STOP LOSS:** [Preço Exato]
            🟢 **TAKE PROFIT:** [Preço Exato]
            ---
            
            📝 **Checklist Rápido:**
            1. **Tendência Macro:** [Alta/Baixa/Lateral]
            2. **Gatilho:** [Ex: Rompimento de Pivô]
            3. **Alerta:** [O que pode dar errado?]
            """
            
            resultado = analisar_grafico(imagens_para_analise, prompt, api_key, temperatura)
            
            st.success("Sinal Gerado com Sucesso!")
            st.markdown(resultado)