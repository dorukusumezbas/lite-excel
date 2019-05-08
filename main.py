import authGoogle
import authNebim
import orderStores
import orderWholesale
import products

sessionID = authNebim.main()
client = authGoogle.main()
orderStores.main(sessionID, client)
orderWholesale.main(sessionID, client)
products.main(sessionID, client)
