import streamlit as st
from openai import OpenAI

# Sayfa Yapılandırması ve Küresel Ayarlar
st.set_page_config(
    page_title="Nvidia Open-Source Quantum AI Studio Pro", 
    page_icon="⚡",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Kapsamlı ve Profesyonel Karanlık Tema Tasarımı (CSS)
st.markdown("""
    <style>
    .main { background-color: #090b0e; color: #f1f5f9; }
    .stTextArea textarea { background-color: #0f1219 !important; color: #ffffff !important; border: 1px solid #1e293b !important; border-radius: 8px; font-size: 1rem; }
    .stTextInput input { background-color: #0f1219 !important; color: #ffffff !important; border: 1px solid #1e293b !important; }
    
    /* Geliştirici Tetikleme Butonu */
    div.stButton > button:first-child { 
        background: linear-gradient(135deg, #059669 0%, #10b981 100%); 
        color: white; border-radius: 8px; width: 100%; font-weight: bold; 
        height: 52px; border: none; font-size: 1.1rem; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
        transition: all 0.2s;
    }
    div.stButton > button:first-child:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4); }
    
    /* Çıktı ve Akıl Yürütme Konteynerleri */
    .chat-container { background-color: #0f1219; padding: 22px; border-radius: 10px; border: 1px solid #1e293b; border-left: 6px solid #3b82f6; margin-bottom: 20px; line-height: 1.7; }
    .reasoning-container { background-color: #141822; padding: 15px; border-radius: 8px; border: 1px solid #334155; border-left: 4px solid #64748b; font-family: monospace; color: #94a3b8; font-size: 0.9rem; margin-bottom: 15px; }
    
    .studio-title { background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 2.5rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='studio-title'>⚡ Quantum AI Studio Pro v10.0</h1>", unsafe_allow_html=True)
st.caption("Nvidia Bulut Motoru ile Entegre Genişletilmiş Dev Model Ordusu Konsolu")

# --- HAFIZA (SESSION STATE) İLKLENDİRME ---
# Sayfa her yenilendiğinde çıktıların kaybolmaması için hafıza kanallarını açıyoruz
if "son_cevap" not in st.session_state:
    st.session_state["son_cevap"] = ""
if "son_dusunme" not in st.session_state:
    st.session_state["son_dusunme"] = ""

# --- STREAMLIT SECRETS BAĞLANTI KONTROLÜ ---
api_key = ""
if "NVIDIA_API_KEY" in st.secrets:
    api_key = st.secrets["NVIDIA_API_KEY"]

# --- YAN MENÜ (SIDEBAR) KONTROLLERİ ---
with st.sidebar:
    st.header("⚙️ Sistem Altyapısı")
    
    if api_key:
        st.success("🔒 Nvidia API Key Aktif (Secrets)")
    else:
        api_key = st.text_input("Nvidia API Anahtarı Girin:", type="password", placeholder="nvapi-...")
    
    st.markdown("---")
    st.header("🤖 Nvidia & Open-Source Model Ordusu")
    
    # Nvidia bulutundaki bizzat Nvidia'nın kendi modelleri ve dev açık kaynak yapısı
    model_havuzu = {
        # --- NVIDIA ÖZ MODELLERİ ---
        "Nvidia Llama 3.3 Nemotron Super (Hız & Performans Şampiyonu)": "nvidia/llama-3.3-nemotron-super",
        "Nvidia Nemotron 4 340B (Üstün Dil & Sentetik Veri Yeteneği)": "nvidia/nemotron-4-340b-instruct",
        "Nvidia NeVA 22B (Gelişmiş Görsel & Resim Analiz Motoru)": "nvidia/neva-22b",
        "Nvidia NV-Embed-QA (Gelişmiş Döküman & Veri Arama)": "nvidia/nv-embedqa-e5-v5",
        
        # --- DEEPSEEK MIMARISI ---
        "DeepSeek V4 Pro (En Gelişmiş Kod & Optimizasyon Canavarı)": "deepseek-ai/deepseek-v4-pro",
        "DeepSeek R1 (Maksimum Akıl Yürütme & Derin Düşünme)": "deepseek-ai/deepseek-r1",
        
        # --- META (LLAMA) SERİSİ ---
        "Llama 3.1 405B (Dünyanın En Büyük Açık Kaynak Modeli)": "meta/llama-3.1-405b-instruct",
        "Llama 3.2 90B Vision (Çoklu Mod & Arayüz Okuma)": "meta/llama-3.2-90b-vision-instruct",
        
        # --- DİĞER KOD VE BAĞLAM DEVLERİ ---
        "GLM 5.2 (Yüksek Bağlam & Kararlı Radyo/Metin Otomasyonu)": "z-ai/glm-5.2",
        "Qwen 2.5 72B (Hatasız Algoritma ve Kodlama Yapıları)": "qwen/qwen-2.5-72b-instruct",
        "Mistral Large 3 (Gelişmiş Akıl Yürütme Amiral Gemisi)": "mistralai/mistral-large-2407"
    }
    
    secilen_etiket = st.selectbox("Çalıştırılacak Model:", list(model_havuzu.keys()))
    aktif_model = model_havuzu[secilen_etiket]
    
    st.markdown("---")
    st.header("🎛️ Hassasiyet Ayarları")
    system_prompt = st.text_area("Sistem Rolü (System Prompt):", value="Sen profesyonel bir yazılım mimarı, kod optimizasyon uzmanı ve radyo otomasyon danışmanısın.", height=90)
    temperature = st.slider("Yaratıcılık Seviyesi (Temperature):", min_value=0.0, max_value=1.0, value=0.5, step=0.05)

# --- ANA ÇALIŞMA ALANI ---
kullanici_girdisi = st.text_area(
    f"🛠️ Yapay zekaya iletmek istediğiniz görev veya komut:", 
    height=230, 
    placeholder="Örn: Hazırladığımız radyo stüdyo mikseri HTML koduna uyumlu, şarkı geçiş efektlerini yöneten modern bir JavaScript kurgula..."
)

# Tetikleme Butonu
if st.button("Kuantum Sürücüyü Tetikle ve Akışı Başlat"):
    if not api_key:
        st.error("🚨 Hata: Sistemde tanımlı geçerli bir Nvidia API anahtarı bulunamadı!")
    elif not kullanici_girdisi.strip():
        st.warning("⚠️ Lütfen boş komut göndermeyin.")
    else:
        try:
            # Nvidia Entegrasyon Ağ Geçidine Bağlantı
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=api_key
            )
            
            st.info("🌐 Nvidia bulut tünelleri açıldı, canlı veri akışı senkronize ediliyor...")
            
            # Dinamik canlı çıktılar için yer tutucular
            reasoning_placeholder = st.empty()
            content_placeholder = st.empty()
            
            st.session_state["son_cevap"] = ""
            st.session_state["son_dusunme"] = ""
            
            # İstek paketinin akışlı (stream=True) olarak gönderilmesi
            completion = client.chat.completions.create(
                model=aktif_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": kullanici_girdisi}
                ],
                temperature=temperature,
                stream=True
            )
            
            for chunk in completion:
                if not getattr(chunk, "choices", None) or len(chunk.choices) == 0:
                    continue
                delta = chunk.choices[0].delta
                
                # DeepSeek R1 gibi modellerin içsel akıl yürütme süreçlerini yakala
                if getattr(delta, "reasoning_content", None) is not None:
                    st.session_state["son_dusunme"] += delta.reasoning_content
                    reasoning_placeholder.markdown(
                        f"**🕵️ Model Akıl Yürütme ve Düşünme Analizi:**\n<div class='reasoning-container'>{st.session_state['son_dusunme']}</div>", 
                        unsafe_allow_html=True
                    )
                
                # Ana metin veya kod çıktılarını yakala
                if getattr(delta, "content", None) is not None:
                    st.session_state["son_cevap"] += delta.content
                    content_placeholder.markdown(
                        f"**✨ Üretilen Çıktı / Kod Bloku:**\n<div class='chat-container'>{st.session_state['son_cevap']}</div>", 
                        unsafe_allow_html=True
                    )
            
            st.success("🎯 Yanıt akışı milisaniyelik senkronizasyonla başarıyla tamamlandı.")

        except Exception as e:
            st.error(f"Sunucu Bağlantı Kesintisi: {str(e)}")

# --- DURAĞAN EKRAN ÇIKTI KONTROLÜ ---
# Eğer hafızada veri varsa, buton tetiklenmese bile ekranda sabit tut ve araçları göster
if st.session_state["son_cevap"]:
    if st.session_state["son_dusunme"]:
        st.markdown(f"**🕵️ Model Akıl Yürütme ve Düşünme Analizi:**\n<div class='reasoning-container'>{st.session_state['son_dusunme']}</div>", unsafe_allow_html=True)
    
    st.markdown(f"**✨ Üretilen Çıktı / Kod Bloku:**\n<div class='chat-container'>{st.session_state['son_cevap']}</div>", unsafe_allow_html=True)
    
    # --- PRO ÇIKTI YÖNETİM İSTASYONU ---
    st.markdown("---")
    st.subheader("💾 Gelişmiş Çıktı Yönetim İstasyonu")
    
    col_copy, col_down_txt, col_down_html = st.columns(3)
    
    with col_copy:
        # Mobil kopyalamayı kolaylaştıran dahili metin alanı
        st.text_area("📋 Kopyalamak İçin Seçin (Tümünü Seç Uyumlu):", value=st.session_state["son_cevap"], height=70)
        st.caption("Kutunun içine dokunup (Ctrl+A ile) çıktının tamamını hızla kopyalayabilirsiniz.")
        
    with col_down_txt:
        st.download_button(
            label="📄 Düz Metin (TXT) Olarak Telefona/PC'ye İndir",
            data=st.session_state["son_cevap"],
            file_name="quantum_ai_output.txt",
            mime="text/plain"
        )
        
    with col_down_html:
        st.download_button(
            label="🌐 Kod Dosyası (HTML/CSS/JS) Olarak İndir",
            data=st.session_state["son_cevap"],
            file_name="studio_output.html",
            mime="text/html"
        )
