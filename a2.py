from models import LPDR_test as test

# 将文件放在'../data/images/ccpd/'下
# 参数：文件名称.文件格式
# 返回值：字符串
def mytest(fname):
  print(test.test(fname))
  return test.test(fname)

# if __name__ == '__main__':
#   print(test.test('test1.png'))
