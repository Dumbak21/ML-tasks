from datetime import datetime
import json
import os

dir = "data/"                                               # Directory of data
number_of_files = len(os.listdir(dir))
all_data = {}

for file in os.listdir(dir):                                # Merging data from all files
    f = open(dir + file, "r")
    temp_data = json.load(f)
    for user_id in list(temp_data.keys()):
        if user_id in all_data:
            for request_id in list(temp_data.get(user_id).keys()):
                if request_id in list(all_data.get(user_id).keys()):
                    all_data[user_id][request_id] += temp_data.get(user_id).get(request_id)
                else:
                    all_data[user_id].update({request_id : temp_data.get(user_id).get(request_id)})
        else:
            all_data.update({user_id : temp_data.get(user_id)})
    f.close()

# -- 1 --
print(str(len(all_data.keys())) + " unique users.")

# -- 2 --
set_of_requests = set()
for user_id in list(all_data.keys()):
    user_values = all_data.get(user_id)
    if len(user_values) > 1:
        set_of_requests.update(set(user_values.keys()))
set_of_requests.remove("variant")
print(str(len(set_of_requests)) + " unique requests.")

# -- 3 --
requests = {}
for user_id in list(all_data.keys()):                       # Merging requests from all user_ids
    user_values = all_data.get(user_id)
    if len(user_values) > 1:
        list_of_requests = list(user_values.keys())
        list_of_requests.remove("variant")
        for request_id in list_of_requests:
            if request_id in requests:
                for cell in range(len(user_values.get(request_id))):
                    if len(user_values.get(request_id)[cell]) != 0:
                        for req in range(len(user_values.get(request_id)[cell])):
                            requests.get(request_id).append(user_values.get(request_id)[cell][req])
            else:
                for cell in range(len(user_values.get(request_id))):
                    if len(user_values.get(request_id)[cell]) != 0:
                        requests.update({request_id : user_values.get(request_id)[cell]})

for item_id in list(requests.keys()):                       # Calculating average time between each item_id requests
    request_times = []
    item_requests = requests.get(item_id)
    for request in range(len(item_requests)):
        request_times.append(item_requests[request][0])
    request_times = sorted(request_times)
    summary = 0
    for req in range(len(request_times)):
        if req != 0:
            summary += int((datetime.fromisoformat(request_times[req]) - datetime.fromisoformat(request_times[req-1])).total_seconds())
    if len(request_times)-1 == 0:
        print("Item_id " + str(item_id) + " was requested only once.") 
    else:
        print("Average time: " + str(int(summary/(len(request_times)-1))) +  "s for item_id: " + str(item_id))

# -- 4 --
for item_id in list(requests.keys()):                       # Finding median time between each item_id requests
    request_times = []
    item_requests = requests.get(item_id)
    for req in range(len(item_requests)):
        request_times.append(item_requests[req][0])
    request_times = sorted(request_times)
    deltas = []
    for req in range(len(request_times)):
        if req != 0:
            deltas.append(int((datetime.fromisoformat(request_times[req]) - datetime.fromisoformat(request_times[req-1])).total_seconds()))
    if len(request_times)-1 == 0:
        print("Item_id " + str(item_id) + " was requested only once.")    
    else:
        print("Median: " + str(sorted(deltas)[int(len(deltas)/2)]) +  "s for item_id: " + str(item_id))

# -- 5 --
item_id_of_max = ""                                         # Extra
max_count = 0
looking_for = "similarInJsonList"
for item_id in list(requests.keys()):                       # Finding max requests of "similarInJsonList" of item_id
    sijl_count = 0
    item_requests = requests.get(item_id)
    for req in range(len(item_requests)):
        if item_requests[req][1] == looking_for:
            sijl_count += 1
    if sijl_count > max_count:
        max_count = sijl_count
        item_id_of_max = item_id
print("Max number of returned \"" + looking_for + "\" was " + str(max_count) + " for item_id " + item_id_of_max)


'''
Machine learning task:

1.  K rozt????zen?? bot do skupin budeme muset ur??it jejich nejpravd??podobn??j???? barvu, tedy naj??t na obr??zku botu 
    a odflitrovat pozad??. Pot?? m????eme vybrat bu?? barvu, kter?? na bot?? p??eva??uje, nebo barvu z??skat zpr??merov??n??m 
    barev boty. Nyn?? kdy?? bota m?? svou barevnou hodnotu vyu??ijeme nejl??pe ML model, kter?? rozd??l?? hodnoty do 
    klastr?? (K-Means). V??hodou je, ??e tento model nepot??ebuje ????dn?? p??edchoz?? tr??nink a boty n??m rozd??l?? na 
    skupiny popdobn??ch barev. Nev??hodou je, ??e v??cebarevn?? boty nebou tak p??esn?? za??azeny.
2.  Zde budeme pot??ebovat ur??it typ boty (tenisky, lodi??ky, ko??a??ky,...) a barvu, na to budeme pot??ebovat vytr??novan?? ML model, kter?? dok????e 
    rozpoznat typ boty a klasifikovat ji. Pot?? v podmno??in?? bot stejn??ho typu najdeme postupem zm??n??n??m v 1. bod?? 
    boty podobn?? barvy a vybereme 10 nejpodobn??j????ch (nejbli??????ch v modelu).

'''