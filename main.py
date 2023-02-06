import psycopg2

db = "clientdb"
user = "postgres"
pw = "03051997"
with psycopg2.connect(database=db, user=user, password=pw) as conn:
    with conn.cursor() as cur:
        def create_structure():

                cur.execute("""create table if not exists client_info(
                        client_id serial primary key,
                        first_name varchar(40),
                        second_name varchar(40),
                        email varchar(40));""")

                cur.execute("""create table if not exists number_phone(
                        phone_id serial,
                        client_id integer references client_info(client_id),
                        number varchar(40));""")


                conn.commit()
                print("Структура базы данных создана")

        def add_client(fname,sname,email):

            cur.execute(""" insert into client_info(first_name, second_name, email)
            values (%s,%s,%s);""", (fname,sname,email))
            conn.commit()
            print("Клиент добавлен в БД")

        def add_phone(fname,sname,num):

            cur.execute(""" select client_id from client_info
            where first_name = %s and second_name = %s;""", (fname,sname))
            cl_id = cur.fetchone()[0]
            cur.execute("""insert into number_phone(client_id,number)
            values(%s, %s);""",(cl_id, num))
            print("Номер телефона добавлен")
            conn.commit()

        def edit_info(fname, sname, fname2, sname2, email2):

            cur.execute("""select client_id from client_info
            where first_name = %s and second_name = %s;""",(fname,sname))
            cl_id = cur.fetchone()[0]
            print(cl_id)
            if fname2 != "-":
                cur.execute("""update client_info 
                set first_name = %s
                where client_id = %s;""", (fname2,cl_id))
            if sname2 != "-":
                cur.execute("""update client_info 
                set second_name = %s
                where client_id = %s;""", (sname2,cl_id))
            if email2 != "-":
                cur.execute("""update client_info 
                set email = %s
                where client_id = %s;""", (email2,cl_id))
            print("Данные обновлены")
            conn.commit()

        def finde_for(fname, sname):
            cur.execute("""select client_info.client_id, client_info.first_name, 
            client_info.second_name, number_phone.phone_id, number_phone.number from client_info
            left join number_phone on client_info.client_id = number_phone.client_id
            where client_info.first_name = %s and client_info.second_name = %s;""", (fname, sname))
            info = cur.fetchall()
            print(info)
        def del_phone(ph_id):

            cur.execute("""
            delete from number_phone
            where phone_id = %s;""", (ph_id,))
            conn.commit()
            print("Номер удален")

        def del_client(fname,sname):

            cur.execute("""select client_info.client_id, client_info.first_name, 
            client_info.second_name, number_phone.phone_id, number_phone.number from client_info
            left join number_phone on client_info.client_id = number_phone.client_id
            where client_info.first_name = %s and client_info.second_name = %s;""", (fname, sname))
            info = cur.fetchall()
            cl_id = info[0][0]
            ph_ids = [i[3] for i in info]
            cur.execute("""delete from number_phone
            where client_id = %s;
            delete from client_info
            where client_id = %s;""",(cl_id,cl_id))
            conn.commit()
            print("Клиент удален")
        def find_client(str):

            cur.execute("""select client_info.client_id, client_info.first_name,
            client_info.second_name, number_phone.phone_id, number_phone.number from client_info
            left join number_phone on client_info.client_id = number_phone.client_id
            where client_info.first_name = %s or client_info.second_name = %s or client_info.email = %s or number_phone.number = %s;""", (str,str,str,str))
            clients = cur.fetchall()
            print(clients)

    # with conn.cursor() as cur:
    #     cur.execute("""
    #     drop table number_phone;
    #     drop table client_info;""")
    #     conn.commit()

        print("Управление БД:\n1.Создать структуру БД\n2.Добавить клиента\n"
              "3.Добавить телефон\n4.Редактировать информацию о клиенте\n5.Удалить телефон\n6.Удалить клиента\n7.Найти клиента\n8.Остановить")
        comands = {1:create_structure,2:add_client,3:add_phone,4:edit_info,5:del_phone,6:del_client,7:find_client}
        while True:
            comand = int(input("Введите команду >>>"))
            if comand == 1:
                comands[comand]()
            if comand == 2:
                fname = str(input("Ведите имя")).title()
                sname = str(input("Введите фамилию")).title()
                email = str(input("Введите email")).title()
                comands[comand](fname,sname,email)
            if comand == 3:
                fname = str(input("Ведите имя")).title()
                sname = str(input("Введите фамилию")).title()
                num = str(input("Введите номер телефона")).title()
                comands[comand](fname, sname, num)
            if comand == 4:
                print("Поиск клиента")
                fname = str(input("Введите имя")).title()
                print("Поиск клиента")
                sname = str(input("Введите фамилию")).title()
                print("Обновление данных о клиенте. Для пропуска введите '-'")
                fname2 = str(input("Имя")).title()
                print("Обновление данных о клиенте. Для пропуска введите '-'")
                sname2 = str(input("Фамилия")).title()
                print("Обновление данных о клиенте. Для пропуска введите '-'")
                email2 = str(input("Email"))
                comands[comand](fname, sname, fname2, sname2, email2)
            if comand == 5:
                print("Поиск клиента")
                fname = str(input("Введите имя")).title()
                print("Поиск клиента")
                sname = str(input("Введите фамилию")).title()
                finde_for(fname,sname)
                ph_id = int(input("Введите ID номера, который хотите удалить"))
                comands[comand](ph_id)
            if comand == 6:
                print("Поиск клиента")
                fname = str(input("Введите имя")).title()
                print("Поиск клиента")
                sname = str(input("Введите фамилию")).title()
                comands[comand](fname, sname)
            if comand == 7:
                str = input("Введите имя, фамилию, email или номер клиента").title()
                comands[comand](str)



