#!C:/Users/oyj67/AppData/Local/Programs/Python/Python310/python.exe
# -*- coding: utf-8 -*-
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from model import CustomerModel, ViewModel, MerchantModel, LogisticModel
from db import conn, cur
import cgi
import json



print("Content-type: application/json\n")

form = cgi.FieldStorage()  
act = form.getvalue('act')

view_model = ViewModel(conn, cur)
customer_model = CustomerModel(conn, cur)
merchant_model = MerchantModel(conn, cur)
logistic_model = LogisticModel(conn, cur)

def browse_products():
    """
    獲取資料庫中(商品)的所有產品, 並返回 JSON 格式的響應
    """
    ###verify
    objects = view_model.browse_products()
    # print(objects)
    return json.dumps(objects)

# g = browse_products()
# print(g)
# exit(0)

def login():
    """
    登入來確認身分
    """
    ###verify
    account = form.getvalue('account') # "user1" #
    password = form.getvalue('password') #"1234" # 
    # print(account, password)
    result , type_acc, name, id = view_model.login(account, password)
    # print(result)
    if result == True:
        return json.dumps({'status': 'success', 'type': str(type_acc), 'name': str(name), 'id': str(id)})
    else:
        return json.dumps({'status': 'fail', 'type':"0"})

def register():
    """
    註冊，將資料加入資料庫
    """
    name = form.getvalue('name')
    account = form.getvalue('account')
    password = form.getvalue('password')
    type_acc = form.getvalue('type')

    # name = "test"
    # account = "user10"
    # password = "1234"
    # type_acc = "1"
    ###verify
    result = view_model.register(name, account, password, type_acc)
    if result == True:
        return json.dumps({'status': 'success'})
    else:
        return json.dumps({'status': 'fail'})

# r = register()
# print(r)
# exit()
# f = login()
# print(f)
# print(type(f))
# exit(0)

# =================================顧客==================================================

def show_cart():
    """
    獲取資料庫(購物車)中的所有產品, 並返回 JSON 格式的響應
    """                                
    ###verify
    MID = int(form.getvalue('id_customer'))
    # MID = 1
    contents = customer_model.shopping_cart(MID)
    return json.dumps(contents)

# s = show_cart()
# print(s)
# exit(0)



def plus_product():
    """
    將一個新的產品添加到購物車中。
    
    """
    MID = int(form.getvalue('id_customer'))
    IID = int(form.getvalue('id_item'))
    quantity = int(form.getvalue('quantity'))

    # MID = 1
    # IID = 1
    # quantity = 1

    ###verify
    customer_model.plus_to_cart(MID, IID, quantity)
    return True


# plus_product()
# exit(0)


def subtract_product():
    """
    將一個新的產品從購物車中減去。
        
    """
    MID = int(form.getvalue('id_customer'))
    IID = int(form.getvalue('id_item'))

    # MID = 1
    # IID = 1
    ###verify
    customer_model.subtract_from_cart(MID, IID)
    return True

# subtract_product()
# exit(0)

def close_account():          
    """
    計算購物車中的所有產品的總價格。
    """                      
    ###verify
    MID = int(form.getvalue('id_customer'))
    # MID = 1
    lst = customer_model.settlement(MID)
    return json.dumps(lst)

# f = close_account()
# print(f)
# exit(0)

def checkout():
    """
    結帳，將購物車中的商品加入訂單
    """
    # MID = 1
    MID = int(form.getvalue('id_customer'))
    ###verify
    customer_model.checkout(MID)
    return True

# checkout()
# exit(0)

def show_order_customer():
    """
    獲取資料庫(訂單)中的所有產品, 並返回 JSON 格式的響應
    """                                
    ###verify
    MID = int(form.getvalue('id_customer'))
    # MID = 1
    contents = customer_model.show_order_customer(MID)
    return json.dumps(contents)

# s = show_order_customer()
# print(s)
# exit(0)

def score_order():
    """
    評分訂單
    """                                
    ###verify
    IID = int(form.getvalue('id_order'))
    score = int(form.getvalue('score'))
    MID = int(form.getvalue('id_customer'))
    # IID = 3
    # score = 5
    # MID = 1
    result = customer_model.score_order(IID, MID, score)
    if result == False:
        return False
    else:
        return True
    

