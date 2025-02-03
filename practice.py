#딕셔너리
db = {
    '전자제품': ['MacBook', 'iPad', 'iPhone'],
    '스포츠용품': ['축구공', '야구글러브', '농구공']
}

print(db['전자제품']) # ['MacBook', 'iPad', 'iPhone']


def getProductOfCategory(category):
    return db.get(category, []) # 없으면 빈 리스트 반환

