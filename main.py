import authGoogle
import authNebim
import orderStores
import orderWholesale
import products
import schedule
import time

sessionID = authNebim.main()
client = authGoogle.main()
orderStores.main(sessionID, client)
orderWholesale.main(sessionID, client)
products.main(sessionID, client)

schedule.every().day.at("03:00").do(products.main, client = client, sessionID = sessionID)
schedule.every().hour.do(orderWholesale.main, client = client, sessionID = sessionID)
schedule.every().hour.do(orderStores.main, client = client, sessionID = sessionID)
print("scheduled")

while True:
    schedule.run_pending()
    time.sleep(60)
