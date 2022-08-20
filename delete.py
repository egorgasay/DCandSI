from colorama import init, Fore
from colorama import Back
from colorama import Style


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
                cur.execute(f'''DROP TABLE {self.table_name}''')
            except Exception as e:
                cur.execute("rollback")
                print(
                    Fore.RED + f"Deleting table {self.table_name} wasn't completed successfully!")
                input(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
                return 0
            con.commit()
            input(f"DROP TABLE {self.table_name} was completed successfully!")
        else:
            input(Fore.RED + "The names of the tables do not match!" + Style.RESET_ALL)
