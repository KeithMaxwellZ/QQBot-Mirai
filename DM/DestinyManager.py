import requests
from DM.manifest_fetcher import manifest_fetcher
from p_var import *


def get_characters(membershipType, destinyMembershipId):
    # Get character
    url = BASE + f"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/"
    print(url)
    param_get_char = {"components": [200, 202]}
    r = requests.get(url, headers=HEADER, params=param_get_char)
    rj = r.json()
    return rj['Response']['characterProgressions']['data'], rj['Response']['characters']['data']


def character_milestone_prog(c_data):
    def quest_progress(lst):
        finished = False
        progress = -1
        total = -1
        for q in lst:
            if q['complete']:
                finished = True
                break
            else:
                total = q['completionValue']
                progress = max(progress, q['progress'])
        return finished, progress, total

    def activity_process(lst):
        finished = False
        progress = -1
        total = -1
        for x in lst:
            for c in x['challenges']:
                if c['objective']['complete']:
                    finished = True
                    break
                else:
                    progress = max(progress, c['objective']['progress'])
                    total = c['objective']['completionValue']
            if finished:
                break
        return finished, progress, total

    res = {}
    for k, v in c_data['milestones'].items():
        m_def = mileStonesDef[k]
        if m_def['showInMilestones'] is True:
            print(m_def['displayProperties']['name'])
            print(m_def['displayProperties']['description'])

            td = {
                "description": m_def['displayProperties']['description']
            }

            if 'availableQuests' in v.keys():
                d = v['availableQuests'][0]['status']['stepObjectives']
                dr, dp, dt = quest_progress(d)
                if dr:
                    td['status'] = "Finished"
                    print('finished')
                else:
                    td['status'] = f'{dp}/{dt}'
                    print(f'{dp}/{dt}')



            elif 'activities' in v.keys():
                d = v['activities']
                dr, dp, dt = activity_process(d)
                if dr:
                    td['status'] = "Finished"
                    print('finished')
                else:
                    td['status'] = f'{dp}/{dt}'
                    print(f'{dp}/{dt}')
            else:
                continue
            res[m_def['displayProperties']['name']] = td
    return res


mf = manifest_fetcher()
mileStonesDef = mf.get_specific('DestinyMilestoneDefinition')
