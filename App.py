import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="Bulut Gök CV",
    page_icon="🤖",
    layout="centered"
)

# --- 2. SENİN BİLGİLERİN (KNOWLEDGE BASE) ---
# Bu metni kendi bilgilerine göre düzenle. Ne kadar detaylı yazarsan bot o kadar iyi konuşur.
MY_INFO = """
İSİM: Bulut Gök
ROL: Lead / Senior Product Manager
İLETİŞİM: bulutgok88@gmail.com | www.linkedin.com/in/bulut-gök-49814646 | Telefon: +905554274616

ÖZET:
13+ yıllık teknoloji deneyimine sahibim. İlk 5 yılım IT tarafında (IT Engineer / IT Administrator / IT Manager) geçti. Son 8 yıldır ise Turkcell’de BiP Messenger ürününde Product Manager ve Master Lead Product Manager olarak çalıştım. Kullanıcı büyümesi, kullanıcı yolculukları, global iş ortaklıkları, AIML ile chatbot geliştirimi, ürün stratejisi, UX geliştirme ve içerik yönetimi gibi alanlarda yoğun tecrübem var.

DENEYİM DETAYLARI:

--- DİJİTAL ÜRÜN YÖNETİMİ (Turkcell - BiP Messenger) ---

**Master Lead Product Manager (2022 - 2024)**
- 100+ milyon kullanıcılı BiP uygulamasının yönetim ekibi üyesi olarak görev yaptım.
- Jamaika ve Papua Yeni Gine gibi pazarlarda BiP'in benimsenmesi için Digicel Pacific ortaklığını yönettim.
- Aktif kullanıcı metriklerini (MAU/DAU) artırmak için stratejik planlar geliştirdim ve Push Notification stratejilerini kurguladım.
- BiP resmi web sitesinin yeniden tasarım sürecini ve içerik ajanslarıyla ilişkileri yönettim.
- Kullanıcı geri bildirimlerini (App Store/Google Play) analiz ederek ürünü iyileştirdim.

**Product Manager (2016 - 2022)**
- BiP Discover/Marketplace platformunun (Chatbotlar) yönetimini üstlendim; Sağlık Bakanlığı, Tarım Bakanlığı, Dr. Mehmet Öz ve çeşitli belediyeler için resmi chatbot'ların tasarım ve geliştirme (AIML/XML) süreçlerini yönettim.
- Büyüme (Growth) ekibinin bir parçası olarak veri analizi (SQL, Mixpanel, Smartcube) yaparak stratejik kararlar aldım.
- Uygulama içi satın alma (In-app purchase) süreçlerini ve ödeme sistemlerini yönettim.

--- IT & MÜHENDİSLİK (IBM, Kantar, Enka) ---

**IT Administrator @ IBM Global Services & Kantar Millward Brown (2014 - 2016)**
- 100'e yakın kullanıcısı olan ofisin tüm IT altyapısını, sunucu (Server 2012 R2) ve yedekleme süreçlerini yönettim.
- Active Directory yönetimi, güvenlik prosedürleri ve SOX standartlarına uyumluluğu sağladım.
- Bu görevimdeki başarım sayesinde "IBM Best IT of EMEA" ödülünü kazandım.

**IT Engineer @ ENKA İnşaat (Gabon, Afrika) (2013)**
- Gabon'daki 3 büyük projenin IT altyapısını (CCTV, Network, Sunucular) sıfırdan kurdum ve yönettim.

**Diğer:** Forensic People'da Adli Bilişim Uzmanı olarak veri kurtarma ve dijital analiz çalışmaları yaptım (2011-2012).

YETENEKLER & ARAÇLAR:
- **Ürün & Analiz:** Ürün Stratejisi, Mixpanel, Google Analytics, A/B Testleri, MVP Yönetimi.
- **Yazılım & Veri:** SQL (İleri Seviye), AIML (Chatbot), XML, C#, Java, HTML, ASP.NET.
- **Sistem & IT:** Active Directory, Windows Server, Exchange Server, SAP, Ağ Yönetimi, Adli Bilişim (Encase, FTK).
- **Diller:** Türkçe (Anadil), İngilizce (C1 - İleri Seviye).

EĞİTİM:
- Ege Üniversitesi, Bilgisayar Mühendisliği (2007 - 2011)

HOBİLER & KİŞİLİK:
- Takım oyuncusuyumdur ama inisiyatif alıp bireysel proje yürütmeyi de severim.
- Yaratıcı yönüm kuvvetlidir; boş zamanlarımda kısa senaryolar yazar, video oyunları oynarım.
- "Maker" ruhuna sahibim; geçmişte Google Play için kendi oyunlarımı geliştirdim ve kişisel web projelerimi hayata geçirdim.
- Sürekli öğrenme tutkunuyum; şu anda 4 büyük Türk üniversitesinin ortaklaşa yürüttüğü kapsamlı "İstatistik ve Yapay Zeka Geliştirimi" eğitim programına devam ediyorum.

SORU CEVAP TARZI:
- "En büyük başarın nedir?" diye sorulursa: "BiP gibi global bir üründe Digicel Pacific ortaklığını yöneterek kullanıcı tabanını okyanus ötesine taşımam ve IT kökenimle teknik ekiplerle kusursuz çalışabilmem." de.
- "Neden IT'den ürüne geçtin?" derlerse: "Teknik sorunları çözmeyi seviyordum ama 'doğru sorunu' çözmenin daha büyük değer yarattığını fark ettim. Şimdi teknik kökenimle doğru ürünü en verimli şekilde inşa ettiriyorum." de.
- Maaş sorulursa: "Bu konuyu Bulut Bey ile yüz yüze görüşmeniz daha sağlıklı olur." de.
"""

