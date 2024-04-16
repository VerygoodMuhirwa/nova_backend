import pymongo
# url= 'mongodb+srv://VerygoodMuhirwa:Verygood@cluster0.c5iqqff.mongodb.net/'
url = 'mongodb://localhost:27017'
client = pymongo.MongoClient(url)
db = client['nova_project']