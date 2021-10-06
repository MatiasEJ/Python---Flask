from werkzeug.security import generate_password_hash,check_password_hash
class User():
    
    def __init__(self,id,name,email,username,password,is_admin) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def set_password(self,password: str) -> None:
        self.password = generate_password_hash(password) 
    