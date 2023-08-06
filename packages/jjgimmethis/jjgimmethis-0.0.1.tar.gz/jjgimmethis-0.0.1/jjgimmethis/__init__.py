from multiprocessing.sharedctypes import Value
import random
import string
from xmlrpc.client import Boolean

# list of first names and/or middle names
firstMidNameBank = [
    'Oliver',
    'Asher',
    'Theodore',
    'Noah',
    'Henry',
    'Fynn'
    'Aiden',
    'Alistair',
    'Liam',
    'Jasper',
    'Declan',
    'Silas',
    'Sebastian',
    'Levi',
    'Leo',
    'Felix',
    'Everett',
    'Alexander',
    'Ethan',
    'Caleb',
    'Gabriel',
    'Atticus',
    'Owen',
    'Benjamin',
    'Grayson',
    'Jackson',
    'Elijah',
    'Lucas',
    'August',
    'Milo',
    'William',
    'Miles',
    'Evander',
    'Theo',
    'Hudson',
    'Emmett',
    'Arlo',
    'Archer',
    'Elias',
    'Ronan',
    'Isaac',
    'Wesley',
    'Micah',
    'Atlas',
    'Beau',
    'Luke',
    'Nathaniel',
    'Thomas',
    'Connor',
    'Landon',
    'Gypsy',
    'Shawnee',
    'Marissa',
    'Ferdy',
    'Raelyn',
    'Bobbie',
    'Ford',
    'Westley',
    'Marigold',
    'Lizzy',
    'Della',
    'Breana',
    'Wilder',
    'Darell',
    'Gypsy',
    'Marcy',
    'Ralph',
    'Doretta',
    'Stevie',
    'Earle',
    'Loyd',
    'Felisha',
    'Keanna',
    'Reynold',
    'Elliott',
    'Aleta',
    'Raquel',
    'Janella',
    'Melvyn',
    'Brinley',
    'Tatianna',
    'Daley',
    'Randall',
    'Robina',
    'Raymund',
    'Adelynn',
    'Roger',
    'Trenton',
    'Lexine',
    'Percival',
    'Salena',
    'Merideth',
    'Abbie',
    'Myrtle',
    'Ella',
    'Debra',
    'Magdalene',
    'Stanford',
    'Charlee',
    'Beckett',
    'Boniface',
    'Frank',
    'Bailee',
    'Shena',
    'Dennis Meg',
    'Ebba Annice',
    'Orville Rob',
    'Astrid Noelene',
    'Shayla',
    'Jen',
    'Mary',
    'Maree',
    'April',
    'Torin',
    'Tarina',
    'Jayce',
    'Harmony',
    'Ingram',
    'Tibby',
    'Layla',
    'Emmitt',
    'Scout',
    'Rob',
    'Louella',
    'Gerald',
    'Maeghan',
    'Amber',
    'Annette',
    'Lauressa',
    'Angel',
    'Peyton',
    'Sandy',
    'Georgia',
    'Marshall',
    'Bridgette',
    'Aretha',
    'Skye',
    'Chet',
    'Reese',
    'Sylvester',
    'Karaugh',
    'Mollie',
    'Queen',
    'Frank',
    'Flora',
    'Easter'
]

# list of surnames
surnameBank = [
    'Smith',
    'Johnson',
    'Jones',
    'Williams',
    'Brown',
    'Garcia',
    'Miller',
    'Davis',
    'Rodriguez',
    'Martinez',
    'Hernandez',
    'Lopez',
    'Gonzales',
    'Wilson',
    'Anderson',
    'Thomas',
    'Taylor',
    'Moore',
    'Jackson',
    'Martin',
    'Lee',
    'Perez',
    'Thompson',
    'White',
    'Harris',
    'Sanchez',
    'Clark',
    'Ramirez',
    'Lewis',
    'Robinson',
    'Walker',
    'Young',
    'Allen',
    'King',
    'Wright',
    'Scott',
    'Torres',
    'Myers',
    'Hill',
    'Flores',
    'Green',
    'Adams',
    'Nelson',
    'Baker',
    'Hall',
    'Rivera',
    'Campbell',
    'Mitchell',
    'Roberts',
    'Carter',
    'Gomez',
    'Ortiz',
    'Morgan',
    'Cooper',
    'Howard',
    'Wrad',
    'Watson',
    'Richardson',
    'Brooks',
    'Reed',
    'Rogers',
    'Cook',
    'Foster',
    'Ross',
    'Long',
    'Sanders',
    'Hughes',
    'Gray',
    'Bennet',
    'James',
    'Wood'
]

