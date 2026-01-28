# 📤 Otomatik Yükleme Kurulum Rehberi

VideoOtoFabrika'yı YouTube ve TikTok'a otomatik yüklemek için kurulum adımları.

---

## 🎥 YouTube Shorts Kurulumu

### Adım 1: Google Cloud Console'a Git

1. https://console.cloud.google.com/ adresine git
2. Google hesabınla giriş yap

### Adım 2: Yeni Proje Oluştur

1. Sol üstteki "Proje Seç" menüsüne tıkla
2. "Yeni Proje" butonuna tıkla
3. Proje adı: `VideoOtoFabrika`
4. "Oluştur" butonuna tıkla

### Adım 3: YouTube Data API v3'ü Etkinleştir

1. Sol menüden "API'ler ve Hizmetler" > "Kitaplık" seçeneğine git
2. Arama kutusuna "YouTube Data API v3" yaz
3. API'yi seç ve "Etkinleştir" butonuna tıkla

### Adım 4: OAuth 2.0 Kimlik Bilgileri Oluştur

1. Sol menüden "API'ler ve Hizmetler" > "Kimlik Bilgileri" seçeneğine git
2. Üstteki "+ KİMLİK BİLGİLERİ OLUŞTUR" butonuna tıkla
3. "OAuth istemci kimliği" seçeneğini seç
4. Uygulama türü: **Masaüstü uygulaması**
5. Ad: `VideoOtoFabrika Desktop`
6. "Oluştur" butonuna tıkla

### Adım 5: JSON Dosyasını İndir

1. Oluşturulan kimlik bilgisinin yanındaki "İndir" ikonuna tıkla
2. İndirilen JSON dosyasını `client_secrets.json` olarak yeniden adlandır
3. Dosyayı `VideoOtoFabrika` klasörüne kopyala

### Adım 6: İlk Kez Çalıştırma

1. `python main.py` komutunu çalıştır
2. Otomatik yükleme seçeneğini seç
3. Tarayıcıda Google hesabına giriş yap
4. İzinleri onayla
5. Artık otomatik yükleme hazır! ✅

---

## 📱 TikTok Kurulumu

### Adım 1: Kütüphaneyi Yükle

```bash
pip install tiktok-uploader
```

### Adım 2: TikTok Session Cookie'lerini Al

#### Yöntem 1: Chrome Extension (Kolay)

1. Chrome'a "Cookie Editor" extension'ını yükle
2. TikTok.com'a git ve hesabına giriş yap
3. Cookie Editor'ı aç
4. Tüm cookie'leri kopyala
5. `tiktok_session.txt` dosyası oluştur ve yapıştır

#### Yöntem 2: Manuel (Gelişmiş)

1. TikTok.com'a git ve hesabına giriş yap
2. F12 tuşuna bas (Developer Tools)
3. "Application" sekmesine git
4. Sol menüden "Cookies" > "https://www.tiktok.com" seç
5. Önemli cookie'ler:
   - `sessionid`
   - `sessionid_ss`
   - `sid_tt`
6. Bu değerleri `tiktok_session.txt` dosyasına kaydet

Format:

```
sessionid=your_session_id_here
sessionid_ss=your_session_ss_here
sid_tt=your_sid_tt_here
```

### Adım 3: Test Et

```bash
python uploader.py
```

---

## ⚠️ Önemli Notlar

### YouTube

- ✅ Resmi API, güvenli
- ✅ Günlük 10,000 quota (yaklaşık 50-100 video)
- ✅ Uzun vadeli kullanım için ideal
- ⚠️ İlk kez OAuth onayı gerekli

### TikTok

- ⚠️ Unofficial API, dikkatli kullan
- ⚠️ Çok fazla yükleme yapma (spam olarak algılanabilir)
- ⚠️ Session cookie'leri periyodik olarak yenilenmeli
- 💡 Günde 5-10 video yüklemek güvenli

---

## 🚀 Kullanım

### Otomatik Yükleme ile Video Oluştur

```bash
python main.py
```

Seçenekler:

1. **Her iki platforma yükle** (Önerilen)
2. **Sadece YouTube** (Güvenli)
3. **Sadece TikTok** (Viral potansiyel)
4. **Manuel yükleme** (Sadece video oluştur)

---

## 🔧 Sorun Giderme

### YouTube: "client_secrets.json bulunamadı"

- Dosyanın doğru klasörde olduğundan emin ol
- Dosya adının tam olarak `client_secrets.json` olduğunu kontrol et

### YouTube: "Quota exceeded"

- Günlük quota dolmuş, yarın tekrar dene
- Veya Google Cloud Console'dan quota artırımı talep et

### TikTok: "Session expired"

- Cookie'leri yeniden al
- TikTok hesabına tekrar giriş yap

### TikTok: "Upload failed"

- İnternet bağlantını kontrol et
- Video formatının doğru olduğundan emin ol (MP4, portrait)
- Çok sık yükleme yapıyor olabilirsin, biraz bekle

---

## 📊 Başarı İpuçları

1. **Düzenli Yükleme**: Günde 2-3 video ideal
2. **Farklı Saatler**: Sabah, öğle, akşam farklı kitlelere ulaşır
3. **Hashtag Stratejisi**: Sistem otomatik ekliyor ama özelleştirebilirsin
4. **İçerik Çeşitliliği**: Gemini her seferinde farklı konu seçiyor
5. **Analiz**: YouTube Analytics ve TikTok Analytics'i takip et

---

## 🎯 Sonraki Adımlar

Kurulum tamamlandıktan sonra:

1. ✅ İlk videoyu test et
2. ✅ Her iki platformda da yayınlandığını kontrol et
3. ✅ Günlük rutin oluştur (örn: her gün 3 video)
4. ✅ Büyümeyi takip et
5. ✅ Para kazanmaya başla! 💰

---

**Başarılar! 🚀**
