from googleapiclient.discovery import build
import json

API_KEY = "API KEY"

youtube = build("youtube", "v3", developerKey=API_KEY)


def get_videos(query):
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=10
    )

    response = request.execute()
    videos = []

    for item in response.get("items", []):
        if "id" in item and "videoId" in item["id"]:

            video_id = item["id"]["videoId"]
            date = item["snippet"]["publishedAt"]

            videos.append({
                "video_id": video_id,
                "date": date
            })

    return videos


def get_comments(video_id):

    comments = []

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=50
        )

        response = request.execute()

        for item in response.get("items", []):

            snippet = item["snippet"]["topLevelComment"]["snippet"]

            comment_text = snippet["textDisplay"]
            comment_date = snippet["publishedAt"]

            # Skip non-English comments
            if not comment_text.isascii():
                continue

            # Skip empty comments
            if len(comment_text.strip()) == 0:
                continue

            comments.append({
                "comment": comment_text,
                "comment_date": comment_date
            })

            # Stop when 10 valid comments collected
            if len(comments) == 10:
                break

    except Exception as e:
        print(f"Skipping video {video_id} because of error: {e}")

    return comments

    return comments

def brand_pulse(brand):
    videos = get_videos(brand)
    data = []

    for video in videos:
        comments = get_comments(video["video_id"])

        data.append({
            "brand": brand,
            "video_id": video["video_id"],
            "date": video["date"],
            "comments": comments
        })

    with open(f"{brand}_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Data saved successfully!")


brand = input("Enter brand name: ")
brand_pulse(brand)