# list of words that will be used when making a username
usernameWordBank = [
    'Logic',
    'Warrant',
    'Iconic',
    'Threat',
    'Strike',
    'Adjacent',
    'Wireless',
    'Vital',
    'Unity',
    'Audio',
    'Schemer',
    'Depth',
    'Thirteen',
    'Mystic',
    'Profound',
    'Atomic',
    'Virtual',
    'Inspired',
    'Abstract',
    'Static',
    'Mosaic',
    'Elite',
    'Trouble',
    'Strategist',
    'Python',
    'Mohawk',
    'Arctic',
    'Linear',
    'Rival',
    'Medieval',
    'Delay',
    'Tension',
    'Phoenix',
    'Combat',
    'Animal',
    'Serious',
    'Integral',
    'Tactical',
    'Proof',
    'Vertical',
    'Absolute',
    'Revised',
    'Equal',
    'Pending',
    'Antics',
    'Variable',
    'Forum',
    'Tangible',
    'Anchor',
    'Ornery',
    'Indigo',
    'Schism',
    'Capture',
    'Relevant',
    'Momentum',
    'Laser',
    'Penalty',
    'Clutch',
    'Leverage',
    'Endeavor',
    'Justice',
    'Crucial',
    'Potato',
    'Taro',
    'Boba',
    'Thousand',
    'Cloud',
    'Sky',
    'Grumpy'
]

# list of random objects and things
objectBank = [
    'traffic light',
    'motorcycle',
    'people',
    'cloud',
    'wood',
    'ball',
    'candle',
    'lamp shade',
    'pool stick',
    'paint brush',
    'shoes',
    'tissue box',
    'stop sign',
    'glasses',
    'button',
    'charger',
    'milk',
    'cell phone',
    'brocolli',
    'rubber duck',
    'zipper',
    'street lights',
    'knife',
    'needle',
    'slipper',
    'ipod',
    'toothbrush',
    'sun glasses',
    'tomato',
    'couch',
    'sharpie',
    'grid paper',
    'pen',
    'house',
    'lotion',
    'washing machine',
    'fork',
    'credit card',
    'twezzers',
    'bread',
    'clothes',
    'purse',
    'door',
    'desk',
    'clay pot',
    'shirt',
    'bracelet',
    'sandal',
    'towel',
    'keys',
    'lip gloss',
    'soy sauce',
    'sailboat',
    'bottle cap',
    'CD',
    'bag',
    'computer',
    'album',
    'milk tea',
    'cardigan',
    'jeans',
    'sakura flower',
    'chicken',
    'cow',
    'outlet',
    'dog',
    'controller',
    'newspaper',
    'soda can',
    'keyboard',
    'pillow',
    'chalk',
    'USB drive',
    'luggage',
    'headphones',
    'car',
    'bicycle',
    'ring',
    'necklace',
    'cake',
    'balloon',
    'pasta',
    'burger',
    'clock',
    'radio',
    'sketch pad',
    'doll',
    'spoon',
    'sponge'
]


def name(num_words: int = 2):
    """
    Generates a random name according to user specification.

    Parameters
    ---------
    num_words: int
        Values ranging from [1-3]. 1 - First name only. 2 - First name and last name. 3 - First name, middle name and last name. Default value is 2.

    Returns
    --------
    str
        A random name generated according to user specification.
    str
        Q - The error value generated when user did not provide values between [1-3].

    Raises
    ------
    TypeError
        If the num_words argument passed in is not an integer value.
    """

    # raise TypeError if user did not supply an integer for num_words argument
    if not isinstance(num_words, int):
        raise TypeError("Only integers are allowed.")

    # dictionary that will act as a switch case
    switcher = {
        1: random.choice(firstMidNameBank),
        2: random.choice(firstMidNameBank) + " " + random.choice(surnameBank),
        3: random.choice(firstMidNameBank) + " " + random.choice(firstMidNameBank) + " " + random.choice(surnameBank),
    }

    # return the appropriate name result
    return switcher.get(num_words, "Q")


def username(isUnderScore: bool = True, isNum: bool = True) -> str:
    """
    Generates a random username according to user specifications.

    Parameters
    ---------
    isUnderScore: bool
        True - The generated username will include an underscore. False - The generated username will not include an underscore. Default value is True.

    isNum: bool
        True - The generated username will include a number. False - The generated username will not include a number. Default value is True.

    If underscore and number options are all off, the username will only contain words. If underscore and number options are all on, the username will contain a mixture of words, underscore and number. 

    Returns
    --------
    str
        A random username generated according to user specifications.

    Raises
    ------
    None
    """

    usernameResult = ""

    # get two words from username word list
    usernameP1 = random.choice(usernameWordBank)
    usernameP2 = random.choice(usernameWordBank)

    # reselect words from word list if both words are the same
    while usernameP1 == usernameP2:
        usernameP1 = random.choice(usernameWordBank)
        usernameP2 = random.choice(usernameWordBank)

    # first letter of first word in username will be lowercase
    usernameP1 = usernameP1[0].lower() + usernameP1[1:]
    usernameResult += usernameP1

    # check if underscore and number is demanded in the username
    if isUnderScore:
        usernameResult += "_" + usernameP2
    else:
        usernameResult += usernameP2

    if isNum:
        usernameResult += str(random.randint(0, 1000))
    else:
        usernameResult = usernameResult

    # return the appropriate username result
    return usernameResult


