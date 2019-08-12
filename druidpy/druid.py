import os
import sys
import json
import string
import requests


class Druid():
    def __init__(self):
        print(" ")

    def print_list(self, list_obj):
        for i in list_obj:
            print((json.dumps(i)).strip('\"'))

    def get_status(self, url):  # Get the status of the node
        try:
            v_url = url+"/status"
            r = requests.get(v_url)
            return r.content
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    def get_health(self, url):  # get the health of the node
        try:
            url = url+"/status/health"
            r = requests.get(url)
            return r.content

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    def raise_error(self, response):
        if response.status_code != 200:
            print("oops!.. Something went wrong ! Please check the values passed!!")
            raise SystemExit()

    # get the current leader f coordinator
    def coordinator_leader(self, coordinator_url):
        try:
            url = coordinator_url+"/druid/coordinator/v1/leader"
            r = requests.get(url)
            return r.content

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    def overlord_leader(self, overlord_url):  # get the current leader of the overlord
        try:
            url = overlord_url+"/druid/indexer/v1/leader"
            r = requests.get(url)
            return r.content

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    # return the list of datasources available
    def list_datasources(self, coordinator_url):
        try:
            url = coordinator_url+"/druid/coordinator/v1/datasources"
            r = requests.get(url)
            res = json.loads(r.content)
            return self.print_list(res)

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    # return the list of segments of given datasource
    def list_segments(self, coordinator_url, dataset):
        try:
            url = coordinator_url+"/druid/coordinator/v1/metadata/datasources/"+dataset+"/segments"
            r = requests.get(url)
            self.raise_error(r)
            res = (json.loads(r.content))
            return self.print_list(res)

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    # return the list of intervals for given datasource
    def list_intervals(self, coordinator_url, dataset):
        try:
            url = coordinator_url+"/druid/coordinator/v1/datasources/"+dataset+"/intervals?simple"
            r = requests.get(url)
            self.raise_error(r)
            v = dict()
            v = json.loads(r.content)
            for n in v.items():
                print(n)

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    # return the metadata of the given datasource
    def datasource_meta(self, coordinator_url, dataset):
        try:
            url = coordinator_url+"/druid/coordinator/v1/datasources/"+dataset
            r = requests.get(url)
            self.raise_error(r)
            return (r.content)

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    # list the tiers available in the cluster
    def list_tiers(self, coordinator_url, formatting=True):
        try:
            url = coordinator_url+"/druid/coordinator/v1/lookups/config"
            r = requests.get(url)
            self.raise_error(r)
            res = json.loads(r.content)
            if formatting == True:
                return self.print_list(res)
            else:
                return res

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    # return all the lookups loaded int the cluster
    def list_lookups(self, coordinator_url, tier, formatting=True):
        try:
            if tier not in self.list_tiers(coordinator_url, False):
                raise SystemExit("oops!... please check the tier name passed!")

            url = coordinator_url+"/druid/coordinator/v1/lookups/config/"+tier
            r = requests.get(url)
            res = json.loads(r.content)
            if formatting == True:
                return self.print_list(res)
            else:
                return res

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    def lookup_meta(self, coordinator_url, tier, lookup):  # return the meta of a lookup
        try:
            if tier not in self.list_tiers(coordinator_url, False):
                raise SystemExit("oops!... please check the tier name passed!")

            url = coordinator_url+"/druid/coordinator/v1/lookups/config/"+tier+"/"+lookup
            r = requests.get(url)
            return json.loads(r.content)

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    # return the status of lookup(s)
    def lookup_status(self, coordinator_url, tier='', lookup=''):
        try:
            if len(lookup) > 1:
                url = coordinator_url+"/druid/coordinator/v1/lookups/status/"+tier+"/"+lookup
                r = requests.get(url)
                return (json.loads(r.content, encoding="UTF-8").values())
            else:
                url = coordinator_url+"/druid/coordinator/v1/lookups/status/"+tier
                r = requests.get(url)
                return json.loads(r.content)

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    def list_lookups_by_state(self, coordinator_url, tier, state=True):
        try:
            url = coordinator_url+"/druid/coordinator/v1/lookups/status/"+tier
            fin_list = list()
            r = requests.get(url)
            res = (json.loads(r.content))
            for i in res.items():
                if i[1]['loaded'] == state:
                    fin_list.append(i)
            return self.print_list(fin_list)

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    def lookup_post(self, coordinator_url, tier, lookup, mysql_jdbc, db_user, db_password, key_column, val_column, poll_min):  # post the lookup into druid
        try:
            if tier not in self.list_tiers(coordinator_url, False):
                raise SystemExit("oops!... please check the tier name passed!")

            if lookup not in self.list_lookups(coordinator_url, tier, False):
                new_version = 0
            else:
                vdata = ''
                res = lookup_meta(coordinator_url, tier, lookup)
                version = res["version"][1:]
                new_version = int(version)+1

            vdata = '{"'+tier+'":{''"'+lookup+'":{"version":"' + 'v'+str(new_version)+'"'+',"lookupExtractorFactory":{' + '"type":"cachedNamespace",'+'"extractionNamespace":{'+'"type":"jdbc",'+'"connectorConfig":{'+'"createTables":true,'+'"connectURI":"'+''+mysql_jdbc + \
                '",'+'"user":"'+db_user+'",'+'"password":"'+db_password+'"'+'},'+'"table":"'+lookup+'",'+'"keyColumn":"'+key_column+'",' + \
                    '"valueColumn":"'+val_column+'",'+'"pollPeriod": "PT' + \
                str(poll_min)+'M"'+'},' + \
                '"firstCacheTimeout":120000,"injective":true' + '}}}}'
            headers = {'Content-Type': 'application/json'}
            url = coordinator_url+"/druid/coordinator/v1/lookups/config"
            r = requests.post(url, data=vdata, headers=headers)

            if r.status_code != 202:
                raise SystemExit("oops!... please check the values  passed!")
            else:
                print("Success : Lookup Posted!")

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    def lookup_delete(self, coordinator_url, tier, lookup):  # delete the lookup
        try:

            if tier not in self.list_tiers(coordinator_url, False):
                raise SystemExit("oops!... please check the tier name passed!")

            if lookup not in self.list_lookups(coordinator_url, tier, False):
                raise SystemExit("oops!...Lookup not found!")

            url = coordinator_url+"/druid/coordinator/v1/lookups/config/"+tier+"/"+lookup
            r = requests.delete(url)

            if r.status_code != 202:
                raise SystemExit("oop!... please check the values  passed!")
            else:
                print("Request for lookup delete posted !")
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    def data_query(self, broker_url, query):  # query the datasources

        try:
            url = broker_url+"/druid/v2/sql?pretty"
            data = '{\"query\":\"'+query+'"}'
            headers = {'Content-type': 'application/json'}
            r = requests.post(url, data=data, headers=headers)
            self.raise_error(r)
            return (r.content)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    def ingest_task(self, overlord_url, ingestion_spec):  # post the ingest task

        try:
            if os.path.exists(ingestion_spec) == False:
                raise SystemExit(
                    "oops! Ingestion spec file does not exists , Please check!")

            headers = {'Content-Type': 'application/json'}
            url = overlord_url+'/druid/indexer/v1/task'

            with open(ingestion_spec, 'r') as f:
                data = f.read()

            r = requests.post(url, headers=headers, data=data)

            if r.status_code != 200:
                raise SystemExit("Task posting is Failed, Please check!")

            p_dict = json.loads(r.content)
            task_id = p_dict['task']
            print("task id is {}".format(task_id))

            status_check_url = overlord_url+'/druid/indexer/v1/task/'+task_id+'/status'
            print(status_check_url)
            st = requests.get(status_check_url, headers=headers)
            g_dict = json.loads(st.content)
            ing_status = g_dict['status']['status']
            print("Ingestion task is in progress...!.")
            cond = True
            while cond:
                if ing_status == 'SUCCESS' or ing_status == 'FAILED':
                    break
                else:
                    r = requests.get(status_check_url, headers=headers)
                    g_dict = json.loads(r.content)
                    ing_status = g_dict['status']['status']

            if ing_status == 'FAILED':
                raise SystemExit(
                    "Ingestion task is failed, please check overlord logs!")
            else:
                return "ingestion is successfull"

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
