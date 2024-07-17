import aiml
from APIconnection import Connector
from subject_detector import SubjectDetector
from context_selection import ContextSelector
from dictionaries import user_options_pol

connector=Connector()
cp=SubjectDetector()
selector=ContextSelector()

k = aiml.Kernel()
k.learn("/home/bunio/PycharmProjects/simpleChatbot/conversations.aiml")


def answer(res, con, case): 
    if case==1 and con=="album":
        return res[0][con]["name"]
    elif case==1 and con!="album":
        return res[0][con+"s"][0]["name"]
    elif case==2 and con=="album":
        return list(map(lambda i: i[con]["name"], res))
    elif case==2 and con!="album":
        return list(map(lambda i: i[con+"s"][0]["name"], res))
    elif case==3:
        return list(map(lambda i: i["name"], res["tracks"]))
    elif case==4:
        return list(map(lambda i: i["name"], res))
    elif case==5 and con=="album":
        return (list(map(lambda i: i[con]["name"], res)))
    elif case==5 and con!="album":
        return (list(map(lambda i: i[con+"s"][0]["name"], res)))
    else:
        return "Nie mogę znaleźć listy!"


def inner_level(results, context):
    question=input("Ty > ")
    reply=k.respond(question)
    if reply=="Albo...":
        print("bot > ", reply, answer(results, context[0], 5))

def base_dialog():
    while True:
        question = input("Ty > ")
        context = selector.choose_context(question)
        subject = cp.extract_subjects(question)
        reply = k.respond(question)

        if reply == None:
            print("bot > Nie mam odpowiedzi.")
            continue

        if context is not None and subject is not None and context!="rozmowa":

            if len(subject)==1 and len(context)==2:
                api_results = connector.get_stand_request(subject[0], context[1])
                print("bot > ", reply, answer(api_results, context[0], 1))
                inner_level(api_results, context)

            elif len(subject)==2 and len(context)==2:
                api_results = connector.get_sub_request(subject[0], subject[1], context[1])
                print("bot > ", reply, answer(api_results, context[0], 2))

            elif len(subject)==1 and len(context)==1:
                con=user_options_pol.get(context[0])
                temp_dict=list(i for i in user_options_pol.values() if i != con)
                print(f"bot > Czy {subject[0]} to {temp_dict[0]} czy może {temp_dict[1]} ?")
                helpful_question=input("Ty > ")
                new_reply=k.respond(helpful_question)
                if new_reply=="Pogubiłem się zacznijmy od nowa.":
                    print("bot > ", new_reply)
                    continue
                helpful_context=selector.choose_context(helpful_question)
                context.append(helpful_context[0])
                api_results = connector.get_stand_request(subject[0], context[1])
                source_id=api_results[0]["id"]
                final_results=connector.get_show_request(context[0], context[1], source_id)
                context_var=(4 if context[0]=="album" or context[1]=="album" else 3)
                print("bot > ", reply, answer(final_results, context[0], context_var))

        else:
            print("bot > ", reply)

if __name__ == "__main__":
    base_dialog()