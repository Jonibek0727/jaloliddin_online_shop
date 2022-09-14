import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE all_users (
            id int NOT NULL,
            name varchar(95) NOT NULL,
            date_of_start date,
            
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)
        
    
    def create_table_reg_users(self):
        sql = """
        CREATE TABLE reg_users(
            id int NOT NULL,
            name varchar(95) ,
            phone varchar(20) ,
            adress varchar(250) ,
            location varchar(250),
            lan varchar(10) ,
            status int,
            
            date_of_start date,
            
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)


    def create_table_products(self):
        sql = """
        CREATE TABLE all_products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name varchar(155) ,
            caption varchar(200) ,
            price int ,
            category varchar(150) ,
            subcategory varchar(150) ,
            photo_url varchar(255),
            date_of_start date
            
            );
"""
        self.execute(sql, commit=True)
        
        
        
    def create_table_sells(self):
        sql = """
        CREATE TABLE sells_table(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id int ,
            pro_id int
            
            );
"""
        self.execute(sql, commit=True)
        
        
        
    def create_table_sell_products(self):
        sql = """
        CREATE TABLE sells_products_table(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id int ,
            products varchar(750),
            check_no varchar(250),
            date date
            
            );
"""
        self.execute(sql, commit=True)
        
        
        
        
    def create_table_sevimlilar(self):
        sql = """
        CREATE TABLE sevimlilar_table(
            
            user_id int ,
            pro_id int PRIMARY KEY      
            
            );
