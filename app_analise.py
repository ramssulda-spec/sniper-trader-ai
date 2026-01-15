import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# --- CARREGAR SENHAS DO ARQUIVO .ENV ---
load_dotenv()
# Mude a linha 9 para isso:
chave_secreta_env = "AIzaSyDWlprue_h8ebH0XqfSP_wXdyKZHG1vvDw"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sniper Trader AI", page_icon="🎯", layout="wide")

# --- CSS (ESTILO) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        height: 3em;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (CONFIGURAÇÕES) ---
with st.sidebar:
    st.header("⚙️ Centro de Comando")
    
    # LÓGICA INTELIGENTE DE LOGIN
    if chave_secreta_env:
        st.success("✅ Chave API Carregada!")
        api_key = chave_secreta_env
    else:
        api_key = st.text_input("Cole sua API Key:", type="password")
        if not api_key:
            st.warning("⚠️ Crie um arquivo .env para não precisar digitar sempre.")
    
    st.markdown("---")
    st.markdown("### 🎚️ Calibragem")
    
    # 1. Slider de Temperatura
    temperatura = st.slider("Agressividade da IA", 0.0, 1.0, 0.2) 
    st.caption("0.0 = Conservador | 1.0 = Arriscado")

    # 2. Seletor de Estratégia
    st.markdown("### 🧠 Estratégia")
    modo_operacao = st.selectbox(
        "Selecione o Estilo:",
        ["Day Trade (Padrão)", "Scalping (Rápido)", "Swing Trade (Longo)", "Reversão (Topo/Fundo)"]
    )

# --- FUNÇÃO DE ANÁLISE ---
def analisar_grafico(image, prompt, api_key, temp):
    try:
        genai.configure(api_key=api_key)
        generation_config = {"temperature": temp}
        
        # Tenta modelo PRO, se falhar vai de FLASH
        try:
            model = genai.GenerativeModel('models/gemini-robotics-er-1.5-preview', generation_config=generation_config)
            response = model.generate_content([prompt, image])
        except:
            model = genai.GenerativeModel('models/gemini-robotics-er-1.5-preview', generation_config=generation_config)
            response = model.generate_content([prompt, image])
            
        return response.text
    except Exception as e:
        return f"Erro na API: {str(e)}"

# --- INTERFACE PRINCIPAL ---
st.title("🎯 Sniper Trader AI")
st.markdown(f"##### Modo Ativo: **{modo_operacao}**")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("1. Gráfico")
    uploaded_file = st.file_uploader("Arraste o print aqui...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='Analisando...', use_container_width=True)

with col2:
    st.subheader("2. Sinal")
    
    if uploaded_file and st.button("🚀 GERAR SINAL"):
        if not api_key:
            st.error("🔒 API Key ausente! Verifique o .env ou a barra lateral.")
        else:
            with st.spinner(f'Calculando setup para {modo_operacao}...'):
                
                # --- LÓGICA DE PROMPT DINÂMICO ---
                detalhe_estrategia = ""
                if "Scalping" in modo_operacao:
                    detalhe_estrategia = "Foque em movimentos curtos de M1/M5. Stop Loss curto. Alvos rápidos (1:1)."
                elif "Swing" in modo_operacao:
                    detalhe_estrategia = "Ignore ruídos. Busque tendências de H4/D1. Alvos longos (1:3+)."
                elif "Reversão" in modo_operacao:
                    detalhe_estrategia = "Busque divergências (RSI), exaustão, Dojis em zonas extremas e falhas de rompimento."
                else:
                    detalhe_estrategia = "Setup padrão de continuidade ou correção. Melhor oportunidade visível."

                prompt = f"""
                Aja como um Trader Profissional operando no estilo: {modo_operacao}.
                Instrução Tática: {detalhe_estrategia}
                
                Analise a imagem. Não explique o básico. Vá direto aos dados de entrada.
                
                Responda ESTRITAMENTE neste formato visual:
                
                # ⚡ SINAL: {modo_operacao.upper()}
                
                **SENTIMENTO:** [ALTA 🐂 / BAIXA 🐻 / NEUTRO 💤]
                
                ---
                🔵 **ENTRADA:** [Preço ou Região Exata]
                🔴 **STOP LOSS:** [Preço que invalida a tese]
                🟢 **TAKE PROFIT:** [Preço Alvo]
                ---
                
                🎯 **Motivo Técnico:** [Resumo em 1 frase]
                ⚖️ **Risco/Retorno:** [Ex: 1 para 3]
                """
                
                resultado = analisar_grafico(image, prompt, api_key, temperatura)
                
                st.info("Sinal Gerado")
                st.markdown(resultado)