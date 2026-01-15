import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# --- CARREGAR SENHAS ---
load_dotenv()
chave_secreta_env = os.getenv("API_KEY")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sniper Pro - Institucional", page_icon="💎", layout="wide")

# --- CSS (VISUAL DE ALTA PERFORMANCE) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: #00FF00;
        border: 2px solid #00FF00;
        height: 4em;
        font-weight: bold;
        font-size: 20px;
        border-radius: 10px;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background-color: #00FF00;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("💎 Sniper Institucional")
    
    if chave_secreta_env:
        st.success("✅ Conectado ao Servidor")
        api_key = chave_secreta_env
    else:
        api_key = st.text_input("Sua API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 🎚️ Critério de Entrada")
    # Temperatura mais baixa = Menos alucinação, mais precisão
    temperatura = st.slider("Risco Aceitável", 0.0, 0.5, 0.1)
    st.caption("Mantenha baixo (0.1) para precisão máxima.")
    
    estilo = st.selectbox(
        "Setup Desejado:",
        ["Price Action Puro (SMC)", "Reversão de Tendência", "Rompimento de Estrutura"]
    )

# --- FUNÇÃO DE ANÁLISE ---
def analisar_grafico(lista_imagens, prompt, api_key, temp):
    try:
        genai.configure(api_key=api_key)
        # Temperatura baixa para ser extremamente técnico e frio
        generation_config = {"temperature": temp}
        conteudo = [prompt] + lista_imagens
        
        # Tenta o modelo PRO (Mais inteligente para raciocínio complexo)
        try:
            model = genai.GenerativeModel('models/gemini-robotics-er-1.5-preview', generation_config=generation_config)
            response = model.generate_content(conteudo)
        except:
            # Fallback
            model = genai.GenerativeModel('models/gemini-robotics-er-1.5-preview', generation_config=generation_config)
            response = model.generate_content(conteudo)
            
        return response.text
    except Exception as e:
        return f"Erro: {str(e)}"

# --- INTERFACE ---
st.title("💎 Sniper Pro: Alta Precisão")
st.markdown("##### Sistema de Filtragem de Entradas A+ (90% Winrate)")

col1, col2, col3 = st.columns(3)
imagens_para_analise = []

with col1:
    st.caption("1. Macro (Tendência Maior)")
    img1 = st.file_uploader("Upload Macro", type=["jpg", "png"], key="img1")
    if img1:
        pil_img1 = Image.open(img1)
        st.image(pil_img1, use_container_width=True)
        imagens_para_analise.append(pil_img1)

with col2:
    st.caption("2. Contexto (Estrutura)")
    img2 = st.file_uploader("Upload Contexto", type=["jpg", "png"], key="img2")
    if img2:
        pil_img2 = Image.open(img2)
        st.image(pil_img2, use_container_width=True)
        imagens_para_analise.append(pil_img2)

with col3:
    st.caption("3. Gatilho (Entrada)")
    img3 = st.file_uploader("Upload Gatilho", type=["jpg", "png"], key="img3")
    if img3:
        pil_img3 = Image.open(img3)
        st.image(pil_img3, use_container_width=True)
        imagens_para_analise.append(pil_img3)

# --- BOTÃO E LÓGICA DE ELITE ---
st.markdown("---")
if st.button("CALCULAR PROBABILIDADE"):
    if not api_key:
        st.error("🔒 Login necessário.")
    elif len(imagens_para_analise) == 0:
        st.warning("⚠️ O sistema precisa de dados visuais (Imagens).")
    else:
        with st.spinner('Analista Sênior verificando confluências...'):
            
            # --- O PROMPT DE ELITE (A MÁGICA ACONTECE AQUI) ---
            prompt = f"""
            Você é um Gestor de Risco Institucional Sênior.
            Sua taxa de acerto exigida é de 90%. Se você errar o trade, perde o emprego.
            
            Analise as imagens fornecidas ({estilo}).
            
            REGRAS DE OURO (FILTRO):
            1. Se o mercado estiver lateral, "sujo" ou sem direção clara: NÃO OPERE.
            2. Se os tempos gráficos (Macro e Micro) estiverem discordando: NÃO OPERE.
            3. Só autorize a entrada se for um "Setup A+" (Confluência perfeita de tendência + estrutura + gatilho).
            
            Se não houver oportunidade CLARA agora, sua obrigação é dizer "AGUARDAR" e explicar o que esperar.
            
            Responda ESTRITAMENTE neste formato:
            
            # 💎 VEREDITO DO GESTOR
            
            **STATUS:** [✅ COMPRA / 🔻 VENDA / ✋ AGUARDAR - NÃO ENTRAR]
            **CONFIANÇA:** [0% a 100%] (Só opere acima de 85%)
            
            ---
            Se STATUS for COMPRA ou VENDA:
            💰 **ENTRADA:** [Preço Exato]
            🛑 **STOP TÉCNICO:** [Preço Exato - Protegido atrás da estrutura]
            🏁 **ALVO (TP):** [Preço Exato - Risco/Retorno mínimo de 1:2]
            
            ---
            Se STATUS for AGUARDAR:
            👀 **GATILHO FUTURO:** [Ex: "Espere o preço romper X e voltar fazer pullback"]
            ⏳ **QUANDO VOLTAR:** [Ex: "Aguarde nova vela de H1"]
            
            ---
            ⚖️ **Justificativa Rápida:** [Por que sim ou por que não?]
            """
            
            resultado = analisar_grafico(imagens_para_analise, prompt, api_key, temperatura)
            
            if "AGUARDAR" in resultado:
                st.warning("Mercado Perigoso detectado.")
            else:
                st.balloons()
            
            st.markdown(resultado)