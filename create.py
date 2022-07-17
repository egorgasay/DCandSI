from clear_screen import clear
from functions import *


class Creator:
    """ 
    To create tables
    """
    def type_finder(x):
        """ 
        Type finder
        """
        try:
            if x == True or x == False:
                return 'bool'
            int(x)
            return 'int'
        except ValueError:
            try:
                float(x)
                return 'float'
            except ValueError:
                if x.lower().startswith('enum'):
                    return 'enum'
                elif x.lower().startswith('set'):
                    return 'set'
                return 'str'

    def base_method(self, con):
        cur = con.cursor()
        table_name = input("Table name: ")

        def create_and_fill(table_name):
            temp_data_of_columns, temp_data_of_columnsArray, count_of_columns = create_only(
                table_name)
            temp_data_of_lines = []
            count_of_lines = int(input("Count of lines: "))
            temp_data_of_linesStringStorage = ''
            temp_data_of_columnsArrayFull = temp_data_of_columns.split(', ')
            try:
                ignore_list = []
                for j in range(1, count_of_lines + 1):
                    for x in range(1, count_of_columns + 1):
                        if 'primary key' not in temp_data_of_columnsArrayFull[x - 1].lower():
                            # todo: сделать обработку неправильного ввода, например когда забыли ввести INT
                            item = input(
                                f"line:{j} item:{temp_data_of_columnsArray[x-1]} > ")
                            item = item.split()
                            item_type = Creator.type_finder(item[0])

                            def if_item_is_null(item, temp_data_of_columnsArray, temp_data_of_columnsArrayFull):
                                if 'null' in item or 'Null' in item or 'NULL' in item:
                                    if 'not null' not in temp_data_of_columnsArrayFull[x - 1].lower():
                                        item = None
                                        return item
                                    print(
                                        f"item:{temp_data_of_columnsArray[x-1]} can't be null")
                                    item = input(
                                        f"line:{j} item:{temp_data_of_columnsArray[x-1]} > ")
                                    if 'null' in item.lower():
                                        return if_item_is_null(item, temp_data_of_columnsArray,
                                                               temp_data_of_columnsArrayFull)
                                    else:
                                        return item
                                else:
                                    return item
                            item = if_item_is_null(
                                item, temp_data_of_columnsArray, temp_data_of_columnsArrayFull)
                            if item_type == 'int' or item_type == 'float':
                                temp_data_of_linesStringStorage += item[0] + ', '
                            else:
                                if item is None:
                                    temp_data_of_linesStringStorage += 'NULL' + ', '
                                else:
                                    temp_data_of_linesStringStorage += '\'' + \
                                        item[0] + '\'' + ', '
                        else:
                            ignore_list.append(
                                temp_data_of_columnsArrayFull[x - 1])

                    temp_data_of_lines.append(temp_data_of_linesStringStorage)

                    temp_data_of_linesStringStorage = ''
            except Exception as e:
                print(e)
                input("Back to main menu")
                return 0
            try:
                ignore_list = list(set(ignore_list))
                temp_data_of_columns_ready = ''
                temp_data_of_linesStringStorage2 = ''
                for counter in range(len(ignore_list)):
                    ignore_list = (" ").join(ignore_list)
                    print(temp_data_of_columnsArray[counter], ignore_list)
                    if temp_data_of_columnsArray[counter] in ignore_list:
                        temp_data_of_columnsArray.pop(counter)
                temp_data_of_columns_ready = ", ".join(
                    temp_data_of_columnsArray)
                for j in range(count_of_lines):
                    temp_data_of_linesStringStorage2 = temp_data_of_lines[j]
                    try:
                        cur.execute(f'''INSERT INTO {table_name} ({temp_data_of_columns_ready})
                        VALUES ({temp_data_of_linesStringStorage2[:-2]})''')
                    except Exception as e:
                        cur.execute("rollback")
                        print(e)
                        input('Something went wrong while inserting lines..')
                        clear()
                        return 0
                con.commit()
                print("Success!")
                try:
                    cur.execute(f'''SELECT * FROM {table_name}''')
                except:
                    cur.execute("rollback")
                query_output_logic(cur.fetchall(), cur.description)
                input("Back to main menu")
                clear()
                return 0
            except Exception as e:
                print(e)
                input("Back to main menu")
                return 0

        def create_only(table_name):
            temp_data_of_columns = ''
            temp_data_of_columnsArray = []
            temp_data_of_columnsArrayFull = []
            count_of_columns = int(input("Count of columns: "))
            print("Example: ID SERIAL PRIMARY KEY")
            for i in range(1, count_of_columns + 1):
                columns = input(f"column:{i} : ")
                temp_data_of_columnsArray.append(columns.split()[0])
                temp_data_of_columnsArrayFull.append(columns.split())
                temp_data_of_columns += columns + ", "
                temp_data_of_columns = temp_data_of_columns.strip('\n')
            try:
                # For MYSQL in the future
                # if 'auto_increment' not in temp_data_of_columns.lower():
                cur.execute(
                    f'''CREATE TABLE {table_name} ({temp_data_of_columns[:-2]})''')
                # else:
                #    cur.execute(f'''CREATE TABLE {table_name}
                #    ({temp_data_of_columns[:-2]+"PRIMARY KEY ({})"})''')
                con.commit()
                # if 'SERIAL PRIMARY KEY' in temp_data_of_columnsArrayFull:
                #     for counter in range(temp_data_of_columnsArrayFull.count("SERIAL PRIMARY KEY")):
                #         temp_data_of_columnsArrayFull.index(value)
                print("Success!")
                # if temp_data_of_columns
                input("Next")
                clear()
            except Exception as e:
                cur.execute("rollback")
                print(e)
                input('Something went wrong while creating table..')
                clear()
                return 0

            return temp_data_of_columns, temp_data_of_columnsArray, count_of_columns

        decision = input(
            f"Do you want to add some data in {table_name}? (Y/n) n - default :")
        if decision.lower() == 'y':
            create_and_fill(table_name)
        else:
            create_only(table_name)
            return 0
