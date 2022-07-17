class Deletor:
    """ 
    To delete tables
    """

    def __init__(self, table_name):
        self.table_name = table_name

    def base_method(self, con):
        cur = con.cursor()
        print(
            f"Confirm deleting the {self.table_name}. Enter the database name.")
        decision = input("SQL: DROP TABLE ")
        if decision == self.table_name:
            try:
                cur.execute(f'''DROP TABLE IF EXISTS {self.table_name}''')
            except:
                cur.execute("rollback")
            con.commit()
            print(f"DROP TABLE {self.table_name} was completed successfully!")
        else:
            input("The names of the tables do not match!")
