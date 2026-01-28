"""
VideoOtoFabrika - Şablon Yöneticisi
Kanalına özel video şablonları
"""

import os
from moviepy import VideoFileClip, ImageClip, TextClip, CompositeVideoClip, ColorClip
from moviepy import concatenate_videoclips
import config


class TemplateManager:
    def __init__(self, template_name="default"):
        """
        Şablon yöneticisini başlat
        
        Args:
            template_name: Kullanılacak şablon adı
        """
        self.template_name = template_name
        self.templates_dir = "templates"
        
        # Şablon ayarları
        self.templates = {
            "default": {
                "name": "Varsayılan",
                "colors": {
                    "primary": "yellow",
                    "secondary": "white",
                    "background": "black",
                    "accent": "#FF6B6B"
                },
                "fonts": {
                    "main": "C:/Windows/Fonts/impact.ttf",
                    "secondary": "C:/Windows/Fonts/arialbd.ttf"
                },
                "text_size": 65,
                "stroke_width": 5,
                "logo_position": "top-right",
                "watermark_opacity": 0.7,
                "intro_duration": 0,  # Intro süresi (saniye)
                "outro_duration": 0   # Outro süresi (saniye)
            },
            "blue_planet": {
                "name": "Blue Planet",
                "colors": {
                    "primary": "#00D4FF",  # Parlak mavi
                    "secondary": "#FFFFFF",  # Beyaz
                    "background": "#001F3F",  # Koyu lacivert
                    "accent": "#00FFFF"  # Cyan
                },
                "fonts": {
                    "main": "C:/Windows/Fonts/impact.ttf",
                    "secondary": "C:/Windows/Fonts/arialbd.ttf"
                },
                "text_size": 68,
                "stroke_width": 6,
                "logo_position": "top-center",
                "watermark_opacity": 0.8,
                "intro_duration": 0,
                "outro_duration": 0
            },
            "modern": {
                "name": "Modern",
                "colors": {
                    "primary": "#00D9FF",  # Cyan
                    "secondary": "white",
                    "background": "black",
                    "accent": "#FF00FF"  # Magenta
                },
                "fonts": {
                    "main": "C:/Windows/Fonts/impact.ttf",
                    "secondary": "C:/Windows/Fonts/arialbd.ttf"
                },
                "text_size": 70,
                "stroke_width": 6,
                "logo_position": "top-left",
                "watermark_opacity": 0.8,
                "intro_duration": 0,
                "outro_duration": 0
            },
            "minimal": {
                "name": "Minimal",
                "colors": {
                    "primary": "white",
                    "secondary": "#CCCCCC",
                    "background": "black",
                    "accent": "#FFD700"  # Gold
                },
                "fonts": {
                    "main": "C:/Windows/Fonts/arial.ttf",
                    "secondary": "C:/Windows/Fonts/arial.ttf"
                },
                "text_size": 60,
                "stroke_width": 3,
                "logo_position": "bottom-right",
                "watermark_opacity": 0.5,
                "intro_duration": 0,
                "outro_duration": 0
            },
            "energetic": {
                "name": "Enerjik",
                "colors": {
                    "primary": "#FF4500",  # Orange Red
                    "secondary": "yellow",
                    "background": "black",
                    "accent": "#00FF00"  # Lime
                },
                "fonts": {
                    "main": "C:/Windows/Fonts/impact.ttf",
                    "secondary": "C:/Windows/Fonts/impact.ttf"
                },
                "text_size": 75,
                "stroke_width": 7,
                "logo_position": "top-center",
                "watermark_opacity": 0.9,
                "intro_duration": 0,
                "outro_duration": 0
            }
        }
        
        self.current_template = self.templates.get(template_name, self.templates["default"])
    
    def get_template_settings(self):
        """Mevcut şablon ayarlarını döndür"""
        return self.current_template
    
    def create_intro(self, video_width, video_height):
        """
        Intro animasyonu oluştur
        
        Args:
            video_width: Video genişliği
            video_height: Video yüksekliği
            
        Returns:
            VideoClip: Intro clip'i veya None
        """
        intro_duration = self.current_template["intro_duration"]
        
        if intro_duration <= 0:
            return None
        
        try:
            # Siyah arka plan
            background = ColorClip(
                size=(video_width, video_height),
                color=(0, 0, 0),
                duration=intro_duration
            )
            
            # Kanal adı (config'den al)
            channel_name = config.CHANNEL_NAME.upper()
            
            title = TextClip(
                text=channel_name,
                font=self.current_template["fonts"]["main"],
                font_size=80,
                color=self.current_template["colors"]["primary"],
                stroke_color=self.current_template["colors"]["background"],
                stroke_width=5
            )
            
            # Animasyon: Fade in
            title = title.with_duration(intro_duration)
            title = title.with_position("center")
            title = title.crossfadein(0.5)
            
            intro = CompositeVideoClip([background, title])
            
            return intro
            
        except Exception as e:
            print(f"⚠️ Intro oluşturulamadı: {e}")
            return None
    
    def create_outro(self, video_width, video_height):
        """
        Outro animasyonu oluştur - Like ve Abone Ol butonları
        
        Args:
            video_width: Video genişliği
            video_height: Video yüksekliği
            
        Returns:
            VideoClip: Outro clip'i veya None
        """
        outro_duration = self.current_template["outro_duration"]
        
        if outro_duration <= 0:
            return None
        
        try:
            # Siyah arka plan
            background = ColorClip(
                size=(video_width, video_height),
                color=(0, 0, 0),
                duration=outro_duration
            )
            
            # "BEĞEN" butonu (sol taraf)
            like_text = TextClip(
                text="👍\nBEĞEN",
                font=self.current_template["fonts"]["main"],
                font_size=50,
                color=self.current_template["colors"]["primary"],
                stroke_color=self.current_template["colors"]["background"],
                stroke_width=3,
                text_align="center"
            )
            
            like_text = like_text.with_duration(outro_duration)
            like_x = video_width // 4  # Sol çeyrek
            like_y = video_height // 2 - 50
            like_text = like_text.with_position((like_x - like_text.w // 2, like_y))
            
            # "ABONE OL" butonu (sağ taraf)
            subscribe_text = TextClip(
                text="🔔\nABONE OL",
                font=self.current_template["fonts"]["main"],
                font_size=50,
                color=self.current_template["colors"]["accent"],
                stroke_color=self.current_template["colors"]["background"],
                stroke_width=3,
                text_align="center"
            )
            
            subscribe_text = subscribe_text.with_duration(outro_duration)
            subscribe_x = (video_width * 3) // 4  # Sağ çeyrek
            subscribe_y = video_height // 2 - 50
            subscribe_text = subscribe_text.with_position((subscribe_x - subscribe_text.w // 2, subscribe_y))
            
            # Fade in animasyonu
            like_text = like_text.crossfadein(0.3)
            subscribe_text = subscribe_text.crossfadein(0.3)
            
            # Tüm elementleri birleştir
            outro = CompositeVideoClip([background, like_text, subscribe_text])
            
            return outro
            
        except Exception as e:
            print(f"⚠️ Outro oluşturulamadı: {e}")
            return None
    
    def add_watermark(self, video_width, video_height, duration):
        """
        Watermark/Logo ekle
        
        Args:
            video_width: Video genişliği
            video_height: Video yüksekliği
            duration: Video süresi
            
        Returns:
            TextClip: Watermark clip'i veya None
        """
        try:
            # Logo dosyası varsa kullan, yoksa metin logo
            logo_path = os.path.join(self.templates_dir, "logo.png")
            
            if os.path.exists(logo_path):
                # Resim logo
                logo = ImageClip(logo_path)
                logo = logo.resized(height=60)  # Yükseklik 60px
                logo = logo.with_duration(duration)
                logo = logo.with_opacity(self.current_template["watermark_opacity"])
            else:
                # Metin logo (config'den al)
                logo_text = config.CHANNEL_USERNAME
                
                logo = TextClip(
                    text=logo_text,
                    font=self.current_template["fonts"]["secondary"],
                    font_size=30,
                    color=self.current_template["colors"]["secondary"],
                    stroke_color=self.current_template["colors"]["background"],
                    stroke_width=2
                )
                
                logo = logo.with_duration(duration)
                logo = logo.with_opacity(self.current_template["watermark_opacity"])
            
            # Pozisyon
            position = self.current_template["logo_position"]
            
            if position == "top-right":
                logo = logo.with_position((video_width - logo.w - 20, 20))
            elif position == "top-left":
                logo = logo.with_position((20, 20))
            elif position == "top-center":
                logo = logo.with_position(("center", 20))
            elif position == "bottom-right":
                logo = logo.with_position((video_width - logo.w - 20, video_height - logo.h - 20))
            elif position == "bottom-left":
                logo = logo.with_position((20, video_height - logo.h - 20))
            else:
                logo = logo.with_position((video_width - logo.w - 20, 20))
            
            return logo
            
        except Exception as e:
            print(f"⚠️ Watermark oluşturulamadı: {e}")
            return None
    
    def list_templates(self):
        """Mevcut şablonları listele"""
        print("\n📋 Mevcut Şablonlar:")
        print("="*60)
        for key, template in self.templates.items():
            print(f"\n🎨 {key.upper()}: {template['name']}")
            print(f"   Renk: {template['colors']['primary']}")
            print(f"   Font Boyutu: {template['text_size']}px")
            print(f"   Logo Pozisyonu: {template['logo_position']}")
        print("\n" + "="*60)


if __name__ == "__main__":
    # Test
    tm = TemplateManager("modern")
    tm.list_templates()
    
    print("\n✅ Seçili Şablon:")
    settings = tm.get_template_settings()
    print(f"İsim: {settings['name']}")
    print(f"Ana Renk: {settings['colors']['primary']}")
