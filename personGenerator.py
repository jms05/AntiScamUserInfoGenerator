"""
A simple program to generate User informations such as
Full details from the Person, Credit card and authentication info.
Usefull for spaming scammmers phishing emails with random data to make them 
lost time checking witch are the valid records and hopeluffy make actual scams delayed.
by ..:: jms05 ::.. 2022
"""

from random import Random, randint, choice, sample, randrange
from math import ceil
from datetime import datetime, date, timedelta
from faker import Faker
import random, pytz

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }

def get_formatted_datetime(outFormat, strDate, strFormat = "%d-%m-%Y %H:%M:%S"):
    return datetime.strptime(strDate, strFormat).strftime(outFormat)

class CreditCard:

    def __init__(self, number, name, randomGenerator, faker):
        self.generator = randomGenerator
        self.faker= faker
        self.number = number
        self.name = self.getCreditCardName(name)
        self.cvv = self.faker.credit_card_security_code()
        self.expireDate= self.faker.credit_card_expire()

    def getCreditCardName(self,fullName):
        splitedNames = fullName.split()
        nameStraategy =  self.generator.randint(0,6)
        if(len(splitedNames)<=2):
            if(nameStraategy<=3):
                return fullName
            return " ".join([splitedNames[0][0],splitedNames[-1]])
        
        if(nameStraategy<1):
            return " ".join([splitedNames[0],splitedNames[-1]])
        if(nameStraategy<2):
            return " ".join([splitedNames[0],self.getRandomMidleName(splitedNames)[0],splitedNames[-1]])
        if(nameStraategy<3):
            return " ".join([splitedNames[0][0],self.getRandomMidleName(splitedNames),splitedNames[-1]])
        if(nameStraategy<4):
            return " ".join([splitedNames[0],self.getRandomMidleName(splitedNames),splitedNames[-1]])
        if(nameStraategy<5):
            return " ".join([splitedNames[0],self.getRandomMidleName(splitedNames),splitedNames[-1][0]])
        if(nameStraategy<6):
            return " ".join([splitedNames[0][0],splitedNames[-1]])

        return " ".join([splitedNames[0][0],self.getRandomMidleName(splitedNames)[0],splitedNames[-1]])

    def getRandomMidleName(self, names):
        return names[self.generator.randint(1,len(names)-2)]

    def __str__(self):
        result = []
        result.append("NAME: " + self.name)
        result.append("NUMBER: " + str(self.number))
        result.append("CVV: " +str(self.cvv))
        result.append("EXPIRE DATE: " +str(self.expireDate))
        return '\n'.join(result)

class CreditCardGenerator:

    def __init__(self):
        self.faker = Faker() 
        self.faker.seed()
        self.generator = Random()
        self.generator.seed() 

    def generateCard(self,cardName):
        creditNumber = self.faker.credit_card_number()
        return CreditCard(creditNumber, cardName, self.generator, self.faker)

class User:
    
    def __init__(self,person,generator):
        self.generator = generator
        self.username = self.generateUserName(person.email,person.phoneNumber)
        self.password = self.generatePassword()

    def generatePassword(self, special_chars = True, digits = True):
        length = self.generator.randint(8,12)
        spec_chars = ['!', '@', '#', '$', '%', '^', '&', '*']
        alpha = "QWERTYUIOPLKJHGFDSAZXCVBNMmnbvcxzasdfghjklpoiuytrewq"
        spec_char_len = dig_char_len = 0
        chars = ""
        paswd = ""
        if special_chars == True:
            spec_char_len = randint(1,ceil(length/4))
            for _ in range(spec_char_len):
                chars += choice(spec_chars)
        if digits == True:
            dig_char_len = randint(1,ceil(length/3))
            for _ in range(dig_char_len):
                chars += str(randint(0,9))
        for _ in range(length - (dig_char_len + spec_char_len)):
            chars += choice(alpha[randint(0, len(alpha) - 1)])

        paswd = ''.join(sample(chars, len(chars)))
        return paswd
    
    def generateUserName(self,email,phoneNumber):
        phoneChose = self.generator.randint(0,2)
        #Mail as user is double as probable tahn the phone
        if phoneChose>=1:
            return email
        return phoneNumber

    def __str__(self):
        result = []
        result.append("NAMENAME: " + self.username )
        result.append("PASSWORD: " + str(self.password))
        return '\n'.join(result)
   
class UserGenerator:

    def __init__(self,generator):
        self.generator= generator

    def generateUser(self, Person):
        return User(Person, self.generator)
    
