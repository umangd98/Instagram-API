from fastapi import FastAPI, HTTPException
from scrape import get_hashtag_id, get_hashtag_posts, get_permalinks, get_usernames, get_user_infos, check_valid_user_infos

app = FastAPI()

@app.get("/hashtag/{hashtag}")
async def analyze_hashtag(hashtag: str, min_followers: int, engagement_rate: int, average_likes: int):
    try:
        hashtag_id = get_hashtag_id(hashtag)
        posts = get_hashtag_posts(hashtag_id)
        permalinks = get_permalinks(posts)
        usernames = get_usernames(permalinks)
        usernames = usernames[:5]
        user_infos = get_user_infos(usernames)
        valid_user_infos = check_valid_user_infos(user_infos, min_followers, engagement_rate, average_likes)
        return {"valid_user_infos": valid_user_infos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Hello World"}