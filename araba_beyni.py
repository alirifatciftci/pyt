"""
Araba Fırsat Avcısı - AI Analiz Modülü
Gemini API ile araba ilanlarını analiz eder
"""

import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()


class GeminiArabaAnaliz:
    def __init__(self):
        """Gemini API'yi yapılandır"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY bulunamadı! .env dosyasını kontrol edin.")
        
        self.client = genai.Client(api_key=api_key)
    
    def analiz_et(self, ilan_verisi):
        """
        Araba ilanını Gemini ile analiz et
        
        Args:
            ilan_verisi (dict): İlan bilgileri
            
        Returns:
            dict: {"puan": 1-10, "yorum": "...", "karar": "AL/SAT"}
        """
        try:
            # İlan bilgilerini prompt'a dönüştür
            prompt = f"""
            Bir ikinci el araba ilanını analiz et ve fırsat puanı ver.
            
            ARAÇ BİLGİLERİ:
            - Marka/Model: {ilan_verisi.get('marka', 'Bilinmiyor')} {ilan_verisi.get('model', 'Bilinmiyor')}
            - Yıl: {ilan_verisi.get('yil', 0)}
            - Kilometre: {ilan_verisi.get('km', 0):,} km
            - Yakıt: {ilan_verisi.get('yakit', 'Bilinmiyor')}
            - Vites: {ilan_verisi.get('vites', 'Bilinmiyor')}
            - Renk: {ilan_verisi.get('renk', 'Bilinmiyor')}
            - Fiyat: {ilan_verisi.get('fiyat', 0):,} TL
            - Açıklama: {ilan_verisi.get('aciklama', 'Yok')}
            
            GÖREV:
            1. Bu aracın fiyat/performans oranını değerlendir
            2. Kilometre ve yıl oranını analiz et (yıllık ortalama km)
            3. Açıklamadaki anahtar kelimeleri değerlendir (hasarsız, boyasız, bakımlı, garaj arabası vb.)
            4. Marka/model güvenilirliğini ve piyasa değerini göz önünde bulundur
            5. 1-10 arası fırsat puanı ver (10 = çok iyi fırsat)
            6. Kısa bir yorum yaz
            7. AL veya SAT kararı ver
            
            DEĞERLENDİRME KRİTERLERİ:
            - Yıllık ortalama km: 15.000-20.000 km ideal
            - Hasarsız/boyasız: Artı puan
            - Bakımlı/garaj arabası: Artı puan
            - İlk sahibinden: Artı puan
            - Acil satılık: Pazarlık şansı
            - Fiyat piyasa ortalamasının altındaysa: Artı puan
            
            CEVAP FORMATI (sadece JSON döndür, başka açıklama yapma):
            {{
                "puan": 8,
                "yorum": "2018 model 80.000 km'de araç için fiyat uygun. Yıllık ortalama km düşük, hasarsız olması avantaj",
                "karar": "AL"
            }}
            """
            
            print(f"🤖 Gemini analiz ediyor: {ilan_verisi.get('marka')} {ilan_verisi.get('model')} {ilan_verisi.get('yil')}...")
            
            response = self.client.models.generate_content(
                model='gemini-1.5-flash-latest',
                contents=prompt
            )
            
            # JSON parse et
            content = response.text.strip()
            
            # JSON'u temizle
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            sonuc = json.loads(content)
            
            # Validasyon
            if "puan" not in sonuc or "yorum" not in sonuc or "karar" not in sonuc:
                raise ValueError("Eksik alanlar var")
            
            # Puan kontrolü
            sonuc["puan"] = max(1, min(10, int(sonuc["puan"])))
            
            # Karar kontrolü
            if sonuc["karar"] not in ["AL", "SAT"]:
                sonuc["karar"] = "SAT"
            
            print(f"✅ Analiz tamamlandı: Puan {sonuc['puan']}/10, Karar: {sonuc['karar']}")
            
            return sonuc
            
        except Exception as e:
            print(f"⚠️ Analiz hatası: {e}")
            # Varsayılan değer döndür
            return {
                "puan": 5,
                "yorum": "Analiz yapılamadı, manuel kontrol gerekli",
                "karar": "SAT"
            }


if __name__ == "__main__":
    # Test
    test_ilan = {
        "marka": "Volkswagen",
        "model": "Polo",
        "yil": 2018,
        "km": 85000,
        "yakit": "Benzin",
        "vites": "Manuel",
        "renk": "Beyaz",
        "fiyat": 450000,
        "aciklama": "Garaj arabası, bakımlı, hasarsız"
    }
    
    analiz = GeminiArabaAnaliz()
    sonuc = analiz.analiz_et(test_ilan)
    print("\n" + "="*50)
    print("TEST SONUCU:")
    print(json.dumps(sonuc, indent=2, ensure_ascii=False))