# --- 3. BOTUN KİŞİLİK AYARLARI (SYSTEM PROMPT) ---
SYSTEM_INSTRUCTION = f"""
Sen, yukarıdaki bilgileri verilen adayın (Yapay Zeka) asistanısın. 
Görevin: İşe alım uzmanlarının (İK) sorularını adayın ağzından değil, onun asistanı olarak yanıtlamak.

KURALLAR:
1. SADECE verilen "MY_INFO" metnindeki bilgileri kullan. 
2. Bilmediğin bir detay sorulursa dürüstçe "Bu detay dosyalarımda yok, ancak kendisine şu kanallardan ulaşabilirsiniz..." diyerek iletişim bilgilerini ver. Asla bilgi uydurma.
3. Profesyonel, nazik ama enerjik bir dil kullan.
4. Cevapların kısa ve net olsun (maksimum 3-4 cümle). Destan yazma.
5. İK yetkilisiyle konuşuyorsun, saygılı ol.
6. ÖNEMLİ: Kullanıcı hangi dilde soru sorarsa (İngilizce, Almanca vb.), o dilde cevap ver.

BİLGİLER:
{MY_INFO}
"""

# --- 4. API BAĞLANTISI ---
# Streamlit Secrets'tan anahtarı alıyoruz
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Anahtarı bulunamadı. Lütfen Streamlit ayarlarından ekleyin.")
    st.stop()

# Modeli Hazırla (Gemini 1.5 Flash - Hızlı ve Bedava Tier uyumlu)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

# --- 5. SOHBET ARAYÜZÜ ---
st.title("👋 Merhaba! Ben Bulut'un Yapay Zeka Asistanıyım")
st.caption("Bulut Gök hakkında merak ettiğiniz her şeyi bana sorabilirsiniz.")

# Sohbet geçmişini tut (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []
    # İlk açılış mesajı
    welcome_msg = "Merhaba! CV, projeler veya yetenekler hakkında ne bilmek istersiniz?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# Geçmiş mesajları ekrana yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan girdi al
if prompt := st.chat_input("Sorunuzu buraya yazın..."):
    
    # 1. Kullanıcı mesajını ekrana bas
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Gemini'ye gönder ve cevap al
    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            try:
                # Sohbet geçmişini Gemini formatına çevir
                chat_history = [
                    {"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]}
                    for msg in st.session_state.messages if msg["role"] != "system"
                ]
                
                # Cevabı üret
                chat = model.start_chat(history=chat_history[:-1]) # Son mesajı hariç tut, onu send_message ile atacağız
                response = chat.send_message(prompt)
                
                st.markdown(response.text)
                
                # 3. Cevabı kaydet
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:

                st.error(f"Bir hata oluştu: {e}")
