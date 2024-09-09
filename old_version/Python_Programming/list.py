ls = ['one', 'two', 'three', 1, 2, 3]
print(ls[0], ls[-1])

L1 = [[1, 2]]
L2 = [[3, 4]]
L = [[5, 5]]

print(L * 3)
print(L1 + L2)

#split function
print("Thought become things.".split())
#join function
L3 = ['hello', 'there']
print(' '.join(L3))
print('-'.join('2012/01/04'.split('/')))

#sort function
li = [2, 3, 1, 5, 4]
print(li.sort())
print(li)
#append(), extend()
L4 = [1, 2]
L4.append([3, 4])
print(L4)
L4.extend([3, 4]) #[3,4] is followed by first-order arrangement continuously 
print(L4) 
#replace()
print('2012/08/26'.replace('/', '-'))
#format()
print(format(1234567890, ','))
'''============================================================================='''
myList = ['Thoughts', 'become', 'things.']
newList = myList[:]
print(newList)
newList[-1] = 'actions.'
print(newList)
print(myList)

#List Including
nums = [1, 2, 3, 4, 5]
squares = []
for x in nums :
    squares.append(x ** 2)
print(squares)

nums2 = [1, 2, 3, 4, 5]
squares2 = [x ** 2 for x in nums2]
even_squares2 = [x ** 2 for x in nums2 if x % 2 == 0]
print(squares2)
print(even_squares2)

