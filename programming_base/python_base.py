name = "안찬후"
birth = "2003"
print(f"나의 아름은 {name}이며, {birth}년에 태어났습니다.")

var = '퀀트 투자 포트폴리오 만들기'
print(var.replace(' ', '_'))
var = "퀀트 투자 포트폴리오 만들기"
print(var.split())

var = [1, 2 ,3]
del var[0]
print(var)

var = [1,2,3, 1, 2, 3]
var.remove(1)
print(var)

var = [1, 2 ,3]
print(var.pop())

var = [1,2, 4231, 212]
var.sort()
print(var)

dic = {'key1' : 1, 'key2' :2}
dic['key3'] = 3
print(dic)
del dic['key3']
print(dic)

print(list(dic.keys()))
print(list(dic.values()))

s = set('banana')
print(s)

s1 = set([1, 2, 3, 4])
s2 = set([3, 4, 5, 6])
print(s1.union(s2))
print(s1.intersection(s2))
print(s1.difference(s2))

"gg"