import streamlit as st
from openai import OpenAI
import json
import time
import uuid
from datetime import datetime

# ============================================================
# SAYFA YAPILANDIRMASI
# ============================================================
st.set_page_config(
    page_title="Quantum AI Studio Pro v11.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# MODERN KOYU TEMA + CAM (GLASSMORPHISM) TASARIM
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }

/* Genel arka plan - koyu, degrade */
.stApp {
    background: radial-gradient(circle at 15% 0%, #1a1f3a 0%, #0b0e1a 45%, #05070f 100%);
    color: #e6e9f5;
}

/* Ana başlık */
.studio-title {
    background: linear-gradient(90deg, #7c3aed 0%, #06b6d4 50%, #10b981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 2.6rem;
    letter-spacing: -0.02em;
    margin-bottom: 0;
}
.studio-subtitle { color: #94a3b8; font-size: 0.95rem; margin-top: -8px; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1324 0%, #0a0d1c 100%) !important;
    border-right: 1px solid rgba(124, 58, 237, 0.25);
}
section[data-testid="stSidebar"] * { color: #dbe1f5 !important; }
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    color: #a78bfa !important; font-weight: 700;
}

/* Kartlar / cam efekti */
.glass-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 14px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}

/* Metrik kutuları */
div[data-testid="stMetric"] {
    background: rgba(124, 58, 237, 0.08);
    border: 1px solid rgba(124, 58, 237, 0.25);
    border-radius: 12px;
    padding: 10px 14px;
}
div[data-testid="stMetricValue"] { color: #a78bfa !important; }

/* Giriş alanları */
.stTextArea textarea, .stTextInput input {
    background-color: rgba(255,255,255,0.05) !important;
    color: #e6e9f5 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border: 1px solid #7c3aed !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.25) !important;
}

/* Selectbox / slider etiketleri */
.stSelectbox label, .stSlider label, .stTextArea label, .stTextInput label, .stRadio label { color: #cbd5e1 !important; font-weight: 500; }

/* Butonlar */
div.stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%);
    color: white !important;
    border-radius: 10px;
    border: none;
    font-weight: 600;
    height: 48px;
    transition: all 0.2s ease;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.3);
}
div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(124, 58, 237, 0.45); }

/* İkincil butonlar (sidebar içindeki bazı butonlar) */
section[data-testid="stSidebar"] div.stButton > button {
    background: rgba(255,255,255,0.06);
    box-shadow: none;
    border: 1px solid rgba(255,255,255,0.12);
}

/* İndirme butonu */
div.stDownloadButton > button {
    background: rgba(16, 185, 129, 0.12);
    color: #34d399 !important;
    border: 1px solid rgba(16, 185, 129, 0.35);
    border-radius: 10px;
    font-weight: 600;
}

/* Sohbet balonları */
.stChatMessage {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 4px;
}

/* Akıl yürütme kutusu */
.reasoning-container {
    background: rgba(6, 182, 212, 0.06);
    border: 1px solid rgba(6, 182, 212, 0.25);
    border-left: 4px solid #06b6d4;
    border-radius: 10px;
    padding: 14px 16px;
    font-family: 'JetBrains Mono', monospace;
    color: #a5f3fc !important;
    font-size: 0.85rem;
    margin-bottom: 10px;
}

