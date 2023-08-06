# 웹툰을 쉽게 받도록
from WebtoonScraper import NaverWebtoonScraper
from WebtoonScraper import WebtoonsScraper
from WebtoonScraper import BestChallengeScraper
from WebtoonScraper import CanvasScraper

class Webtoon:
    NAVER = 'naver'
    BEST_CHALLENGE = 'best_challenge'
    WEBTOONS = 'webtoons'
    CANVAS = 'canvas'

    def __init__(self):
        pass
    
    def get_webtoon_type(self, webtoon_type):
        if webtoon_type.lower() == 'naver':
            webtoonscraper = NaverWebtoonScraper()
        elif webtoon_type.lower() == 'best_challenge':
            webtoonscraper = BestChallengeScraper()
        elif webtoon_type.lower() == 'webtoons':
            webtoonscraper = WebtoonsScraper()
        elif webtoon_type.lower() == 'canvas':
            webtoonscraper = CanvasScraper()
        else:
            raise ValueError('webtoon_type should be among naver, best_challenge, webtoons, and canvas.')
        return webtoonscraper
    
    def get_webtoon(self, webtoon_id:int, webtoon_type:str):
        webtoonscraper = self.get_webtoon_type(webtoon_type)
        webtoonscraper.download_one_webtoon(None, webtoon_id, 50)

    async def get_webtoon_async(self, webtoon_id:int, webtoon_type:str):
        webtoonscraper = self.get_webtoon_type(type)
        await webtoonscraper.download_one_webtoon_async(titleid=webtoon_id)