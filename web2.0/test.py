## encoding: UTF-8  
import re
# 
## 将正则表达式编译成Pattern对象
pattern = re.compile(r'Ada Lovelac,')
 
# 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
match = pattern.match('Ada Lovelace,F,96,ISTJ,Linux,M,24,99')
 
if match:
    # 使用Match获得分组信息
    print match.string
else:
	print "wrong"
## 
##
##print pattern.groups
##### 输出 ###
### hello
#import locale
#import string
#str = "0123456789"; tt = ""
#t1 = str.split("-")
#tt.join(t1)
#print t1
#print tt
#str1 = str[::2]
#str2 = str[1::2]
#
#print str1
#print str2
#
#for i in str1:
#	print string.atoi(i) + 1
#	
#print locale.atoi("234235")


#n1 = 11 % 10
#print n1

c = "cwj"
a = c.find("wsdbe")
print a


tmp="1c3"
aaa=int(tmp) + 1
print aaa