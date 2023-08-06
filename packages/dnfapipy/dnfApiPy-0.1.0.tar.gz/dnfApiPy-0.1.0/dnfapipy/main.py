import json
from urllib.parse import quote
from requests import get

class apiModule:

    # https://developers.neople.co.kr/ 에 회원가입해서 얻은 API Key를 발급받아 apiKey로 활용
    def __init__(self, apiKey:str):
        self.key = apiKey
        self.rootUrl = 'https://api.neople.co.kr/df/'

    # optionalInput에서 정보를 가져와 url을 생성
    def createUrlFromOptions(self, url:str, optionalInput:dict):
        optionalInput_keys = optionalInput.keys()
        for key in optionalInput_keys:
            if key in ['sort', 'q']:
                url += f'&{key}='
                optionalInput_keys_lv2 = optionalInput[key].keys()
                for key_lv2 in optionalInput_keys_lv2:
                    url += f'{key_lv2}:{optionalInput[key][key_lv2]},'
                url = url[:-1]
            else:
                option = optionalInput[key]
                url += f'&{key}={option}'

        return url

    # url 확정 후 호출 결과 리턴
    def getResponse(self, url:str):
        rep = get(url)
        if rep.status_code == 200:
            return json.loads(rep.text)
        else:
            error = rep.json()['error']['message']
            return f'Bad response: {rep.status_code}, {error}'

    # 01. 서버 정보
    def serverInfo(self):
        url = self.rootUrl + f'servers?apikey={self.key}'
        return self.getResponse(url)

    ### 캐릭터 관련

    # 02. 캐릭터 검색
    # optionalInput
    # {
    #   jobId:str
    #   jobGrowId:str
    #   limit:int
    #   wordType:str
    # }
    def characterSearch(self, serverId:str, characterName:str, optionalInput:dict = None):
        url = self.rootUrl + f'servers/{serverId}/characters?characterName={quote(characterName)}'
        if optionalInput:
            url = self.createUrlFromOptions(url, optionalInput)

        url += f'&apikey={self.key}'
        return self.getResponse(url)

    # 03. 캐릭터 '기본 정보' 조회
    def characterInfo(self, serverId:str, characterId:str):
        url = self.rootUrl + f'servers/{serverId}/characters/{characterId}?apikey={self.key}'
        return self.getResponse(url)

    # 04. 캐릭터 '타임라인 정보' 조회
    # optionalInput
    # {
    #   startDate:str
    #   endDate:str
    #   code:str
    #   next:str
    # }
    def characterTimelineInfo(self, serverId:str, characterId:str, limit:int = 10, optionalInput:dict = None):
        url = self.rootUrl + f'servers/{serverId}/characters/{characterId}/timeline?limit={limit}'
        if optionalInput:
            url = self.createUrlFromOptions(url, optionalInput)

        url += f'&apikey={self.key}'
        return self.getResponse(url)

    # 05. 캐릭터 '능력치 정보' 조회
    def characterStatusInfo(self, serverId:str, characterId:str):
        url = self.rootUrl + f'servers/{serverId}/characters/{characterId}/status?apikey={self.key}'
        return self.getResponse(url)

    # 06-10. 캐릭터 '장착 장비', '장착 아바타', '장착 크리쳐', '장착 휘장', '장착 탈리스만' 조회
    # possible keywords: [equipment, avatar, creature, flag, talisman]
    def characterEquip(self, serverId:str, characterId:str, keyword:str):
        url = self.rootUrl + f'servers/{serverId}/characters/{characterId}/equip/{keyword}?apikey={self.key}'
        return self.getResponse(url)

    # 11-14. 캐릭터 '스킬 스타일', '버프 스킬 강화 장착 장비', '버프 스킬 강화 장착 아바타', '버프 스킬 강화 장착 크리쳐' 조회
    # possible keywords: [equipment, avatar, creature]
    def characterSkill(self, serverId:str, characterId:str, keyword:str = None):
        url = self.rootUrl
        if keyword:
            url += f'servers/{serverId}/characters/{characterId}/skill/buff/equip/{keyword}?apikey={self.key}'
        else:
            url += f'servers/{serverId}/characters/{characterId}/skill/style?apikey={self.key}'

        return self.getResponse(url)

    ### 경매장 관련

    # 15. 경매장 등록 아이템 검색
    # optionalInput
    # {
    #   limit:int
    #   sort:dict
    #   wordType:str
    #   wordShort:bool
    #   q:dict
    # }
    def auctionSearch(self, itemInfo:dict, optionalInput:dict = None):
        url = self.rootUrl + f'auction?'
        itemInfo_key = itemInfo.keys()

        if 'itemId' in itemInfo_key  and 'itemName' not in itemInfo_key:
            item = itemInfo['itemId']
            url += f'itemId={item}'
        elif 'itemId' not in itemInfo_key  and 'itemName' in itemInfo_key:
            item = itemInfo['itemName']
            url += f'itemName={quote(item)}'
        elif 'itemId' in itemInfo_key  and 'itemName' in itemInfo_key:
            item = [itemInfo['itemId'],itemInfo['itemName']]
            url += f'itemId={item[0]}&itemName={quote(item[1])}'
        else:
            return 'Bad Input!!'

        if optionalInput:
            url = self.createUrlFromOptions(url, optionalInput)

        url += f'&apikey={self.key}'
        return self.getResponse(url)

    # 16. 경매장 등록 아이템 조회
    def auctionItem(self, auctionNo:int):
        url = self.rootUrl + f'auction/{auctionNo}?apikey={self.key}'
        return self.getResponse(url)

    # 17. 경매장 시세 검색
    # optionalInput
    # {
    #   limit:int
    #   wordType:str
    #   wordShort:bool
    # }
    def auctionSold(self, itemInfo:dict, optionalInput:dict = None):
        url = self.rootUrl + f'auction-sold?'
        itemInfo_key = itemInfo.keys()

        if 'itemId' in itemInfo_key  and 'itemName' not in itemInfo_key:
            item = itemInfo['itemId']
            url += f'itemId={item}'
        elif 'itemId' not in itemInfo_key  and 'itemName' in itemInfo_key:
            item = quote(itemInfo['itemName'])
            url += f'itemName={item}'
        elif 'itemId' in itemInfo_key  and 'itemName' in itemInfo_key:
            item = [itemInfo['itemId'],itemInfo['itemName']]
            url += f'itemId={item[0]}&itemName={quote(item[1])}'
        else:
            return 'Bad Input!!'

        if optionalInput:
            url = self.createUrlFromOptions(url, optionalInput)

        url += f'&apikey={self.key}'
        return self.getResponse(url)

    ### 아바타 마켓 관련

    # 18. 아바타 마켓 상품 검색
    # optionalInput
    # {
    #   sort:dict
    #   hashtag:str
    #   title:str
    #   wordType:str
    #   q:dict
    # }
    def avatarMarketSold(self, limit:int = 10, optionalInput:dict = None):
        url = self.rootUrl + f'avatar-market/sale?limit={limit}'
        if optionalInput:
            url = self.createUrlFromOptions(url, optionalInput)

        url += f'&apikey={self.key}'
        return self.getResponse(url)

    # 19. 아바타 마켓 상품 조회
    def avatarMarketSaleGoods(self, goodsNo:int):
        url = self.rootUrl + f'avatar-market/sale/{goodsNo}?apikey={self.key}'
        return self.getResponse(url)

    # 20. 아바타 마켓 상품 시세 검색
    # optionalInput
    # {
    #   sort:dict
    #   hashtag:str
    #   title:str
    #   wordType:str
    #   q:dict
    # }
    def avatarMarketSold(self, limit:int = 10, optionalInput:dict = None):
        url = self.rootUrl + f'avatar-market/sold?limit={limit}'
        if optionalInput:
            url = self.createUrlFromOptions(url, optionalInput)

        url += f'&apikey={self.key}'
        return self.getResponse(url)

    # 21. 아바타 마켓 상품 시세 조회
    def avatarMarketSoldGoods(self, goodsNo:int):
        url = self.rootUrl + f'avatar-market/sold/{goodsNo}?apikey={self.key}'
        return self.getResponse(url)

    # 22. 아바타 마켓 해시태그 조회
    def avatarMarketHashtag(self, hashtagType:str):
        url = self.rootUrl + f'avatar-market/hashtag?hashtagType={hashtagType}&apikey={self.key}'
        return self.getResponse(url)

    ### 아이템 관련

    # 23. 아이템 검색
    # optionalInput
    # {
    #   sort:dict
    #   hashtag:str
    #   title:str
    #   wordType:str
    #   q:dict
    # }
    def itemSearch(self, itemName:str, optionalInput:dict = None):
        url = self.rootUrl + f'items?itemName={itemName}'
        if optionalInput:
            url = self.createUrlFromOptions(url, optionalInput)

        url += f'&apikey={self.key}'
        return self.getResponse(url)

    # 24. 아이템 상세 정보 조회
    def itemInfo(self, itemId:str):
        url = self.rootUrl + f'items/{itemId}?apikey={self.key}'
        return self.getResponse(url)

    # 25. 아이템 상점 판매 정보 조회
    def itemShop(self, itemId:str):
        url = self.rootUrl + f'items/{itemId}/shop?apikey={self.key}'
        return self.getResponse(url)

    # 26. 다중 아이템 상세 정보 조회
    def itemMulti(self, itemIds:list):
        url = self.rootUrl + f'multi/items?itemIds='
        for itemId in itemIds:
            url += f'{itemId},'
        url = url[:-1] + f'&apikey={self.key}'
        return self.getResponse(url)

    # 27. 세트 아이템 검색
    # optionalInput
    # {
    #   limit:int
    #   wordType:str
    # }
    def setItemSearch(self, setItemName:str, optionalInput:dict = None):
        url = self.rootUrl + f'setitems?setItemName={quote(setItemName)}'
        if optionalInput:
            url = self.createUrlFromOptions(url, optionalInput)

        url += f'&apikey={self.key}'
        return self.getResponse(url)

    # 28. 세트 아이템 상세 정보 조회
    def setItemInfo(self, setItemId:str):
        url = self.rootUrl + f'setitems/{setItemId}?apikey={self.key}'
        return self.getResponse(url)

    # 29. 다중 세트 아이템 상세 정보 조회
    def setItemMulti(self, setItemIds:list):
        url = self.rootUrl + f'multi/setitems?setItemIds='
        for itemId in setItemIds:
            url += f'{itemId},'
        url = url[:-1] + f'&apikey={self.key}'
        return self.getResponse(url)

    # 30. 장비 조합 세트 아이템 활성화 정보 조회
    def setItemCustom(self, itemIds:list):
        url = self.rootUrl + f'custom/equipment/setitems?itemIds='
        for itemId in itemIds:
            url += f'{itemId},'
        url = url[:-1] + f'&apikey={self.key}'
        return self.getResponse(url)

    ### 직업 관련

    # 31. 직업정보
    def jobsInfo(self):
        url = self.rootUrl + f'jobs?apikey={self.key}'
        return self.getResponse(url)

    # 32. 직업별 스킬 리스트
    def jobsSkillList(self, jobId:str, jobGrowId:str):
        url = self.rootUrl + f'skills/{jobId}?jobGrowId={jobGrowId}&apikey={self.key}'
        return self.getResponse(url)

    # 33. 직업별 스킬 상세 정보 조회
    def jobsSkillInfo(self, jobId:str, skillId:str):
        url = self.rootUrl + f'skills/{jobId}/{skillId}?apikey={self.key}'
        return self.getResponse(url)

if __name__ == "__main__":
    apiModule = apiModule()
    itemInfo = {
        'itemId': 'ba8c13a72e13e5bbdc30a282e3bf8fb1'
    }

    print(apiModule.auctionSold(itemInfo=itemInfo))

    # resp = get(f'https://api.neople.co.kr/df/avatar-market/sale?apikey={apiModule.key}')
    # print(resp.text)

