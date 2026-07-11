import streamlit as st
from openai import OpenAI

# Sayfa Yapılandırması ve Küresel Ayarlar
st.set_page_config(
    page_title="Nvidia Open-Source Quantum AI Studio Pro", 
    page_icon="⚡",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Tamamen Açık Renk ve Net Okunabilir Yazı Tasarımı (CSS)
st.markdown("""
    <style>
    /* Ana Ekran Arka Planı - Açık Gri/Beyaz */
    .main { background-color: #f8fafc; color: #0f172a; }
    
    /* Girdiler ve Form Alanları - Beyaz Arka Plan, Siyah Yazı */
    .stTextArea textarea { background-color: #ffffff !important; color: #0f172a !important; border: 1px solid #cbd5e1 !important; border-radius: 8px; font-size: 1rem; }
    .stTextInput input { background-color: #ffffff !important; color: #0f172a !important; border: 1px solid #cbd5e1 !important; }
    
    /* Yan Menü (Sidebar) Optimizasyonu */
    section[data-testid="stSidebar"] { background-color: #f1f5f9 !important; }
    section[data-testid="stSidebar"] * { color: #0f172a !important; }
    
    /* Geliştirici Tetikleme Butonu */
    div.stButton > button:first-child { 
        background: linear-gradient(135deg, #059669 0%, #10b981 100%); 
        color: white !important; border-radius: 8px; width: 100%; font-weight: bold; 
        height: 52px; border: none; font-size: 1.1rem; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
        transition: all 0.2s;
    }
    div.stButton > button:first-child:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4); }
    
    /* Çıktı Alanı - BEYAZ ARKA PLAN / SİYAH YAZI */
    .chat-container { 
        background-color: #ffffff !important; 
        color: #0f172a !important; 
        padding: 22px; 
        border-radius: 10px; 
        border: 1px solid #e2e8f0; 
        border-left: 6px solid #10b981; 
        margin-bottom: 20px; 
        line-height: 1.7;
        font-size: 1.05rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Akıl Yürütme Alanı - Hafif Açık Ton / Koyu Gri Yazı */
    .reasoning-container { 
        background-color: #f1f5f9 !important; 
        padding: 15px; 
        border-radius: 8px; 
        border: 1px solid #e2e8f0; 
        border-left: 4px solid #64748b; 
        font-family: monospace; 
        color: #334155 !important; 
        font-size: 0.9rem; 
        margin-bottom: 15px; 
    }
    
    /* Başlık Alanı */
    .studio-title { background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 2.5rem; }
    
    /* Alt Etiket Yazıları */
    .stMarkdown p, .stCaption { color: #334155 !important; }
    
    /* Kod Bloklarının Açık Temada Düzgün Görünmesi İçin */
    code { color: #0f172a !important; background-color: #e2e8f0 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='studio-title'>⚡ Quantum AI Studio Pro v10.0</h1>", unsafe_allow_html=True)
st.caption("Nvidia Bulut Motoru ile Entegre Genişletilmiş Dev Model Ordusu Konsolu")

# --- HAFIZA (SESSION STATE) İLKLENDİRME ---
if "son_cevap" not in st.session_state:
    st.session_state["son_cevap"] = ""
if "son_dusunme" not in st.session_state:
    st.session_state["son_dusunme"] = ""
if "islem_tamamlandi" not in st.session_state:
    st.session_state["islem_tamamlandi"] = False

# --- STREAMLIT SECRETS BAĞLANTI KONTROLÜ ---
api_key = st.secrets.get("NVIDIA_API_KEY", "")

# --- YAN MENÜ (SIDEBAR) KONTROLLERİ ---
with st.sidebar:
    st.header("⚙️ Sistem Altyapısı")
    
    if api_key:
        st.success("🔒 Nvidia API Key Aktif")
    else:
        api_key = st.text_input("Nvidia API Anahtarı Girin:", type="password", placeholder="nvapi-...")
    
    st.markdown("---")
    st.header("🤖 Model Havuzu")
    
    model_havuzu = {
        "Nvidia Llama 3.3 Nemotron Super (Hız & Performans Şampiyonu)": "nvidia/llama-3.3-nemotron-super",
        "Nvidia Nemotron 4 340B (Üstün Dil Yeteneği)": "nvidia/nemotron-4-340b-instruct",
        "Nvidia NeVA 22B (Resim Analiz Motoru)": "nvidia/neva-22b",
        "DeepSeek V4 Pro (En Gelişmiş Kod Canavarı)": "deepseek-ai/deepseek-v4-pro",
        "DeepSeek R1 (Derin Düşünme & Akıl Yürütme)": "deepseek-ai/deepseek-r1",
        "Llama 3.1 405B (Dünyanın En Büyük Açık Kaynak Modeli)": "meta/llama-3.1-405b-instruct",
        "Qwen 2.5 72B (Hatasız Algoritma ve Kodlama Yapıları)": "qwen/qwen-2.5-72b-instruct"
    }
    
    secilen_etiket = st.selectbox("Çalıştırılacak Model:", list(model_havuzu.keys()))
    aktif_model = model_havuzu[secilen_etiket]
    
    st.markdown("---")
    st.header("🎛️ Hassasiyet Ayarları")
    system_prompt = st.text_area("Sistem Rolü (System Prompt):", value="Sen profesyonel bir yazılım mimarı, kod optimizasyon uzmanı ve otomasyon danışmanısın.", height=90)
    temperature = st.slider("Yaratıcılık Seviyesi (Temperature):", min_value=0.0, max_value=1.0, value=0.5, step=0.05)

# --- ANA ÇALIŞMA ALANI ---
kullanici_girdisi = st.text_area(
    "🛠️ Yapay zekaya iletmek istediğiniz görev veya komut:", 
    height=180, 
    placeholder="Komutunuzu buraya yazın..."
)

# Tetikleme Butonu
tetiklendi = st.button("Kuantum Sürücüyü Tetikle ve Akışı Başlat")

if tetiklendi:
    if not api_key:
        st.error("🚨 Hata: Sistemde tanımlı geçerli bir Nvidia API anahtarı bulunamadı!")
    elif not kullanici_girdisi.strip():
        st.warning("⚠️ Lütfen boş komut göndermeyin.")
    else:
        try:
            client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)
            st.info("🌐 Nvidia bulut bağlantısı sağlandı, veri akışı senkronize ediliyor...")
            
            reasoning_placeholder = st.empty()
            content_placeholder = st.empty()
            
            st.session_state["son_cevap"] = ""
            st.session_state["son_dusunme"] = ""
            st.session_state["islem_tamamlandi"] = False
            
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
                
                # Derin Düşünme Modelleri İçin Akıl Yürütme Akışı
                if getattr(delta, "reasoning_content", None) is not None:
                    st.session_state["son_dusunme"] += delta.reasoning_content
                    reasoning_placeholder.markdown(
                        f"**🕵️ Model Akıl Yürütme ve Düşünme Analizi:**\n<div class='reasoning-container'>{st.session_state['son_dusunme']}</div>", 
                        unsafe_allow_html=True
                    )
                
                # Ana Çıktı Akışı
                if getattr(delta, "content", None) is not None:
                    st.session_state["son_cevap"] += delta.content
                    content_placeholder.markdown(
                        f"**✨ Üretilen Çıktı / Kod Bloku:**\n<div class='chat-container'>{st.session_state['son_cevap']}</div>", 
                        unsafe_allow_html=True
                    )
            
            st.session_state["islem_tamamlandi"] = True
            st.rerun()  # Akış bittiğinde ekranı yenile ve temiz çıktı moduna geç

        except Exception as e:
            st.error(f"Bağlantı Hatası: {str(e)}")

# --- TEKİL STATİK ÇIKTI EKRANI ---
if st.session_state["islem_tamamlandi"] or (st.session_state["son_cevap"] and not tetiklendi):
    
    if st.session_state["son_dusunme"]:
        st.markdown(f"**🕵️ Model Akıl Yürütme:**\n<div class='reasoning-container'>{st.session_state['son_dusunme']}</div>", unsafe_allow_html=True)
    
    # Net ve kontrastı yüksek beyaz zeminli ana çıktı
    st.markdown(f"**✨ Üretilen Çıktı / Kod Bloku:**\n<div class='chat-container'>{st.session_state['son_cevap']}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Kelime / Karakter Sayıcı
    kelime_sayisi = len(st.session_state["son_cevap"].split())
    karakter_sayisi = len(st.session_state["son_cevap"])
    st.caption(f"📊 **Çıktı Raporu:** Toplam {kelime_sayisi} kelime | {karakter_sayisi} karakter.")
    
    st.subheader("💾 Gelişmiş Çıktı Yönetim İstasyonu")
    col_copy, col_down_txt, col_down_html = st.columns(3)
    
    with col_copy:
        st.text_area("📋 Kopyalama Alanı (Tümünü Seç):", value=st.session_state["son_cevap"], height=80)
        st.caption("Metne dokunup hızla kopyalayabilirsin.")
        
    with col_down_txt:
        st.download_button(
            label="📄 TXT Dosyası Olarak İndir",
            data=st.session_state["son_cevap"],
            file_name="quantum_output.txt",
            mime="text/plain"
        )
        
    with col_down_html:
        st.download_button(
            label="🌐 Kod Dosyası Olarak İndir",
            data=st.session_state["son_cevap"],
            file_name="studio_output.html",
            mime="text/html"
        )
