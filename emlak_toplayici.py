"""
Emlak Fırsat Avcısı - İlan Toplayıcı Modülü
Sahibinden.com'dan gerçek ilanları çeker

NOT: Sahibinden.com bot koruması nedeniyle şu an demo modda çalışıyor.
Gerçek scraping için Selenium veya API kullanılması gerekiyor.
"""

import requests
from bs4 import BeautifulSoup
import time
import re
import random


class IlanToplayici:
    def __init__(self, demo_mode=True):
        """
        Sahibinden.com scraper'ı başlat
        
        Args:
            demo_mode (bool): Demo modda çalış (gerçek scraping yerine örnek veriler)
        """
        self.base_url = "https://www.sahibinden.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.sahibinden.com/'
        }
        self.demo_mode = demo_mode
    
    def ilan_ara(self, ilce="corlu", kategori="satilik-daire", max_ilan=5):
        """
        Sahibinden.com'dan ilan ara
        
        Args:
            ilce (str): İlçe adı (örn: corlu, cerkezkoy)
            kategori (str): Kategori (satilik-daire, kiralik-daire)
            max_ilan (int): Maksimum ilan sayısı
            
        Returns:
            list: İlan verileri listesi
        """
        if self.demo_mode:
            print("⚠️ DEMO MOD: Sahibinden.com bot koruması nedeniyle örnek veriler kullanılıyor")
            print("💡 Gerçek scraping için Selenium kurulumu gerekiyor\n")
            return self._demo_ilanlar_olustur(ilce, max_ilan)
        
        try:
            # URL oluştur (Tekirdağ için)
            search_url = f"{self.base_url}/satilik-daire/tekirdag-{ilce}"
            
            print(f"🔍 Sahibinden.com'da arama yapılıyor...")
            print(f"📍 URL: {search_url}")
            
            session = requests.Session()
            response = session.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # İlan listesini bul
            ilan_listesi = soup.find_all('tr', class_='searchResultsItem')
            
            if not ilan_listesi:
                print("⚠️ İlan bulunamadı, demo moda geçiliyor...")
                return self._demo_ilanlar_olustur(ilce, max_ilan)
            
            print(f"📊 {len(ilan_listesi)} ilan bulundu")
            
            ilanlar = []
            
            for idx, ilan_item in enumerate(ilan_listesi[:max_ilan]):
                try:
                    # İlan linkini bul
                    ilan_link_tag = ilan_item.find('a', class_='classifiedTitle')
                    
                    if not ilan_link_tag:
                        ilan_link_tag = ilan_item.find('a', href=True)
                    
                    if not ilan_link_tag:
                        continue
                    
                    ilan_href = ilan_link_tag.get('href', '')
                    
                    if not ilan_href.startswith('http'):
                        ilan_href = self.base_url + ilan_href
                    
                    ilan_baslik = ilan_link_tag.get('title', '') or ilan_link_tag.text.strip()
                    
                    print(f"\n📄 İlan {idx+1}: {ilan_baslik[:50]}...")
                    print(f"🔗 Link: {ilan_href}")
                    
                    # İlan detayını çek
                    time.sleep(2)  # Rate limiting
                    ilan_detay = self._ilan_detay_cek(ilan_href)
                    
                    if ilan_detay:
                        ilan_detay['link'] = ilan_href
                        ilan_detay['baslik'] = ilan_baslik
                        ilanlar.append(ilan_detay)
                        print(f"✅ İlan {idx+1} eklendi")
                    
                except Exception as e:
                    print(f"⚠️ İlan {idx+1} işlenemedi: {e}")
                    continue
            
            if not ilanlar:
                print("⚠️ Hiç ilan çekilemedi, demo moda geçiliyor...")
                return self._demo_ilanlar_olustur(ilce, max_ilan)
            
            print(f"\n✅ Toplam {len(ilanlar)} ilan başarıyla toplandı")
            return ilanlar
            
        except Exception as e:
            print(f"❌ İlan arama hatası: {e}")
            print("⚠️ Demo moda geçiliyor...")
            return self._demo_ilanlar_olustur(ilce, max_ilan)
    
    def _demo_ilanlar_olustur(self, ilce, max_ilan):
        """
        Demo amaçlı gerçekçi ilan verileri oluştur
        
        Args:
            ilce (str): İlçe adı
            max_ilan (int): İlan sayısı
            
        Returns:
            list: Demo ilan verileri
        """
        mahalleler = {
            "corlu": ["Önerler", "Muhittin", "Havuzlar", "Şeyh Sinan", "Esentepe"],
            "cerkezkoy": ["Fatih", "Gazi Mustafa Kemal", "Merkez", "Karaağaç", "Yeni"],
            "suleymanpasa": ["Hürriyet", "Barbaros", "Ertuğrul", "Aydoğdu", "Turgut"],
            "kapaklı": ["Merkez", "Yeni", "Cumhuriyet", "Atatürk", "İstiklal"]
        }
        
        aciklamalar = [
            "Acil satılık, krediye uygun, kelepir fırsat",
            "Sahibinden, takas olur, merkezi konumda",
            "Yeni bina, lüks daire, site içinde",
            "Yatırımlık, kiracılı, düşük aidat",
            "Deniz manzaralı, havuzlu site, otoparklı",
            "Krediye uygun, tapu masrafları alıcıya",
            "Acele satılık, pazarlık payı var",
            "Sıfır bina, asansörlü, güvenlikli site"
        ]
        
        ilanlar = []
        mahalle_listesi = mahalleler.get(ilce.lower(), ["Merkez", "Yeni", "Cumhuriyet"])
        
        for i in range(max_ilan):
            ilan_id = random.randint(1000000000, 1999999999)
            
            ilan = {
                "ilce": ilce.title(),
                "mahalle": random.choice(mahalle_listesi),
                "fiyat": random.randint(1800000, 4500000),
                "m2": random.randint(75, 150),
                "oda": random.choice(["2+1", "3+1", "4+1"]),
                "aciklama": random.choice(aciklamalar),
                "link": f"https://www.sahibinden.com/ilan/emlak-konut-satilik-{ilan_id}",
                "baslik": f"{ilce.title()} {random.choice(mahalle_listesi)} Satılık Daire"
            }
            
            ilanlar.append(ilan)
            print(f"✅ Demo İlan {i+1}: {ilan['ilce']} - {ilan['mahalle']} ({ilan['fiyat']:,} TL)")
        
        print(f"\n✅ {len(ilanlar)} demo ilan oluşturuldu")
        return ilanlar
    
    def _ilan_detay_cek(self, ilan_url):
        """
        İlan detay sayfasından bilgileri çek
        
        Args:
            ilan_url (str): İlan URL'i
            
        Returns:
            dict: İlan detayları
        """
        try:
            response = requests.get(ilan_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Fiyat
            fiyat_tag = soup.find('h3', class_='classifiedInfo')
            fiyat = 0
            if fiyat_tag:
                fiyat_text = fiyat_tag.text.strip()
                fiyat_sayilar = re.findall(r'\d+', fiyat_text.replace('.', '').replace(',', ''))
                if fiyat_sayilar:
                    fiyat = int(fiyat_sayilar[0])
            
            # Özellikler tablosu
            ozellikler = {}
            ozellik_listesi = soup.find_all('li')
            
            for li in ozellik_listesi:
                strong = li.find('strong')
                span = li.find('span')
                
                if strong and span:
                    anahtar = strong.text.strip()
                    deger = span.text.strip()
                    ozellikler[anahtar] = deger
            
            # İlçe ve Mahalle
            ilce = ozellikler.get('İlçe', 'Bilinmiyor')
            mahalle = ozellikler.get('Mahalle', 'Bilinmiyor')
            
            # Metrekare
            m2_text = ozellikler.get('Net m²', '0')
            m2 = 0
            m2_sayilar = re.findall(r'\d+', m2_text.replace('.', '').replace(',', ''))
            if m2_sayilar:
                m2 = int(m2_sayilar[0])
            
            # Oda sayısı
            oda = ozellikler.get('Oda Sayısı', 'Bilinmiyor')
            
            # Açıklama
            aciklama_tag = soup.find('div', id='classifiedDescription')
            aciklama = ""
            if aciklama_tag:
                aciklama = aciklama_tag.text.strip()[:200]
            
            ilan_verisi = {
                "ilce": ilce,
                "mahalle": mahalle,
                "fiyat": fiyat,
                "m2": m2 if m2 > 0 else 100,
                "oda": oda,
                "aciklama": aciklama if aciklama else "Açıklama yok"
            }
            
            return ilan_verisi
            
        except Exception as e:
            print(f"⚠️ Detay çekme hatası: {e}")
            return None


if __name__ == "__main__":
    # Test
    toplayici = IlanToplayici(demo_mode=True)
    ilanlar = toplayici.ilan_ara(ilce="corlu", max_ilan=3)
    
    print("\n" + "="*60)
    print("TEST SONUÇLARI:")
    for idx, ilan in enumerate(ilanlar, 1):
        print(f"\nİlan {idx}:")
        print(f"  Konum: {ilan['ilce']} - {ilan['mahalle']}")
        print(f"  Fiyat: {ilan['fiyat']:,} TL")
        print(f"  Metrekare: {ilan['m2']} m²")
        print(f"  Oda: {ilan['oda']}")
        print(f"  Link: {ilan.get('link', 'Yok')}")
