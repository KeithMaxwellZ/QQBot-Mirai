import requests
from pprint import pprint
from p_var import BASE, HEADER


class profile_fetcher:
    def __init__(self, id: str = None):
        self.id = id
        self.membershipData = []

    def get_membership_type(self, membershipType=-1):
        url = BASE + f"/User/GetMembershipsById/{self.id}/{membershipType}/"
        print(url)
        r = requests.get(url, headers=HEADER)
        rj = r.json()
        pprint(rj)
        if rj['ErrorCode'] != 1:
            return -1
        for x in rj['Response']['destinyMemberships']:
            self.membershipData.append([x['membershipType'], x['membershipId']])
        if "primaryMembershipId" in rj['Response'].keys():
            self.membershipData.sort(key=lambda xv: xv[0] == rj['Response']['primaryMembershipId'], reverse=True)
        return 0

    def save_data(self):
        res = {
            "id": self.id,
            "membershipData": self.membershipData,
        }

        return res

    def load_data(self, paylaod:dict):
        self.id = paylaod["id"]
        self.membershipData = paylaod["membershipData"]