/* Kod blokları */
code { color: #c4b5fd !important; background-color: rgba(124,58,237,0.12) !important; }
pre { border-radius: 10px !important; border: 1px solid rgba(255,255,255,0.08) !important; }

/* Badge / etiketler */
.badge {
    display: inline-block; padding: 3px 10px; border-radius: 999px;
    background: rgba(124,58,237,0.15); border: 1px solid rgba(124,58,237,0.4);
    color: #c4b5fd; font-size: 0.75rem; font-weight: 600; margin-right: 6px;
}

hr { border-color: rgba(255,255,255,0.08) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='studio-title'>⚡ Quantum AI Studio Pro v11.0</div>", unsafe_allow_html=True)
st.markdown("<p class='studio-subtitle'>Nvidia Bulut Motoru · Çoklu Oturum · Akıl Yürütme Akışı · Gelişmiş Dışa Aktarım</p>", unsafe_allow_html=True)
st.write("")

# ============================================================
# SABİTLER
# ============================================================
MODEL_HAVUZU = {
    "Nvidia Llama 3.3 Nemotron Super (Hız & Performans)": "nvidia/llama-3.3-nemotron-super",
    "Nvidia Nemotron 4 340B (Üstün Dil Yeteneği)": "nvidia/nemotron-4-340b-instruct",
    "Nvidia NeVA 22B (Görsel Analiz Motoru)": "nvidia/neva-22b",
    "DeepSeek V4 Pro (Gelişmiş Kod Üretimi)": "deepseek-ai/deepseek-v4-pro",
    "DeepSeek R1 (Derin Düşünme & Akıl Yürütme)": "deepseek-ai/deepseek-r1",
    "Llama 3.1 405B (En Büyük Açık Kaynak Model)": "meta/llama-3.1-405b-instruct",
    "Qwen 2.5 72B (Kod & Algoritma Uzmanı)": "qwen/qwen-2.5-72b-instruct",
}

SISTEM_PRESETLERI = {
    "Yazılım Mimarı": "Sen profesyonel bir yazılım mimarı, kod optimizasyon uzmanı ve otomasyon danışmanısın. Kısa, net ve üretime hazır kod örnekleri sun.",
    "Veri Bilimci": "Sen deneyimli bir veri bilimcisin. İstatistiksel doğruluğa önem verir, varsayımlarını açıkça belirtir ve kodunu adım adım açıklarsın.",
    "Metin Editörü": "Sen titiz bir metin editörüsün. Dil bilgisi, akıcılık ve ton tutarlılığına odaklanırsın; gereksiz süslemeden kaçınırsın.",
    "Kısa & Öz Asistan": "Kısa, öz ve doğrudan cevaplar ver. Gereksiz açıklamalardan kaçın, sadece istenen çıktıyı üret.",
    "Serbest / Özel": None,
}

# ============================================================
# OTURUM DURUMU (SESSION STATE) İLKLENDİRME
# ============================================================
if "sohbetler" not in st.session_state:
    ilk_id = str(uuid.uuid4())[:8]
    st.session_state["sohbetler"] = {
        ilk_id: {"ad": "Yeni Sohbet 1", "mesajlar": [], "olusturma": datetime.now().isoformat()}
    }
    st.session_state["aktif_sohbet_id"] = ilk_id

if "aktif_sohbet_id" not in st.session_state:
    st.session_state["aktif_sohbet_id"] = list(st.session_state["sohbetler"].keys())[0]

aktif_id = st.session_state["aktif_sohbet_id"]
aktif_sohbet = st.session_state["sohbetler"][aktif_id]

# ============================================================
# API ANAHTARI
# ============================================================
api_key = st.secrets.get("NVIDIA_API_KEY", "")

# ============================================================
# YAN MENÜ
# ============================================================
with st.sidebar:
    st.header("⚙️ Sistem Altyapısı")
    if api_key:
        st.success("🔒 Nvidia API Key Aktif (Secrets)")
    else:
        api_key = st.text_input("Nvidia API Anahtarı Girin:", type="password", placeholder="nvapi-...")

    st.markdown("---")
    st.header("💬 Sohbet Oturumları")

    if st.button("➕ Yeni Sohbet Başlat", use_container_width=True):
        yeni_id = str(uuid.uuid4())[:8]
        st.session_state["sohbetler"][yeni_id] = {
            "ad": f"Yeni Sohbet {len(st.session_state['sohbetler']) + 1}",
            "mesajlar": [],
            "olusturma": datetime.now().isoformat()
        }
        st.session_state["aktif_sohbet_id"] = yeni_id
        st.rerun()

    sohbet_secenekleri = {v["ad"]: k for k, v in st.session_state["sohbetler"].items()}
    secilen_ad = st.selectbox("Aktif Sohbet:", list(sohbet_secenekleri.keys()),
                               index=list(sohbet_secenekleri.values()).index(aktif_id))
    if sohbet_secenekleri[secilen_ad] != aktif_id:
        st.session_state["aktif_sohbet_id"] = sohbet_secenekleri[secilen_ad]
        st.rerun()

    col_yeniden, col_sil = st.columns(2)
    with col_yeniden:
        yeni_ad = st.text_input("Sohbeti yeniden adlandır:", value=aktif_sohbet["ad"], label_visibility="collapsed")
        if yeni_ad != aktif_sohbet["ad"]:
            aktif_sohbet["ad"] = yeni_ad
    with col_sil:
        if st.button("🗑️ Sohbeti Sil", use_container_width=True) and len(st.session_state["sohbetler"]) > 1:
            del st.session_state["sohbetler"][aktif_id]
            st.session_state["aktif_sohbet_id"] = list(st.session_state["sohbetler"].keys())[0]
            st.rerun()

    st.markdown("---")
    st.header("🤖 Model Havuzu")
    secilen_etiket = st.selectbox("Çalıştırılacak Model:", list(MODEL_HAVUZU.keys()))
    aktif_model = MODEL_HAVUZU[secilen_etiket]

    st.markdown("---")
    st.header("🎛️ Sistem Rolü")
    preset_secim = st.selectbox("Hazır Rol Şablonu:", list(SISTEM_PRESETLERI.keys()))
    if SISTEM_PRESETLERI[preset_secim] is not None:
        system_prompt = st.text_area("Sistem Rolü (System Prompt):", value=SISTEM_PRESETLERI[preset_secim], height=100)
    else:
        system_prompt = st.text_area("Sistem Rolü (System Prompt):",
                                      value="Sen yardımsever ve uzman bir asistansın.", height=100)

    st.markdown("---")
    st.header("🎚️ Hassasiyet Ayarları")
    temperature = st.slider("Yaratıcılık (Temperature):", 0.0, 1.0, 0.5, 0.05)
    top_p = st.slider("Çeşitlilik (Top-P):", 0.1, 1.0, 0.9, 0.05)
    max_tokens = st.slider("Maksimum Yanıt Uzunluğu (Token):", 256, 8192, 2048, 128)

    st.markdown("---")
    st.header("📎 Bağlam Dosyası (Opsiyonel)")
    yuklenen_dosya = st.file_uploader("Metin/Kod dosyası ekle (.txt, .md, .py, .json)", type=["txt", "md", "py", "json", "csv"])
    dosya_icerigi = ""
    if yuklenen_dosya is not None:
        try:
            dosya_icerigi = yuklenen_dosya.read().decode("utf-8", errors="ignore")
            st.caption(f"✅ `{yuklenen_dosya.name}` yüklendi ({len(dosya_icerigi)} karakter). Bir sonraki mesaja otomatik eklenecek.")
        except Exception:
            st.warning("Dosya okunamadı.")

    st.markdown("---")
    if st.button("🧹 Sohbet Geçmişini Temizle", use_container_width=True):
        aktif_sohbet["mesajlar"] = []
        st.rerun()

# ============================================================
# ÜST BİLGİ BANDI (İSTATİSTİKLER)
# ============================================================
toplam_mesaj = len(aktif_sohbet["mesajlar"])
toplam_kelime = sum(len(m["content"].split()) for m in aktif_sohbet["mesajlar"])
kullanici_mesaj_sayisi = sum(1 for m in aktif_sohbet["mesajlar"] if m["role"] == "user")

c1, c2, c3, c4 = st.columns(4)
c1.metric("💬 Mesaj Sayısı", toplam_mesaj)
c2.metric("📝 Toplam Kelime", toplam_kelime)
c3.metric("🔁 Tur Sayısı", kullanici_mesaj_sayisi)
c4.metric("🤖 Aktif Model", secilen_etiket.split(" (")[0])

st.markdown("---")

# ============================================================
# GEÇMİŞ SOHBETİ GÖSTER
# ============================================================
for mesaj in aktif_sohbet["mesajlar"]:
    avatar = "🧑‍💻" if mesaj["role"] == "user" else "⚡"
    with st.chat_message(mesaj["role"], avatar=avatar):
        if mesaj.get("dusunme"):
            st.markdown(f"<div class='reasoning-container'>🕵️ <b>Akıl Yürütme:</b><br>{mesaj['dusunme']}</div>", unsafe_allow_html=True)
        st.markdown(mesaj["content"])

# ============================================================
# YARDIMCI FONKSİYON: MODEL ÇAĞRISI (STREAM)
# ============================================================
def modelden_yanit_al(client, model, mesaj_listesi, temperature, top_p, max_tokens,
                       reasoning_placeholder, content_placeholder):
    tam_cevap = ""
    tam_dusunme = ""
    completion = client.chat.completions.create(
        model=model,
        messages=mesaj_listesi,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        stream=True
    )
    for chunk in completion:
        if not getattr(chunk, "choices", None):
            continue
        delta = chunk.choices[0].delta

        if getattr(delta, "reasoning_content", None):
            tam_dusunme += delta.reasoning_content
            reasoning_placeholder.markdown(
                f"<div class='reasoning-container'>🕵️ <b>Akıl Yürütme:</b><br>{tam_dusunme}</div>",
                unsafe_allow_html=True
            )
        if getattr(delta, "content", None):
            tam_cevap += delta.content
            content_placeholder.markdown(tam_cevap)

    return tam_cevap, tam_dusunme

# ============================================================
# SOHBET GİRİŞİ (ÇOKLU TUR)
# ============================================================
kullanici_girdisi = st.chat_input("Komutunuzu yazın ve Enter'a basın...")

if kullanici_girdisi:
    if not api_key:
        st.error("🚨 Sistemde tanımlı geçerli bir Nvidia API anahtarı bulunamadı!")
    else:
        nihai_girdi = kullanici_girdisi
        if dosya_icerigi:
            nihai_girdi = f"{kullanici_girdisi}\n\n--- Eklenen Dosya İçeriği ---\n{dosya_icerigi}"

        aktif_sohbet["mesajlar"].append({"role": "user", "content": kullanici_girdisi, "dusunme": ""})

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(kullanici_girdisi)

        with st.chat_message("assistant", avatar="⚡"):
            reasoning_placeholder = st.empty()
            content_placeholder = st.empty()

            try:
                client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)

                gecmis_mesajlar = [{"role": "system", "content": system_prompt}]
                for m in aktif_sohbet["mesajlar"][:-1]:
                    gecmis_mesajlar.append({"role": m["role"], "content": m["content"]})
                gecmis_mesajlar.append({"role": "user", "content": nihai_girdi})

                baslangic = time.time()
                cevap, dusunme = modelden_yanit_al(
                    client, aktif_model, gecmis_mesajlar, temperature, top_p, max_tokens,
                    reasoning_placeholder, content_placeholder
                )
                sure = round(time.time() - baslangic, 2)

                aktif_sohbet["mesajlar"].append({"role": "assistant", "content": cevap, "dusunme": dusunme})
                st.caption(f"⏱️ Yanıt süresi: {sure} sn · {len(cevap.split())} kelime")

            except Exception as e:
                st.error(f"Bağlantı Hatası: {str(e)}")

        st.rerun()

# ============================================================
# ALT ARAÇ ÇUBUĞU: YENİDEN ÜRET / DIŞA AKTAR
# ============================================================
if aktif_sohbet["mesajlar"]:
    st.markdown("---")
    st.subheader("💾 Dışa Aktarım ve Ek Araçlar")

    col_regen, col_md, col_json, col_txt = st.columns(4)

    with col_regen:
        if st.button("🔁 Son Yanıtı Yeniden Üret", use_container_width=True):
            if len(aktif_sohbet["mesajlar"]) >= 2 and api_key:
                aktif_sohbet["mesajlar"].pop()  # son asistan mesajını kaldır
                st.rerun()

    markdown_ciktisi = "\n\n".join(
        f"**{'Kullanıcı' if m['role'] == 'user' else 'Asistan'}:**\n{m['content']}"
        for m in aktif_sohbet["mesajlar"]
    )
    json_ciktisi = json.dumps(aktif_sohbet["mesajlar"], ensure_ascii=False, indent=2)
    txt_ciktisi = "\n\n".join(
        f"[{'SEN' if m['role'] == 'user' else 'AI'}] {m['content']}" for m in aktif_sohbet["mesajlar"]
    )

    with col_md:
        st.download_button("📄 Markdown İndir", data=markdown_ciktisi,
                            file_name=f"{aktif_sohbet['ad']}.md", mime="text/markdown", use_container_width=True)
    with col_json:
        st.download_button("🧾 JSON İndir", data=json_ciktisi,
                            file_name=f"{aktif_sohbet['ad']}.json", mime="application/json", use_container_width=True)
    with col_txt:
        st.download_button("📝 TXT İndir", data=txt_ciktisi,
                            file_name=f"{aktif_sohbet['ad']}.txt", mime="text/plain", use_container_width=True)
else:
    st.info("👋 Henüz bir sohbet başlatılmadı. Aşağıdaki kutuya yazarak başlayabilirsiniz.")
