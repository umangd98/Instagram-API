from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from scrape import get_hashtag_id, get_hashtag_posts, get_permalinks, get_usernames, get_user_infos, check_valid_user_infos

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hashtag/{hashtag}")
async def analyze_hashtag(hashtag: str, min_followers: int, max_followers:int, engagement_rate: int, average_likes: int):
    try:
        hashtag_id = get_hashtag_id(hashtag)
        posts = get_hashtag_posts(hashtag_id)
        permalinks = get_permalinks(posts)
        usernames = get_usernames(permalinks)
        usernames = usernames
        user_infos = get_user_infos(usernames)
        valid_user_infos = check_valid_user_infos(user_infos, min_followers, max_followers, engagement_rate, average_likes)
        return {"valid_user_infos": valid_user_infos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Hello World"}