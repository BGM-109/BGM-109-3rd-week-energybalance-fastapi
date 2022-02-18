from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from jamo import j2h 
from jamo import j2hcj
from jamo_generator import JamoGenerator 
from naver_scraper import Scraper


app = FastAPI()

origins = ["*"]

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#singletone
scraper = Scraper()
jamo_generator = JamoGenerator()

with open("energy_balance.json") as f:
    t = f.read().replace("\n","")
    nutrients = json.loads(t)

def filterResult(keyword: str, brand: str):
    filterd_nutrient = []
    check_chosung = list(filter(lambda x: x in jamo_generator.CHOSUNG_LIST, keyword))
    if len(check_chosung) == len(keyword):
        for n in nutrients:
            if keyword in jamo_generator.create_chosung(n["제품명"]):
                filterd_nutrient.append(n)
    elif keyword != "":
        for n in nutrients:
            if keyword in n["제품명"]:
                filterd_nutrient.append(n)
            elif n["브랜드"] != None and keyword in n["브랜드"]:
                filterd_nutrient.append(n)
    else:
        filterd_nutrient = nutrients

    if brand != "":
        temp_nutrient = []
        for f in filterd_nutrient:
            if f["브랜드"] != None and brand in f["브랜드"]:
                temp_nutrient.append(f)
        else:
            filterd_nutrient = temp_nutrient
    return filterd_nutrient

@app.get("/")
async def root():
    brands_list = set([nut["브랜드"] for nut in nutrients if nut["브랜드"]])
    response = {
        "brands": brands_list,
        "nutrients" : nutrients,
        "total": len(nutrients),
    }
    return response

@app.get("/tags")
async def read_tags():
    all_tags = []
    for n in nutrients:
        all_tags += list(n["제품명"].split())
        if n["브랜드"] is not None:
            all_tags.append(n["브랜드"])
    tags = {}
    for t in all_tags:
        tags[t] = tags.get(t, 0) + 1
    tags_result = []

    for t in sorted(tags.items(), key = lambda x: x[1], reverse = True):
        tags_result.append({
            "tag": t[0],
            "count": t[1]
        })

    response = {
        "tags": tags_result
    }
        
    return response

@app.get("/nutrients")
async def read_nutrients(page_num: int = 1, page_size: int = 60, keyword: str = "", brand: str = ""):
    #filtering 
    filterd_nutrient = []
    recommended_keyword = ""
    filterd_nutrient = filterResult(keyword, brand)
    if filterd_nutrient == []:
        recommended_keywords = scraper.naver_keyword(keyword)
        if recommended_keywords != [] and len(recommended_keywords) == 1:
            recommended_keyword = recommended_keywords[0]
            filterd_nutrient = filterResult(recommended_keyword, brand)

    start = (page_num - 1) * page_size
    end = start + page_size 

    response = {
        "nutrients": filterd_nutrient[start:end],
        "total": len(filterd_nutrient),
        "count": page_size,
        "pagination": {},
        "recommended_keyword": recommended_keyword,
    }

    # Pagination
    if end >= len(filterd_nutrient):
        response["pagination"]["next"] = None
        if page_num > 1:
            response["pagination"]["previous"] = f"/nutrients?page_num={page_num - 1}&page_size={page_size}&keyword={keyword}"
        else :
            response["pagination"]["previous"] = None
    else :
        if page_num > 1:
            response["pagination"]["previous"] = f"/nutrients?page_num={page_num - 1}&page_size={page_size}&keyword={keyword}"
        else:
            response["pagination"]["previous"] = None
        response["pagination"]["next"] = f"/nutrients?page_num={page_num + 1}&page_size={page_size}&keyword={keyword}"


    return response


