"""
VideoOtoFabrika - Yapılandırma Dosyası
Kanal ayarlarını buradan yönet
"""

# ==========================================
# KANAL AYARLARI
# ==========================================

# Kanal Bilgileri
CHANNEL_NAME = "Blue Planet"  # Kanalın adı
CHANNEL_USERNAME = "@blueplanet"  # Kullanıcı adı (watermark için)

# ==========================================
# ŞABLON AYARLARI
# ==========================================

# Kullanılacak şablon (default, blue_planet, modern, minimal, energetic)
# Şablonu değiştirmek için aşağıdaki değeri değiştir ve programı yeniden çalıştır
DEFAULT_TEMPLATE = "blue_planet"

# Şablon açıklamaları:
# - default: Sarı yazılar, klasik TikTok/Shorts tarzı
# - blue_planet: Mavi tonlar, okyanus/gezegen teması (Blue Planet kanalı için)
# - modern: Cyan/Magenta, modern ve teknolojik görünüm
# - minimal: Beyaz, temiz ve minimalist tasarım
# - energetic: Turuncu/Yeşil, enerjik ve dikkat çekici

# NOT: Tüm videolarda aynı şablon kullanılır (marka tutarlılığı için)
# Farklı şablon denemek istersen DEFAULT_TEMPLATE değerini değiştir

# ==========================================
# VİDEO AYARLARI
# ==========================================

# Ses hızı (1.0 = normal, 1.5 = 1.5x hızlı)
VOICE_SPEED = 1.5

# Ses modeli (tr-TR-AhmetNeural veya tr-TR-EmelNeural)
VOICE_MODEL = "tr-TR-AhmetNeural"

# ==========================================
# YÜKLEME AYARLARI
# ==========================================

# Varsayılan yükleme platformları
# Seçenekler: ['youtube'], ['tiktok'], ['youtube', 'tiktok']
DEFAULT_UPLOAD_PLATFORMS = ['youtube']

# Otomatik yükleme aktif mi? (True/False)
AUTO_UPLOAD = True  # Otomatik YouTube yükleme aktif

# ==========================================
# GELİŞMİŞ AYARLAR
# ==========================================

# Intro süresi (saniye, 0 = intro yok)
INTRO_DURATION = 0

# Outro süresi (saniye, 0 = outro yok)
OUTRO_DURATION = 2  # Like ve Abone ol için 2 saniye

# Watermark/Logo göster (True/False)
SHOW_WATERMARK = True

# Zoom efekti aktif (True/False)
ENABLE_ZOOM_EFFECT = True

# Zoom miktarı (0.15 = %15 zoom)
ZOOM_AMOUNT = 0.15
