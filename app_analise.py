import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# --- CARREGAR SENHAS ---
load_dotenv()
chave_secreta_env = os.getenv("API_KEY")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sniper Universal", page_icon="🌐", layout="wide")

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
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🌐 Sniper Universal")
    
    if chave_secreta_env:
        st.success("✅ Conectado")
        api_key = chave_secreta_env
    else:
        api_key = st.text_input("Cole sua API Key:", type="password")
    
    st.markdown("---")
    temperatura = st.slider("Criatividade", 0.0, 1.0, 0.4)
    estilo = st.selectbox("Modo:", ["Day Trade", "Scalping", "Swing"])
    st.info("ℹ️ Sistema de Auto-Adaptação de Modelo Ativo")

# --- FUNÇÃO DE ANÁLISE (O SEGREDO ESTÁ AQUI) ---
def analisar_grafico(lista_imagens, prompt, api_key, temp):
    genai.configure(api_key=api_key)
    generation_config = {"temperature": temp}
    conteudo = [prompt] + lista_imagens
    
    # LISTA DE TODOS OS MODELOS POSSÍVEIS (DO NOVO AO ANTIGO)
    # Se um falhar, ele pula para o próximo automaticamente.
    lista_modelos = [
        "gemini-1.5-flash",          # 1. O ideal (Rápido)
        "models/gemini-1.5-flash",   # 2. Variação de nome
        "gemini-1.5-flash-latest",   # 3. Variação de versão
        "gemini-pro",                # 4. O Clássico (Funciona sempre)
        "models/gemini-pro"          # 5. Variação do clássico
    ]
    
    log_erros = []

    for modelo_atual in lista_modelos:
        try:
            # Tenta gerar com o modelo da vez
            model = genai.GenerativeModel(modelo_atual, generation_config=generation_config)
            response = model.generate_content(conteudo)
            
            # Se chegou aqui, funcionou! Retorna o texto e avisa qual modelo usou.
            return f"✅ SUCESSO (Motor usado: {modelo_atual})\n\n" + response.text
            
        except Exception as e:
            # Se falhar, guarda o erro e tenta o próximo
            log_erros.append(f"❌ {modelo_atual}: Falhou ({str(e)})")
            continue

    # Se saiu do loop, é porque NENHUM funcionou
    return f"⛔ ERRO TOTAL. Todos os modelos falharam.\nDetalhes:\n" + "\n".join(log_erros)

# --- INTERFACE ---
st.title("🌐 Sniper: Sistema Universal")
st.markdown("##### Se um modelo falhar, o próximo assume o comando.")

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

if st.button("🔎 ANALISAR AGORA"):
    if not api_key:
        st.error("🔒 Sem API Key.")
    elif len(imagens_para_analise) == 0:
        st.warning("⚠️ Suba pelo menos 1 imagem.")
    else:
        with st.spinner('Testando conexões de IA...'):
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
            
            if "⛔ ERRO TOTAL" in resultado:
                st.error(resultado)
            else:
                st.success("Sinal Gerado!")
                st.markdown(resultado)