import sys
sys.path.insert(0,'/home/ubuntu/projects/lite-excel')
import authGoogle
import authNebim
import orderStores
import orderWholesale
import products
import datetime

print(datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S"))

def main():
    sessionID = authNebim.main()
    client = authGoogle.main()
    orderStores.main(sessionID, client)
    orderWholesale.main(sessionID, client)
    products.main(sessionID, client)

print(datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S") + " ended")
main()