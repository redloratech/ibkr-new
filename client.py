from http import client
import time
from main import ApiWrapper
from queue import Queue
 
# Initializing a queue
q = Queue(maxsize = 1)


client = ApiWrapper(queue=q)
client.reqAccountSummary(6, "All", "AccountType")

while not client.response:
    time.sleep(1)
print(client.response)
    


