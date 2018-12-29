#!/usr/bin/python3.5
import time
import re
import sys, os
from socket import inet_aton
from copy import deepcopy


class Data:

    def __init__(self):
        self.parsed_data={}
        self.merged_data ={}
        self.sorted_by_type={}
        self.old_data=[]

    def __str__(self):
        return

    def calc(self):
        parsed_data = self.get_parsed_data()
        merged_data = self.merge_data(parsed_data)
        ## Inform if nothing was scanned
        # if not self.data["arp_raw"]:
        #     print("Nothing was found")
        sorted_by_type = self.sort_by_type(merged_data)
        if self.old_data:
            data_to_print=self.update_data(sorted_by_type, self.old_data)
        else:
            data_to_print=self.timed_data(sorted_by_type)
        self.old_data = self.printing(data_to_print)

        pass

    def printing(self, data_table_dict):

        colors_dict = {"yellow": '\033[94m',
                       "green": '\033[0;32m',
                       "red": "\033[31m",
                       "blue": "\033[34m",
                       "regular": '\033[0m'}

        # Get another dict for future iterations
        dict_copy = deepcopy(data_table_dict)

        # Get rid of the empty keys
        data_table_dict_short = sorted([key_ for key_ in data_table_dict if data_table_dict[key_]])

        # # Insert delimiters if Host name exists
        # for key_ in data_table_dict:
        #     for element in data_table_dict[key_]:
        #         if element["HostName"]:
        #             element["HostName"] = "["+element["HostName"]+"]"


        # Get current time
        cur_time = time.time()

        if len(sys.argv) > 1:
            # Clear the previous output from the terminal
            os.system('clear')

        # Print Data
        for key in data_table_dict_short:

            # Color choice
            cur_color = {
                       "AP:": colors_dict["yellow"],
                       "Mini PC:": colors_dict["blue"],
                      }.get(key, colors_dict["regular"])

            # Print current color and key
            print(cur_color, key)

            # Print data from keys one by one
            for iter_, line in enumerate(data_table_dict[key], 1):
                if re.findall("\(DUP: \d+\)", line["Vendor"]):
                    dict_copy[key].remove(line)
                if line["HostName"]:
                    line["HostName"] = "["+line["HostName"]+"]"
                template = '{iter:2}. {row[IP]:15}\t{row[MAC]:<17}{time:^9.1f}{row[Vendor]}{row[HostName]}'

                # Paint a line if not visible or new
                if self.old_data:
                    if line["Status"] == "New":
                        print(colors_dict["green"], end="")
                    elif line["Status"] == "Not visible":
                        print(colors_dict["red"], end="")
                else:
                    print(colors_dict["green"], end="")
                    
                print(template.format(iter=iter_, row=line, time=(cur_time - line["Time"])), cur_color)
            print()

        return dict_copy


    @staticmethod
    def timed_data(data):
        current_time = time.time()
        for key_ in data:
            for each_entery in data[key_]:
                each_entery.update({"Time": current_time})
        return data

    @staticmethod
    def update_data(data_table_dict, data_table_dict_old):

        #iterable_new_dict = deepcopy(data_table_dict)


        # "Updated" is False to all
        for key_ in data_table_dict:
            for old_element in data_table_dict_old[key_]:
                old_element["Status"] = False

        # For every filtered data type
        for key_ in data_table_dict_old:



            # If both old data and new data exist
            if not data_table_dict[key_] == data_table_dict_old[key_]:

                needs_soring = False

                # Iterate through old data
                for old_data in data_table_dict_old[key_]:
                    # Get the last octet of the old IP for comparison
                    old_ip = inet_aton(old_data["IP"])



                    # Iterate through new data
                    for new_data in deepcopy(data_table_dict[key_]):
                        # Get the last octet of the new IP for comparison
                        new_ip = inet_aton(new_data["IP"])

                        # In case when new IP is smaller
                        if old_ip > new_ip and old_data["Vendor"] == new_data["Vendor"]:

                            # Update the information about the item
                            data_table_dict[key_].remove(new_data)
                            new_data["Status"] = "New"
                            new_data["Time"] = time.time()

                            # Save it to the old data
                            data_table_dict_old[key_].append(new_data)
                            needs_soring = True
                            continue

                        # In case of equality
                        elif old_ip == new_ip and old_data["Vendor"] == new_data["Vendor"]:

                            # Do not update the information about the item
                            data_table_dict[key_].remove(new_data)
                            if not round(time.time() - old_data["Time"]) > 3:
                                old_data["Status"] = "New"
                            else:
                                old_data["Status"] = "Old"
                            # Delete the item from new list
                            # old_data["Time"] = time.time()
                            break

                        # In case new IP is bigger
                        elif old_ip < new_ip and old_data["Vendor"] == new_data["Vendor"]:

                            # Update old element, as it doesn't exist in the new list
                            old_data["Status"] = "Not visible"
                            old_data["Time"] = time.time()
                            break

                    # In case when new-list last value is smaller then old list last value (old data is not visible)
                    else:
                        old_data["Status"] = "Not visible"
                        old_data["Time"] = time.time()

                else:
                    # If there are bigger elements in the new list, append them
                    for bigger_element in deepcopy(data_table_dict[key_]):

                        # Update the information about the item
                        # bigger_new_element["Updated"] = True
                        bigger_element["Time"] = time.time()
                        bigger_element["Status"] = "New"
                        data_table_dict_old[key_].append(bigger_element)
                        # data_table_dict[key_].remove(bigger_element)
                        needs_soring = True

                    # Sort the data afterwards if the new list is empty.
                    if needs_soring:
                        data_table_dict_old[key_].sort(key=lambda sorting: inet_aton(sorting["IP"]))



        return data_table_dict_old

    @staticmethod
    def sort_by_type(merged_data):

        data_table_dict = {sort_type: [] for sort_type in ["AP:", "Mini PC:", "Others:"]}

        append_mapping = {
            r"Sendtek Corporation": data_table_dict["AP:"].append,
            r'PCS Systemtechnik GmbH': data_table_dict["Mini PC:"].append,
            r"Others": data_table_dict["Others:"].append
            }

        # Get the separated dicts of AP/PC/Else from the scan
        for data_table_row in merged_data:
            append_mapping.get(data_table_row["Vendor"], append_mapping["Others"])(data_table_row)

        return data_table_dict

    @staticmethod
    def merge_data(parsed_data):

        # # Merge Dicts
        for nmap_el in parsed_data["nmap_dict"]:
            for arp_el in parsed_data["arp_dict"]:
                if nmap_el["IP"] == arp_el["IP"]:
                    nmap_el.update(arp_el)
                    parsed_data["arp_dict"].pop(parsed_data["arp_dict"].index(arp_el))
                    break

        # Return the merged dict
        return parsed_data["nmap_dict"]


    @staticmethod
    def get_parsed_data():
        # get arp
        arp_raw = os.popen("arp-scan -l| grep -E '([0-9]+\.){3}'").read().rstrip("\n")

        # parse arp
        arp_parsed = [i.split("\t") for i in arp_raw.split("\n")]
        arp_dict = [dict(zip(["IP", "MAC", "Vendor"], i)) for i in arp_parsed]
        arp_dict.sort(key=lambda sorting: inet_aton(sorting["IP"]))

        # get ips for nmap
        ips_from_arp = [scanned_element["IP"] for scanned_element in arp_dict]

        # get nmap
        nmap_raw = os.popen("nmap -sL " + " ".join(ips_from_arp)).read()

        # parse nmap
        re_pattern=r"(?<=\nNmap scan report for)\s?(.*)\s\(?((?:\d{1,3}\.){3}\d{1,3})(?=\)?\n)"
        nmap_parsed = re.findall(re_pattern, nmap_raw)
        nmap_dict=[dict(zip(["HostName", "IP"], i)) for i in nmap_parsed]

        # Return pared nmap and arp
        return {"nmap_dict":nmap_dict,"arp_dict":arp_dict}

test = Data()
if len(sys.argv) > 1:
    while True:
        test.calc()
test.calc()
