"""
VideoOtoFabrika - Ana Kontrol Modülü
Geliştirilmiş video üretim sistemi
"""

import asyncio
import os
import glob
from content_generator import ContentGenerator
from voice_generator import VoiceGenerator
from video_manager import VideoManager
from uploader import VideoUploader
import config


class VideoOtoFabrika:
    def __init__(self):
        """
        VideoOtoFabrika'yı başlat (config.py'den ayarları al)
        """
        # Config'den ayarları al
        self.content_gen = ContentGenerator()
        self.voice_gen = VoiceGenerator(
            voice=config.VOICE_MODEL, 
            speed_multiplier=config.VOICE_SPEED
        )
        self.video_mgr = VideoManager(template_name=config.DEFAULT_TEMPLATE)
        self.uploader = VideoUploader() if config.AUTO_UPLOAD else None
        self.auto_upload = config.AUTO_UPLOAD
        self.upload_platforms = config.DEFAULT_UPLOAD_PLATFORMS
        
        # Geçici dosya yolları
        self.temp_audio = "temp_audio.mp3"
        self.temp_video = "temp_video.mp4"
        self.output_dir = "C:/Users/aliri/Desktop"
    
    def get_next_filename(self):
        """
        Masaüstünde mevcut videoları kontrol edip sonraki numarayı bul
        
        Returns:
            str: Yeni dosya yolu (örn: C:/Users/aliri/Desktop/video_1.mp4)
        """
        # Mevcut video dosyalarını bul
        pattern = os.path.join(self.output_dir, "video_*.mp4")
        existing_files = glob.glob(pattern)
        
        if not existing_files:
            # Hiç video yoksa 1'den başla
            next_number = 1
        else:
            # En yüksek numarayı bul
            numbers = []
            for file in existing_files:
                try:
                    # video_5.mp4 -> 5
                    basename = os.path.basename(file)
                    num = int(basename.replace("video_", "").replace(".mp4", ""))
                    numbers.append(num)
                except:
                    continue
            
            next_number = max(numbers) + 1 if numbers else 1
        
        filename = f"video_{next_number}.mp4"
        return os.path.join(self.output_dir, filename)
    
    async def create_video(self):
        """
        Geliştirilmiş tam otomatik video oluşturma süreci
        """
        try:
            print("\n" + "="*60)
            print("🚀 VideoOtoFabrika Başlatılıyor...")
            print("="*60 + "\n")
            
            # Dosya adını belirle
            final_output = self.get_next_filename()
            print(f"📁 Hedef dosya: {os.path.basename(final_output)}\n")
            
            # 1. İçerik üret
            print("📝 ADIM 1: İçerik Üretimi")
            print("-" * 60)
            scenario, search_term = self.content_gen.generate_content()
            print(f"\n📄 Senaryo:\n{scenario}\n")
            print(f"🔍 Video arama terimi: '{search_term}'\n")
            
            # 2. Sesi oluştur
            print("🎤 ADIM 2: Ses Üretimi")
            print("-" * 60)
            await self.voice_gen.generate_voice(scenario, self.temp_audio)
            
            # 3. Video bul ve indir - KONUYLA ALAKALI BIRDEN FAZLA VIDEO
            print("\n🎥 ADIM 3: Konuyla Alakalı Videolar Arama")
            print("-" * 60)
            print(f"🔍 '{search_term}' ile ilgili videolar aranıyor...")
            video_urls = self.video_mgr.search_video(search_term)
            
            # Birden fazla video indir
            downloaded_videos = self.video_mgr.download_multiple_videos(video_urls, "temp_video")
            
            if not downloaded_videos:
                print("⚠️ Video indirilemedi, tek video ile devam ediliyor...")
                video_url = video_urls[0] if video_urls else None
                if video_url:
                    self.video_mgr.download_video(video_url, self.temp_video)
                    downloaded_videos = [self.temp_video]
            
            print(f"✅ Toplam {len(downloaded_videos)} video hazır")
            
            # 4. Final videoyu oluştur (geliştirilmiş alt yazı ile + birden fazla video)
            print("\n🎬 ADIM 4: Final Video Oluşturma")
            print("-" * 60)
            print("✨ Geliştirilmiş alt yazı sistemi kullanılıyor...")
            
            # Eğer birden fazla video varsa, önce birleştir
            if len(downloaded_videos) > 1:
                print(f"✨ {len(downloaded_videos)} farklı video birleştiriliyor...")
                from moviepy import VideoFileClip, concatenate_videoclips
                
                # Ses süresini al
                from moviepy import AudioFileClip
                audio_temp = AudioFileClip(self.temp_audio)
                audio_duration = audio_temp.duration
                audio_temp.close()
                
                # Her videoyu yükle ve eşit süreye böl
                clips = []
                duration_per_video = audio_duration / len(downloaded_videos)
                
                for idx, video_path in enumerate(downloaded_videos):
                    clip = VideoFileClip(video_path)
                    
                    # Videoyu hedef süreye göre ayarla
                    if clip.duration < duration_per_video:
                        # Kısaysa döngüye al
                        loops = int(duration_per_video / clip.duration) + 1
                        clip = concatenate_videoclips([clip] * loops)
                    
                    # Kes
                    clip = clip.subclipped(0, min(duration_per_video, clip.duration))
                    clips.append(clip)
                
                # Birleştir ve kaydet
                combined = concatenate_videoclips(clips, method="compose")
                combined_path = "temp_combined_video.mp4"
                combined.write_videofile(combined_path, codec='libx264', audio=False, fps=30, preset='fast', threads=4, logger=None)
                combined.close()
                
                # Clip'leri kapat
                for clip in clips:
                    clip.close()
                
                print(f"✅ Videolar birleştirildi: {combined_path}")
                final_video_path = combined_path
            else:
                final_video_path = downloaded_videos[0]
            
            # Şimdi tek video olarak işle
            self.video_mgr.create_final_video(
                final_video_path,
                self.temp_audio,
                final_output,
                subtitle_text=scenario,
                audio_speed=self.voice_gen.speed_multiplier
            )
            
            # 5. Otomatik yükleme (eğer aktifse)
            if self.auto_upload and self.uploader:
                print("\n📤 ADIM 5: Otomatik Yükleme")
                print("-" * 60)
                try:
                    self.uploader.upload_video(
                        final_output,
                        scenario,
                        platforms=self.upload_platforms
                    )
                except Exception as e:
                    print(f"⚠️ Yükleme hatası: {e}")
                    print("💾 Video yine de kaydedildi, manuel yükleyebilirsin")
            
            # 6. Geçici dosyaları temizle
            print("\n🧹 ADIM 6: Temizlik")
            print("-" * 60)
            self._cleanup()
            
            print("\n" + "="*60)
            print("✅ İŞLEM TAMAMLANDI!")
            print(f"📁 Video konumu: {final_output}")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"\n❌ HATA: {e}")
            self._cleanup()
            raise
    
    def _cleanup(self):
        """Geçici dosyaları temizle"""
        # Tek temp_video.mp4
        if os.path.exists(self.temp_video):
            try:
                os.remove(self.temp_video)
                print(f"🗑️ Silindi: {self.temp_video}")
            except Exception as e:
                print(f"⚠️ Silinemedi {self.temp_video}: {e}")
        
        # Birleştirilmiş video
        if os.path.exists("temp_combined_video.mp4"):
            try:
                os.remove("temp_combined_video.mp4")
                print(f"🗑️ Silindi: temp_combined_video.mp4")
            except Exception as e:
                print(f"⚠️ Silinemedi temp_combined_video.mp4: {e}")
        
        # Birden fazla temp_video_X.mp4
        for i in range(1, 10):
            temp_file = f"temp_video_{i}.mp4"
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    print(f"🗑️ Silindi: {temp_file}")
                except Exception as e:
                    print(f"⚠️ Silinemedi {temp_file}: {e}")
        
        # Ses dosyası
        if os.path.exists(self.temp_audio):
            try:
                os.remove(self.temp_audio)
                print(f"🗑️ Silindi: {self.temp_audio}")
            except Exception as e:
                print(f"⚠️ Silinemedi {self.temp_audio}: {e}")


