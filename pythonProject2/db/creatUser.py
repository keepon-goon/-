from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['education']
collection = db['educationUser']

users_data =[
    {
        'username':'student1',
        'password':'student1',
        'email':'studentEmail1',
        'roles':'学生',
    },
    {
        'username':'teacher1',
        'password':'teacher1',
        'email':'teacherEmail1',
        'roles':'教师',
    },
    {
        'username':'manager1',
        'password':'manager1',
        'email':'managerEmail1',
        'roles':'管理',
    }
]

results = collection.insert_many(users_data)
