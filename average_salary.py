import pymongo
import numpy as np

mongo_host = "localhost"
mongo_port = 27017
mongo_db_name = "job_data"
mongo_collection_name = "jobs"
city_name = "Noida, Uttar Pradesh"  
query = {"location": city_name}
client = pymongo.MongoClient(mongo_host, mongo_port)
db = client[mongo_db_name]
collection = db[mongo_collection_name]
cursor = collection.find(query)
salaries = np.array([job["salary"] for job in cursor if job["salary"] is not None])
average_salary = np.mean(salaries)
print(f"Average salary for Python developers in {city_name}: Rs{average_salary:.2f}")
client.close()
