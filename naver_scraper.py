from requests_html import HTMLSession, AsyncHTMLSession

class Scraper():
    BASE_URL = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="

    def naver_keyword(self, keyword):
        result = []
        url = f'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={keyword}'
        s = HTMLSession()
        r = s.get(url)
        recommended = r.html.find('strong.source')
        for r in recommended:
            result.append(r.text)
        return result




if __name__ == '__main__':
    scraper = Scraper()
    arr = scraper.naver_keyword("버타민")