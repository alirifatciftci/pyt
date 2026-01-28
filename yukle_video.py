"""
Mevcut videoyu YouTube'a yükle
"""

from uploader import VideoUploader

# Video bilgileri
video_path = "C:/Users/aliri/Desktop/video_6.mp4"
scenario = "DUR! Elon Musk'ın gizli projesini duydun mu? Mars'ta şehir kurmaktan çok daha çılgın bir hedefi var! İnsan beynini bilgisayarlara yüklemek! Evet, yanlış duymadın! Düşüncelerini, anılarını, her şeyini dijitalleştirmek istiyor! Peki neden mi? Ölümsüzlüğü bulmak! Daha hızlı öğrenmek ve daha zeki olmak için! Bu çılgın fikir sence mümkün mü? Yorumlara yaz!"

print("🚀 Video YouTube'a yükleniyor...")
print(f"📁 Dosya: {video_path}")

uploader = VideoUploader()
results = uploader.upload_video(video_path, scenario, platforms=['youtube'])

if results['youtube']:
    print(f"\n✅ BAŞARILI! Video linki: {results['youtube']}")
else:
    print("\n❌ Yükleme başarısız!")
