import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

# Find the ids that send out page rank - we only are interested
# in pages in the SCC that have in and out links
cur.execute('''SELECT DISTINCT from_id FROM Links''')		#throwing out the duplicates
from_ids = list()
for row in cur:
    from_ids.append(row[0])
    
#find the ids that receive page rank
to_ids = list()
links = list()
cur.execute('''SELECT DISTINCT from_id, to_id FROM Links''')
for row in cur:
		from_id = row[0]
		to_id = row[1]
		if from_id == to_id : continue		#if from_id is the same as to_id we are not interested
		if from_id not in from_ids : continue
		if to_id not in from_ids : continue			#skip if the link points to nowhere or points to a page that is not yet retrieved
		links.append(row)									#this is a filter on the from_ids and to_ids from the links table containing only the links we ahve already retrieved
		if to_id not in to_ids : to_ids.append(to_id)

# Get latest page ranks for strongly connected component
#strongly connected component, meaning any of these ids there is a path from every id to every other id
prev_ranks = dict()
for node in from_ids:
    cur.execute('''SELECT new_rank FROM Pages WHERE id=?''', (node, ))
    row = cur.fetchone()
    prev_ranks[node] = row[0]			#a dict based on id, the primary key, which is what node is. so we are takikng
																	#the new_rank's number and sticking it into a dict based on the primary key
																	#so will have a dict with new_id mapped to id
sval = input('How many iterations: ')
many = 1
if (len(sval) > 0) : many = int(sval)

#sanity check
if len(prev_ranks) < 1 :			#if no values then it is bad
		print('Nothing to page rank. Check data')
		quit()

#let's do page rank in memory so it is really fast

for i in range(many) :
		#print prev_ranks.items()[:5]
		next_ranks = dict()
		total = 0.0
		for (node, old_rank) in list(prev_ranks.items()) :			#going to loop thru the previous ranks
				total = total + old_rank
				next_ranks[node] = 0.0
		#print total

		#find the number of outbound links and set the page rank down each
		for (node, old_rank) in list (prev_ranks.items()) :
				#print node, old_rank
				give_ids = list()
				for (from_id, to_id) in links:
						if from_id != node : continue
						#print '  ', from_id, to_id
						if to_id not in to_ids : continue
						give_ids.append(to_id)						#give_ids are the ids that node is going to share its goodness
				if (len(give_ids) < 1) : continue
				amount = old_rank / len(give_ids)			#amount is how much goodness are we going to float outbound based on our previous rank
																							#of this particular node (old_rank) and the number of outbound links we have (give_ids)
				#print node, old_rank, amount, give_ids

				for id in give_ids:
						next_ranks[id] = next_ranks[id] + amount
		
		newtot = 0
		for (node, next_rank) in list(next_ranks.items()):
				newtot = newtot + next_rank
		evap = (total - newtot) / len(next_ranks)		#evaporation= (noun)- in PageRank algorithms, some or all of a ducumnet's PageRank may be distributed to the rest of the documents in the collection.
																								#happens when links have a nofollow attribute

		#print newtot, evap
		for node in next_ranks:
				next_ranks[node] = next_ranks[node] + evap

		newtot = 0
		for (node, next_rank) in list(next_ranks.items()):
				newtot = newtot + next_rank
		
		#compute the per-page averagve change from old rank to new rank (the difference)
		#as indicaiton of convergence of the algorithm
		totdiff = 0
		for (node, old_rank) in list(prev_ranks.items()):
				new_rank = next_ranks[node]
				diff = abs(old_rank-new_rank)
				totdiff = totdiff + diff
		
		avgdiff = totdiff / len(prev_ranks)
		print(i+1, avgdiff)

		#rotate, or take the new ranks and make them the old ranks
		prev_ranks = next_ranks

#put the final ranks back into the database;  updating all the rankings so they have a new rank
print(list(next_ranks.items())[:5])
cur.execute('''UPDATE Pages SET old_rank=new_rank''')
for (id, new_rank) in list(next_ranks.items()):
		cur.execute('''UPDATE Pages SET new_rank=? WHERE id=?''', (new_rank, id))
conn.commit()
cur.close()