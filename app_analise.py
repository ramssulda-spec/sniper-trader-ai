import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# --- CARREGAR SENHAS ---
load_dotenv()
chave_secreta_env = os.getenv("API_KEY")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sniper Flash V14", page_icon="⚡", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        height: 4em;
        font-weight: bold;
        font-size: 20px;
        border-radius: 8px;
        border: none;
    }
    [data-testid='stFileUploader'] {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚡ Sniper Rápido")
    
    if chave_secreta_env:
        st.success("✅ Conectado")
        api_key = chave_secreta_env
    else:
        api_key = st.text_input("Cole sua API Key:", type="password")
    
    st.markdown("---")
    temperatura = st.slider("Criatividade", 0.0, 1.0, 0.4)
    estilo = st.selectbox("Modo:", ["Day Trade", "Scalping", "Swing"])
    st.caption("Rodando exclusivamente em Gemini 1.5 Flash")

# --- FUNÇÃO DE ANÁLISE ---
def analisar_grafico(lista_imagens, prompt, api_key, temp):
    try:
        genai.configure(api_key=api_key)
        generation_config = {"temperature": temp}
        conteudo = [prompt] + lista_imagens
        
        # AQUI ESTÁ A CORREÇÃO: Usamos o nome exato e oficial
        model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)
        
        response = model.generate_content(conteudo)
        return response.text

    except Exception as e:
        erro = str(e)
        if "429" in erro:
            return "⛔ Erro de Cota: O Google limitou sua velocidade. Espere 1 minuto e tente de novo."
        elif "404" in erro:
            return "⚠️ Erro de Versão: O servidor não achou o modelo. Atualize o requirements.txt."
        else:
            return f"Erro Técnico: {erro}"

# --- INTERFACE ---
st.title("⚡ Sniper: Análise Ilimitada")
st.markdown("##### Versão leve para evitar bloqueios de API")

col1, col2, col3 = st.columns(3)
imagens_para_analise = []

with col1:
    st.caption("1. Macro")
    img1 = st.file_uploader("Upload Macro", type=["jpg", "png", "jpeg"], key="img1")
    if img1:
        pil_img1 = Image.open(img1)
        st.image(pil_img1, use_container_width=True)
        imagens_para_analise.append(pil_img1)

with col2:
    st.caption("2. Padrão")
    img2 = st.file_uploader("Upload Padrão", type=["jpg", "png", "jpeg"], key="img2")
    if img2:
        pil_img2 = Image.open(img2)
        st.image(pil_img2, use_container_width=True)
        imagens_para_analise.append(pil_img2)

with col3:
    st.caption("3. Gatilho")
    img3 = st.file_uploader("Upload Gatilho", type=["jpg", "png", "jpeg"], key="img3")
    if img3:
        pil_img3 = Image.open(img3)
        st.image(pil_img3, use_container_width=True)
        imagens_para_analise.append(pil_img3)

if st.button("🔎 ANALISAR"):
    if not api_key:
        st.error("🔒 Sem API Key.")
    elif len(imagens_para_analise) == 0:
        st.warning("⚠️ Suba pelo menos 1 imagem.")
    else:
        with st.spinner('Analisando...'):
            prompt = f"""
            Trader: {estilo}.
            Analise as imagens.
            
            # ⚡ SINAL
            **AÇÃO:** [COMPRA/VENDA]
            **RISCO:** [🟢/🟡/🔴]
            ---
            🔵 **ENTRADA:** [Preço]
            🔴 **STOP:** [Preço]
            🟢 **ALVO:** [Preço]
            ---
            📝 **Motivo:** [1 Frase]
            """
            
            resultado = analisar_grafico(imagens_para_analise, prompt, api_key, temperatura)
            
            if "⛔" in resultado or "⚠️" in resultado:
                st.error(resultado)
            else:
                st.success("Sinal Gerado!")
                st.markdown(resultado)