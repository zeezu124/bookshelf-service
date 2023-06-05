from django.shortcuts import render
from pymongo import MongoClient
import environ

env = environ.Env()
environ.Env.read_env()

connect_string = env('DATABASE_URL')
my_client = MongoClient(connect_string)

#Check if env db_name exists
try:
    env.get_value('DATABASE_NAME')
    db_name = env('DATABASE_NAME')
    dbname = my_client[db_name]
    collection_name = dbname['books_library']
    print(db_name)
except:
    db_name = 'main'
    dbname = my_client[db_name]
    print(db_name)
    collection_name = dbname['libraries']
    

"""
#For testing
dbname = my_client['test_lib']
collection_name = dbname['libraries']
"""


from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import LibrarySerializer, BookSerializer

# Create your views here.

#Display welcome page
def welcome_page(request):
    return render(request, 'welcome.html')

class LibraryViewSet(viewsets.ViewSet):
    #Lists all books for a user
    def list(self, request, user): # /api/books/<str:user>
        books = collection_name.find({"username": user})
        serializer = LibrarySerializer(books, many=True)
        return Response(serializer.data)

    #Stores a new book for a user
    def create(self, request, user): # /api/books/<str:user>
        
        books = collection_name.find({"username": user})
        library_serializer = LibrarySerializer(books, many=True)
        
        book_serializer = BookSerializer(data=request.data)
        book_serializer.is_valid(True)        
        book_id = book_serializer.data['book_id']
        
        #Checks if user exists
        if library_serializer.data != []:
            
            #Check if book exists
            result = collection_name.find({ 
                "username": user,
                "book_ids": { "$in": [book_id]}
                })
            
            if LibrarySerializer(result, many=True).data != []:
                return Response("Book already exists in library", status=status.HTTP_405_METHOD_NOT_ALLOWED)

            collection_name.update({"username": user}, { "$push": {"book_ids": book_id}})
            return Response(book_serializer.data, status=status.HTTP_201_CREATED)
        
        #Checks if library collection is empty
        if LibrarySerializer(collection_name.find(), many=True).data != []:
            highest_id = collection_name.find_one(sort=[("id", -1)])["id"]
            
            entry = {
                "id": highest_id + 1,
                "username": user, 
                "book_ids": [book_id]
                }

            #Creates library with book for current user
            collection_name.insert_one(entry)
            
            return Response(book_serializer.data, status=status.HTTP_201_CREATED)
        
        #Creates new base user and adds book to library
        entry = {
                "id": 1001,
                "username": user, 
                "book_ids": [book_id]
                }

        collection_name.insert_one(entry)
        return Response(book_serializer.data, status=status.HTTP_201_CREATED)
    

    #Retrieves a specific book from a user's library
    def retrieve(self, request, user, b_id): # /api/books/<str:user>/<str:b_id>
         #Check if book exists
        result = collection_name.find({ 
            "username": user,
            "book_ids": { "$in": [b_id]}
            })
        
        serializer = LibrarySerializer(result, many=True)    
        
        if serializer.data != []:
            return Response(serializer.data)

        return Response("Book does not exist in library", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    
    #Deletes a book for a user's library
    def destroy(self, request, user, b_id): # /api/books/<str:user>/<str:b_id>
        #Check if book exists
        result = collection_name.find({ 
            "username": user,
            "book_ids": { "$in": [b_id]}
            })
            
        if LibrarySerializer(result, many=True).data == []:
            return Response("Book does not exist in library", status=status.HTTP_405_METHOD_NOT_ALLOWED)

        collection_name.update({"username": user}, { "$pull": {"book_ids": b_id}})
        return Response("Deleted " + b_id ,status=status.HTTP_204_NO_CONTENT)