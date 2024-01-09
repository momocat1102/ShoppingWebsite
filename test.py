import unittest, json
from model import ViewModel  # 替换为你的模型类名
from db import conn, cur

class TestYourModelClass(unittest.TestCase):  # 替换为你的模型类名
    def setUp(self):
        self.model = ViewModel(conn, cur)  # 创建模型实例

    def test_login(self):
        account = 'user1'  # 替换为测试账号
        password = '1234'  # 替换为测试密码
        result , type = self.model.login(account, password)
        # print(result)
        if result == True:
            ans =  json.dumps({'status': 'success', 'type': str(type)})
        else:
            ans =  json.dumps({'status': 'fail', 'type':"0"})
        
        expected_result = {}  # 替换为预期结果
        print(ans) 
        print(type(ans))
        # result = self.model.login(account, password)
        # self.assertEqual(ans, expected_result)

if __name__ == '__main__':
    # unittest.main()
    model = ViewModel(conn, cur)
    account = 'user1'  # 替换为测试账号
    password = '1234'  # 替换为测试密码
    result, account_type = model.login(account, password)
    # print(result)
    if result == True:
        ans =  json.dumps({'status': 'success', 'type': str(account_type)})
    else:
        ans =  json.dumps({'status': 'fail', 'type':"0"})
    
    expected_result = {}  # 替换为预期结果
    print(ans) 
    print(type(ans))
    # result = self.model.login(account, password)
    # self.assertEqual(ans, expected_result)