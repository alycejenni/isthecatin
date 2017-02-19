import psycopg2

conn = psycopg2.connect("postgres://uewjvsqepsqrra:4faf00aa89a3ed61d3119c2bc4261579533b246e70472a149de6b2a253779305@ec2-54-228-189-223.eu-west-1.compute.amazonaws.com:5432/dcjpp0f01kdbo9")
cur = conn.cursor()
cur.execute("select * from information_schema.columns;")
res = cur.fetchall()
print(res)
conn.close()