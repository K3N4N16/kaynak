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
    page_title="Quantum AI Studio Pro v12.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# TEMA: KOYU SIDEBAR + BEYAZ / YÜKSEK OKUNAKLI ÇIKTI ALANI
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }

.stApp {
    background: radial-gradient(circle at 15% 0%, #1a1f3a 0%, #0b0e1a 45%, #05070f 100%);
    color: #e6e9f5;
}

.studio-title {
    background: linear-gradient(90deg, #7c3aed 0%, #06b6d4 50%, #10b981 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-weight: 800; font-size: 2.6rem; letter-spacing: -0.02em; margin-bottom: 0;
}
.studio-subtitle { color: #94a3b8; font-size: 0.95rem; margin-top: -8px; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1324 0%, #0a0d1c 100%) !important;
    border-right: 1px solid rgba(124, 58, 237, 0.25);
}
section[data-testid="stSidebar"] * { color: #dbe1f5 !important; }
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 { color: #a78bfa !important; font-weight: 700; }

div[data-testid="stMetric"] {
    background: rgba(124, 58, 237, 0.08);
    border: 1px solid rgba(124, 58, 237, 0.25);
    border-radius: 12px; padding: 10px 14px;
}
div[data-testid="stMetricValue"] { color: #a78bfa !important; }

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

.stSelectbox label, .stSlider label, .stTextArea label, .stTextInput label, .stRadio label { color: #cbd5e1 !important; font-weight: 500; }

div.stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%);
    color: white !important; border-radius: 10px; border: none;
    font-weight: 600; height: 48px; transition: all 0.2s ease;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.3);
}
div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(124, 58, 237, 0.45); }

section[data-testid="stSidebar"] div.stButton > button {
    background: rgba(255,255,255,0.06); box-shadow: none; border: 1px solid rgba(255,255,255,0.12);
}

div.stDownloadButton > button {
    background: rgba(16, 185, 129, 0.12); color: #34d399 !important;
    border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 10px; font-weight: 600;
}

/* ---- ÇIKTI / SOHBET ALANI: BEYAZ ZEMİN, SİYAH YAZI (OKUNAKLILIK İÇİN) ---- */
.stChatMessage {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px !important;
    padding: 10px 14px !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.18);
}
.stChatMessage p, .stChatMessage li, .stChatMessage span, .stChatMessage div,
.stChatMessage h1, .stChatMessage h2, .stChatMessage h3, .stChatMessage strong {
    color: #0f172a !important;
}
.stChatMessage code { color: #7c3aed !important; background-color: #f1f5f9 !important; }
.stChatMessage pre { background-color: #0f172a !important; border-radius: 10px !important; }
.stChatMessage pre code { color: #e6e9f5 !important; background-color: transparent !important; }

/* Akıl yürütme kutusu - açık zemin, koyu yazı */
.reasoning-container {
    background-color: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-left: 4px solid #06b6d4 !important;
    border-radius: 10px; padding: 14px 16px;
    font-family: 'JetBrains Mono', monospace;
    color: #334155 !important; font-size: 0.85rem; margin-bottom: 10px;
}

.badge {
    display: inline-block; padding: 3px 10px; border-radius: 999px;
    background: rgba(124,58,237,0.15); border: 1px solid rgba(124,58,237,0.4);
    color: #c4b5fd; font-size: 0.75rem; font-weight: 600; margin-right: 6px;
}

hr { border-color: rgba(255,255,255,0.08) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='studio-title'>⚡ Quantum AI Studio Pro v12.0</div>", unsafe_allow_html=True)
st.markdown("<p class='studio-subtitle'>Nvidia & Açık Kaynak Model Ordusu · Çoklu Oturum · Model Karşılaştırma · Beyaz Zeminli Okunaklı Çıktı</p>", unsafe_allow_html=True)
st.write("")

# ============================================================
# MODEL HAVUZU (GENİŞLETİLMİŞ VE EKSİKSİZ)
# ============================================================
model_havuzu = {
    "Nvidia Llama 3.3 Nemotron Super (Hız & Performans Şampiyonu)": "nvidia/llama-3.3-nemotron-super",
    "Nvidia Nemotron 4 340B (Üstün Dil & Sentetik Veri Yeteneği)": "nvidia/nemotron-4-340b-instruct",
    "Nvidia NeVA 22B (Gelişmiş Görsel & Resim Analiz Motoru)": "nvidia/neva-22b",
    "Nvidia NV-Embed-QA (Gelişmiş Döküman & Veri Arama)": "nvidia/nv-embedqa-e5-v5",
    "DeepSeek V4 Pro (En Gelişmiş Kod & Optimizasyon Canavarı)": "deepseek-ai/deepseek-v4-pro",
    "DeepSeek R1 (Maksimum Akıl Yürütme & Derin Düşünme)": "deepseek-ai/deepseek-r1",
    "Llama 3.1 405B (Dünyanın En Büyük Açık Kaynak Modeli)": "meta/llama-3.1-405b-instruct",
    "Llama 3.2 90B Vision (Çoklu Mod & Arayüz Okuma)": "meta/llama-3.2-90b-vision-instruct",
    "GLM 5.2 (Yüksek Bağlam & Kararlı Otomasyon)": "z-ai/glm-5.2",
    "Qwen 2.5 72B (Hatasız Algoritma ve Kodlama Yapıları)": "qwen/qwen-2.5-72b-instruct",
    "Mistral Large 3 (Gelişmiş Akıl Yürütme Amiral Gemisi)": "mistralai/mistral-large-2407",
    "Mixtral 8x22B (Uzman Karışımı / MoE Mimarisi)": "mistralai/mixtral-8x22b-instruct-v0.1",
    "Google Gemma 2 27B (Verimli & Hızlı Açık Kaynak)": "google/gemma-2-27b-it",
    "Microsoft Phi-3 Medium (Kompakt & Güçlü)": "microsoft/phi-3-medium-4k-instruct",
    "Cohere Command R+ (Araç Kullanımı & RAG Uzmanı)": "cohere/command-r-plus",
}

SISTEM_PRESETLERI = {
    "Yazılım Mimarı": "Sen profesyonel bir yazılım mimarı, kod optimizasyon uzmanı ve otomasyon danışmanısın. Kısa, net ve üretime hazır kod örnekleri sun.",
    "Veri Bilimci": "Sen deneyimli bir veri bilimcisin. İstatistiksel doğruluğa önem verir, varsayımlarını açıkça belirtir ve kodunu adım adım açıklarsın.",
    "Metin Editörü": "Sen titiz bir metin editörüsün. Dil bilgisi, akıcılık ve ton tutarlılığına odaklanırsın; gereksiz süslemeden kaçınırsın.",
    "Kısa & Öz Asistan": "Kısa, öz ve doğrudan cevaplar ver. Gereksiz açıklamalardan kaçın, sadece istenen çıktıyı üret.",
    "Serbest / Özel": None,
}

# ============================================================
# OTURUM DURUMU İLKLENDİRME
# ============================================================
if "sohbetler" not in st.session_state:
    ilk_id = str(uuid.uuid4())[:8]
    st.session_state["sohbetler"] = {
        ilk_id: {"ad": "Yeni Sohbet 1", "mesajlar": [], "olusturma": datetime.now().isoformat(), "favori_modeller": []}
    }
    st.session_state["aktif_sohbet_id"] = ilk_id

if "aktif_sohbet_id" not in st.session_state:
    st.session_state["aktif_sohbet_id"] = list(st.session_state["sohbetler"].keys())[0]

if "favori_modeller" not in st.session_state:
    st.session_state["favori_modeller"] = []

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
            "mesajlar": [], "olusturma": datetime.now().isoformat(), "favori_modeller": []
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
        yeni_ad = st.text_input("Yeniden adlandır:", value=aktif_sohbet["ad"], label_visibility="collapsed")
        if yeni_ad != aktif_sohbet["ad"]:
            aktif_sohbet["ad"] = yeni_ad
    with col_sil:
        if st.button("🗑️ Sohbeti Sil", use_container_width=True) and len(st.session_state["sohbetler"]) > 1:
            del st.session_state["sohbetler"][aktif_id]
            st.session_state["aktif_sohbet_id"] = list(st.session_state["sohbetler"].keys())[0]
            st.rerun()

    # Sohbet içi arama
    arama_terimi = st.text_input("🔍 Bu sohbette ara:", placeholder="anahtar kelime...")

    st.markdown("---")
    st.header("🤖 Nvidia & Open-Source Model Ordusu")
    secilen_etiket = st.selectbox("Çalıştırılacak Model:", list(model_havuzu.keys()))
    aktif_model = model_havuzu[secilen_etiket]

    if st.button("⭐ Bu Modeli Favorilere Ekle", use_container_width=True):
        if aktif_model not in st.session_state["favori_modeller"]:
            st.session_state["favori_modeller"].append(aktif_model)

    if st.session_state["favori_modeller"]:
        favori_etiketler = [k for k, v in model_havuzu.items() if v in st.session_state["favori_modeller"]]
        st.caption("⭐ Favoriler: " + ", ".join(favori_etiketler))

    st.markdown("---")
    st.header("⚔️ Model Karşılaştırma Modu")
    karsilastirma_aktif = st.checkbox("Aynı komutu birden fazla modelde çalıştır")
    karsilastirma_modelleri = []
    if karsilastirma_aktif:
        karsilastirma_modelleri = st.multiselect(
            "Karşılaştırılacak modeller:", list(model_havuzu.keys()),
            default=list(model_havuzu.keys())[:2]
        )

    st.markdown("---")
    st.header("🎛️ Sistem Rolü")
    preset_secim = st.selectbox("Hazır Rol Şablonu:", list(SISTEM_PRESETLERI.keys()))
    if SISTEM_PRESETLERI[preset_secim] is not None:
        system_prompt = st.text_area("Sistem Rolü (System Prompt):", value=SISTEM_PRESETLERI[preset_secim], height=100)
    else:
        system_prompt = st.text_area("Sistem Rolü (System Prompt):", value="Sen yardımsever ve uzman bir asistansın.", height=100)

    st.markdown("---")
    st.header("🎚️ Hassasiyet Ayarları")
    temperature = st.slider("Yaratıcılık (Temperature):", 0.0, 1.0, 0.5, 0.05)
    top_p = st.slider("Çeşitlilik (Top-P):", 0.1, 1.0, 0.9, 0.05)
    max_tokens = st.slider("Maksimum Yanıt Uzunluğu (Token):", 256, 8192, 2048, 128)
    frequency_penalty = st.slider("Tekrar Cezası (Frequency Penalty):", 0.0, 2.0, 0.0, 0.1)
    presence_penalty = st.slider("Konu Çeşitliliği (Presence Penalty):", 0.0, 2.0, 0.0, 0.1)

    st.markdown("---")
    st.header("📎 Bağlam Dosyası (Opsiyonel)")
    yuklenen_dosya = st.file_uploader("Metin/Kod dosyası ekle (.txt, .md, .py, .json, .csv)", type=["txt", "md", "py", "json", "csv"])
    dosya_icerigi = ""
    if yuklenen_dosya is not None:
        try:
            dosya_icerigi = yuklenen_dosya.read().decode("utf-8", errors="ignore")
            st.caption(f"✅ `{yuklenen_dosya.name}` yüklendi ({len(dosya_icerigi)} karakter). Bir sonraki mesaja otomatik eklenecek.")
        except Exception:
            st.warning("Dosya okunamadı.")

    st.markdown("---")
    st.header("📥 Sohbet İçe Aktar")
    ice_aktarilan = st.file_uploader("Daha önce indirilen JSON sohbeti yükle", type=["json"], key="import_json")
    if ice_aktarilan is not None:
        if st.button("İçe Aktarımı Onayla", use_container_width=True):
            try:
                yuklenen_mesajlar = json.loads(ice_aktarilan.read().decode("utf-8"))
                yeni_id = str(uuid.uuid4())[:8]
                st.session_state["sohbetler"][yeni_id] = {
                    "ad": f"İçe Aktarılan Sohbet",
                    "mesajlar": yuklenen_mesajlar,
                    "olusturma": datetime.now().isoformat(),
                    "favori_modeller": []
                }
                st.session_state["aktif_sohbet_id"] = yeni_id
                st.success("Sohbet başarıyla içe aktarıldı.")
                st.rerun()
            except Exception as e:
                st.error(f"İçe aktarım hatası: {e}")

    st.markdown("---")
    if st.button("🧹 Sohbet Geçmişini Temizle", use_container_width=True):
        aktif_sohbet["mesajlar"] = []
        st.rerun()

# ============================================================
# ÜST BİLGİ BANDI
# ============================================================
toplam_mesaj = len(aktif_sohbet["mesajlar"])
toplam_kelime = sum(len(m["content"].split()) for m in aktif_sohbet["mesajlar"])
kullanici_mesaj_sayisi = sum(1 for m in aktif_sohbet["mesajlar"] if m["role"] == "user")
tahmini_token = int(toplam_kelime * 1.3)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💬 Mesaj Sayısı", toplam_mesaj)
c2.metric("📝 Toplam Kelime", toplam_kelime)
c3.metric("🔢 Tahmini Token", tahmini_token)
c4.metric("🔁 Tur Sayısı", kullanici_mesaj_sayisi)
c5.metric("🤖 Aktif Model", secilen_etiket.split(" (")[0])

st.markdown("---")

# ============================================================
# GEÇMİŞ SOHBETİ GÖSTER (ARAMA FİLTRESİ İLE)
# ============================================================
for idx, mesaj in enumerate(aktif_sohbet["mesajlar"]):
    if arama_terimi and arama_terimi.lower() not in mesaj["content"].lower():
        continue
    avatar = "🧑‍💻" if mesaj["role"] == "user" else "⚡"
    with st.chat_message(mesaj["role"], avatar=avatar):
        if mesaj.get("dusunme"):
            st.markdown(f"<div class='reasoning-container'>🕵️ <b>Akıl Yürütme:</b><br>{mesaj['dusunme']}</div>", unsafe_allow_html=True)
        st.markdown(mesaj["content"])
        if mesaj["role"] == "assistant":
            with st.expander("📋 Bu yanıtı kopyala / görüntüle", expanded=False):
                st.code(mesaj["content"], language=None)

# ============================================================
# YARDIMCI FONKSİYON: MODEL ÇAĞRISI (STREAM)
# ============================================================
def modelden_yanit_al(client, model, mesaj_listesi, temperature, top_p, max_tokens,
                       frequency_penalty, presence_penalty,
                       reasoning_placeholder, content_placeholder):
    tam_cevap = ""
    tam_dusunme = ""
    completion = client.chat.completions.create(
        model=model,
        messages=mesaj_listesi,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
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
# SOHBET GİRİŞİ (ÇOKLU TUR + KARŞILAŞTIRMA MODU)
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

        # Sohbet ilk mesajsa, oturuma otomatik başlık ver
        if kullanici_mesaj_sayisi == 0:
            aktif_sohbet["ad"] = (kullanici_girdisi[:28] + "…") if len(kullanici_girdisi) > 28 else kullanici_girdisi

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(kullanici_girdisi)

        try:
            client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)
            gecmis_mesajlar = [{"role": "system", "content": system_prompt}]
            for m in aktif_sohbet["mesajlar"][:-1]:
                gecmis_mesajlar.append({"role": m["role"], "content": m["content"]})
            gecmis_mesajlar.append({"role": "user", "content": nihai_girdi})

            if karsilastirma_aktif and len(karsilastirma_modelleri) >= 2:
                # ---- MODEL KARŞILAŞTIRMA MODU ----
                st.markdown("### ⚔️ Model Karşılaştırma Sonuçları")
                kolonlar = st.columns(len(karsilastirma_modelleri))
                for kolon, model_etiket in zip(kolonlar, karsilastirma_modelleri):
                    with kolon:
                        st.markdown(f"**{model_etiket.split(' (')[0]}**")
                        reasoning_placeholder = st.empty()
                        content_placeholder = st.empty()
                        baslangic = time.time()
                        try:
                            cevap, dusunme = modelden_yanit_al(
                                client, model_havuzu[model_etiket], gecmis_mesajlar,
                                temperature, top_p, max_tokens, frequency_penalty, presence_penalty,
                                reasoning_placeholder, content_placeholder
                            )
                            sure = round(time.time() - baslangic, 2)
                            st.caption(f"⏱️ {sure} sn · {len(cevap.split())} kelime")
                        except Exception as e:
                            st.error(f"Hata: {e}")
                # Karşılaştırma modunda ilk seçilen modelin cevabı geçmişe kaydedilir
                aktif_sohbet["mesajlar"].append({
                    "role": "assistant",
                    "content": f"*(Model karşılaştırma modu çalıştırıldı: {', '.join(karsilastirma_modelleri)})*",
                    "dusunme": ""
                })
            else:
                # ---- TEKİL MODEL MODU ----
                with st.chat_message("assistant", avatar="⚡"):
                    reasoning_placeholder = st.empty()
                    content_placeholder = st.empty()
                    baslangic = time.time()
                    cevap, dusunme = modelden_yanit_al(
                        client, aktif_model, gecmis_mesajlar,
                        temperature, top_p, max_tokens, frequency_penalty, presence_penalty,
                        reasoning_placeholder, content_placeholder
                    )
                    sure = round(time.time() - baslangic, 2)
                    kelime_sn = round(len(cevap.split()) / sure, 1) if sure > 0 else 0
                    st.caption(f"⏱️ Yanıt süresi: {sure} sn · {len(cevap.split())} kelime · ~{kelime_sn} kelime/sn")

                aktif_sohbet["mesajlar"].append({"role": "assistant", "content": cevap, "dusunme": dusunme})

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
                aktif_sohbet["mesajlar"].pop()
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
