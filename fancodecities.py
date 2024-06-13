import json
import sys
import configparser
import requests
import logging


class FanCode:
    """
    Class With All Methods For The Computation
    """
    def __init__(self, endpoint, city_lng_range, city_lat_range ):
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
            incity=False
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
                    self.logger.info("User With User ID %s Belongs To The Given City. Adding It To The List" % str(item.get("id")))
                    userlist.append(item)
        if userlist:
            return userlist
        else:
            return "Empty List"

    def getalltodoforuser(self):
        usertodomap = {}  #
        response = requests.get("%s/todos"% self.endpoint)
        if response.status_code != 200:
            self.logger.info("Didn't Get Expected Status Code %s" % str(response.status_code))
            self.logger.info("Response %s" % str(response.text))
            return False
        todolist = response.json()
        if todolist:
            for item in todolist:
                userid = item.get("userId")
                if userid not in usertodomap.keys():
                    usertodomap[userid] = {"tasks":[], "completed":0}
                usertodomap[userid]["tasks"].append(item)
                if item.get("completed"):
                    usertodomap[userid]["completed"] += 1
            return usertodomap
        return False






    def main(self):
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
        usertodocompeted = {}   # this will hold all the user who have completed at least 50 % if this task {"userid" : {"data":{}, "tasks":[{task1}, {task2}]}}
        for item in userlist:
            userid = item.get("id")
            if userid in todousermaping.keys():
                completed_task = int(todousermaping.get(userid).get("completed"))
                total_task = len(todousermaping.get(userid).get("tasks"))
                if completed_task >= total_task * 0.5:
                    usertodocompeted[userid] = {"data": item, "tasks": todousermaping.get(userid).get("tasks")}
            else:
                logging.info("No To DO Task Found For User Id %s" % str(userid))
        self.logger.info("Users With At Least 50% Completed Task In Given City Are As Follow")
        # json output
        output  = []
        config = configparser.ConfigParser()
        config.read('coloums.cfg')
        userkeys = config.get("keys", "userkeys").split(",")
        for key in usertodocompeted.keys():
            pass








if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('coloums.cfg')
    print(config.get("keys", "userkeys"))
    obj = FanCode("http://jsonplaceholder.typicode.com/", [5, 100],[-40, 5])
    #obj.main()

