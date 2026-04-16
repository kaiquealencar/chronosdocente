from locust import HttpUser, task, between

class WebAppUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        payload = {
            "username": "usuario_teste",
            "password": "senha123"
        }
        
        response = self.client.post("/login", data=payload)
        
        if response.status_code == 200 and "login" in response.url:
            print("AVISO: O login parece ter falhado (permaneceu na página de login).")
        else:
            print(f"Login enviado! Status: {response.status_code}")


    @task(1)
    def index_page(self):
        self.client.get("/")

    @task(2)
    def view_disciplinas(self):
        self.client.get("/disciplinas")

    @task(3)
    def view_escolas(self):
        self.client.get("/escolas")

    @task(4)
    def view_aulas(self):
        self.client.get("/aulas") 
    
    @task(5)
    def view_estruturas(self):
        self.client.get("/estruturas") 

    @task(6)
    def view_usuarios(self):
        self.client.get("/usuarios") 


    @task(1)
    def logout_test(self):
        self.client.get("/logout")
        self.on_start()