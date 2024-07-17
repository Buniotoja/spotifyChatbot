import re
from dictionaries import keywords

class ContextSelector:

    def _select(self, input_str):
        result_array=[]
        input_array=[]
        word=""
        for letter in input_str+" ":
            if letter==" ":
                input_array.append(word)
                word=""
            else:
                word+=letter

        for w in input_array:
            for k in keywords.keys():
                for kk in keywords.get(k):
                    if w.__contains__(kk) and not result_array.__contains__(kk):
                        result_array.append(k)

        return result_array

    def choose_context(self, input_str):
        user_array=self._select(input_str)
        if len(user_array)==0:
            user_array.append(4)
        return_obj=[]
        match user_array[0]:
            case 1:
                return_obj.append("album")
                if len(user_array)==2:
                    return_obj.append("artist" if user_array[1]==2 else "track")
            case 2:
                return_obj.append("artist")
                if len(user_array) == 2:
                    return_obj.append("album" if user_array[1] == 1 else "track")
            case 3:
                return_obj.append("track")
                if len(user_array) == 2:
                    return_obj.append("album" if user_array[1] == 1  else "artist")
            case 4:
                return_obj.append("rozmowa")
            case _:
                return_obj.append("Błąd kontekstu")

        return return_obj




