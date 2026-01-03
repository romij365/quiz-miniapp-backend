cat > backend/models.py << EOL
from pydantic import BaseModel

class Answer(BaseModel):
    user_id:int
    answer:str

class Withdraw(BaseModel):
    user_id:int
    amount:float
    method:str
    number:str
EOL
