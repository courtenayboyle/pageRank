import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

#showing the number of links, ordering by inbound links desc (so we see the most linked things)
cur.execute('''SELECT COUNT(from_id) AS inbound, old_rank, new_rank, id, url
		FROM Pages JOIN Links ON Pages.id = Links.to_id
    WHERE html IS NOT NULL
    GROUP BY id ORDER BY inbound DESC''')

count = 0
for row in cur:
		if count < 50 : print(row)		#showing top 50 only
		count = count + 1
print(count, 'rows.')
cur.close()