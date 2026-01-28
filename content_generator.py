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
            Bana TikTok/YouTube Shorts için 30 saniyelik, VİRAL olabilecek ilgi çekici bir içerik senaryosu yaz.
            
            ÖNEMLİ KURALLAR:
            1. İLK CÜMLE BOMBA GİBİ OLMALI! Merak uyandırmalı (örnek: "DUR! Bunu duymadan geçme!", "İnanmayacaksın ama...", "ŞOK! Herkes bunu konuşuyor!")
            2. Sadece SESLENDIRME metni yaz. Görsel talimatlar verme
            3. Anlatıcı tarzında, doğrudan izleyiciye hitap et
            4. Kısa, akıcı ve BOMBASTIK cümleler kullan
            5. 30 saniyede rahatça okunabilecek uzunlukta olsun (yaklaşık 80-100 kelime)
            6. Türkçe olmalı ve sadece düz metin olarak ver
            7. TEK BİR KONU hakkında konuş
            8. SON CÜMLE ETKILEŞIM İSTEMELI (örnek: "Sen ne düşünüyorsun?", "Yorumlara yaz!", "Beğenmeyi unutma!")
            
            VİRAL İÇERİK KATEGORİLERİ (Her seferinde FARKLI birini seç):
            
            🔥 ÜNLÜLER & DEDIKODU:
            - Ünlü isimlerin az bilinen gerçekleri
            - Hollywood sırları ve skandallar
            - Ünlülerin lüks yaşamları
            - Ünlü çiftlerin ilişki hikayeleri
            - Sosyal medya fenomenleri
            
            💰 PARA & BAŞARI:
            - Genç yaşta zengin olanlar
            - İş dünyası sırları
            - Kripto ve teknoloji milyarderleri
            - Lüks yaşam tarzları
            - Başarı hikayeleri
            
            🌍 GÜNCEL OLAYLAR & TRENDLER:
            - Viral olan olaylar
            - Sosyal medya trendleri
            - Teknoloji haberleri
            - Popüler kültür olayları
            - Şok edici haberler
            
            🎬 EĞLENCE & MEDYA:
            - Film ve dizi sırları
            - Müzik dünyası skandalları
            - Netflix ve platformlar
            - Oyun dünyası haberleri
            - Viral videolar
            
            💎 LÜKS & YAŞAM TARZI:
            - En pahalı şeyler
            - Lüks otomobiller
            - Milyonluk evler
            - Pahalı tatiller
            - Lüks markalar
            
            🚀 TEKNOLOJİ & GELECEK:
            - Yapay zeka gelişmeleri
            - Uzay haberleri
            - Yeni teknolojiler
            - Gelecek tahminleri
            - Bilim kurgu gerçek oluyor
            
            🧠 İLGİNÇ BİLGİLER & BİLİM:
            - Şaşırtıcı bilimsel gerçekler
            - İnsan vücudu hakkında ilginç bilgiler
            - Hayvanlar aleminden şok edici detaylar
            - Tarihten ilginç olaylar
            - Psikoloji ve beyin bilimi
            
            ÇOK ÖNEMLİ - DOĞRULUK KURALLARI:
            ❗ İçerik MUTLAKA GERÇEK olmalı (uydurma bilgi verme!)
            ❗ Doğrulanabilir kaynaklara dayanmalı
            ❗ Abartma ama gerçekleri çarpıtma
            ❗ Clickbait olabilir ama yalan söyleme
            ❗ Şüpheli bilgiler için "iddiaya göre" gibi ifadeler kullan
            ❗ Her video FARKLI bir konu olmalı
            ❗ Pexels'te videosu bulunabilecek konular seç
            
            ARAMA TERİMİ İÇİN:
            - Ünlüler için: "celebrity" veya "famous people" veya "paparazzi"
            - Para için: "money" veya "luxury lifestyle" veya "rich"
            - Teknoloji için: "technology" veya "artificial intelligence" veya "future"
            - Lüks için: "luxury car" veya "mansion" veya "yacht"
            - Şehir için: "city lights" veya "urban" veya "nightlife"
            - Bilim için: "science" veya "laboratory" veya "research"
            - Genel için: "people" veya "lifestyle" veya "modern"
            
            Formatı şu şekilde olsun:
            SENARYO:
            [sadece seslendirme metni buraya - viral ve ilgi çekici ama GERÇEK]
            
            ARAMA_TERİMİ:
            [Pexels'te bulunabilecek genel arama terimi - 1-2 kelime]
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
                
                # Arama terimini al (1-2 kelime olabilir)
                search_term_raw = parts[1].strip().split('\n')[0].strip()
                # Sadece ilk 2 kelimeyi al
                search_term_words = search_term_raw.split()[:2]
                search_term = " ".join(search_term_words).lower()
            else:
                # Fallback: Tüm metni senaryo olarak al
                scenario = content.strip()
                search_term = "nature"  # Varsayılan arama terimi
            
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
