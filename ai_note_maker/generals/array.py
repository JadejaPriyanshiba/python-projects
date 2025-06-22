def moveElement(array, fromIndex, toIndex):
    if( not (isinstance(array, list) and isinstance(fromIndex, int) and isinstance(toIndex, int))):
        print("invalid data types ", type(array), type(fromIndex), type(toIndex))
        return
    elif(fromIndex<0 or fromIndex>=len(array) or toIndex>=len(array) or toIndex<0 or toIndex==fromIndex):
        print("Invalid ranges: ", fromIndex, toIndex, len(array))
        return
    item = array.pop(fromIndex)
    array.insert(toIndex, item)