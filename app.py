import streamlit as st
from openai import OpenAI

# Sayfa Genişlik ve Kimlik Ayarları
st.set_page_config(
    page_title="Nvidia Open-Source AI Studio", 
    page_icon="🤖",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Stüdyo Kalitesinde Karanlık Tema Tasarımı (CSS)
st.markdown("""
    <style>
    .main { background-color: #0b0d10; color: #e2e8f0; }
    .stTextArea textarea { background-color: #12151c !important; color: #ffffff !important; border: 1px solid #1e293b !important; border-radius: 8px; font-size: 1rem; }
    .stTextInput input { background-color: #12151c !important; color: #ffffff !important; border: 1px solid #1e293b !important; }
    div.stButton > button:first-child { background-color: #10b981; color: white; border-radius: 8px; width: 100%; font-weight: bold; height: 50px; border: none; font-size: 1.1rem; transition: all 0.3s; }
    div.stButton > button:first-child:hover { background-color: #059669; transform: translateY(-2px); }
    .chat-container { background-color: #12151c; padding: 20px; border-radius: 10px; border: 1px solid #1e293b; border-left: 6px solid #10b981; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .reasoning-container { background-color: #181c26; padding: 15px; border-radius: 8px; border: 1px solid #334155; border-left: 4px solid #64748b; font-family: 'Courier New', Courier, monospace; color: #94a3b8; font-size: 0.9rem; margin-bottom: 15px; }
    .studio-header { background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='studio-header'>🤖 Open-Source AI Quantum Studio</h1>", unsafe_allow_html=True)
st.caption("Tek Bir Nvidia API Anahtarı ile Dünyanın En Güçlü Açık Kaynak Yapay Zekalarını Yönetin")

# --- YAN MENÜ (DİNAMİK KONTROL PANELİ) ---
with st.sidebar:
    st.header("🔑 Güvenli Bağlantı")
    # API Key girişi (Kodun içinde açıkça yazmaması için buradan şifreli girilecek)
    api_key_input = st.text_input("Nvidia API Anahtarınız:", type="password", placeholder="nvapi-...")
    
    st.markdown("---")
    st.header("🧠 Açık Kaynak Model Havuzu")
    
    # Nvidia bulutundaki en güncel ve en güçlü açık kaynak modeller
    model_havuzu = {
        "DeepSeek R1 (Derin Akıl Yürütme & Matematik)": "deepseek-ai/deepseek-r1",
        "DeepSeek V4 Pro (En Gelişmiş Kod & Mantık)": "deepseek-ai/deepseek-v4-pro",
        "GLM 5.2 (Yüksek Bağlam & Kararlı Çıktı)": "z-ai/glm-5.2",
        "Llama 3.3 Nemotron Super (Nvidia Hız Canavarı)": "nvidia/llama-3.3-nemotron-super",
        "Llama 3.1 405B (Dünyanın En Büyük Açık Kaynak Modeli)": "meta/llama-3.1-405b-instruct",
        "Mistral Large 3 (Avrupa'nın Amiral Gemisi)": "mistralai/mistral-large-2407",
        "Qwen 2.5 72B (Asya'nın En Güçlü Kod Motoru)": "qwen/qwen-2.5-72b-instruct"
    }
    
    secilen_etiket = st.selectbox("Çalıştırılacak Yapay Zeka:", list(model_havuzu.keys()))
    aktif_model = model_havuzu[secilen_etiket]
    
    st.markdown("---")
    st.header("🎛️ İnce Ayar Mikseri")
    
    # İnce ayar mekanizmaları
    system_prompt = st.text_area("Sistem Rolü (System Prompt):", value="Sen profesyonel bir yazılım mimarı ve radyo otomasyon uzman yardımcısısın.", height=100)
    temperature = st.slider("Yaratıcılık Oranı (Temperature):", min_value=0.0, max_value=1.0, value=0.6, step=0.05)
    max_tokens = st.slider("Maksimum Yanıt (Tokens):", min_value=1024, max_value=16384, value=8192, step=512)

# --- ANA EKRAN ÇALIŞMA ALANI ---
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"⚡ Aktif Motor: `{aktif_model}`")
with col2:
    st.metric(label="Hedef Sıcaklık", value=f"{temperature}°C")

# Kullanıcı komut alanı
kullanici_girdisi = st.text_area(
    "Modele göndermek istediğiniz görev veya projenizin detayları:", 
    height=280, 
    placeholder="Örn: Radyo otomasyon mikserimiz için şarkı geçişlerinde donmayı önleyen kararlı bir JavaScript Web Worker yapısı kurgula..."
)

# Tetikleme mekanizması
if st.button("Kuantum İşlemciyi Tetikle ve Akışı Başlat"):
    if not api_key_input:
        st.error("🚨 İşlem Başarısız: Lütfen sol menüden geçerli bir Nvidia API Anahtarı girin!")
    elif not kullanici_girdisi.strip():
        st.warning("⚠️ Lütfen göndermek için boş bir mesaj bırakmayın.")
    else:
        try:
            # Nvidia Entegrasyon Ağ geçidine Güvenli İstek Kuruluyor
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=api_key_input
            )
            
            st.info("🌐 Nvidia bulut sunucularına bağlanıldı. Kanallar açılıyor, akış senkronize ediliyor...")
            
            # Canlı ekrana basım için dinamik yer tutucular
            reasoning_placeholder = st.empty()
            content_placeholder = st.empty()
            
            tam_cevap = ""
            dusunme_sureci = ""
            
            # İstek paketinin OpenAI kütüphanesi üzerinden Nvidia mimarisine gönderimi
            completion = client.chat.completions.create(
                model=aktif_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": kullanici_girdisi}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            # Gelen verinin canlı olarak çözümlenmesi (Stream işleme)
            for chunk in completion:
                if not getattr(chunk, "choices", None) or len(chunk.choices) == 0:
                    continue
                
                delta = chunk.choices[0].delta
                
                # DeepSeek R1 gibi modellerin "düşünme" (Reasoning) verisini yakala
                if getattr(delta, "reasoning_content", None) is not None:
                    dusunme_sureci += delta.reasoning_content
                    reasoning_placeholder.markdown(
                        f"**🕵️ Modelin İçsel Düşünme ve Akıl Yürütme Süreci:**\n<div class='reasoning-container'>{dusunme_sureci}</div>", 
                        unsafe_allow_html=True
                    )
                
                # Modelin asıl ürettiği cevabı/kodu yakala ve ekrana bas
                if getattr(delta, "content", None) is not None:
                    tam_cevap += delta.content
                    content_placeholder.markdown(
                        f"**✨ Yapay Zeka Stüdyo Yanıtı:**\n<div class='chat-container'>{tam_cevap}</div>", 
                        unsafe_allow_html=True
                    )
                    
            st.success("🎯 Yanıt akışı milisaniyelik senkronizasyonla başarıyla tamamlandı.")
            
        except Exception as e:
            st.error(f"Sunucu Bağlantı Hatası: {str(e)}\nLütfen Nvidia API anahtarınızı veya model adını kontrol edin.")
