"""
Emlak Fırsat Avcısı - Ana Modül
Sahibinden.com'dan gerçek ilanları çekip Gemini AI ile analiz eder
"""

from emlak_beyni import GeminiAnaliz
from emlak_rapor import RaporOlusturucu
from emlak_toplayici import IlanToplayici


def main():
    """Ana fonksiyon"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║            🏠 EMLAK FIRSAT AVCISI 🏠                     ║
    ║                                                          ║
    ║      Sahibinden.com + Gemini AI ile Akıllı Analiz       ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Kullanıcıdan arama parametrelerini al
    print("🔍 ARAMA PARAMETRELERİ")
    print("="*60)
    
    try:
        ilce = input("İlçe adı (örn: corlu, cerkezkoy, suleymanpasa) [corlu]: ").strip().lower() or "corlu"
    except:
        ilce = "corlu"
    
    try:
        max_ilan = int(input("Kaç ilan analiz edilsin? [5]: ").strip() or "5")
    except:
        max_ilan = 5
    
    print("\n" + "="*60)
    print(f"📍 Arama: Tekirdağ/{ilce.title()}")
    print(f"📊 Hedef: {max_ilan} ilan")
    print("="*60 + "\n")
    
    # Sahibinden.com'dan ilanları topla
    print("🌐 ADIM 1: Sahibinden.com'dan İlanlar Toplanıyor")
    print("-"*60)
    
    toplayici = IlanToplayici()
    ilan_listesi = toplayici.ilan_ara(ilce=ilce, max_ilan=max_ilan)
    
    if not ilan_listesi:
        print("\n❌ İlan bulunamadı! Lütfen farklı bir ilçe deneyin.")
        return
    
    print(f"\n✅ {len(ilan_listesi)} gerçek ilan toplandı!")
    print("="*60)
    
    try:
        # Gemini analiz modülünü başlat
        print("\n🤖 ADIM 2: Gemini AI ile İlanlar Analiz Ediliyor")
        print("-"*60)
        analiz_motoru = GeminiAnaliz()
        print("✅ Gemini AI hazır\n")
        
        # Her ilanı analiz et
        analiz_sonuclari = []
        
        for idx, ilan in enumerate(ilan_listesi, 1):
            print(f"\n📍 İlan {idx}/{len(ilan_listesi)}")
            print("-" * 60)
            print(f"   Konum: {ilan['ilce']} - {ilan['mahalle']}")
            print(f"   Fiyat: {ilan['fiyat']:,} TL")
            print(f"   Metrekare: {ilan['m2']} m²")
            print(f"   Fiyat/m²: {ilan['fiyat']/ilan['m2']:,.0f} TL")
            print(f"   Oda: {ilan['oda']}")
            print(f"   🔗 Link: {ilan.get('link', 'Yok')}")
            
            # Gemini'ye analiz ettir
            sonuc = analiz_motoru.analiz_et(ilan)
            analiz_sonuclari.append(sonuc)
            
            print(f"   ⭐ Fırsat Puanı: {sonuc['puan']}/10")
            print(f"   💬 Yorum: {sonuc['yorum']}")
            print(f"   🎯 Karar: {sonuc['karar']}")
        
        print("\n" + "="*60)
        print("✅ Tüm ilanlar analiz edildi!")
        
        # Excel raporu oluştur
        print("\n🤖 ADIM 3: Excel Raporu Oluşturuluyor")
        print("-"*60)
        
        # Zaman damgalı dosya adı
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dosya_adi = f"firsatlar_{timestamp}.xlsx"
        
        rapor = RaporOlusturucu(dosya_adi)
        rapor.excel_olustur(ilan_listesi, analiz_sonuclari)
        
        print("\n" + "="*60)
        print("🎉 İŞLEM TAMAMLANDI!")
        print(f"📁 Rapor dosyası: {dosya_adi}")
        print("💡 Excel'de ilanların linklerini görebilirsiniz!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ HATA: {e}")
        raise


if __name__ == "__main__":
    main()
