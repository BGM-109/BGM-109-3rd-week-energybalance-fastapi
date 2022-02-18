from jamo import j2h 
from jamo import j2hcj 

class JamoGenerator():
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'] 
    JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'] 
    JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'] ####################################################################################

    def korean_jamo(self, k_word: str): 
        r_lst = [] 
        for w in list(k_word.strip()): 
            if '가'<=w<='힣': 
                ch1 = (ord(w) - ord('가'))//588 
                ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28 
                ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2 
                r_lst.append([self.CHOSUNG_LIST[ch1], self.JUNGSUNG_LIST[ch2], self.JONGSUNG_LIST[ch3]]) 
            else: r_lst.append([w]) 
        return "".join(sum(r_lst, []))

    def create_chosung(self, word: str):
        r_lst = [] 
        for w in list(word.strip()): 
            if '가'<=w<='힣': 
                ch1 = (ord(w) - ord('가'))//588 
                ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28 
                ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2 
                r_lst.append([self.CHOSUNG_LIST[ch1]]) 
            else: r_lst.append([w]) 
        return "".join(sum(r_lst, []))



if __name__ == '__main__':
    generator = JamoGenerator()
    arr = generator.korean_jamo("안녕하세요")
    print(arr)

