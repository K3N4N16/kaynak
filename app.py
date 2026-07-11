import streamlit as st
from openai import OpenAI

# Sayfa Yapılandırması ve Küresel Ayarlar
st.set_page_config(
    page_title="Nvidia Open-Source Quantum AI Studio Pro", 
    page_icon="⚡",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Okunabilirliği Artırılmış Şeffaf Tasarım (CSS)
st.markdown("""
    <style>
    /* Ana Ekran Arka Plan Ayarları */
    .main { background-color: #090b0e; color: #f1f5f9; }
    
    /* Input ve Form Alanları */
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
    
    /* Çıktı Alanı - Şeffaf ve Maksimum Okunabilir */
    .chat-container { 
        background-color: rgba(255, 255, 255, 0.03) !important; 
        color: #f8fafc !important; 
        padding: 22px; 
        border-radius: 10px; 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        border-left: 6px solid #10b981; 
        margin-bottom: 20px; 
        line-height: 1.7;
        font-size: 1.05rem;
    }
    
    /* Akıl Yürütme Alanı - Şeffaf */
    .reasoning-container { 
        background-color: rgba(255, 255, 255, 0.01) !important; 
        padding: 15px; 
        border-radius: 8px; 
        border: 1px solid rgba(255, 255, 255, 0.05); 
        border-left: 4px solid #64748b; 
        font-family: monospace; 
        color: #94a3b8; 
        font-size: 0.9rem; 
        margin-bottom: 15px; 
    }
    
    .studio-title { background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 2.5rem; }
    
    /* Metin Seçim Rengini Parlat */
    ::selection { background: #10b981; color: white; }
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
        st.success("🔒 Nvidia API Key Aktif (Secrets)")
    else:
        api_key = st.text_input("Nvidia API Anahtarı Girin:", type="password", placeholder="nvapi-...")
    
    st.markdown("---")
    st.header("🤖 Nvidia & Open-Source Model Ordusu")
    
    model_havuzu = {
        "Nvidia Llama 3.3 Nemotron Super (Hız & Performans Şampiyonu)": "nvidia/llama-3.3-nemotron-super",
        "Nvidia Nemotron 4 340B (Üstün Dil & Sentetik Veri Yeteneği)": "nvidia/nemotron-4-340b-instruct",
        "Nvidia NeVA 22B (Gelişmiş Görsel & Resim Analiz Motoru)": "nvidia/neva-22b",
        "Nvidia NV-Embed-QA (Gelişmiş Döküman & Veri Arama)": "nvidia/nv-embedqa-e5-v5",
        "DeepSeek V4 Pro (En Gelişmiş Kod & Optimizasyon Canavarı)": "deepseek-ai/deepseek-v4-pro",
        "DeepSeek R1 (Maksimum Akıl Yürütme & Derin Düşünme)": "deepseek-ai/deepseek-r1",
        "Llama 3.1 405B (Dünyanın En Büyük Açık Kaynak Modeli)": "meta/llama-3.1-405b-instruct",
        "Llama 3.2 90B Vision (Çoklu Mod & Arayüz Okuma)": "meta/llama-3.2-90b-vision-instruct",
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
    "🛠️ Yapay zekaya iletmek istediğiniz görev veya komut:", 
    height=180, 
    placeholder="Örn: Hazırladığımız radyo stüdyo mikseri HTML koduna uyumlu, şarkı geçiş efektlerini yöneten modern bir JavaScript kurgula..."
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
            st.info("🌐 Nvidia bulut tünelleri açıldı, canlı veri akışı senkronize ediliyor...")
            
            # Dinamik yer tutucular (Eski mükerrer basımı engellemek için)
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
                
                # Akıl yürütme verisi akışı
                if getattr(delta, "reasoning_content", None) is not None:
                    st.session_state["son_dusunme"] += delta.reasoning_content
                    reasoning_placeholder.markdown(
                        f"**🕵️ Model Akıl Yürütme ve Düşünme Analizi:**\n<div class='reasoning-container'>{st.session_state['son_dusunme']}</div>", 
                        unsafe_allow_html=True
                    )
                
                # Ana içerik akışı
                if getattr(delta, "content", None) is not None:
                    st.session_state["son_cevap"] += delta.content
                    content_placeholder.markdown(
                        f"**✨ Üretilen Çıktı / Kod Bloku:**\n<div class='chat-container'>{st.session_state['son_cevap']}</div>", 
                        unsafe_allow_html=True
                    )
            
            st.session_state["islem_tamamlandi"] = True
            st.rerun()  # Akış bittiğinde ekranı temizle ve kararlı statik çıktı moduna geç

        except Exception as e:
            st.error(f"Sunucu Bağlantı Kesintisi: {str(e)}")

# --- KARARLI VE TEKİL ÇIKTI EKRANI ---
# Eğer akış bittiyse veya hafızada veri varsa sadece BU blok çalışır (Çift basım engellendi)
if st.session_state["islem_tamamlandi"] or (st.session_state["son_cevap"] and not tetiklendi):
    
    if st.session_state["son_dusunme"]:
        st.markdown(f"**🕵️ Model Akıl Yürütme ve Düşünme Analizi:**\n<div class='reasoning-container'>{st.session_state['son_dusunme']}</div>", unsafe_allow_html=True)
    
    # Şeffaf ve okunaklı ana çıktı
    st.markdown(f"**✨ Üretilen Çıktı / Kod Bloku:**\n<div class='chat-container'>{st.session_state['son_cevap']}</div>", unsafe_allow_html=True)
    
    # --- YENİ ENTEGRE ÖZELLİKLER VE ARAÇLAR ---
    st.markdown("---")
    
    # 1. Yeni Özellik: İstatistik Sayacı (Kelime & Karakter Dağılımı)
    kelime_sayisi = len(st.session_state["son_cevap"].split())
    karakter_sayisi = len(st.session_state["son_cevap"])
    st.caption(f"📊 **Çıktı Analizi:** Toplam {kelime_sayisi} kelime | {karakter_sayisi} karakter üretildi.")
    
    st.subheader("💾 Gelişmiş Çıktı Yönetim İstasyonu")
    col_copy, col_down_txt, col_down_html = st.columns(3)
    
    with col_copy:
        # 2. Yeni Özellik: Dahili Kopyalama ve Seçim Alanı
        st.text_area("📋 Tek Tıkla Kopyalama Alanı (Ctrl+A / Tümünü Seç):", value=st.session_state["son_cevap"], height=80)
        st.caption("Mobil veya masaüstünde kutunun içine dokunup tümünü kopyalayabilirsin.")
        
    with col_down_txt:
        st.download_button(
            label="📄 TXT Dosyası Olarak İndir",
            data=st.session_state["son_cevap"],
            file_name="quantum_output.txt",
            mime="text/plain"
        )
        
    with col_down_html:
        st.download_button(
            label="🌐 Kod Dosyası (HTML/CSS/JS) Olarak İndir",
            data=st.session_state["son_cevap"],
            file_name="studio_output.html",
            mime="text/html"
        )
