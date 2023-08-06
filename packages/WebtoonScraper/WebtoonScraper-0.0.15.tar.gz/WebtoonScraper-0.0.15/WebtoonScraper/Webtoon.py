# 웹툰을 쉽게 받도록
from WebtoonScraper import NaverWebtoonScraper
class Webtoon:
    NAVER = 'naver'
    BEST_CHALLENGE = 'best_challenge'
    WEBTOONS = 'webtoons'
    CANVAS = 'canvas'

    def __init__(self):
        pass
    
    def get_type(self, type):
        if type.lower() == 'naver':
            webtoonscraper = NaverWebtoonScraper()
        elif type.lower() == 'best_challenge':
            webtoonscraper = BestChallengeScraper()
        elif type.lower() == 'webtoons':
            webtoonscraper = WebtoonsScraper()
        elif type.lower() == 'canvas':
            webtoonscraper = CanvasScraper()
        else:
            raise ValueError('type should be among naver, best_challenge, webtoons, and canvas.')
        return webtoonscraper
    
    def get_webtoon(self, webtoon_id:int, type:str):
        webtoonscraper = self.get_type(type)
        webtoonscraper.download_one_webtoon(None, webtoon_id, 50)

    async def get_webtoon_async(self, webtoon_id:int, type:str):
        webtoonscraper = self.get_type(type)
        await webtoonscraper.download_one_webtoon_async(titleid=webtoon_id)