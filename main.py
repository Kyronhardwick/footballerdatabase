from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel
import os
from dotenv import load_dotenv, dotenv_values


dbpassword=os.environ.get('DB_PASSWORD')
dbhost=os.environ.get('DB_HOST')
dbuser=os.environ.get('DB_USER')
db=os.environ.get('DB')

# MySQL connection
mydb = mysql.connector.connect(
  host=dbhost,
  user=dbuser,
  password=dbpassword,
  database=db
)

myfirst=os.environ.get('DB_PASSWORD')
print(myfirst)
cursor = mydb.cursor()

app = FastAPI()

# Student Pydantic model
class Footballer(BaseModel):
    id:int
    firstname: str
    lastname:str
    age: int
   

# Get all students
@app.get("/footballers")
def get_footballers():
    cursor.execute("SELECT * FROM footballers")
    footballers = cursor.fetchall()
    print(myfirst)
    return {"students": footballers}

@app.get("/footballers/{id}")
def get_footballer_by_id(id:int):
    cursor.execute("SELECT * FROM footballers where id=%s",(id,))
    footballers = cursor.fetchone()
    return {"students": footballers}

@app.post("/footballers/")
def post_footballer(footballer:Footballer):
    cursor.execute("insert into footballer.footballers (id,firstname,lastname,age)values (%s,%s,%s,%s)",(footballer.id,footballer.firstname,footballer.lastname,footballer.age))
    mydb.commit()
    return {"students": footballer}

@app.delete("/footballers/{id}")
def delete_footballer(id: int):
  """Deletes a footballer based on their ID"""
  cursor.execute("DELETE FROM footballers WHERE id = %s", (id,))
  mydb.commit()
  return {"message": f"Footballer with ID {id} deleted successfully."}


@app.put("/footballers/")
def update_footballer(footballer:Footballer):

    cursor.execute("UPDATE footballer.footballers set firstname = %s, lastname = %s, age = %s where id = %s",(footballer.firstname, footballer.lastname, footballer.age,footballer.id ))
    mydb.commit()
    return {"message": "Footballer with ID updated successfully."}