def password(length: int = 12, isUpper: bool = True, isNum: bool = True, isSym: bool = True) -> str:
    """
    Generates a random password according to user specifications.

    Parameters
    ---------
    length: int
        The length of the password. The integer value passed in must be greater than or equal to 8. Default value is 12.

    isUpper: bool
        True - The password will include at least one uppercase letter. False - The password will not include an uppercase letter. Default value is True.

    isNum: bool
        True - The password will include at least one number. False - The password will not include a number. Default value is True.

    isSym: bool
        True - The password will include at least one symbol/punctuation. False - The password will not include a symbol/punctuation. Default value is True.

    If uppercase, number and symbol options are all off, the password will only contain lowercase letters. If uppercase, number and symbol options are all on, the password will contain a mixture of lowercase letters, uppercase letters, numbers and symbols.

    Returns
    -------
    str
        A random password generated according to user specifications.

    Raises
    ------
    TypeError
        If the length argument passed in is not an integer value.

    ValueError
        If the length argument passed is an integer with value less than 8.
    """

    # raise TypeError if user did not supply an integer for length argument
    if not isinstance(length, int):
        raise TypeError("Only integers are allowed.")

    # raise ValueError if user did not supply an integer that is >= 8 for num_words argument
    if length < 8:
        raise ValueError(
            "Only integers bigger than or equal to 8 are allowed.")

    # using pre-initialized strings
    lowercase = string.ascii_lowercase  # store all lowercase letters
    uppercase = string.ascii_uppercase  # store all uppercase letters
    numbers = string.digits  # store all digits
    symbols = string.punctuation  # store all punctuation/symbols

    # concatenate the pre-initialized strings
    full_combination = lowercase + uppercase + numbers + symbols

    # initialize empty lists
    tempUp = []
    tempNum = []
    tempSym = []

    # check for user specification and select 2 characters from list
    if isUpper:  # wants uppercase letters
        tempUp = random.sample(uppercase, 2)

    if isNum:  # wants numbers
        tempNum = random.sample(numbers, 2)

    if isSym:  # wants symbols
        tempSym = random.sample(symbols, 2)

    # further checking on user specifications

    if(not isUpper and not isNum and not isSym):  # no additional toppings (just all lowercase)

        passlist = random.sample(lowercase, length)

        password = "".join(passlist)

    elif(isUpper and isNum and isSym):  # wants all additional toppings

        # get 2 lowercase characters
        tempLow = random.sample(lowercase, 2)

        # user specified length - (2+2+2+2)
        diff = length - 8

        if diff > 0:  # user specified length is bigger than 8

            # select some more characters to meet requirement
            tempRan = random.sample(full_combination, diff)
            passlist = tempLow + tempUp + tempNum + tempSym + tempRan

        else:  # user specified length is 8
            passlist = tempLow + tempUp + tempNum + tempSym

        # shuffle items in list
        random.shuffle(passlist)

        # get all items from list as string
        password = "".join(passlist)

    else:  # has some additional toppings (not sure which)

        # get 2 lowercase characters
        tempLow = random.sample(lowercase, 2)

        # concatenate lists' items
        passlist = tempLow + tempUp + tempNum + tempSym

        # count num of items in list
        num = len(passlist)

        # still require XX more character(s)
        diff = length - num

        # select XX more characters to meet requirement
        if(isUpper):

            if(isUpper and isNum):
                combination = uppercase + numbers + lowercase
                tempRan = random.sample(combination, diff)

            if(isUpper and isSym):
                combination = uppercase + symbols + lowercase
                tempRan = random.sample(combination, diff)

            combination = uppercase + lowercase
            tempRan = random.sample(combination, diff)

        if(isNum):

            if(isNum and isSym):
                combination = numbers + symbols + lowercase
                tempRan = random.sample(combination, diff)

            combination = numbers + lowercase
            tempRan = random.sample(combination, diff)

        if(isSym):
            combination = symbols + lowercase
            tempRan = random.sample(combination, diff)

        # update passlist
        passlist += tempRan

        # shuffle items in list
        random.shuffle(passlist)

        # get all items from list as string
        password = "".join(passlist)

    # return the appropriate password result
    return password


def things() -> str:
    """ 
    Generates random things.

    Parameters
    ---------
    None

    Returns
    -------
    str
        A random thing.

    Raises
    ------
    None
    """

    # return an object from the list of objects
    return random.choice(objectBank)
