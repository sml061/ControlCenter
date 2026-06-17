from api.api import Aluno

def Main():
  Aluno.add("Samuel Bonfim Araujo", "samuelbonfimaraujo@gmail.com", "61996445622", "09/02/2010", "1")
  Aluno.show()

if __name__ == "__main__":
  Main()