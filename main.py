from Input_pip import Query
from Generation import *
import pandas as pd
# You should run retrivalDB.py first if your database is not established locally.
# You should also run faiss_index.py if your wiki_faiss.index is not created
# Then you could run this file
print('************* System Checking *******************')

greeting = 'Hey there! This is MemePyscho. I\'d love to help you to learn yourself better! Please describe your feelings with scenarios and we will figure out!\n'

query = input(greeting)
#query = "There are times where it honest to god feels like I'm trapped inside of a cage in my own head and someone else is at the controls. I should clean the house today, nope. I could just get up right now, and pick up the swiffer, nope. Maybe just dust th- nope. Then it's midnight and nothing has gotten done all day and you fucking hate yourself."
print('-------------------------------------------------------------')

candidates = Query.generate_candidate(query, 5)

# check candidates
# for topic in candidates.keys():
#    print(topic)

print('-------------------------------------------------------------')
follwup = followup_agent(query,candidates)
print(follwup)
#follow = 'yes'
# I dont find myself have repetitive and unwanted thoughts. I have a good sleep patterns, and without any issues. But I do have involuntary movements like I shake my legs a lot. I feel energtic during the day but just having hard time focusing.
follow = input()
votes  = vote_for_results(candidates,query, follwup, follow )
agent, diagosis  = select_agent(votes)

# check which agent is selected
print(f'{agent} steps in!')
final_agent(agent,diagosis, candidates, query, follwup, follow)

print('------------------------- Final Reponse ---------------------------------')

