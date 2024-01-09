#!C:/Users/oyj67/AppData/Local/Programs/Python/Python310/python.exe
# -*- coding: utf-8 -*-
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import datetime

class ViewModel:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def browse_products(self):
        """
        獲取資料庫中(商品)的所有產品, 並返回 JSON 格式的響應
        """
        try:
            self.cur.execute("SELECT * FROM Item;")  
            result = self.cur.fetchall()
            
            prds = []                             
            for data in result:
                # 找出每個商品跟廠商的對應
                sql = "SELECT OID1 FROM orel WHERE Type = 1 AND OID2 = %s;"
                values = (data[0],)
                self.cur.execute(sql, values)
                merchant = self.cur.fetchone()[0]
                # 找出廠商的名字
                sql = "SELECT Name FROM member WHERE Type = 2 AND MID = %s;"
                values = (merchant,)
                self.cur.execute(sql, values)
                merchant_name = self.cur.fetchone()[0]
                
                # 找出顧客的評價在orel中type = 3 來統計此廠商的評價
                sql = "SELECT Content FROM orel WHERE Type = 3 AND OID2 = %s;"
                values = (merchant,)
                self.cur.execute(sql, values)
                evaluations = self.cur.fetchall()
                # 如果沒有評價就給0
                if len(evaluations) < 1:
                    score = 0
                else:
                    score = 0
                    for i in range(len(evaluations)):
                        score += evaluations[i][0]
                    score = round(score / len(evaluations), 1)
                    
                # print(merchant_name, score, data[0], data[1], data[2], data[3])
                prds.append([merchant_name, score, data[0], data[1], data[2], data[3]])
            
            return prds

        except Exception as e:
            print(f"Error listing products: {e}")

    def login(self, account, password):
        """
        登入來確認身分
        """
        try:
            # 比對資料庫中的帳號密碼
            self.cur.execute("SELECT * FROM Member;")
            result = self.cur.fetchall()
            # print(result)
            for data in result:
                # print(data[2], data[3])
                if str(account) == str(data[2]) and str(password == data[3]):
                    return [True, data[1], data[4], data[0]]        
            return [False, -1]

        except Exception as e:
            print(f"Error listing products: {e}")

    def register(self, name, account, password, type_acc):
        """
        註冊，將資料加入資料庫
        """
        try:
            # 將資料加入資料庫
            sql = "INSERT INTO `Member` (Name, Account, Password, Type) VALUES (%s, %s, %s, %s);"
            values = (name, account, password, type_acc)
            self.cur.execute(sql, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error registering: {e}")

    def evaluate(self, MID):
        try:
            # 計算商家的評價
            sql = "SELECT * FROM `orel` WHERE `Type` = 3 AND `OID2` = %s;"
            values = (MID,)
            self.cur.execute(sql, values)
            result = self.cur.fetchall()
            if len(result) < 1:
                return 0
            else:
                score = 0
                for row in result:
                    score += row[6]
                score = score / len(result)
                return score
        except Exception as e:
            print(f"Error evaluating: {e}")
    

class CustomerModel:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur         

    def shopping_cart(self, MID):
        try:

            # sql = "SELECT * FROM `orel` WHERE `OID1` = %s; AND `Type` = 2"
            sql = "SELECT I.IID, I.Name, I.Description, I.Price, O.Content \
                    FROM orel AS O, item AS I \
                    WHERE O.OID1 = %s AND O.OID2 = I.IID AND O.Type = 2;"
            values = (MID,)
            self.cur.execute(sql, values)  
            result = self.cur.fetchall()
            # print(result)
            # 找出所有商品的資訊
            # IIDs = [data[1] for data in result]
            
            # sql = "SELECT * FROM `Item` WHERE `id` IN %s;"
            # values = (tuple(IIDs),)
            # self.cur.execute(sql, values)
            # cart = []                                
            # for data in result:
            #     cart.append(data)
            return result

        except Exception as e:
            print(f"Error generating cart: {e}")

    def plus_to_cart(self, MID, IID, quantity):
        try:
            

            sql = "SELECT * FROM `orel` WHERE `Type` = 2 AND `OID1` = %s AND `OID2` = %s;"
            values = (MID, IID)
            self.cur.execute(sql, values)
            result = self.cur.fetchone()

            if result:
                sql = "UPDATE `orel` SET `Content` = `Content` + %s, `Since` = %s WHERE `OID1` = %s AND `OID2` = %s;"
                values = (quantity, datetime.datetime.now(), MID, IID)
                self.cur.execute(sql, values)
            else:
                sql = "INSERT INTO `orel` (OID1, OID2, Content, Type, Since) VALUES (%s, %s, %s, %s, %s);"
                values = (MID, IID, quantity, 2, datetime.datetime.now())
                self.cur.execute(sql, values)
            self.conn.commit()
            return True
                
        except Exception as e:
            print(f"Error adding to cart: {e}")
 
    def subtract_from_cart(self, MID, IID):
        try:
            sql = "SELECT * FROM `orel` WHERE `Type` = 2 AND `OID1` = %s AND `OID2` = %s;"
            values = (MID, IID)
            self.cur.execute(sql, values)
            result = self.cur.fetchone()
            
            if result:
                if result[3] > 1:
                    sql = "UPDATE `orel` SET `Content` = `Content` - 1, `Since` = %s WHERE `OID1` = %s AND `OID2` = %s;"
                    values = (datetime.datetime.now(), MID, IID)
                    self.cur.execute(sql, values)
                else:
                    sql = "DELETE FROM `orel` WHERE `OID1` = %s AND `OID2` = %s;"
                    values = (MID, IID)
                    self.cur.execute(sql, values)
            
            self.conn.commit()
            return True
        
        except Exception as e:
            print(f"Error deleting from cart: {e}")
        
    def settlement(self, MID):
        try:
            # 計算購物車中所有商品總價格
            sql = "SELECT I.Price, O.Content \
                    FROM orel AS O, item AS I \
                    WHERE O.OID1 = %s AND O.OID2 = I.IID AND O.Type = 2;"
            values = (MID,)
            self.cur.execute(sql, values)
            result = self.cur.fetchall()
            if len(result) < 1:
                return [0, 0]
            
            else:
                '''
                quantity = sum(row[0] for row in result)
                price = sum(row[0] * row[1] for row in result)
                buycar = [quantity, price]
                return buycar
                '''
                quantity = 0
                price = 0
                buycar = []
                
                for row in result:
                    quantity += row[1]
                    price += (row[0] * row[1])
                buycar.extend([quantity, price])

                return buycar

        except Exception as e:
            print(f"Error fetching settlement: {e}")

    def checkout(self, MID):
        try:
            # 將購物車中的所有商品添加到訂單中, 將type從2改成4, state 改成 1
            sql = "UPDATE `orel` SET `Type` = 4, `State` = 1 WHERE `OID1` = %s AND `Type` = 2;"
            values = (MID,)
            self.cur.execute(sql, values)
            self.conn.commit()
            return True

        except Exception as e:
            print(f"Error checking out: {e}")

    def show_order_customer(self, MID):
        try:
            # 顯示所有訂單
            sql = "SELECT O.OID2, I.Name, I.Description, I.Price, O.Content, O.state \
                    FROM orel AS O, item AS I \
                    WHERE O.OID1 = %s AND O.OID2 = I.IID AND O.Type = 4;"
            values = (MID,)
            self.cur.execute(sql, values)
            result = self.cur.fetchall()
            # print(result)
            return result

        except Exception as e:
            print(f"Error showing order: {e}")

    def score_order(self, IID, MID, score):
        try:
            # 評分訂單
            # 先找出廠商
            sql = "SELECT OID1 FROM `orel` WHERE `OID2` = %s AND `Type` = 1;"
            values = (IID,)
            self.cur.execute(sql, values)
            merch_id = self.cur.fetchone()[0]

            # print(result[0])
            # 先確認是否已經評分過
            sql = "SELECT * FROM `orel` WHERE `OID1` = %s AND `OID2` = %s  AND `State` = %s AND `Type` = 3;"
            values = (MID, merch_id, IID)
            self.cur.execute(sql, values)
            result = self.cur.fetchone()
            print(result)
            if result != None:
                return False
            else:
                # 進行評分
                sql = "INSERT INTO `orel` (OID1, OID2, Type, Since, Content, State) VALUES (%s, %s, 3, %s, %s, %s);"
                values = (MID, merch_id, datetime.datetime.now(), score, IID)
                self.cur.execute(sql, values)
                self.conn.commit()
                return True

        except Exception as e:
            print(f"Error scoring order: {e}")
            

class MerchantModel:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def show_items(self, MID):
        try:
            # 顯示此商家所有訂單
            sql = "SELECT O.OID2, I.Name, I.Description, I.Price \
                    FROM orel AS O, item AS I \
                    WHERE O.OID1 = %s AND O.OID2 = I.IID AND O.Type = 1;"
            values = (MID,)
            
            self.cur.execute(sql, values)
            result = self.cur.fetchall()
            # print(result)
            # prds = []                             
            # for data in result:
            #     prds.append(data)
            return result

        except Exception as e:
            print(f"Error showing order: {e}")

    def add_product(self, MID, Name, Description, price):
        """
        新增新的產品到資料庫中。
        """
        try:
            sql = "INSERT INTO `Item` (Name, Description, Price) VALUES (%s, %s, %s);"
            values = (Name, Description, price)
            self.cur.execute(sql, values)
            self.conn.commit()

            last_id = self.cur.lastrowid

            sql = "INSERT INTO `orel` (OID1, OID2, Type, Since) VALUES (%s, %s, 1, %s)"
            values = (MID, last_id, datetime.datetime.now())
            self.cur.execute(sql, values)
            self.conn.commit()

            return True
        except Exception as e:
            print(f"Error adding product: {e}")

    def delete_product(self, MID, IID):
        """
        從資料庫中刪除產品。
        """
        try:
            # 確認是否有被加進購物車或訂單
            sql = "SELECT * FROM `orel` WHERE `OID2` = %s AND (`Type` = 2 OR `Type` = 4);"
            values = (IID,)
            self.cur.execute(sql, values)
            result = self.cur.fetchone()
            # print(result)
            if result != None:
                return False
            else:
                # 先找出要刪除的ID 刪除orel中的資料跟item中的資料
                sql = "DELETE FROM `orel` WHERE `OID1` = %s AND `OID2` = %s AND `Type` = 1;"
                values = (MID, IID)
                self.cur.execute(sql, values)
                self.conn.commit()

                sql = "DELETE FROM `Item` WHERE `IID` = %s;"
                values = (IID,)
                self.cur.execute(sql, values)
                self.conn.commit()
                return True
            
        except Exception as e:
            print(f"Error deleting product: {e}")

    def edit_product(self, IID, Name, Description, price):
        """
        編輯資料庫中的產品。
        """
        try:
            # 先找出要編輯的ID
            sql = "UPDATE `Item` SET `Name` = %s, `Description` = %s, `Price` = %s WHERE `IID` = %s;"
            values = (Name, Description, price, IID)
            self.cur.execute(sql, values)
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error editing product: {e}")
    
    def show_order_merchant(self, MID):
        try:
            # Find all orders with items purchased by customers who have ordered from the merchant
            sql = "SELECT O.OID1, O.OID2, O.Content, O.State, O.ORID \
                FROM orel AS O \
                INNER JOIN item AS I ON O.OID2 = I.IID \
                WHERE O.Type = 4 AND O.OID2 IN (SELECT OID2 FROM orel WHERE Type = 1 AND OID1 = %s);"
            values = (MID,)
            self.cur.execute(sql, values)
            result = self.cur.fetchall()
            # print(result)
            # Find the names of the customers

            object = []
            for data in result:
                self.cur.execute("SELECT Name FROM member WHERE Type = 1 AND MID = %s;", (data[0],))
                name = self.cur.fetchone()
                self.cur.execute("SELECT Name, Description, price FROM item WHERE IID = %s;", (data[1],))
                item = self.cur.fetchone()
                # print(name[0], item[0], item[1], item[2], data[2], data[3], data[4])
                object.append([name[0], item[0], item[1], item[2], data[2], data[3], data[4]])

            return object
        
        except Exception as e:
            print(f"Error finding orders with merchant items: {e}")

    def update_order_status(self, ORID, status):
        try:
            # Update the status of the order
            sql = "UPDATE orel SET State = %s WHERE ORID = %s;"
            values = (status, ORID)
            self.cur.execute(sql, values)
            self.conn.commit()
            return True
        
        except Exception as e:
            print(f"Error updating order status: {e}")

class LogisticModel:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def show_order_logistic(self):
        try:
            # Find all orders with items purchased by customers who have ordered from the merchant
            sql = "SELECT O.OID1, O.OID2, O.Content, O.State, O.ORID \
                FROM orel AS O \
                INNER JOIN item AS I ON O.OID2 = I.IID \
                WHERE O.Type = 4 AND O.State = 3;"
            self.cur.execute(sql)
            result = self.cur.fetchall()
            # print(result)
            # Find the names of the customers

            object = []
            for data in result:
                self.cur.execute("SELECT Name FROM member WHERE Type = 1 AND MID = %s;", (data[0],))
                name = self.cur.fetchone()
                self.cur.execute("SELECT Name, Description, price FROM item WHERE IID = %s;", (data[1],))
                item = self.cur.fetchone()
                # print(name[0], item[0], item[1], item[2], data[2], data[3], data[4])
                object.append([name[0], item[0], item[1], item[2], data[2], data[3], data[4]])

            return object
        
        except Exception as e:
            print(f"Error finding orders with merchant items: {e}")

    def update_order_status(self, ORID):
        try:
            # Update the status of the order
            sql = "UPDATE orel SET State = 4 WHERE ORID = %s;"
            values = (ORID, )
            self.cur.execute(sql, values)
            self.conn.commit()
            return True
        
        except Exception as e:
            print(f"Error updating order status: {e}")



'''#use for debug
from db import conn, cur
c = CustomerModel(conn, cur)
r = c.shopping_cart()

a = CustomerModel(conn, cur)
r2 = a.subtract_from_cart(1)
print(r2)
'''










'''
            self.cur.execute("SET SQL_SAFE_UPDATES = 0;")
            self.cur.execute("DELETE FROM settlement;")
            self.cur.execute("SET SQL_SAFE_UPDATES = 1;")

            self.cur.execute("SELECT `unit_quantity`, `one_price` FROM customer;")
            result = self.cur.fetchall()

            sql = "INSERT INTO `customer` (quantity, price) VALUES(%s, %s);"   #It won't actually be used here, maybe for inspection.
            values = (quantity, price)
            self.cur.execute(sql, values)
            self.conn.commit()
'''





'''
在 add_to_cart 和 delete_from_cart 方法中，可以使用 ON DUPLICATE KEY UPDATE 來實現一個 SQL 查詢，這樣可以更有效地處理相同商品的添加和刪除。這需要在 customer 表上添加一個唯一索引（Unique Key）。


def add_to_cart(self, prdID):
    try:
        sql = "INSERT INTO `customer` (c_id, c_name, one_price, unit_quantity) VALUES (%s, %s, %s, 1) ON DUPLICATE KEY UPDATE unit_quantity = unit_quantity + 1;"
        self.cur.execute(sql, (prdID, prdN, prdP))
        self.conn.commit()
        return True
    except Exception as e:
        print(f"Error adding to cart: {e}")

def delete_from_cart(self, prdID):
    try:
        sql = "UPDATE `customer` SET `unit_quantity` = `unit_quantity` - 1 WHERE `c_id` = %s AND `unit_quantity` > 1;"
        self.cur.execute(sql, (prdID,))
        self.conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting from cart: {e}")

'''