"""
        self.execute(sql, commit=True)
        
        
        
        
        
        
        
        
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int,  name: str,  date_of_start: str ):
        # SQL_EXAMPLE = "INSERT INTO all_users(id, Name, tabrik_ism) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO all_users(id, name, date_of_start) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, date_of_start), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM all_users
        """
        return self.execute(sql, fetchall=True)





    def add_reg_user(self, id: int,  name: str, phone: str, adress: str, lan:str, status:int,  date_of_start: str ):
        # SQL_EXAMPLE = "INSERT INTO all_users(id, Name, tabrik_ism) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO reg_users(id, name, phone, adress, lan, status,  date_of_start) VALUES(?, ?, ?,?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, phone, adress, lan, status,  date_of_start), commit=True)


    def select_user(self,  id: int, d:int):
        sql = """
        SELECT * FROM reg_users where id=? and id=?
        """
        return self.execute(sql, parameters=(id, d), fetchone=True)




    def update_user_info(self,  name: str, phone: str, adress: str, id:int):
        # SQL_EXAMPLE = "UPDATE Users SET tabrik_ism=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE reg_users SET name=?, phone = ?, adress=? WHERE id=?
        """
        return self.execute(sql, parameters=(name, phone, adress,  id), commit=True)


    def update_user_lan(self,  lan: str, id:int):
        # SQL_EXAMPLE = "UPDATE Users SET tabrik_ism=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE reg_users SET lan=? WHERE id=?
        """
        return self.execute(sql, parameters=(lan,  id), commit=True)



    def add_product(self,   name: str, caption: str, price: int, category: str,  subcategory: str, photo_url: str, date_of_start: str ):
      
        sql = """
        INSERT INTO all_products( name, caption, price, category,  subcategory, photo_url, date_of_start) VALUES( ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=( name, caption, price, category, subcategory, photo_url, date_of_start), commit=True)


    def select_product(self,  id: int, d:int):
        sql = """
        SELECT * FROM all_products where id=? and id=?
        """
        return self.execute(sql, parameters=(id, d), fetchone=True)

    def select_all_product(self):
        sql = """
        SELECT * FROM all_products 
        """
        return self.execute(sql, fetchall=True)
    
    def edit_product_name(self, name, id):
        # SQL_EXAMPLE = "UPDATE Users SET tabrik_ism=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE all_products SET name=? WHERE id=?
        """
        print("name ozgartilrildi")
        return self.execute(sql, parameters=(name, id), commit=True)


    def edit_product_desc(self, desc, id):
        # SQL_EXAMPLE = "UPDATE Users SET tabrik_ism=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE all_products SET caption=? WHERE id=?
        """
        return self.execute(sql, parameters=(desc, id), commit=True)

    def edit_product_price(self, price, id):
        # SQL_EXAMPLE = "UPDATE Users SET tabrik_ism=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE all_products SET price=? WHERE id=?
        """
        return self.execute(sql, parameters=(price, id), commit=True)

    def edit_product_photo_url(self, photo_url, id):
        # SQL_EXAMPLE = "UPDATE Users SET tabrik_ism=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE all_products SET photo_url=? WHERE id=?
        """
        return self.execute(sql, parameters=(photo_url, id), commit=True)

    
    
    
    def select_product_category(self,  category:str, subcategory:str):
        sql = """
        SELECT * FROM all_products where category=? and subcategory=?
        """
        return self.execute(sql, parameters=(category, subcategory), fetchall=True)


    def delete_product(self,  id: int, d:int):
        sql = """
        DELETE FROM all_products WHERE id=? AND id=?
        """
        self.execute(sql, parameters=(id, d), commit=True)




    def add_sell_product(self,   user_id:int, pro_id: int):
      
        sql = """
        INSERT INTO sells_table( user_id, pro_id) VALUES( ?, ?)
        """
        self.execute(sql, parameters=(user_id, pro_id), commit=True)
        
        

    def select_sells_product(self,  id: int, d:int):
        sql = """
        SELECT * FROM sells_table where user_id=? and user_id=?
        """
        return self.execute(sql, parameters=(id, d), fetchall=True)



    def delete_sells_product(self,  user_id: int, pro_id:int):
        sql = """
        DELETE FROM sells_table WHERE user_id=? AND pro_id=?
        """
        self.execute(sql, parameters=(user_id, pro_id), commit=True)



    def delete_sells_all_product(self,  user_id: int, id:int):
        sql = """
        DELETE FROM sells_table WHERE user_id=? AND user_id=?
        """
        self.execute(sql, parameters=(user_id, id), commit=True)




    def add_sells_products(self,   user_id:int, products:str, check:str, date:str,):
      
        sql = """
        INSERT INTO sells_products_table( user_id, products, check_no, date ) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, products, check,  date), commit=True)
        


    def select_sells_product_check(self,  id: int, d:int):
        sql = """
        SELECT * FROM sells_products_table where user_id=? and user_id=?
        """
        return self.execute(sql, parameters=(id, d), fetchone=True)


    def update_sells_labelpriced(self, labelpriced, id):
        # SQL_EXAMPLE = "UPDATE Users SET tabrik_ism=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET labeledprices=? WHERE user_id=?
        """
        return self.execute(sql, parameters=(labeledprices, id), commit=True)


    def select_sells_labelpriced(self,  labeledprices: int, user_id:int):
        sql = """
        SELECT * FROM sells_table where labeledprices=? and user_id=?
        """
        return self.execute(sql, parameters=(labeledprices, user_id), fetchone=True)



    def add_sevimlilar(self, user_id: int, pro_id:int):
        # SQL_EXAMPLE = "INSERT INTO all_users(id, Name, tabrik_ism) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO sevimlilar_table(user_id, pro_id) VALUES(?, ?)
        """
        self.execute(sql, parameters=(user_id, pro_id), commit=True)


    def select_sevimlilar(self,  id: int, user_id:int):
        sql = """
        SELECT * FROM sevimlilar_table where user_id=? and user_id=?
        """
        return self.execute(sql, parameters=(id, user_id), fetchall=True)



    def delete_sevimlilar(self,  user_id: int, pro_id:int):
        sql = """
        DELETE FROM sevimlilar_table WHERE user_id=? AND pro_id=?
        """
        self.execute(sql, parameters=(user_id, pro_id), commit=True)




    # def select_user(self, id: int):
    #     # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
    #     sql = "SELECT * FROM Users WHERE "
    #     sql, parameters = self.format_args(sql, kwargs)

    #     return self.execute(sql, parameters=parameters, fetchone=True)

    # def select_check_sub(self):
    #     sql = """
    #     SELECT id FROM Users WHERE check_sub = 1
    #     """
    #     return self.execute(sql, fetchall=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_mintaqa(self, user_mintaqa, user_mintaqa_nomi, id):
        # SQL_EXAMPLE = "UPDATE Users SET tabrik_ism=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET user_mintaqa=?, user_mintaqa_nomi = ? WHERE id=?
        """
        return self.execute(sql, parameters=(user_mintaqa, user_mintaqa_nomi, id), commit=True)

    def update_check_sub(self, check_sub, id):
        # SQL_EXAMPLE = "UPDATE Users SET tabrik_ism=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET check_sub=? WHERE id=?
        """
        return self.execute(sql, parameters=(check_sub, id), commit=True)

    def update_user_tabrik_ism(self, tabrik_ism, id):
        # SQL_EXAMPLE = "UPDATE Users SET tabrik_ism=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET tabrik_ism=? WHERE id=?
        """
        return self.execute(sql, parameters=(tabrik_ism, id), commit=True)

    def update_user_tabrik_tr(self, tabrik_tr, id):
        # SQL_EXAMPLE = "UPDATE Users SET tabrik_tr=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET tabrik_tr=? WHERE id=?
        """
        return self.execute(sql, parameters=(tabrik_tr, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


def logger(statement):
    pass
#     print(f"""
# _____________________________________________________        
# Executing: 
# {statement}
# _____________________________________________________
# """)
