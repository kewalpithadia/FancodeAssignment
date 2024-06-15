import json
import sys
import configparser
import requests
import logging
from tabulate import tabulate


class FanCode:
    """
    Class With All Methods For The Computation
    """

    def __init__(self, endpoint, city_lng_range, city_lat_range):
        """
        string :param endpoint: Endpoint URL for the Api Path
        List :param city_lng_range:  Longitude Range in Array With First Being The Lowest Value And Last Value Being The Largest Value For Longitude
        List :param city_lat_range: Latitude Range in Array With First Being The Lowest Value And Last Value Being The Largest Value For Latitude
        """
        self.endpoint = endpoint
        self.city_lng = city_lng_range
        self.city_lat = city_lat_range
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("Fancode")

    def withinthecity(self, location):
        """
        Dict :param location: Loaction which is having key-value pair of longitude and latitude.
        Boolean :return: Returns True False based on if given location is in the range of longitude and latitude.
        """
        if self.city_lat[0] <= float(location.get("lat")) <= self.city_lat[-1] and \
                self.city_lng[0] <= float(location.get("lng")) <= self.city_lng[-1]:
            incity = True
        else:
            incity = False
        return incity

    def fetchallfancodecityusers(self):
        """
        List :return: List Of All The User Which Belongs To The Given City
        """
        response = requests.get("%s/users" % self.endpoint)
        userlist = []
        if response.status_code != 200:
            self.logger.info("Didn't Get Expected Output Status Code %s" % str(response.status_code))
            return False
        else:
            data = response.json()
            for item in data:
                location = item.get("address").get("geo")
                self.logger.info("Checking If User With User ID %s Belongs To The Given City" % str(item.get("id")))
                if self.withinthecity(location):
                    self.logger.info(
                        "User With User ID %s Belongs To The Given City. Adding It To The List" % str(item.get("id")))
                    userlist.append(item)
        if userlist:
            return userlist
        else:
            return "Empty List"

    def getalltodoforuser(self):
        usertodomap = {}  #
        response = requests.get("%s/todos" % self.endpoint)
        if response.status_code != 200:
            self.logger.info("Didn't Get Expected Status Code %s" % str(response.status_code))
            self.logger.info("Response %s" % str(response.text))
            return False
        todolist = response.json()
        if todolist:
            for item in todolist:
                userid = item.get("userId")
                if userid not in usertodomap.keys():
                    usertodomap[userid] = {"tasks": [], "completed": 0}
                usertodomap[userid]["tasks"].append(item)
                if item.get("completed"):
                    usertodomap[userid]["completed"] += 1
            return usertodomap
        return False

    def main(self, format=None):
        userlist = self.fetchallfancodecityusers()
        if userlist:
            self.logger.info("Fetched All User List In The Given City")
        elif userlist == "Empty List":
            self.logger.info("No User For The Given City. Hence Exiting")
            sys.exit(0)
        else:
            self.logger.error("There Was Some Issue In Fetching User List. Hence Exiting")
            sys.exit(1)
        todousermaping = self.getalltodoforuser()
        if todousermaping:
            self.logger.info("To Do Task Mapping Done With Users")
        else:
            self.logger.error("There Was Some Issue In Mapping To Do Task With Users")
            sys.exit(1)
        usertodocompeted = {}  # this will hold all the user who have completed at least 50 % if this task {"userid" : {"data":{}, "tasks":[{task1}, {task2}]}}
        for item in userlist:
            userid = item.get("id")
            if userid in todousermaping.keys():
                completed_task = int(todousermaping.get(userid).get("completed"))
                total_task = len(todousermaping.get(userid).get("tasks"))
                if completed_task > total_task * 0.5:
                    usertodocompeted[userid] = {"data": item, "tasks": todousermaping.get(userid).get("tasks"),
                                                "CompletedTask": completed_task, "TotalTask": total_task}
            else:
                logging.info("No To DO Task Found For User Id %s" % str(userid))
        self.logger.info("Users With At Least 50% Completed Task In Given City Are As Follow")
        # json selected_output
        if format:
            selected_output = {}
            config = configparser.ConfigParser()

            try:
                config.read('columns.cfg')
                userkeys = [value for value in config.get("keys", "userkeys").split(",") if value]
                if not userkeys:
                    self.logger.info("No Selected Keys Found For User Hence Exiting")
                    self.logger.info("Showing Complete Data")
                    for key in usertodocompeted.keys():
                        userkeys = [x for x in usertodocompeted.get(key).get("data").keys()]
                        break
            except Exception as err:
                self.logger.info("Error In Fetching Columns Config With Error :- %s" % str(err))
                sys.exit(1)
            for key in usertodocompeted.keys():
                user_data = usertodocompeted.get(key)
                selected_output[key] = {}
                for item in userkeys:
                    userdatakey = item.split(".")
                    if len(userdatakey) == 1:
                        if userdatakey[0] in user_data.get("data").keys():
                            selected_output[key].update({userdatakey[0]: user_data.get("data").get(userdatakey[0])})
                        else:
                            selected_output[key].update({userdatakey[0]: "Key Not Found In User Data"})
                    else:
                        basekey = userdatakey[0]
                        basedata = user_data["data"][basekey]
                        for i in range(1, len(userdatakey)):
                            if isinstance(basedata, dict):
                                if userdatakey[i] in basedata.keys():
                                    if i == len(userdatakey) - 1:
                                        selected_output[key].update({".".join(userdatakey): basedata[userdatakey[i]]})
                                    else:
                                        basedata = basedata[userdatakey[i]]
                                else:
                                    selected_output[key].update({".".join(userdatakey): "Key Not Found In User Data"})
                            else:
                                self.logger.info("No Proper Structure Provided For %s " % ".".join(userdatakey))
                                selected_output[key].update({".".join(userdatakey): "No Proper Structure Provided"})
                selected_output[key].update({"CompletedTasks": int(todousermaping.get(key).get("completed")),
                                             "TotalTask": len(todousermaping.get(key).get("tasks"))})
            self.logger.info(
                "Details For Users In %s Format Who have Completed At least 50 Percent Of Task With Selected Coloums" % format)
            if format == "json":
                for key in selected_output.keys():
                    self.logger.info(json.dumps(selected_output.get(key), indent=4))
            elif format == "table":
                tableformat = []
                for key in selected_output.keys():
                    tableformat.append([x for x in selected_output[key].keys()])
                    break
                for key in selected_output.keys():
                    tableformat.append([selected_output[key][i] for i in selected_output[key].keys()])
                table = tabulate(tableformat)
                self.logger.info(table)
            else:
                pass
            return selected_output
        else:
            self.logger.info("Details For Users Who have Completed At least 50 % Of Task With Complete Data")
            for key in usertodocompeted.keys():
                self.logger.info(json.dumps(usertodocompeted.get(key), indent=4))
            return usertodocompeted


if __name__ == "__main__":
    endpoint = "http://jsonplaceholder.typicode.com/"  # Default Value
    city_lng = [5, 100]
    city_lat = [-40, 5]
    format = None
    for item in sys.argv:
        if item.startswith("endpoint="):
            endpoint = item.split("=")[-1]
        if item.startswith("latrange="):
            city_lat = [int(x) for x in item.split("=")[-1].split(",")]
        if item.startswith("lngrange="):
            city_lng = [int(x) for x in item.split("=")[-1].split(",")]
        if item.startswith("format="):
            format = item.split("=")[-1]

    if format not in ["json", "table"]:
        format = None
        print("All Users Having More Than 50 Percent Task Completed Data Will Be Printed As JSON")
    else:
        print("All Users Having More Than 50 Percent Task Selected Data Will Be Printed As %s" % format.upper())
    if city_lat[0]> city_lat[1]:
        print("No Proper Range Provided For City Latitude")
        sys.exit(1)
    if city_lng[0]> city_lng[1]:
        print("No Proper Range Provided For City Longitude")
        sys.exit(1)
    obj = FanCode(endpoint, city_lng_range=city_lng, city_lat_range=city_lat)
    response = obj.main(format)
