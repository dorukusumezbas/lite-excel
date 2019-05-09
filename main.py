import sys
sys.path.insert(0,'/home/ubuntu/projects/lite-excel')
import authGoogle
import authNebim
import orderStores
import orderWholesale
import products
import schedule
import time

def main():
    sessionID = authNebim.main()
    client = authGoogle.main()
    orderStores.main(sessionID, client)
    orderWholesale.main(sessionID, client)
    products.main(sessionID, client)

main()

while True:
    schedule.run_pending()
    time.sleep(60)
