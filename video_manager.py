"""
VideoOtoFabrika - Video Yönetici Modülü
Pexels'ten video indirir ve MoviePy ile ses ekler.
"""

import os
import requests
import re
from dotenv import load_dotenv
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip
from template_manager import TemplateManager
import config

load_dotenv()


class VideoManager:
    def __init__(self, template_name="default"):
        """
        Pexels API'yi yapılandır
        
        Args:
            template_name: Kullanılacak şablon adı
        """
        self.api_key = os.getenv('PEXELS_API_KEY')
        if not self.api_key:
            raise ValueError("PEXELS_API_KEY bulunamadı! .env dosyasını kontrol edin.")
        
        self.headers = {
            'Authorization': self.api_key
        }
        self.base_url = 'https://api.pexels.com/videos'
        
        # Şablon yöneticisi
        self.template = TemplateManager(template_name)
        self.template_settings = self.template.get_template_settings()
    
    def search_video(self, search_term, orientation='portrait'):
        """
        Pexels'te video ara - Birden fazla video döndür
        
        Args:
            search_term: Arama terimi
            orientation: Video yönü (portrait/landscape)
            
        Returns:
            list: Video indirme URL'leri listesi (3-5 video)
        """
        try:
            print(f"🔍 Pexels'te '{search_term}' arıyor...")
            
            params = {
                'query': search_term,
                'per_page': 15  # Daha fazla seçenek
            }
            
            response = requests.get(
                f'{self.base_url}/search',
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            print(f"📊 API Yanıtı: {len(data.get('videos', []))} video bulundu")
            
            if not data.get('videos'):
                print(f"⚠️ '{search_term}' için video bulunamadı, 'nature' ile deneniyor...")
                params['query'] = 'nature'
                response = requests.get(
                    f'{self.base_url}/search',
                    headers=self.headers,
                    params=params,
                    timeout=10
                )
                data = response.json()
            
            # Birden fazla HD portrait video bul
            video_urls = []
            
            for video in data['videos']:
                if len(video_urls) >= 5:  # Maksimum 5 video
                    break
                    
                for file in video['video_files']:
                    # Portrait HD video ara
                    if file.get('quality') == 'hd' and file.get('width') and file.get('height'):
                        if orientation == 'portrait' and file['width'] < file['height'] and file['height'] >= 1080:
                            video_urls.append(file['link'])
                            print(f"✅ Video {len(video_urls)}: {file['width']}x{file['height']}")
                            break
            
            # Yeterli HD portrait bulunamazsa SD portrait ekle
            if len(video_urls) < 3:
                for video in data['videos']:
                    if len(video_urls) >= 5:
                        break
                        
                    for file in video['video_files']:
                        if file.get('width') and file.get('height'):
                            if orientation == 'portrait' and file['width'] < file['height']:
                                if file['link'] not in video_urls:
                                    video_urls.append(file['link'])
                                    print(f"✅ Video {len(video_urls)}: {file['width']}x{file['height']}")
                                    break
            
            if not video_urls:
                print("⚠️ Portrait video bulunamadı, landscape videolarla deneniyor...")
                # Landscape videoları da kabul et
                for video in data['videos']:
                    if len(video_urls) >= 5:
                        break
                    for file in video['video_files']:
                        if file.get('quality') in ['hd', 'sd']:
                            if file['link'] not in video_urls:
                                video_urls.append(file['link'])
                                print(f"✅ Video {len(video_urls)}: {file.get('width', '?')}x{file.get('height', '?')}")
                                break
            
            if not video_urls:
                raise Exception("Uygun video bulunamadı!")
            
            print(f"✅ Toplam {len(video_urls)} farklı video bulundu")
            return video_urls
            
        except Exception as e:
            print(f"❌ Video arama hatası: {e}")
            raise
    
    def download_video(self, video_url, output_path="temp_video.mp4"):
        """
        Videoyu indir
        
        Args:
            video_url: Video URL'i
            output_path: Kayıt yolu
            
        Returns:
            str: İndirilen dosya yolu
        """
        try:
            print("⬇️ Video indiriliyor...")
            
            response = requests.get(video_url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(f"✅ Video indirildi: {output_path} ({file_size:.2f} MB)")
            return output_path
            
        except Exception as e:
            print(f"❌ Video indirme hatası: {e}")
            raise
    
    def download_multiple_videos(self, video_urls, base_name="temp_video"):
        """
        Birden fazla videoyu indir
        
        Args:
            video_urls: Video URL'leri listesi
            base_name: Dosya adı tabanı
            
        Returns:
            list: İndirilen dosya yolları
        """
        downloaded_files = []
        
        for idx, url in enumerate(video_urls):
            output_path = f"{base_name}_{idx+1}.mp4"
            try:
                print(f"⬇️ Video {idx+1}/{len(video_urls)} indiriliyor...")
                
                response = requests.get(url, stream=True, timeout=30)
                response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                print(f"✅ Video {idx+1} indirildi ({file_size:.2f} MB)")
                downloaded_files.append(output_path)
                
            except Exception as e:
                print(f"⚠️ Video {idx+1} indirilemedi: {e}")
                continue
        
        return downloaded_files
    
    def create_word_by_word_subtitle(self, text, video_width, video_height, duration):
        """
        2 satırlık kelime kelime vurgulu alt yazı oluştur - Ekranın daha geniş alanını kullan
        
        Args:
            text: Alt yazı metni
            video_width: Video genişliği
            video_height: Video yüksekliği
            duration: Video süresi
            
        Returns:
            list: Alt yazı clip'leri listesi
        """
        # Şablon ayarlarından font al
        selected_font = self.template_settings["fonts"]["main"]
        
        if not os.path.exists(selected_font):
            selected_font = "Arial"
        
        # Metni kelimelere böl
        words = text.split()
        
        # Her kelime için süre hesapla
        time_per_word = duration / len(words)
        
        subtitle_clips = []
        
        # Her 4-6 kelimeyi 2 satırda göster
        words_per_group = 6
        
        for i in range(0, len(words), words_per_group):
            group = words[i:i+words_per_group]
            
            # 2 satıra böl
            mid = len(group) // 2
            line1 = " ".join(group[:mid])
            line2 = " ".join(group[mid:])
            
            # İki satırlı metin
            group_text = f"{line1}\n{line2}"
            
            start_time = i * time_per_word
            group_duration = len(group) * time_per_word
            
            try:
                # Şablon ayarlarıyla metin oluştur - DAHA BÜYÜK ALAN
                main_text = TextClip(
                    text=group_text.upper(),
                    font=selected_font,
                    font_size=self.template_settings["text_size"],
                    color=self.template_settings["colors"]["primary"],
                    stroke_color=self.template_settings["colors"]["background"],
                    stroke_width=self.template_settings["stroke_width"],
                    method="caption",
                    size=(video_width - 100, None),  # Daha geniş alan (60'tan 100'e)
                    text_align="center",
                    interline=-5  # Satır arası boşluk daha az
                )
                
                # Pozisyon: Ekranın ortasında ama biraz daha yukarıda
                y_position = int(video_height * 0.40)  # Ekranın %40'ında (daha yukarı)
                
                main_text = main_text.with_start(start_time).with_duration(group_duration)
                main_text = main_text.with_position(("center", y_position))
                
                subtitle_clips.append(main_text)
                
            except Exception as e:
                print(f"⚠️ Kelime grubu {i} için alt yazı oluşturulamadı: {e}")
                continue
        
        return subtitle_clips
    
    def create_background_overlay(self, video_width, video_height, duration):
        """
        Alt ve üst kısımda koyu arka plan oluştur (yazılar daha okunabilir olsun)
        
        Args:
            video_width: Video genişliği
            video_height: Video yüksekliği
            duration: Video süresi
            
        Returns:
            list: Arka plan clip'leri
        """
        try:
            from moviepy import ColorClip
            
            overlays = []
            
            # Üst kısım (koyu, yarı saydam)
            top_overlay = ColorClip(
                size=(video_width, video_height // 4),
                color=(0, 0, 0),  # Siyah
                duration=duration
            ).with_opacity(0.3)  # %30 saydam
            
            top_overlay = top_overlay.with_position(("center", 0))
            overlays.append(top_overlay)
            
            # Alt kısım (koyu, yarı saydam)
            bottom_overlay = ColorClip(
                size=(video_width, video_height // 4),
                color=(0, 0, 0),
                duration=duration
            ).with_opacity(0.3)
            
            bottom_overlay = bottom_overlay.with_position(("center", video_height - video_height // 4))
            overlays.append(bottom_overlay)
            
            return overlays
            
        except Exception as e:
            print(f"⚠️ Arka plan overlay oluşturulamadı: {e}")
            return []
    
    def create_scrolling_subtitle(self, text, video_width, video_height, duration):
        """
        Aşağıdan yukarıya kayan alt yazı oluştur (daha ilgi çekici)
        
        Args:
            text: Alt yazı metni
            video_width: Video genişliği
            video_height: Video yüksekliği
            duration: Video süresi
            
        Returns:
            TextClip: Kayan alt yazı clip'i
        """
        # Font seçenekleri
        font_options = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/impact.ttf",  # Daha bold
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
        ]
        
        selected_font = None
        for font in font_options:
            if os.path.exists(font):
                selected_font = font
                break
        
        if not selected_font:
            selected_font = "Arial"
        
        # Metni satırlara böl (her satır max 25 karakter - daha okunaklı)
        words = text.split()
        lines = []
        current_line = ""
        max_chars_per_line = 25  # Daha kısa satırlar
        
        for word in words:
            test_line = current_line + (" " + word if current_line else word)
            if len(test_line) <= max_chars_per_line:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        subtitle_text = "\n".join(lines)
        
        try:
            # Alt yazı oluştur - DAHA BÜYÜK VE RENKLI
            subtitle = TextClip(
                text=subtitle_text,
                font=selected_font,
                font_size=56,  # Daha büyük (48'den 56'ya)
                color="yellow",  # Sarı - daha dikkat çekici
                stroke_color="black",
                stroke_width=4,  # Daha kalın kontur
                method="caption",
                size=(video_width - 60, None),
                text_align="center"
            )
            
            # Başlangıç ve bitiş pozisyonları (AŞAĞIDAN YUKARIYA)
            start_y = video_height  # Ekranın altından başla
            end_y = -subtitle.h     # Ekranın üstünden çık
            
            # Hareket süresini uzat (daha yavaş kaydırma için)
            scroll_duration = duration * 1.8
            
            # Hareket fonksiyonu
            def scroll_position(t):
                progress = t / scroll_duration
                
                if progress > 1:
                    progress = 1
                
                current_y = start_y + (end_y - start_y) * progress
                return ("center", current_y)
            
            # Pozisyonu zamanla değiştir
            subtitle = subtitle.with_position(scroll_position)
            subtitle = subtitle.with_duration(duration)
            
            return subtitle
            
        except Exception as e:
            print(f"⚠️ Kayan alt yazı oluşturulamadı: {e}")
            return None
    
    def create_final_video(self, video_path, audio_path, output_path, subtitle_text=None, audio_speed=1.0):
        """
        Video ve sesi birleştir, alt yazı ekle (YouTube Shorts formatında)
        
        Args:
            video_path: Video dosyası yolu
            audio_path: Ses dosyası yolu
            output_path: Çıktı dosyası yolu
            subtitle_text: Alt yazı metni (opsiyonel)
            audio_speed: Ses hızı çarpanı (Edge-TTS'de zaten uygulandı)
        """
        try:
            print("🎬 Video ve ses birleştiriliyor...")
            
            # Video ve sesi yükle
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)
            
            audio_duration = audio.duration
            video_duration = video.duration
            
            print(f"📊 Ses süresi: {audio_duration:.2f}s, Video süresi: {video_duration:.2f}s")
            
            # YouTube Shorts için süre kontrolü (max 60 saniye)
            if audio_duration > 60:
                print("⚠️ Video 60 saniyeden uzun, YouTube Shorts için kısaltılıyor...")
                audio = audio.subclipped(0, 60)
                audio_duration = 60
            
            # Video süresini ses süresine göre ayarla
            if video_duration < audio_duration:
                # Video kısaysa döngüye al
                print("🔄 Video döngüye alınıyor...")
                loops_needed = int(audio_duration / video_duration) + 1
                # Manuel olarak videoyu döngüye al
                clips = [video] * loops_needed
                from moviepy import concatenate_videoclips
                video = concatenate_videoclips(clips)
            
            # Videoyu ses süresine göre kes
            video = video.subclipped(0, audio_duration)
            
            # YouTube Shorts için boyut kontrolü ve düzenleme (9:16 - Portrait)
            target_width = 1080
            target_height = 1920
            
            current_width = video.w
            current_height = video.h
            
            print(f"📐 Mevcut boyut: {current_width}x{current_height}")
            
            # Eğer video zaten portrait değilse veya boyut uygun değilse düzenle
            if current_width != target_width or current_height != target_height:
                print(f"📐 YouTube Shorts formatına dönüştürülüyor: {target_width}x{target_height}")
                
                # Video aspect ratio'sunu hesapla
                video_aspect = current_width / current_height
                target_aspect = target_width / target_height  # 9:16 = 0.5625
                
                if video_aspect > target_aspect:
                    # Video çok geniş, yüksekliği hedef yap ve genişliği kırp
                    new_height = target_height
                    new_width = int(current_width * (target_height / current_height))
                else:
                    # Video çok dar veya uygun, genişliği hedef yap ve yüksekliği kırp
                    new_width = target_width
                    new_height = int(current_height * (target_width / current_width))
                
                # Resize
                video = video.resized(width=new_width, height=new_height)
                
                # Merkezi kırp
                x_center = new_width / 2
                y_center = new_height / 2
                
                video = video.cropped(
                    x_center=x_center,
                    y_center=y_center,
                    width=target_width,
                    height=target_height
                )
                
                print(f"✅ Video boyutu ayarlandı: {target_width}x{target_height} (YouTube Shorts)")

            
            # Zoom efekti ekle (config'den kontrol et)
            if config.ENABLE_ZOOM_EFFECT:
                print("🎬 Zoom efekti ekleniyor...")
                def zoom_effect(get_frame, t):
                    """Yavaş zoom-in efekti"""
                    frame = get_frame(t)
                    # Zoom faktörü: config'den al
                    zoom_factor = 1.0 + (t / audio_duration) * config.ZOOM_AMOUNT
                    
                    h, w = frame.shape[:2]
                    new_h, new_w = int(h * zoom_factor), int(w * zoom_factor)
                    
                    # Merkezi kırp
                    y1 = (new_h - h) // 2
                    x1 = (new_w - w) // 2
                    
                    # Resize ve crop
                    import cv2
                    resized = cv2.resize(frame, (new_w, new_h))
                    cropped = resized[y1:y1+h, x1:x1+w]
                    
                    return cropped
                
                try:
                    video = video.transform(zoom_effect)
                    print("✅ Zoom efekti eklendi")
                except Exception as e:
                    print(f"⚠️ Zoom efekti eklenemedi: {e}, normal video kullanılıyor")
            else:
                print("ℹ️ Zoom efekti kapalı (config.py)")
            
            # Sesi videoya ekle
            video_with_audio = video.with_audio(audio)
            
            # Alt yazı ekle (kelime kelime vurgulu - Şablon tarzı)
            if subtitle_text:
                print(f"📝 Alt yazı ekleniyor (Şablon: {self.template_settings['name']})...")
                
                # Arka plan overlay'leri oluştur
                overlays = self.create_background_overlay(video.w, video.h, audio_duration)
                
                # Kelime kelime alt yazılar oluştur
                subtitle_clips = self.create_word_by_word_subtitle(
                    subtitle_text,
                    video.w,
                    video.h,
                    audio_duration
                )
                
                # Watermark ekle (config'den kontrol et)
                watermark = None
                if config.SHOW_WATERMARK:
                    watermark = self.template.add_watermark(video.w, video.h, audio_duration)
                
                if subtitle_clips:
                    # Video + overlay'ler + alt yazılar + watermark
                    all_clips = [video_with_audio] + overlays + subtitle_clips
                    if watermark:
                        all_clips.append(watermark)
                    
                    main_video = CompositeVideoClip(all_clips)
                    print(f"✅ {len(subtitle_clips)} kelime grubu alt yazı eklendi")
                else:
                    print("⚠️ Alt yazı oluşturulamadı, alt yazısız devam ediliyor...")
                    main_video = video_with_audio
            else:
                main_video = video_with_audio
            
            # Intro ve Outro ekle
            intro = self.template.create_intro(video.w, video.h)
            outro = self.template.create_outro(video.w, video.h)
            
            clips_to_concat = []
            
            if intro:
                clips_to_concat.append(intro)
                print("✅ Intro eklendi")
            
            clips_to_concat.append(main_video)
            
            if outro:
                clips_to_concat.append(outro)
                print("✅ Outro eklendi")
            
            # Tüm parçaları birleştir
            if len(clips_to_concat) > 1:
                from moviepy import concatenate_videoclips
                final_video = concatenate_videoclips(clips_to_concat)
            else:
                final_video = main_video
            
            # Çıktıyı kaydet
            print(f"💾 Final video kaydediliyor: {output_path}")
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                fps=30,
                preset='medium',
                threads=4
            )
            
            # Kaynakları temizle
            video.close()
            audio.close()
            final_video.close()
            
            print(f"✅ Video başarıyla oluşturuldu: {output_path}")
            
        except Exception as e:
            print(f"❌ Video oluşturma hatası: {e}")
            raise


if __name__ == "__main__":
    # Test
    manager = VideoManager()
    video_url = manager.search_video("ocean")
    print(f"Test video URL: {video_url}")
