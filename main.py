import sys
sys.path.insert(0,'/Projects/lite-excel/')
import authGoogle
import authNebim
import orderStores
import orderWholesale
import products
import datetime



def main():
    sessionID = authNebim.main()
    client = authGoogle.main()
    orderStores.main(sessionID, client)
    orderWholesale.main(sessionID, client)
    products.main(sessionID, client)
print(datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S"))
main()
print(datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S") + " ended")