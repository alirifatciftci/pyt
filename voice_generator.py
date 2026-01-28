"""
VideoOtoFabrika - Ses Üretici Modülü
Edge-TTS kullanarak metni Türkçe sese çevirir.
"""

import asyncio
import edge_tts
import os


class VoiceGenerator:
    def __init__(self, voice="tr-TR-AhmetNeural", speed_multiplier=1.5):
        """
        Ses üreticiyi başlat
        
        Args:
            voice: Kullanılacak ses modeli (varsayılan: tr-TR-AhmetNeural)
            speed_multiplier: Ses hızı çarpanı (varsayılan: 1.5x) - MoviePy'de kullanılacak
        """
        self.voice = voice
        self.speed_multiplier = speed_multiplier
    
    async def generate_voice(self, text, output_path="output_audio.mp3"):
        """
        Metni sese çevir (hızlandırılmış)
        
        Args:
            text: Seslendirilecek metin
            output_path: Çıktı dosyası yolu
            
        Returns:
            str: Oluşturulan ses dosyasının yolu
        """
        try:
            print(f"🎤 Ses üretiliyor (Ses: {self.voice}, Hız: {self.speed_multiplier}x)...")
            
            # Edge-TTS rate parametresi ile hız ayarı
            # rate: +0% (normal), +50% (1.5x), +100% (2x)
            rate_percent = int((self.speed_multiplier - 1.0) * 100)
            rate_str = f"+{rate_percent}%" if rate_percent > 0 else f"{rate_percent}%"
            
            # Edge-TTS ile hızlandırılmış ses oluştur
            communicate = edge_tts.Communicate(text, self.voice, rate=rate_str)
            await communicate.save(output_path)
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024  # KB
                print(f"✅ Ses dosyası oluşturuldu: {output_path} ({file_size:.2f} KB)")
                return output_path
            else:
                raise FileNotFoundError("Ses dosyası oluşturulamadı!")
                
        except Exception as e:
            print(f"❌ Ses üretimi hatası: {e}")
            raise


async def main():
    """Test fonksiyonu"""
    generator = VoiceGenerator(voice="tr-TR-AhmetNeural")
    test_text = "Merhaba! Bu bir test mesajıdır. VideoOtoFabrika projesi çalışıyor."
    await generator.generate_voice(test_text, "test_audio.mp3")


if __name__ == "__main__":
    asyncio.run(main())
