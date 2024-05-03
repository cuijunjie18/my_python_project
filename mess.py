test = {1:12,2:9,3:7}
print(test)

a = sorted(test.keys())
print(a)

b = sorted(test.values())
print(b)

c = sorted(test.items(),key = lambda d:d[1],reverse = False)
print(c)