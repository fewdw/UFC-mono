from pytube import YouTube
import os


class YouTubeDownloader:
    @staticmethod
    def download_audio(youtube_url: str, output_dir: str = "temp_audio") -> str:
        """
        Returns path to downloaded audio file
        """
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = audio_stream.download(output_dir=output_dir)
        mp3_path = os.path.splitext(file_path)[0] + '.mp3'
        os.rename(file_path, mp3_path)

        return mp3_path