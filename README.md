'''
ICompass Assignment: Jwala Kompalli

Here is a simple Flask API where we can send CRUD requests to a database which has information about various products.

I took the liberty of changing the json response if the input payload doesn't have any characters that is pertaining to the SQL Injection attacks. 
We will simply get a dump of products inside the database instead of 'sanitized' response!

We can also access single products from the data base and I implemented another sanitization check there to see if the input is sanitized or not.

I have used the Flask, SQLALchemy and Marshmallow libraries to implement the below API
