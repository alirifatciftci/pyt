"""
Araba Fırsat Avcısı - Basit Mod
Kullanıcı ilan bilgilerini girer, AI en iyi 5'i seçer
"""

from araba_beyni import GeminiArabaAnaliz
from araba_rapor import ArabaRaporOlusturucu


def ilan_gir():
    """Kullanıcıdan ilan bilgilerini al"""
    print("\n" + "="*60)
    print("📝 İLAN BİLGİLERİNİ GİR")
    print("="*60)
    
    try:
        marka = input("Marka (örn: Volkswagen): ").strip() or "Bilinmiyor"
        model = input("Model (örn: Polo): ").strip() or "Bilinmiyor"
        yil = int(input("Yıl (örn: 2018): ").strip() or "2020")
        km = int(input("Kilometre (örn: 85000): ").strip() or "0")
        fiyat = int(input("Fiyat TL (örn: 450000): ").strip() or "0")
        yakit = input("Yakıt (Benzin/Dizel/LPG) [Benzin]: ").strip() or "Benzin"
        vites = input("Vites (Manuel/Otomatik) [Manuel]: ").strip() or "Manuel"
        renk = input("Renk [Beyaz]: ").strip() or "Beyaz"
        aciklama = input("Açıklama (hasarsız, bakımlı vb.) [Yok]: ").strip() or "Açıklama yok"
        link = input("Sahibinden.com linki (opsiyonel): ").strip() or f"https://www.sahibinden.com/ilan/{marka.lower()}-{model.lower()}"
        
        return {
            "marka": marka,
            "model": model,
            "yil": yil,
            "km": km,
            "fiyat": fiyat,
            "yakit": yakit,
            "vites": vites,
            "renk": renk,
            "aciklama": aciklama,
            "link": link,
            "baslik": f"{marka} {model} {yil}"
        }
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None


def main():
    """Ana fonksiyon"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║         🚗 ARABA FIRSAT AVCISI - BASİT MOD 🚗           ║
    ║                                                          ║
    ║      Manuel Giriş + AI Analizi = En İyi 5 İlan         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    print("📋 NASIL KULLANILIR:")
    print("="*60)
    print("1. Sahibinden.com'da ilanları gez")
    print("2. Her ilan için bilgileri buraya gir")
    print("3. 10-15 ilan gir (daha fazla = daha iyi analiz)")
    print("4. AI en iyi 5'i seçecek!")
    print("="*60)
    
    ilan_listesi = []
    
    while True:
        print(f"\n🚗 İLAN {len(ilan_listesi) + 1}")
        print("-"*60)
        
        devam = input("\nYeni ilan ekle? (E/H) [E]: ").strip().upper()
        
        if devam == 'H':
            break
        
        ilan = ilan_gir()
        
        if ilan:
            ilan_listesi.append(ilan)
            print(f"\n✅ İlan {len(ilan_listesi)} eklendi: {ilan['marka']} {ilan['model']} {ilan['yil']} - {ilan['fiyat']:,} TL")
        else:
            print("⚠️ İlan eklenemedi!")
    
    if not ilan_listesi:
        print("\n❌ Hiç ilan girilmedi!")
        return
    
    print(f"\n{'='*60}")
    print(f"📊 Toplam {len(ilan_listesi)} ilan girildi")
    print("="*60)
    
    # Gemini ile analiz et
    print("\n🤖 ADIM 1: Gemini AI ile İlanlar Analiz Ediliyor")
    print("-"*60)
    
    analiz_motoru = GeminiArabaAnaliz()
    print("✅ Gemini AI hazır\n")
    
    analiz_sonuclari = []
    
    for idx, ilan in enumerate(ilan_listesi, 1):
        print(f"\n📍 İlan {idx}/{len(ilan_listesi)}")
        print("-" * 60)
        print(f"   Araç: {ilan['marka']} {ilan['model']} {ilan['yil']}")
        print(f"   Fiyat: {ilan['fiyat']:,} TL")
        print(f"   Kilometre: {ilan['km']:,} km")
        
        # Yıllık ortalama km
        yil_farki = 2026 - ilan['yil']
        yillik_km = round(ilan['km'] / yil_farki) if yil_farki > 0 else 0
        print(f"   Yıllık Ort. KM: {yillik_km:,} km")
        
        # Gemini'ye analiz ettir
        sonuc = analiz_motoru.analiz_et(ilan)
        analiz_sonuclari.append(sonuc)
        
        print(f"   ⭐ Fırsat Puanı: {sonuc['puan']}/10")
        print(f"   🎯 Karar: {sonuc['karar']}")
    
    # En iyi 5'i seç
    print("\n" + "="*60)
    print("🔥 EN İYİ 5 İLAN SEÇİLİYOR...")
    print("="*60)
    
    # Puanlara göre sırala
    ilan_puan_listesi = list(zip(ilan_listesi, analiz_sonuclari))
    ilan_puan_listesi.sort(key=lambda x: x[1]['puan'], reverse=True)
    
    # En iyi 5'i al (veya daha azsa hepsini)
    en_iyi_5 = ilan_puan_listesi[:min(5, len(ilan_puan_listesi))]
    en_iyi_ilanlar = [x[0] for x in en_iyi_5]
    en_iyi_analizler = [x[1] for x in en_iyi_5]
    
    print(f"\n✅ En iyi {len(en_iyi_5)} ilan seçildi!")
    
    for idx, (ilan, analiz) in enumerate(en_iyi_5, 1):
        print(f"\n🏆 #{idx} - Puan: {analiz['puan']}/10 - Karar: {analiz['karar']}")
        print(f"   {ilan['marka']} {ilan['model']} {ilan['yil']}")
        print(f"   {ilan['fiyat']:,} TL - {ilan['km']:,} km")
        print(f"   💬 {analiz['yorum']}")
    
    # Excel raporu oluştur
    print("\n🤖 ADIM 2: Excel Raporu Oluşturuluyor")
    print("-"*60)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dosya_adi = f"araba_en_iyi_{len(en_iyi_5)}_{timestamp}.xlsx"
    
    rapor = ArabaRaporOlusturucu(dosya_adi)
    rapor.excel_olustur(en_iyi_ilanlar, en_iyi_analizler)
    
    print("\n" + "="*60)
    print("🎉 İŞLEM TAMAMLANDI!")
    print(f"📁 Rapor dosyası: {dosya_adi}")
    print(f"🏆 EN İYİ {len(en_iyi_5)} İLAN Excel'de!")
    print("💡 Fırsat puanına göre sıralanmış!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
