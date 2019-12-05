# Druidpy

Druidpy provides all the required methods to use the Druid ( an open source database which gives sub second query performance ). Druidpy makes life of druid users easy and simple. 

# Overview

Druid users will be doing the below regular activities for working with druid and all of these activities can be done using the druidpy

  - Perform an ingestion
  - Post a lookup
  - Delete a lookup
  - Query the datasource
  - Get the meta details about datasource/Lookup/node
  - Get the status of nodes
  - Get the details about overlord leader & coordinator leader
  - Get the lookup status 
  - Get the list of datasources/intervals/segments/lookups


# Usage

In the following paragraphs, I am going to describe how you can get and use druidpy for your own projects.

# Downloading it

To download druidpy, either fork this github repo or simply use Pypi via pip.

            $ pip install druidpy

# Using it


            from druidpy import Druid
            
# Available methods to use

     get_status(url)  
         This function returns the status of node passed. Url is the connection url of any druid process type like broker, coordintor,overlord etc.
         example : get_status("http://localhost:8090")

     get_health(url) 
        This function returns the health of the node passed. Url is the connection url of any druid process type like broker, coordintor,overlord etc.
        example : get_health("http://localhost:8090")

     coordinator_leader(coordinator_url)
        This function returns the current  coordinator leader.
        example : coordinator_leader("http://localhost:8081")

     overlord_leader(overlord_url)  
        This function returns the current  overlord leader.
        example : overlord_leader("http://localhost:8090")

     list_datasources(coordinator_url)
        This function returns the list of all the data sources available in the cluster of which the passsed coordinator belongs to.
        example : list_datasources("http://localhost:8081")

     list_segments(coordinator_url, datasource)
        This function returns the list of all the available segments for the passed data source.
        example : list_segments("http://localhost:8081","wikipedia")

     list_intervals(coordinator_url, dataset)
        This function returns the list of all the available intervals for the passed data source.
        example : list_intervals("http://localhost:8081","wikipedia")

     datasource_meta(coordinator_url, dataset)
        This function returns the meta data of the passed data source.
        example : datasource_meta("http://localhost:8081","wikipedia")

     list_tiers(coordinator_url)
        This function returns all the lookup tiers available in  the  cluster.
        example : list_tiers("http://localhost:8081")

     list_lookups(coordinator_url, tier)
        This function returns all the lookups available in the cluster.
        example : list_lookups("http://localhost:8081")

     lookup_meta(coordinator_url, tier, lookup)  
        This function returns the meta data of the passed lookup within the given tier.
        example : list_lookups("http://localhost:8081","_default_tier","test_lkp")

     lookup_status(coordinator_url, tier, lookup)
        This function returns the state of all the lookups available in the given tier , if the lookup name passed as the parameter then it will return the status of the lookup.
        example : list_lookups("http://localhost:8081","_default_tier","test_lkp") 
                  list_lookups("http://localhost:8081","_default_tier")

     list_lookups_by_state(coordinator_url, tier, state)
        This function returns all the lookups with the requested state in the given tier. By default all the lookups with the `True` state will be returned
         example : list_lookups_by_state("http://localhost:8081","_default_tier",True)  
                   list_lookups_by_state("http://localhost:8081","_default_tier",False) 

     lookup_post(coordinator_url, tier, lookup name, mysql_jdbc, db_user, db_password, key_column, val_column, poll_min):  
        This function can be used to post the lookup into druid cluster with the given details
        example : lookup_post("http://localhost:8081","_default_tier","test_lkp","<jdbc url of the metastore database with port number>","<db user name>","<db password>","tst_key_col","tst_desc_col","10")
        
     lookup_delete(coordinator_url, tier, lookup)  
        This function can be used to delete the lookup in the given tier.
        example: lookup_delete("http://localhost:8081", "_default_tier", "test_lkp")

     data_query(broker_url, query)  
        This function can be used to query the data sources availble in the druid.
        example : data_query("http://localhost:8082", "select count(*) from wikipedia") 

     ingest_task(overlord_url, ingestion_spec)  
        This function can be used to post the ingestion task to overlord
        example : ingest_task("http://localhost:8090", "/u/users/sampleuser/wikipedia_ingestion.json") 
            
And you are ready to go!




# License
MIT License
Copyright (c) 2018 NARESH KUMAR B N
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
