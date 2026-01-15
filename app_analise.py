import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# --- CARREGAR SENHAS ---
load_dotenv()
chave_secreta_env = os.getenv("API_KEY")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sniper AI - MultiTimeframe", page_icon="🦅", layout="wide")

# --- CSS PERSONALIZADO ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #00D100;
        color: white;
        height: 3.5em;
        font-weight: bold;
        font-size: 18px;
        border-radius: 10px;
    }
    .uploaded-img { border: 2px solid #333; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🦅 Centro de Comando")
    
    # Login Automático
    if chave_secreta_env:
        st.success("✅ Sistema Online (.env)")
        api_key = chave_secreta_env
    else:
        api_key = st.text_input("Cole sua API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 🎚️ Configuração")
    temperatura = st.slider("Criatividade da IA", 0.0, 1.0, 0.1)
    
    estilo = st.selectbox(
        "Estilo de Operação:",
        ["Day Trade (Padrão)", "Scalping (Agressivo)", "Swing Trade (Longo)"]
    )
    
    st.info("💡 Dica: Para maior precisão, faça upload de pelo menos 2 tempos gráficos (Ex: H1 e M5).")

# --- FUNÇÃO DE ANÁLISE (AGORA ACEITA LISTA DE IMAGENS) ---
def analisar_multi_graficos(lista_imagens, prompt, api_key, temp):
    try:
        genai.configure(api_key=api_key)
        generation_config = {"temperature": temp}
        
        # Monta o pacote de dados para enviar (Texto + Imagem 1 + Imagem 2...)
        conteudo = [prompt] + lista_imagens
        
        try:
            model = genai.GenerativeModel('models/gemini-robotics-er-1.5-preview', generation_config=generation_config)
            response = model.generate_content(conteudo)
        except:
            model = genai.GenerativeModel('models/gemini-robotics-er-1.5-preview', generation_config=generation_config)
            response = model.generate_content(conteudo)
            
        return response.text
    except Exception as e:
        return f"Erro Crítico: {str(e)}"

# --- INTERFACE PRINCIPAL ---
st.title("🦅 Sniper AI: Multi-Timeframe")
st.markdown("##### Análise de Confluência (Top-Down Analysis)")

# ÁREA DE UPLOAD (3 COLUNAS)
col1, col2, col3 = st.columns(3)

imagens_para_analise = []
legendas_contexto = []

with col1:
    st.markdown("### 1️⃣ Macro (Tendência)")
    st.caption("Ex: Diário ou H4")
    img1 = st.file_uploader("Upload Macro", type=["jpg", "png"], key="img1")
    if img1:
        pil_img1 = Image.open(img1)
        st.image(pil_img1, use_container_width=True)
        imagens_para_analise.append(pil_img1)
        legendas_contexto.append("IMAGEM 1 (VISÃO MACRO/TENDÊNCIA)")

with col2:
    st.markdown("### 2️⃣ Estrutura (Padrão)")
    st.caption("Ex: H1 ou M15")
    img2 = st.file_uploader("Upload Médio", type=["jpg", "png"], key="img2")
    if img2:
        pil_img2 = Image.open(img2)
        st.image(pil_img2, use_container_width=True)
        imagens_para_analise.append(pil_img2)
        legendas_contexto.append("IMAGEM 2 (ESTRUTURA/CORREÇÃO)")

with col3:
    st.markdown("### 3️⃣ Gatilho (Entrada)")
    st.caption("Ex: M5 ou M1")
    img3 = st.file_uploader("Upload Micro", type=["jpg", "png"], key="img3")
    if img3:
        pil_img3 = Image.open(img3)
        st.image(pil_img3, use_container_width=True)
        imagens_para_analise.append(pil_img3)
        legendas_contexto.append("IMAGEM 3 (GATILHO DE ENTRADA FINA)")

# --- BOTÃO E LÓGICA ---
st.markdown("---")
if st.button("🚀 ANALISAR CONFLUÊNCIA"):
    if not api_key:
        st.error("🔒 Sem API Key!")
    elif len(imagens_para_analise) == 0:
        st.warning("⚠️ Faça upload de pelo menos 1 gráfico.")
    else:
        with st.spinner(f'Cruzando dados de {len(imagens_para_analise)} tempos gráficos...'):
            
            # PROMPT PODEROSO DE CONFLUÊNCIA
            prompt = f"""
            Você é um Analista Institucional Sênior operando {estilo}.
            Você recebeu {len(imagens_para_analise)} imagens sequenciais do MESMO ativo em tempos gráficos diferentes (Top-Down Analysis).
            
            CONTEXTO DAS IMAGENS:
            {legendas_contexto}
            
            SUA MISSÃO:
            1. Analise a Imagem Macro para definir se somos COMPRADORES ou VENDEDORES.
            2. Analise a Imagem de Estrutura para ver se o preço está barato ou caro.
            3. Analise a Imagem de Gatilho para achar o ponto exato.
            
            Regra de Ouro: Se a tendência Macro for Alta, ignore sinais de venda no Micro (e vice-versa), a menos que seja uma reversão clara.
            
            Responda neste Formato (Use Markdown):
            
            # 🦅 RELATÓRIO DE CONFLUÊNCIA
            
            ### 1. Leitura de Cenário
            * **Macro:** [Resumo curto]
            * **Micro:** [Resumo curto]
            * **Conclusão:** Os tempos gráficos estão alinhados? (Sim/Não)
            
            ---
            # 💣 SINAL FINAL: [{estilo.upper()}]
            
            **VIÉS:** [COMPRA 🐂 / VENDA 🐻 / AGUARDAR ✋]
            **(Probabilidade Estimada: 0-100%)**
            
            🔵 **ENTRADA:** [Preço/Região no gráfico menor]
            🔴 **STOP LOSS:** [Técnico]
            🟢 **TAKE PROFIT:** [Alvo na estrutura maior]
            
            📉 **Racional:** [Explique porque alinhou os tempos gráficos]
            """
            
            resultado = analisar_multi_graficos(imagens_para_analise, prompt, api_key, temperatura)
            
            st.success("Análise Finalizada!")
            st.markdown(resultado)