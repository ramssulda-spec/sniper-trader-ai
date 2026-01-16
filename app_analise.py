import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# --- CARREGAR SENHAS ---
load_dotenv()
chave_secreta_env = os.getenv("API_KEY")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sniper G3 - Next Gen", page_icon="🧬", layout="wide")

# --- CSS ---
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
    st.header("🧬 Sniper Gemini 3")
    
    if chave_secreta_env:
        st.success("✅ Conectado")
        api_key = chave_secreta_env
    else:
        api_key = st.text_input("Cole sua API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 🧠 Cérebro da IA")
    
    # A LISTA ATUALIZADA COM OS NOVOS MODELOS QUE VOCÊ DESCOBRIU
    modelo_selecionado = st.selectbox(
        "Selecione a Tecnologia:",
        [
            "models/gemini-3-pro-preview",      # 🚀 O MAIS NOVO E PODEROSO
            "models/gemini-3-flash-preview",    # ⚡ O MAIS RÁPIDO DA GERAÇÃO 3
            "models/gemini-2.5-pro",            # Versão 2.5 Pro (Intermediário)
            "models/gemini-2.0-flash",          # O Padrão Ouro (Estável)
            "models/gemini-2.0-flash-lite",     # Ultra Leve
            "models/gemini-1.5-flash"           # O Clássico (Backup)
        ]
    )
    
    st.caption(f"Motor Ativo: {modelo_selecionado.replace('models/', '')}")
    
    st.markdown("---")
    temperatura = st.slider("Agressividade", 0.0, 1.0, 0.4)
    estilo = st.selectbox("Modo:", ["Day Trade", "Scalping", "Swing"])

# --- FUNÇÃO DE ANÁLISE ---
def analisar_grafico(lista_imagens, prompt, api_key, temp, modelo_nome):
    try:
        genai.configure(api_key=api_key)
        generation_config = {"temperature": temp}
        conteudo = [prompt] + lista_imagens
        
        # Chama o modelo escolhido na lista
        model = genai.GenerativeModel(modelo_nome, generation_config=generation_config)
        
        response = model.generate_content(conteudo)
        return response.text

    except Exception as e:
        erro = str(e)
        if "404" in erro:
            return f"⛔ O modelo {modelo_nome} não foi encontrado. Tente atualizar o requirements.txt ou escolha outro na lista."
        elif "429" in erro:
            return f"⏳ Cota excedida para {modelo_nome}. Escolha um modelo 'Flash' ou 'Lite' na lista!"
        else:
            return f"Erro Técnico: {erro}"

# --- INTERFACE ---
st.title(f"🧬 Sniper: {modelo_selecionado.split('/')[-1]}")
st.markdown("##### Testando a nova geração de Inteligência Artificial no Trading.")

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

if st.button("🧬 ANALISAR COM GEMINI 3"):
    if not api_key:
        st.error("🔒 Sem API Key.")
    elif len(imagens_para_analise) == 0:
        st.warning("⚠️ Suba pelo menos 1 imagem.")
    else:
        with st.spinner(f'Consultando o oráculo ({modelo_selecionado})...'):
            prompt = f"""
            Trader: {estilo}.
            Analise as imagens com profundidade máxima.
            
            # 🧬 SINAL G3
            **AÇÃO:** [COMPRA/VENDA]
            **CONFIANÇA:** [0-100%]
            **RISCO:** [🟢/🟡/🔴]
            ---
            🔵 **ENTRADA:** [Preço]
            🔴 **STOP:** [Preço]
            🟢 **ALVO:** [Preço]
            ---
            📝 **Motivo:** [1 Frase]
            """
            
            resultado = analisar_grafico(imagens_para_analise, prompt, api_key, temperatura, modelo_selecionado)
            
            if "⛔" in resultado or "⏳" in resultado:
                st.error(resultado)
            else:
                st.success("Sinal Gerado!")
                st.markdown(resultado)