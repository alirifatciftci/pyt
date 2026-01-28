"""
Emlak Fırsat Avcısı - AI Analiz Modülü
Gemini API ile emlak ilanlarını analiz eder
"""

import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()


class GeminiAnaliz:
    def __init__(self):
        """Gemini API'yi yapılandır"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY bulunamadı! .env dosyasını kontrol edin.")
        
        self.client = genai.Client(api_key=api_key)
    
    def analiz_et(self, ilan_verisi):
        """
        Emlak ilanını Gemini ile analiz et
        
        Args:
            ilan_verisi (dict): İlan bilgileri
            
        Returns:
            dict: {"puan": 1-10, "yorum": "...", "karar": "AL/SAT"}
        """
        try:
            # İlan bilgilerini prompt'a dönüştür
            prompt = f"""
            Bir emlak ilanını analiz et ve fırsat puanı ver.
            
            İLAN BİLGİLERİ:
            - İlçe: {ilan_verisi.get('ilce', 'Bilinmiyor')}
            - Mahalle: {ilan_verisi.get('mahalle', 'Bilinmiyor')}
            - Fiyat: {ilan_verisi.get('fiyat', 0):,} TL
            - Metrekare: {ilan_verisi.get('m2', 0)} m²
            - Oda Sayısı: {ilan_verisi.get('oda', 'Bilinmiyor')}
            - Açıklama: {ilan_verisi.get('aciklama', 'Yok')}
            
            GÖREV:
            1. Bu ilanın fırsat olup olmadığını değerlendir
            2. Fiyat/m² oranını hesapla
            3. Açıklamadaki anahtar kelimeleri analiz et (acil, kelepir, krediye uygun vb.)
            4. 1-10 arası fırsat puanı ver (10 = çok iyi fırsat)
            5. Kısa bir yorum yaz
            6. AL veya SAT kararı ver
            
            CEVAP FORMATI (sadece JSON döndür, başka açıklama yapma):
            {{
                "puan": 8,
                "yorum": "Fiyat/m² oranı iyi, acil satılık olduğu için pazarlık şansı var",
                "karar": "AL"
            }}
            """
            
            print(f"🤖 Gemini analiz ediyor: {ilan_verisi.get('ilce')} - {ilan_verisi.get('mahalle')}...")
            
            response = self.client.models.generate_content(
                model='gemini-1.5-flash-latest',
                contents=prompt
            )
            
            # JSON parse et
            content = response.text.strip()
            
            # JSON'u temizle (markdown kod bloğu varsa)
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
        "ilce": "Çorlu",
        "mahalle": "Önerler",
        "fiyat": 3500000,
        "m2": 110,
        "oda": "3+1",
        "aciklama": "Acil satılık, krediye uygun, kelepir"
    }
    
    analiz = GeminiAnaliz()
    sonuc = analiz.analiz_et(test_ilan)
    print("\n" + "="*50)
    print("TEST SONUCU:")
    print(json.dumps(sonuc, indent=2, ensure_ascii=False))
