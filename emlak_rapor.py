"""
Emlak Fırsat Avcısı - Rapor Modülü
Analiz sonuçlarını Excel'e kaydeder
"""

import pandas as pd
from datetime import datetime


class RaporOlusturucu:
    def __init__(self, dosya_adi="firsatlar.xlsx"):
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
                satir = {
                    "İlçe": ilan.get("ilce", ""),
                    "Mahalle": ilan.get("mahalle", ""),
                    "Fiyat (TL)": ilan.get("fiyat", 0),
                    "Metrekare": ilan.get("m2", 0),
                    "Fiyat/m²": round(ilan.get("fiyat", 0) / ilan.get("m2", 1), 2),
                    "Oda": ilan.get("oda", ""),
                    "Açıklama": ilan.get("aciklama", "")[:100],  # İlk 100 karakter
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
                df.to_excel(writer, sheet_name='Fırsatlar', index=False)
                
                # Worksheet'i al ve formatla
                worksheet = writer.sheets['Fırsatlar']
                
                # Sütun genişliklerini ayarla
                worksheet.column_dimensions['A'].width = 15  # İlçe
                worksheet.column_dimensions['B'].width = 20  # Mahalle
                worksheet.column_dimensions['C'].width = 15  # Fiyat
                worksheet.column_dimensions['D'].width = 12  # Metrekare
                worksheet.column_dimensions['E'].width = 12  # Fiyat/m²
                worksheet.column_dimensions['F'].width = 10  # Oda
                worksheet.column_dimensions['G'].width = 40  # Açıklama
                worksheet.column_dimensions['H'].width = 15  # Fırsat Puanı
                worksheet.column_dimensions['I'].width = 50  # AI Yorumu
                worksheet.column_dimensions['J'].width = 10  # Karar
                worksheet.column_dimensions['K'].width = 60  # İlan Linki
            
            print(f"✅ Excel raporu oluşturuldu: {self.dosya_adi}")
            print(f"📈 Toplam {len(rapor_verileri)} ilan analiz edildi")
            
            # Özet istatistikler
            al_sayisi = sum(1 for r in rapor_verileri if r["Karar"] == "AL")
            ortalama_puan = sum(r["Fırsat Puanı"] for r in rapor_verileri) / len(rapor_verileri)
            
            print(f"\n📊 ÖZET:")
            print(f"   🎯 AL önerisi: {al_sayisi}/{len(rapor_verileri)}")
            print(f"   ⭐ Ortalama fırsat puanı: {ortalama_puan:.1f}/10")
            
            if al_sayisi > 0:
                print(f"\n🔥 {al_sayisi} adet fırsat ilan bulundu!")
            
        except Exception as e:
            print(f"❌ Excel oluşturma hatası: {e}")
            raise


if __name__ == "__main__":
    # Test
    test_ilanlar = [
        {"ilce": "Çorlu", "mahalle": "Önerler", "fiyat": 3500000, "m2": 110, "oda": "3+1", "aciklama": "Acil satılık"}
    ]
    
    test_analizler = [
        {"puan": 8, "yorum": "İyi fırsat", "karar": "AL"}
    ]
    
    rapor = RaporOlusturucu("test_firsatlar.xlsx")
    rapor.excel_olustur(test_ilanlar, test_analizler)
