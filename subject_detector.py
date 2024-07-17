
class SubjectDetector:

    def extract_subjects(self, input_str):
        subjects=[]
        if input_str.count('<')>0:
            ind_start=input_str.find('<')
            ind_start+=1
            ind_end=input_str.find('>')
            sub=input_str[ind_start:ind_end]
            subjects.append(sub)

            if input_str.count('<')==2:
                ind_temp=input_str.find(">")+1
                input_substr=input_str[ind_temp:]
                ind_start=input_substr.find('<')+1
                ind_end=input_substr.find('>')
                sub = input_substr[ind_start:ind_end]
                subjects.append(sub)
            return subjects
        else:
            return None

