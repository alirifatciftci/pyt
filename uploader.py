"""
VideoOtoFabrika - Otomatik Yükleme Modülü
TikTok ve YouTube Shorts'a otomatik video yükleme
"""

import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import pickle

load_dotenv()


class VideoUploader:
    def __init__(self):
        """Video yükleyiciyi başlat"""
        self.youtube_credentials = None
        
    def generate_title_description(self, scenario):
        """
        Senaryo için başlık ve açıklama üret
        
        Args:
            scenario: Video senaryosu
            
        Returns:
            tuple: (başlık, açıklama, hashtags)
        """
        # İlk cümleyi başlık yap ama daha çekici
        sentences = scenario.split('.')
        first_sentence = sentences[0].strip()
        
        # Başlık optimizasyonu
        title = first_sentence
        
        # Emoji ekle (dikkat çekici)
        emoji_map = {
            'hazır': '🤯',
            'inanmayacaksın': '😱',
            'şok': '⚡',
            'biliyormusun': '🧠',
            'düşünsene': '💭',
            'inanılmaz': '🔥'
        }
        
        for keyword, emoji in emoji_map.items():
            if keyword in title.lower():
                title = f"{emoji} {title}"
                break
        
        # Başlık çok uzunsa kısalt
        if len(title) > 80:
            title = title[:77] + "..."
        
        # Açıklama - #Shorts hashtag'i ÖNEMLİ!
        description = f"{scenario}\n\n"
        
        # Hashtag'ler - YouTube Shorts için optimize edilmiş
        hashtags = [
            "#Shorts",
            "#YouTubeShorts",
            "#viral",
            "#keşfet",
            "#ilginçbilgiler",
            "#şaşırtıcıgerçekler",
            "#öğren",
            "#bilgiçağı",
            "#fyp",
            "#foryou",
            "#türkiye",
            "#türkçe",
            "#eğitim",
            "#bilim",
            "#teknoloji"
        ]
        
        description += "\n".join(hashtags)
        
        return title, description, hashtags
    
    def upload_to_youtube(self, video_path, title, description):
        """
        YouTube Shorts'a video yükle
        
        Args:
            video_path: Video dosyası yolu
            title: Video başlığı
            description: Video açıklaması
            
        Returns:
            str: Video URL'i veya None
        """
        try:
            print("\n📤 YouTube'a yükleniyor...")
            
            # YouTube API kimlik doğrulama
            youtube = self._authenticate_youtube()
            
            if not youtube:
                print("❌ YouTube kimlik doğrulama başarısız!")
                return None
            
            # Video metadata - YouTube Shorts için optimize edilmiş
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': ['shorts', 'ilginç bilgiler', 'eğitim', 'bilgi', 'türkiye', 'viral'],
                    'categoryId': '27'  # Education
                },
                'status': {
                    'privacyStatus': 'public',  # public, private, unlisted
                    'selfDeclaredMadeForKids': False,
                    'madeForKids': False
                }
            }
            
            print("📱 YouTube Shorts formatında yükleniyor (9:16, <60s)...")
            
            # Video yükleme
            media = MediaFileUpload(
                video_path,
                mimetype='video/mp4',
                resumable=True,
                chunksize=1024*1024  # 1MB chunks
            )
            
            request = youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            print("⏳ Yükleniyor... (Bu biraz zaman alabilir)")
            
            response = None
            while response is None:
                try:
                    status, response = request.next_chunk()
                    if status:
                        progress = int(status.progress() * 100)
                        print(f"📤 Yükleme: %{progress}")
                except Exception as chunk_error:
                    print(f"⚠️ Chunk hatası: {chunk_error}")
                    raise
            
            video_id = response['id']
            video_url = f"https://youtube.com/shorts/{video_id}"
            
            print(f"✅ YouTube'a yüklendi: {video_url}")
            return video_url
            
        except Exception as e:
            print(f"❌ YouTube yükleme hatası: {e}")
            return None
    
    def _authenticate_youtube(self):
        """
        YouTube API kimlik doğrulama
        
        Returns:
            YouTube API service veya None
        """
        try:
            SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
            credentials = None
            
            # Token dosyası varsa yükle
            if os.path.exists('youtube_token.pickle'):
                with open('youtube_token.pickle', 'rb') as token:
                    credentials = pickle.load(token)
            
            # Token yoksa veya geçersizse yenile
            if not credentials or not credentials.valid:
                if credentials and credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                else:
                    # OAuth akışı başlat
                    if not os.path.exists('client_secrets.json'):
                        print("⚠️ client_secrets.json dosyası bulunamadı!")
                        print("📝 YouTube API kurulumu için:")
                        print("1. https://console.cloud.google.com/ adresine git")
                        print("2. Yeni proje oluştur")
                        print("3. YouTube Data API v3'ü etkinleştir")
                        print("4. OAuth 2.0 Client ID oluştur (Desktop app)")
                        print("5. JSON'u indir ve 'client_secrets.json' olarak kaydet")
                        return None
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'client_secrets.json',
                        SCOPES
                    )
                    credentials = flow.run_local_server(port=0)
                
                # Token'ı kaydet
                with open('youtube_token.pickle', 'wb') as token:
                    pickle.dump(credentials, token)
            
            # YouTube service oluştur
            youtube = build('youtube', 'v3', credentials=credentials)
            return youtube
            
        except Exception as e:
            print(f"❌ YouTube kimlik doğrulama hatası: {e}")
            return None
    
    def upload_to_tiktok(self, video_path, title, hashtags):
        """
        TikTok'a video yükle
        
        Args:
            video_path: Video dosyası yolu
            title: Video başlığı
            hashtags: Hashtag listesi
            
        Returns:
            bool: Başarılı mı?
        """
        try:
            print("\n📤 TikTok'a yükleniyor...")
            
            # TikTok için başlık + hashtag
            caption = f"{title}\n\n" + " ".join(hashtags[:5])  # İlk 5 hashtag
            
            # TikTok uploader kütüphanesi
            try:
                from tiktok_uploader.upload import upload_video
                from tiktok_uploader.auth import AuthBackend
            except ImportError:
                print("⚠️ tiktok-uploader kütüphanesi yüklü değil!")
                print("📦 Yüklemek için: pip install tiktok-uploader")
                return False
            
            # TikTok session dosyası kontrolü
            if not os.path.exists('tiktok_session.txt'):
                print("⚠️ TikTok oturum dosyası bulunamadı!")
                print("📝 TikTok kurulumu için:")
                print("1. TikTok hesabına giriş yap")
                print("2. Session cookie'lerini 'tiktok_session.txt' dosyasına kaydet")
                print("3. Detaylı kurulum: https://github.com/wkaisertexas/tiktok-uploader")
                return False
            
            # Video yükleme
            failed_videos = upload_video(
                video_path,
                description=caption,
                cookies='tiktok_session.txt'
            )
            
            if not failed_videos:
                print("✅ TikTok'a yüklendi!")
                return True
            else:
                print(f"❌ TikTok yükleme başarısız: {failed_videos}")
                return False
                
        except Exception as e:
            print(f"❌ TikTok yükleme hatası: {e}")
            return False
    
    def upload_video(self, video_path, scenario, platforms=['youtube', 'tiktok']):
        """
        Videoyu seçilen platformlara yükle
        
        Args:
            video_path: Video dosyası yolu
            scenario: Video senaryosu
            platforms: Yüklenecek platformlar listesi
            
        Returns:
            dict: Yükleme sonuçları
        """
        results = {
            'youtube': None,
            'tiktok': False
        }
        
        # Başlık ve açıklama üret
        title, description, hashtags = self.generate_title_description(scenario)
        
        print("\n" + "="*60)
        print("📤 VIDEO YÜKLEME")
        print("="*60)
        print(f"📝 Başlık: {title}")
        print(f"🏷️ Hashtag'ler: {' '.join(hashtags[:5])}")
        
        # YouTube'a yükle
        if 'youtube' in platforms:
            youtube_url = self.upload_to_youtube(video_path, title, description)
            results['youtube'] = youtube_url
        
        # TikTok'a yükle
        if 'tiktok' in platforms:
            tiktok_success = self.upload_to_tiktok(video_path, title, hashtags)
            results['tiktok'] = tiktok_success
        
        print("\n" + "="*60)
        print("📊 YÜKLEME SONUÇLARI")
        print("="*60)
        
        if results['youtube']:
            print(f"✅ YouTube: {results['youtube']}")
        else:
            print("❌ YouTube: Yüklenemedi")
        
        if results['tiktok']:
            print("✅ TikTok: Başarılı")
        else:
            print("❌ TikTok: Yüklenemedi")
        
        print("="*60 + "\n")
        
        return results


if __name__ == "__main__":
    # Test
    uploader = VideoUploader()
    
    # Test senaryosu
    test_scenario = "Hazır mısın? Balinalar aslında uyurken nefes almayı unutmuyor!"
    
    print("Test Başlık ve Açıklama:")
    title, desc, tags = uploader.generate_title_description(test_scenario)
    print(f"Başlık: {title}")
    print(f"Açıklama: {desc}")
    print(f"Hashtag'ler: {tags}")
