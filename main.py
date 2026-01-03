cat > backend/main.py << EOL
from fastapi import FastAPI
from datetime import date
import random
from database import conn,cursor
from models import Answer,Withdraw

app = FastAPI()
DAILY_LIMIT=120
REWARD=0.1
MIN_WITHDRAW=25

def reset(user_id):
    today=str(date.today())
    cursor.execute("SELECT last_date FROM users WHERE user_id=?", (user_id,))
    r=cursor.fetchone()
    if r and r[0]!=today:
        cursor.execute("UPDATE users SET answered=0,last_date=? WHERE user_id=?", (today,user_id))
        conn.commit()

@app.get("/get-question")
def get_q(user_id:int):
    cursor.execute("INSERT OR IGNORE INTO users(user_id,last_date) VALUES(?,?)",(user_id,str(date.today())))
    conn.commit()
    reset(user_id)
    cursor.execute("SELECT answered FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone()[0]>=DAILY_LIMIT:
        return {"question":"আজকের কুইজ শেষ","options":[]}
    cursor.execute("SELECT id,question,option1,option2,option3,option4 FROM questions ORDER BY RANDOM() LIMIT 1")
    q=cursor.fetchone()
    cursor.execute("UPDATE users SET current_q=? WHERE user_id=?", (q[0],user_id))
    conn.commit()
    return {"question":q[1],"options":[q[2],q[3],q[4],q[5]]}

@app.post("/submit-answer")
def submit(a:Answer):
    cursor.execute("SELECT current_q,balance,answered FROM users WHERE user_id=?", (a.user_id,))
    qid,bal,ans=cursor.fetchone()
    cursor.execute("SELECT answer FROM questions WHERE id=?", (qid,))
    correct=cursor.fetchone()[0]
    msg="❌ ভুল উত্তর"
    if a.answer==correct:
        bal+=REWARD
        msg="✅ সঠিক উত্তর! +0.1 টাকা"
    cursor.execute("UPDATE users SET balance=?,answered=? WHERE user_id=?", (bal,ans+1,a.user_id))
    conn.commit()
    return {"message":msg,"balance":bal}

@app.post("/withdraw")
def withdraw(w:Withdraw):
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (w.user_id,))
    bal=cursor.fetchone()[0]
    if bal<w.amount or w.amount<MIN_WITHDRAW:
        return {"error":"Invalid amount"}
    cursor.execute("UPDATE users SET balance=balance-? WHERE user_id=?", (w.amount,w.user_id))
    cursor.execute("INSERT INTO withdraws(user_id,amount,method,number,status) VALUES(?,?,?,?,?)",
        (w.user_id,w.amount,w.method,w.number,"pending"))
    conn.commit()
    return {"message":"Withdraw request sent"}
EOL