async def main():
    """Ana fonksiyon"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║         🎬 VideoOtoFabrika v2.1 - Geliştirilmiş 🎬      ║
    ║                                                          ║
    ║     ✨ Daha İyi Alt Yazı + Konuyla Alakalı Video ✨     ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Config'den ayarları göster
    print("⚙️ Mevcut Ayarlar (config.py):")
    print("="*60)
    print(f"📺 Kanal: {config.CHANNEL_NAME} ({config.CHANNEL_USERNAME})")
    print(f"🎨 Şablon: {config.DEFAULT_TEMPLATE}")
    print(f"🎤 Ses: {config.VOICE_MODEL} ({config.VOICE_SPEED}x hız)")
    print(f"📤 Otomatik Yükleme: {'Aktif' if config.AUTO_UPLOAD else 'Kapalı'}")
    if config.AUTO_UPLOAD:
        platforms_str = ", ".join(config.DEFAULT_UPLOAD_PLATFORMS)
        print(f"🌐 Platformlar: {platforms_str}")
    print("="*60 + "\n")
    
    print("🎯 GELİŞTİRİLMİŞ ÖZELLİKLER:")
    print("  ✅ Alt yazılar ekranın daha geniş alanını kaplıyor")
    print("  ✅ Alt yazılar daha yukarıda (ekranın %40'ında)")
    print("  ✅ Arka plan videosu anlatılan konuyla alakalı")
    print("  ✅ Daha akıcı ve profesyonel görünüm\n")
    
    # Kullanıcıya sor: Devam edilsin mi?
    print("▶️ Video oluşturulsun mu?")
    print("1. Evet - Ayarlarla devam et")
    print("2. Hayır - Çıkış yap")
    
    choice = input("\nSeçiminiz (1-2): ").strip()
    
    if choice != '1':
        print("👋 Çıkılıyor...")
        return
    
    print("\n🚀 Video oluşturuluyor...\n")
    
    fabrika = VideoOtoFabrika()
    await fabrika.create_video()


if __name__ == "__main__":
    asyncio.run(main())
