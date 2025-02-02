from googleapiclient.discovery import build
from src.Config import Config

class YouTubeComments:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=Config.YOUTUBE_API_KEY)

    def get_video_comments(self, video_id: str, max_results: int = 100) -> list:
        comments = []
        results = self.youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=max_results
        ).execute()

        while results:
            for item in results["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)

            if "nextPageToken" in results:
                results = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    pageToken=results["nextPageToken"],
                    maxResults=max_results
                ).execute()
            else:
                break

        return comments