from random import randrange


localData = {
    "security_key_offset": 0xD3,
    "security_key": 0
}


def createRandomKey():
    localData["security_key"] = randrange(1000, 10000)
    return localData["security_key"]


def checkKey(key_to_test):
    print(key_to_test)
    if localData["security_key"] != 0:
        if (key_to_test - localData["security_key_offset"]) == localData["security_key"]:
            return True
        else:
            return False
    else:
        return False


