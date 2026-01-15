import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# --- CARREGAR SENHAS ---
load_dotenv()
chave_secreta_env = os.getenv("API_KEY")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sniper AI - Hunter", page_icon="🦅", layout="wide")

# --- CSS (ESTILO AGRESSIVO) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #0056b3; /* Azul Profissional */
        color: white;
        height: 4em;
        font-weight: bold;
        font-size: 20px;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #004494;
    }
    .big-font { font-size:20px !important; }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🦅 Modo Caçador")
    
    if chave_secreta_env:
        st.success("✅ Sistema Ativo")
        api_key = chave_secreta_env
    else:
        api_key = st.text_input("Sua API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 🎯 Perfil Operacional")
    
    # Agora a temperatura padrão é 0.4 para permitir que ela "enxergue" oportunidades onde o conservador não veria
    temperatura = st.slider("Criatividade / Busca", 0.0, 1.0, 0.4)
    
    estilo = st.selectbox(
        "Estilo de Trade:",
        ["Day Trade (Intraday)", "Scalping (Tiro Curto)", "Swing (Tendência)"]
    )
    
    st.info("ℹ️ O sistema sempre buscará um sinal, classificando o risco para você decidir.")

# --- FUNÇÃO DE ANÁLISE ---
def analisar_grafico(lista_imagens, prompt, api_key, temp):
    try:
        genai.configure(api_key=api_key)
        generation_config = {"temperature": temp}
        conteudo = [prompt] + lista_imagens
        
        # Tenta o modelo PRO (Melhor raciocínio)
        try:
            model = genai.GenerativeModel('models/gemini-robotics-er-1.5-preview', generation_config=generation_config)
            response = model.generate_content(conteudo)
        except:
            model = genai.GenerativeModel('models/gemini-robotics-er-1.5-preview', generation_config=generation_config)
            response = model.generate_content(conteudo)
            
        return response.text
    except Exception as e:
        return f"Erro: {str(e)}"

# --- INTERFACE ---
st.title("🦅 Sniper Hunter V7")
st.markdown("##### Detector de Oportunidades com Classificação de Risco")

col1, col2, col3 = st.columns(3)
imagens_para_analise = []

with col1:
    st.caption("1. Tendência (Macro)")
    img1 = st.file_uploader(" ", type=["jpg", "png"], key="img1")
    if img1:
        pil_img1 = Image.open(img1)
        st.image(pil_img1, use_container_width=True)
        imagens_para_analise.append(pil_img1)

with col2:
    st.caption("2. Padrão (Intermediário)")
    img2 = st.file_uploader(" ", type=["jpg", "png"], key="img2")
    if img2:
        pil_img2 = Image.open(img2)
        st.image(pil_img2, use_container_width=True)
        imagens_para_analise.append(pil_img2)

with col3:
    st.caption("3. Gatilho (Entrada)")
    img3 = st.file_uploader(" ", type=["jpg", "png"], key="img3")
    if img3:
        pil_img3 = Image.open(img3)
        st.image(pil_img3, use_container_width=True)
        imagens_para_analise.append(pil_img3)

# --- BOTÃO E LÓGICA DE CAÇADOR ---
st.markdown("---")
if st.button("🔎 LOCALIZAR MELHOR ENTRADA"):
    if not api_key:
        st.error("🔒 Faça login na barra lateral.")
    elif len(imagens_para_analise) == 0:
        st.warning("⚠️ O gráfico é necessário para a análise.")
    else:
        with st.spinner('Varrendo o gráfico em busca de oportunidades...'):
            
            # --- PROMPT V7: O CAÇADOR DE OPORTUNIDADES ---
            prompt = f"""
            Você é um Trader de Elite Agressivo operando no estilo: {estilo}.
            Sua missão: Encontrar a MELHOR oportunidade de trade presente nestas imagens AGORA.
            
            Não aceito "Aguardar" como resposta principal. Você deve analisar a estrutura atual e projetar um trade, mas deve CLASSIFICAR O RISCO HONESTAMENTE.
            
            Analise a confluência entre Macro e Micro.
            
            Gere o sinal neste formato ESTRITO:
            
            # ⚡ OPORTUNIDADE DETECTADA
            
            **SINAL:** [COMPRA 🐂 / VENDA 🐻]
            
            **NÍVEL DE RISCO:** [ESCOLHA UM:]
            - 🟢 **BAIXO RISCO:** (Confluência total, a favor da tendência)
            - 🟡 **MÉDIO RISCO:** (Trade válido, mas contra tendência macro ou sem pullback)
            - 🔴 **ALTO RISCO:** (Tentativa de adivinhar topo/fundo ou mercado lateral)
            
            ---
            🔵 **ENTRADA:** [Preço Exato]
            🛑 **STOP LOSS:** [Preço Exato]
            🟢 **TAKE PROFIT:** [Preço Exato]
            ---
            
            📝 **Análise Técnica:**
            1. **Por que entrar?** [Motivo técnico direto]
            2. **Onde mora o perigo?** [Explique o fator de risco deste trade específico]
            """
            
            resultado = analisar_grafico(imagens_para_analise, prompt, api_key, temperatura)
            
            st.success("Sinal Gerado!")
            st.markdown(resultado)