# f = score_order()
# print(f)
# exit(0)
# =================================商家==================================================

def show_merchant_items():
    """
    找到商家的所有商品
    """                                
    ###verify
    MID = int(form.getvalue('id_merchant'))
    # MID = 3
    contents = merchant_model.show_items(MID)

    return json.dumps(contents)

# d = show_merchant_items()
# print(d)
# exit(0)

def add_product():
    """
    將一個新的產品添加進資料庫中。
    
    """
    MID = form.getvalue('id_merchant')
    name = form.getvalue('name')
    description = form.getvalue('description')
    price = form.getvalue('price')

    # MID = 3
    # name = "testsd"
    # description = "test111"
    # price = 122

    ###verify
    merchant_model.add_product(MID, name, description, price)
    return True

# p = add_product()
# print(p)
# exit(0)

def edit_product():
    """
    修改一個產品的資料。
    
    """
    IID = form.getvalue('id_item')
    name = form.getvalue('name')
    description = form.getvalue('description')
    price = form.getvalue('price')

    # IID = 3
    # name = "test"
    # description = "test111"
    # price = 12232

    ###verify
    merchant_model.edit_product(IID, name, description, price)
    return True

# f = edit_product()
# print(f)
# exit(0)

def delete_product():
    """
    刪除一個產品。
    
    """
    MID = form.getvalue('id_merchant')
    IID = form.getvalue('id_item')

    # MID = 3
    # IID = 7

    ###verify
    result = merchant_model.delete_product(MID, IID)
    if result == False:
        return False
    else:
        return True

# f = delete_product()
# print(f)
# exit(0)

def show_order_merchant():
    """
    獲取資料庫(訂單)中的所有產品, 並返回 JSON 格式的響應
    """                                
    ###verify
    MID = int(form.getvalue('id_merchant'))
    # MID = 3
    contents = merchant_model.show_order_merchant(MID)
    return json.dumps(contents)

# f = show_order_merchant()
# print(f)
# exit(0)

def update_order_status():
    """
    更新訂單狀態
    """                                
    ###verify
    ORID = int(form.getvalue('id_order'))
    state = form.getvalue('state')
    
    # MID = 3
    # state = None

    merchant_model.update_order_status(ORID, state)
    
    return True

# f = update_order_status()
# print(f)
# exit(0)

# =================================物流===================================================

def show_order_logistics():
    """
    獲取資料庫(訂單)中的所有產品, 並返回 JSON 格式的響應
    """                                
    ###verify

    contents = logistic_model.show_order_logistic()
    return json.dumps(contents)

# f = show_order_logistics()
# print(f)
# exit(0)

def update_order_status_logistics():
    """
    更新訂單狀態
    """                                
    ###verify
    ORID = int(form.getvalue('id_order'))
    # ORID = 6

    logistic_model.update_order_status(ORID)
    
    return True

# f = update_order_status_logistics()
# print(f)
# exit(0)

if act == 'browse':
    response = browse_products()
elif act == 'login':
    response = login()
elif act == 'register':
    response = register()
# ====================================顧客==================================================
elif act == 'cart':
    response = show_cart()
elif act == 'plus_prd':
    response = plus_product()
elif act == 'subtract':
    response = subtract_product()
elif act == 'settlement':
    response = close_account()
elif act == 'checkout':
    response = checkout()
elif act == 'show_order_customer':
    response = show_order_customer()
elif act == 'score_order':
    response = score_order()
# ====================================商家==================================================
elif act == 'show_merchant_items':
    response = show_merchant_items()
elif act == 'add_product':
    response = add_product()
elif act == 'edit_product':
    response = edit_product()
elif act == 'delete_product':
    response = delete_product()
elif act == 'show_order_merchant':
    response = show_order_merchant()
elif act == 'update_order_status':
    response = update_order_status()
# ====================================物流===================================================
elif act == 'show_order_logistics':
    response = show_order_logistics()
elif act == 'update_order_status_logistics':
    response = update_order_status_logistics()
else:
    response = json.dumps({'error': 'Invalid action'})

print(response)
