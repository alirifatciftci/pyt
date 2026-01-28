"""
VideoOtoFabrika - İçerik Üretici Modülü
Gemini API kullanarak TikTok senaryosu ve arama terimi üretir.
"""

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


class ContentGenerator:
    def __init__(self):
        """Gemini API'yi yapılandır"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY bulunamadı! .env dosyasını kontrol edin.")
        
        self.client = genai.Client(api_key=api_key)
    
    def generate_content(self):
        """
        TikTok için senaryo ve Pexels arama terimi üret
        
        Returns:
            tuple: (senaryo_metni, search_term)
        """
        try:
            prompt = """
            Bana TikTok/YouTube Shorts için 30 saniyelik, VİRAL olabilecek BOMBASTIK bir içerik senaryosu yaz.
            
            ÖNEMLİ KURALLAR:
            1. İLK CÜMLE BOMBA GİBİ OLMALI! Merak uyandırmalı (örnek: "DUR! Bunu duymadan geçme!", "İnanmayacaksın ama...", "ŞOK! Herkes bunu konuşuyor!")
            2. Sadece SESLENDIRME metni yaz. Görsel talimatlar verme
            3. Anlatıcı tarzında, doğrudan izleyiciye hitap et
            4. Kısa, akıcı ve BOMBASTIK cümleler kullan
            5. 30 saniyede rahatça okunabilecek uzunlukta olsun (yaklaşık 80-100 kelime)
            6. Türkçe olmalı ve sadece düz metin olarak ver
            7. TEK BİR KONU hakkında konuş
            8. SON CÜMLE ETKILEŞIM İSTEMELİ (örnek: "Sen ne düşünüyorsun?", "Yorumlara yaz!", "Beğenmeyi unutma!")
            
            VİRAL İÇERİK KATEGORİLERİ (SADECE EN VİRAL OLANLARI SEÇ):
            
            🔥 PARA & LÜKS YAŞAM (ÇOK VİRAL):
            - Genç yaşta zengin olanlar (örn: "18 yaşında milyoner oldu!")
            - Lüks arabalar ve fiyatları (örn: "Bu arabanın fiyatı inanılmaz!")
            - Pahalı evler ve yatlar (örn: "Dünyanın en pahalı evi!")
            - Kripto milyonerleri (örn: "Bitcoin'den zengin oldu!")
            - İş dünyası sırları (örn: "Amazon'un gizli stratejisi!")
            
            💰 BAŞARI HİKAYELERİ (ÇOK VİRAL):
            - Sıfırdan zirveye (örn: "Evsizken milyoner oldu!")
            - Genç girişimciler (örn: "20 yaşında şirket kurdu!")
            - Teknoloji devleri (örn: "Elon Musk'ın ilk işi!")
            - Spor yıldızları (örn: "Ronaldo'nun bilinmeyen hikayesi!")
            
            🌍 ŞOK EDİCİ GERÇEKLER (ÇOK VİRAL):
            - İnanılmaz bilimsel gerçekler (örn: "Güneş aslında...")
            - Tarihten şok edici olaylar (örn: "Titanik'in gizli sırrı!")
            - Hayvanlar aleminden inanılmaz detaylar (örn: "Köpekbalıkları aslında...")
            - İnsan vücudu hakkında şaşırtıcı bilgiler (örn: "Beynin gizli gücü!")
            
            🚀 TEKNOLOJİ & GELECEK (VİRAL):
            - Yapay zeka gelişmeleri (örn: "AI artık bunu yapabiliyor!")
            - Uzay haberleri (örn: "Mars'ta su bulundu!")
            - Yeni teknolojiler (örn: "iPhone'un gizli özelliği!")
            - Gelecek tahminleri (örn: "2030'da hayat böyle olacak!")
            
            ❌ BUNLARDAN KAÇIN (DÜŞÜK VİRAL):
            - Sıradan günlük bilgiler
            - Herkesin bildiği şeyler
            - Sıkıcı tarih dersleri
            - Genel kültür bilgileri
            - Ünlü kişilerin hayatları (Pexels'te görseli yok)
            
            ÇOK ÖNEMLİ - DOĞRULUK KURALLARI:
            ❗ İçerik MUTLAKA GERÇEK olmalı (uydurma bilgi verme!)
            ❗ Doğrulanabilir kaynaklara dayanmalı
            ❗ Abartma ama gerçekleri çarpıtma
            ❗ Clickbait olabilir ama yalan söyleme
            ❗ Şüpheli bilgiler için "iddiaya göre" gibi ifadeler kullan
            ❗ Her video FARKLI bir konu olmalı
            ❗ Pexels'te görseli bulunabilecek konular seç
            
            ARAMA TERİMİ İÇİN (KONUYLA TAM UYUMLU):
            - Para/Lüks için: "money", "luxury car", "mansion", "yacht", "gold", "cash"
            - Başarı için: "success", "entrepreneur", "business", "startup", "office"
            - Teknoloji için: "technology", "ai", "robot", "computer", "future"
            - Bilim için: "science", "space", "laboratory", "research", "brain"
            - Hayvanlar için: "shark", "lion", "eagle", "ocean", "wildlife"
            - Spor için: "football", "basketball", "athlete", "stadium", "training"
            
            ÇOK ÖNEMLİ - ARAMA TERİMİ KURALLARI:
            ❗ Arama terimi KONUNUN ÖZÜ olmalı (örn: Para → "money", Araba → "luxury car")
            ❗ Genel terimler kullan (örn: "celebrity" değil, "money" veya "success")
            ❗ Pexels'te mutlaka bulunabilecek terimler seç
            ❗ İngilizce olmalı ve 1-2 kelime olmalı
            
            Formatı şu şekilde olsun:
            SENARYO:
            [sadece seslendirme metni buraya - viral ve ilgi çekici ama GERÇEK]
            
            ARAMA_TERİMİ:
            [Pexels'te bulunabilecek genel arama terimi - 1-2 kelime, konuyla TAM UYUMLU]
            """
            
            print("🤖 Gemini'den içerik üretiliyor...")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            
            # Yanıtı parse et
            content = response.text
            
            # Senaryo ve arama terimini ayır
            if "SENARYO:" in content and "ARAMA_TERİMİ:" in content:
                parts = content.split("ARAMA_TERİMİ:")
                scenario = parts[0].replace("SENARYO:", "").strip()
                
                # Arama terimini al (1-2 kelime)
                search_term_raw = parts[1].strip().split('\n')[0].strip()
                # Sadece ilk 2 kelimeyi al
                search_term_words = search_term_raw.split()[:2]
                search_term = " ".join(search_term_words).lower()
            else:
                # Fallback: Tüm metni senaryo olarak al
                scenario = content.strip()
                search_term = "money"  # Varsayılan viral arama terimi
            
            print(f"✅ Senaryo üretildi ({len(scenario)} karakter)")
            print(f"🔍 Arama terimi: {search_term}")
            
            return scenario, search_term
            
        except Exception as e:
            print(f"❌ İçerik üretimi hatası: {e}")
            raise


if __name__ == "__main__":
    # Test
    generator = ContentGenerator()
    scenario, term = generator.generate_content()
    print("\n" + "="*50)
    print("SENARYO:")
    print(scenario)
    print("\n" + "="*50)
    print(f"ARAMA TERİMİ: {term}")
