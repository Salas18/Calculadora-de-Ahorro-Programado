import psycopg2

connection = psycopg2.connect(database="calculadora_ahorro_programado",
user="calculadora_ahorro_programado_user", password="orYqASYvNI0zNzx5GOARh2Rk7qtFsukV",
host="dpg-d7ln3p3eo5us73don7hg-a.virginia-postgres.render.com", port ="5432")

cursor = connection.cursor()

nombre_municipio = input("Ingrese el nombre del municipio: ")

cursor.execute("SELECT codigo_departamento FROM public.municipios where nombre_municipio like '%{nombre_municipio}%'".format(nombre_municipio=nombre_municipio))
departamento = cursor.fetchall()

cursor.execute("SELECT nombre_departamento FROM public.departamentos where codigo_departamento like '{departamento}'".format(departamento=departamento[0][0]))
nombre_departamento = cursor.fetchall()

print("Resultados: ", nombre_departamento)

