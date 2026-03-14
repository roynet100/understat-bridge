from fastapi import FastAPI, HTTPException
from understat import Understat
import asyncio
import aiohttp

app = FastAPI()

@app.get("/stats/{team_slug}")
async def get_team_stats(team_slug: str):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        try:
            # מושך נתונים לעונת 2025 (שהיא 2025/26)
            data = await understat.get_team_results(team_slug, 2025)
            # מחזיר רק משחקים שהסתיימו (שיש להם xG)
            finished_matches = [m for m in data if m['xG']['h'] is not None]
            return finished_matches[-5:] # 5 האחרונים
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
