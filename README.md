# flask-graphql
### Python 3.6.9

1. git clone https://github.com/PauloDuarte43/flask-graphql.git
2. pip install -r requirements.txt
3. python initdb.py
4. python app.py runserver
5. open http://localhost:5000/graphql
6. execute query:
```
query {
  allCustomers {
    edges {
      node {
        id
        name
        lastName
      }
    }
  }
}
```
7. execute query:
```
query {
  allAddresses {
    edges {
      node {
        id
        street
        district
        number
      }
    }
  }
}
```
