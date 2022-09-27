from src.personGenerator import PersonGenerator

personGenerator = PersonGenerator()

for i in range(20):
    user = personGenerator.generatePerson()
    print(str(user))
