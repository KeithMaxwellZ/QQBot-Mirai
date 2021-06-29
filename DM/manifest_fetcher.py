import requests
from p_var import BASE, HEADER


class manifest_fetcher:
    def __init__(self):
        self.ind = {}
        self.archived = {}
        self.manifest_database = {}
        self.preproc()

    def preproc(self):
        self.update_manifest()
        for i in self.manifest_database.keys():
            self.ind[i] = None
            self.archived[i] = None

    def update_manifest(self):
        url = BASE + "/Destiny2/Manifest/"
        r = requests.get(url, headers=HEADER)
        rj = r.json()
        self.manifest_database = rj['Response']['jsonWorldComponentContentPaths']['zh-chs']

    # Get specific manifest from dict
    def get_specific(self, k: str) -> dict:
        if k in self.manifest_database.keys():
            val = self.manifest_database[k]
            file_name = val.split('/')[-1]
            if self.ind[k] == file_name:
                return self.archived[k]
            else:
                url = "https://www.bungie.net/" + self.manifest_database[k]
                r = requests.get(url)
                rj = r.json()
                self.ind[k] = self.manifest_database[k].split('/')[-1]
                self.archived[k] = rj
                return rj
        else:
            raise Exception(f"key {k} not found")