class Person:

    def __init__(self, randomGenerator, faker, creditCardGenerator, userGenerator):
        self.generator = randomGenerator
        self.faker= faker
        self.fullName = self.generateName()
        self.phoneNumber = self.generatePhoneNumber()
        self.socialSecurity = self.faker.ssn()
        self.birthdate = self.generateBirthdate(31,65)
        self.country= self.faker.country()
        self.creditCard= creditCardGenerator.generateCard(self.fullName)
        self.generateAddress()
        self.email = self.generateEmail()
        self.user = userGenerator.generateUser(self)

    def generateName(self):
        numSenconNames =  self.generator.randint(0,2)+1
        numSenconSurnams =  self.generator.randint(0,2)+1
        nameresult = []
        for x in range(numSenconNames):
            nameresult.append(self.faker.first_name())
        for x in range(numSenconSurnams):
            nameresult.append(self.faker.last_name())
        return " ".join(nameresult)

    def generateAddress(self):
        tmpADDR = ""
        error = True
        while('\n' not in tmpADDR or error):
            tmpADDR = self.faker.address()
            if('\n' in tmpADDR):
                error=False
                try:
                    self.address = tmpADDR.replace('\n',' ')
                    self.zipCode = self.address.split(',')[1].split()[1]
                    self.state = states[self.address.split(',')[1].split()[0]]
                    self.address = self.address.split(',')[0]
                except:
                    error=True

    def generatePhoneNumber(self, country_code = True):
        phone = ""
        if country_code == True:
            cCodes = [91, 144, 141, 1, 44, 86, 52, 61, 32, 20, 33, 62, 81, 31, 7]
            phone = "+"
            phone += str(choice(cCodes))
            phone += " "
        for i in range(0,10):
            if i == 0:
                phone += str(randint(6,9))
            else:
                phone += str(randint(0,9))
        return phone

    #TODO Better email generation with more info about the full name not only first and last
    def generateEmail(self):
        domains = ["gmail", "yahoo", "hotmail", "live",  "outlook",]
        extentions = ['com', 'in', 'jp', 'us', 'co.uk', 'org', 'edu', 'au', 'de', 'co', 'me', 'biz', 'dev', 'ngo', 'site', 'zero', 'tech']
        
        c = randint(0,2)
        dmn = '@' + choice(domains)
        ext = choice(extentions)
        splitedName = self.fullName.split()
        if c == 0:
            email = splitedName[0] + get_formatted_datetime("%Y", self.birthdate, "%d %b, %Y") + dmn + "." + ext
        elif c == 1:
            email = splitedName[-1] + get_formatted_datetime("%d", self.birthdate, "%d %b, %Y") + dmn + "." + ext
        else:
            email = splitedName[0] + get_formatted_datetime("%y", self.birthdate, "%d %b, %Y") + dmn + "." + ext
        return email.lower()

    def generateBirthdate(self, startAge = None, endAge = None, _format = "%d %b, %Y"):
        startRange = datetime.today()
        endRange = datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)
        if startAge != None:
            if type(startAge).__name__ != 'int':
                raise ValueError("Starting age value must be integer.")
        if endAge != None:
            if type(endAge).__name__ != 'int':
                raise ValueError("Ending age value must be integer.")
        if startAge != None and endAge != None: #If both are given in arg
            if startAge >= endAge:
                raise ValueError("Starting age must be less than ending age.")
            else:
                startRange = datetime(datetime.now().year - startAge, 12, 31, 23, 59, 59, 0, pytz.UTC)
                endRange = datetime(datetime.now().year - endAge, 1, 1, 0, 0, 0, 0, pytz.UTC)
        elif startAge != None or endAge != None: #If anyone is given in arg
            ageYear = startAge if startAge != None else endAge
            startRange = datetime(datetime.now().year - ageYear, 12, 31, 23, 59, 59, 0, pytz.UTC)
            endRange = datetime(datetime.now().year - ageYear, 1, 1, 0, 0, 0, 0, pytz.UTC)
        else:
            pass
        startTs = startRange.timestamp()
        endTs = endRange.timestamp()
        return datetime.fromtimestamp(randrange(int(endTs), int(startTs))).strftime(_format)

    def __str__(self):
        result = []
        result.append('-----------------------')
        result.append("NAME: " + self.fullName )
        result.append("PHONE: " + str(self.phoneNumber) )
        result.append("socialSecurity: " + str(self.socialSecurity) )
        result.append("BIRTHDATE:" + self.birthdate)
        result.append("COUNTRY:" + self.country)
        result.append("ADDREES:" + self.address)
        result.append("ZIP:" + self.zipCode)
        result.append("STATE:" + self.state)
        result.append('    ---CREDIT CARD---   ')
        result.append(str(self.creditCard))
        result.append('    ---USER DATA---   ')
        result.append(str(self.user))
        result.append('-----------------------')
        return '\n'.join(result)

class PersonGenerator:

    def __init__(self):
        self.creditCardGenerator = CreditCardGenerator()
        self.faker = self.creditCardGenerator.faker
        self.generator= self.creditCardGenerator.generator
        self.userGenerator = UserGenerator(self.generator)


    def generatePerson(self):
        return Person(self.generator,self.faker,self.creditCardGenerator,self.userGenerator)
