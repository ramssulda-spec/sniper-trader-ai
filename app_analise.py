import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# --- CARREGAR SENHAS ---
load_dotenv()
chave_secreta_env = os.getenv("API_KEY")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sniper Pro - Flash", page_icon="⚡", layout="wide")

# --- CSS (ESTILO DARK) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #00D100;
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
    [data-testid='stFileUploader'] {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚡ Sniper Flash")
    
    if chave_secreta_env:
        st.success("✅ Conectado")
        api_key = chave_secreta_env
    else:
        api_key = st.text_input("Cole sua API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 🎚️ Ajustes")
    
    # Temperatura ideal para o Flash ser criativo na busca de sinais
    temperatura = st.slider("Agressividade", 0.0, 1.0, 0.4)
    
    estilo = st.selectbox(
        "Modo:",
        ["Day Trade (Intraday)", "Scalping (Rápido)", "Swing Trade (Longo)"]
    )
    
    st.info("ℹ️ Rodando em Gemini 1.5 Flash (Alta Velocidade e Sem Limites)")

# --- FUNÇÃO DE ANÁLISE ---
def analisar_grafico(lista_imagens, prompt, api_key, temp):
    try:
        genai.configure(api_key=api_key)
        generation_config = {"temperature": temp}
        conteudo = [prompt] + lista_imagens
        
        # AQUI ESTÁ A CORREÇÃO: Forçamos o uso do modelo mais estável e com maior cota
        try:
            model = genai.GenerativeModel('models/gemini-pro-latest', generation_config=generation_config)
            response = model.generate_content(conteudo)
            return response.text
        except Exception as e:
             # Se der erro, tentamos a variação do nome (algumas contas pedem 'models/')
            try:
                model = genai.GenerativeModel('models/gemini-pro-latest', generation_config=generation_config)
                response = model.generate_content(conteudo)
                return response.text
            except Exception as e2:
                return f"⚠️ Erro de API: {str(e2)}. Verifique sua Chave."

    except Exception as e:
        return f"Erro de Conexão: {str(e)}"

# --- INTERFACE PRINCIPAL ---
st.title("⚡ Sniper Pro: Flash Version")
st.markdown("##### Análise Visual de Alta Velocidade")

col1, col2, col3 = st.columns(3)
imagens_para_analise = []

# COLUNA 1 - MACRO
with col1:
    st.caption("1. Macro (Tendência)")
    img1 = st.file_uploader("Upload Macro", type=["jpg", "png", "jpeg"], key="img1")
    if img1:
        pil_img1 = Image.open(img1)
        st.image(pil_img1, use_container_width=True)
        imagens_para_analise.append(pil_img1)

# COLUNA 2 - ESTRUTURA
with col2:
    st.caption("2. Padrão (Estrutura)")
    img2 = st.file_uploader("Upload Padrão", type=["jpg", "png", "jpeg"], key="img2")
    if img2:
        pil_img2 = Image.open(img2)
        st.image(pil_img2, use_container_width=True)
        imagens_para_analise.append(pil_img2)

# COLUNA 3 - GATILHO
with col3:
    st.caption("3. Gatilho (Entrada)")
    img3 = st.file_uploader("Upload Gatilho", type=["jpg", "png", "jpeg"], key="img3")
    if img3:
        pil_img3 = Image.open(img3)
        st.image(pil_img3, use_container_width=True)
        imagens_para_analise.append(pil_img3)

# --- BOTÃO DE AÇÃO ---
st.markdown("---")
if st.button("🔎 ANALISAR AGORA"):
    if not api_key:
        st.error("🔒 Sem API Key.")
    elif len(imagens_para_analise) == 0:
        st.warning("⚠️ Suba pelo menos 1 imagem.")
    else:
        with st.spinner('Processando via Gemini Flash...'):
            
            prompt = f"""
            Você é um Trader Profissional de Elite ({estilo}).
            Analise as imagens (Top-Down).
            
            Encontre a MELHOR oportunidade AGORA.
            Seja direto. Sem textos longos.
            
            Responda ESTRITAMENTE neste formato:
            
            # ⚡ SINAL DETECTADO
            
            **AÇÃO:** [COMPRA 🐂 / VENDA 🐻]
            
            **RISCO:** [🟢 BAIXO / 🟡 MÉDIO / 🔴 ALTO]
            
            ---
            🔵 **ENTRADA:** [Preço/Região]
            🔴 **STOP:** [Preço]
            🟢 **ALVO:** [Preço]
            ---
            
            📝 **Motivo:** 
            """
            
            resultado = analisar_grafico(imagens_para_analise, prompt, api_key, temperatura)
            
            st.success("Sinal Gerado!")
            st.markdown(resultado)