"""
Araba Fırsat Avcısı - Rapor Modülü
Analiz sonuçlarını Excel'e kaydeder
"""

import pandas as pd
from datetime import datetime


class ArabaRaporOlusturucu:
    def __init__(self, dosya_adi="araba_firsatlari.xlsx"):
        """
        Rapor oluşturucuyu başlat
        
        Args:
            dosya_adi (str): Excel dosya adı
        """
        self.dosya_adi = dosya_adi
    
    def excel_olustur(self, ilan_listesi, analiz_sonuclari):
        """
        İlanları ve analiz sonuçlarını Excel'e kaydet
        
        Args:
            ilan_listesi (list): İlan verileri listesi
            analiz_sonuclari (list): Analiz sonuçları listesi
        """
        try:
            print(f"\n📊 Excel raporu oluşturuluyor: {self.dosya_adi}")
            
            # Verileri birleştir
            rapor_verileri = []
            
            for ilan, analiz in zip(ilan_listesi, analiz_sonuclari):
                # Yıllık ortalama km hesapla
                yil = ilan.get("yil", 2020)
                km = ilan.get("km", 0)
                yil_farki = 2026 - yil
                yillik_km = round(km / yil_farki) if yil_farki > 0 else 0
                
                satir = {
                    "Marka": ilan.get("marka", ""),
                    "Model": ilan.get("model", ""),
                    "Yıl": ilan.get("yil", 0),
                    "Kilometre": ilan.get("km", 0),
                    "Yıllık Ort. KM": yillik_km,
                    "Yakıt": ilan.get("yakit", ""),
                    "Vites": ilan.get("vites", ""),
                    "Renk": ilan.get("renk", ""),
                    "Fiyat (TL)": ilan.get("fiyat", 0),
                    "Açıklama": ilan.get("aciklama", "")[:100],
                    "Fırsat Puanı": analiz.get("puan", 0),
                    "AI Yorumu": analiz.get("yorum", ""),
                    "Karar": analiz.get("karar", "SAT"),
                    "İlan Linki": ilan.get("link", "")
                }
                rapor_verileri.append(satir)
            
            # DataFrame oluştur
            df = pd.DataFrame(rapor_verileri)
            
            # Fırsat puanına göre sırala (yüksekten düşüğe)
            df = df.sort_values("Fırsat Puanı", ascending=False)
            
            # Excel'e kaydet
            with pd.ExcelWriter(self.dosya_adi, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Araba Fırsatları', index=False)
                
                # Worksheet'i al ve formatla
                worksheet = writer.sheets['Araba Fırsatları']
                
                # Sütun genişliklerini ayarla
                worksheet.column_dimensions['A'].width = 15  # Marka
                worksheet.column_dimensions['B'].width = 15  # Model
                worksheet.column_dimensions['C'].width = 8   # Yıl
                worksheet.column_dimensions['D'].width = 12  # Kilometre
                worksheet.column_dimensions['E'].width = 15  # Yıllık Ort. KM
                worksheet.column_dimensions['F'].width = 10  # Yakıt
                worksheet.column_dimensions['G'].width = 12  # Vites
                worksheet.column_dimensions['H'].width = 10  # Renk
                worksheet.column_dimensions['I'].width = 15  # Fiyat
                worksheet.column_dimensions['J'].width = 40  # Açıklama
                worksheet.column_dimensions['K'].width = 15  # Fırsat Puanı
                worksheet.column_dimensions['L'].width = 50  # AI Yorumu
                worksheet.column_dimensions['M'].width = 10  # Karar
                worksheet.column_dimensions['N'].width = 60  # İlan Linki
            
            print(f"✅ Excel raporu oluşturuldu: {self.dosya_adi}")
            print(f"📈 Toplam {len(rapor_verileri)} ilan analiz edildi")
            
            # Özet istatistikler
            al_sayisi = sum(1 for r in rapor_verileri if r["Karar"] == "AL")
            ortalama_puan = sum(r["Fırsat Puanı"] for r in rapor_verileri) / len(rapor_verileri)
            ortalama_fiyat = sum(r["Fiyat (TL)"] for r in rapor_verileri) / len(rapor_verileri)
            
            print(f"\n📊 ÖZET:")
            print(f"   🎯 AL önerisi: {al_sayisi}/{len(rapor_verileri)}")
            print(f"   ⭐ Ortalama fırsat puanı: {ortalama_puan:.1f}/10")
            print(f"   💰 Ortalama fiyat: {ortalama_fiyat:,.0f} TL")
            
            if al_sayisi > 0:
                print(f"\n🔥 {al_sayisi} adet fırsat araç bulundu!")
            
        except Exception as e:
            print(f"❌ Excel oluşturma hatası: {e}")
            raise


if __name__ == "__main__":
    # Test
    test_ilanlar = [
        {
            "marka": "Volkswagen",
            "model": "Polo",
            "yil": 2018,
            "km": 85000,
            "yakit": "Benzin",
            "vites": "Manuel",
            "renk": "Beyaz",
            "fiyat": 450000,
            "aciklama": "Garaj arabası",
            "link": "https://www.sahibinden.com/test"
        }
    ]
    
    test_analizler = [
        {"puan": 8, "yorum": "İyi fırsat", "karar": "AL"}
    ]
    
    rapor = ArabaRaporOlusturucu("test_araba.xlsx")
    rapor.excel_olustur(test_ilanlar, test_analizler)
