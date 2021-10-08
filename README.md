# **datagovindia**

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/addypy/datagovindia/blob/master/LICENSE.txt) [![Downloads](https://static.pepy.tech/personalized-badge/datagovindia?period=total&units=international_system&left_color=grey&right_color=limegreen&left_text=Downloads)](https://pepy.tech/project/datagovindia)


### A Python API-wrapper for Government of India’s [Open Government Data OGD platform](https://data.gov.in/)
**`datagovindia`** is an API wrapper for `117186` (and counting) APIs available at Government of India’s *[Open Government Data OGD platform](https://data.gov.in/ogpl_apis)*

-------

## Features
> - **DISCOVERY**
>> *Find the right API resource.*
> - **INFORMATION**
>> *Retrieve information about an API resource.*
> - **DATA**
>> *Download data in a convenient pandas DataFrame from the chosen API.*

## Prerequisites

>  - An account on *data.gov.in*
>  - An API key from the My Account page
    - (Instructions here : [Official Guide](https://data.gov.in/help/how-use-datasets-apis))

## Installation
> - Using PIP
```sh
pip install -U datagovindia
```
-------
> - Clone the Git-Repository
```sh
git clone https://github.com/addypy/datagovindia

python setup.py install

```

## Basic Usage

### Import Library
```python
from datagovindia import DataGovIndia
```

### Initialize Class
```python
datagovin = DataGovIndia("579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b")
```

> Performs :
>> 1) Tests datagov.in API-server status.
>> 2) Validates API-Key. You only need to set this once.
>> 2) Fetches latest details about available APIs.

### Search
```python
datagovin.search(description="Wheat",max_results=1,print_results=True)
```

> Output:

```
# Returns:
1 of 395 results      

==================================================================================

Resource-ID:	4c88fba5e3174e06a34af33194ab4b2d

Daily FCI Stock postion of the commodity Wheat, for the Haryana region in 2019 (till last week)

==================================================================================
```

> Returns:

```json

[{"4c88fba5e3174e06a34af33194ab4b2d": "Daily FCI Stock postion of the commodity Wheat, for the Haryana region in 2019 (till last week)"}]

```

### Download Data
```python
data = datagovin.get_data("b7ea044ea17149ed886c37ed5729b75a",num_results='all')
data.head()
```

> Returns:

|date                |code                |commodityid|commodityname       |districtname|districtcode|stock         |commoditystock|totalstock    |
|--------------------|--------------------|-----------|--------------------|------------|------------|--------------|--------------|--------------|
|2019-07-20T00:00:00Z|Region Name: Haryana|01         |Wheat(Including URS)|FARIDABAD   |NC12        |2214591.87343 |35769407.44149|35769407.44149|
|2019-07-20T00:00:00Z|Region Name: Haryana|01         |Wheat(Including URS)|HISSAR      |NC13        |17954629.80074|35769407.44149|35769407.44149|
|2019-07-20T00:00:00Z|Region Name: Haryana|01         |Wheat(Including URS)|KARNAL      |NC14        |1787375.5789  |35769407.44149|35769407.44149|
|2019-07-20T00:00:00Z|Region Name: Haryana|01         |Wheat(Including URS)|KURUKSHETRA |NC15        |3552965.00293 |35769407.44149|35769407.44149|
|2019-07-20T00:00:00Z|Region Name: Haryana|01         |Wheat(Including URS)|ROHTAK      |NC16        |10259845.18549|35769407.44149|35769407.44149|

-------
________

## Detailed Examples

--------

> ## A. **SETUP**
> ### Import *`DataGovIndia`* from *`datagovindia`*

```python
from datagovindia import DataGovIndia
```
> ### Get `API-KEY` from *[data.gov.in/user](https://data.gov.in/user)*
>
> See : [Official Guide](https://data.gov.in/help/how-use-datasets-apis)

```python
api_key = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
```

> ### Initialize Class

```python
# Initializing the library -
# 1) Tests datagov.in API-server status.
# 2) Validates API-Key. You only need to set this once.
# 2) Fetches latest details about available APIs.


datagovin = DataGovIndia(api_key)

# The API key you provided is valid. You won't need to set it again.
# Latest resources loaded. You may begin.                                                    
```

--------

> ## B. **DISCOVERY**

## Check available ***`attributes`***

### 1. List of ***`Organization-Names`***

```python
datagovin.list_org_names()

# Returns:
['Adi Dravidar and Tribal Welfare Department, Tamil Nadu',
 'Agriculture Department',
 'Agriculture Department, Meghalaya',
     ...,
 'Department of AIDS Control',
 'Department of Agricultural Research and Education (DARE)',
 'Department of Animal Husbandry, Dairying and Fisheries',
 'Department of Atomic Energy',
     ....,
 'Micro Small and Medium Enterprises Department, Tamil Nadu',
 'Ministry of Agriculture and Farmers Welfare',
    ....,
]
```

### 2. List of ***`Organization-Types`***

```python
datagovin.list_org_types()

# Returns:
['Central',
 'City',
 'State']

```
### 3. List of ***`Sectors`***
```python
datagovin.list_sectors()

# Returns:
['Adult Education',
'Agricultural',
'Agricultural Marketing',
'Agricultural Research & Extension',
'Agriculture',
    .
    .,
'Water Quality',
'Water Resources',
'Water and Sanitation',
'Water ways']
```

### 4. List of ***`Sources`***

```python
datagovin.list_sources()

# Returns:
['data.gov.in', 'smartcities.data.gov.in', 'tn.data.gov.in']
```

### 5. List of ***`All Attributes`***
```python
datagovin.list_all_attributes()
# Returns:
```    
```json
 { "org_types": ["Central", "City", "State"],  
  "sources": ["data.gov.in", "smartcities.data.gov.in", "tn.data.gov.in"],       
 "org_names": [ "Adi Dravidar and Tribal Welfare Department, Tamil Nadu",
                 "Agricultural Census, New Delhi",
                 "Agriculture Department",
                        ,
                        ,
                        ,
                 "Department of Agriculture, Cooperation and Farmers Welfare",
                 "Department of Animal Husbandry, Dairying and Fisheries",
                 "Department of Atomic Energy",
                 "Department of Ayurveda, Yoga and Naturopathy, Unani, Siddha "
                        ,
                        ,
                        ,
                 "Tourism, Culture and Religious Endowments Department",
                 "Transport Department, Madhya Pradesh",
                 "Transport Department, Tamil Nadu",
                        ,
                        ,
                 "West Bengal"],
  "sectors": [ "Adult Education",
               "Agricultural",
               "Agricultural Marketing",
               "Agriculture",
                        ,
                        ,          
               "Atmospheric Science",
               "Aviation",
               "Banking",
               "Biotechnology",
               "Broadcasting",
               "Census",
                        ,
                        ,          
               "District Adminstration",
               "Drinking Water",
               "Earth Sciences",,
               "Education",
               "Employment",
               "Environment and Forest",
                        ,
                        ,               
               "Municipal Waste",
               "National Population Register",
               "Natural Resources",
               "Noise Pollution",
               "Panchayati Raj",
               "Parliament Of india",
               "Passport",
               "Power and Energy",
                        ,
                        ,            
               "Water Quality",
               "Water Resources",
               "Water and Sanitation",
               "Water ways"]
               }
```

### 6. List of ***`recently created resources`***

```python
datagovin.list_recently_created(days=5,max_results=5,print_results=True)
```
```
# Prints:

5 of 1443 results that were created in the last - `5` days

==================================================================================

Resource-ID:	52d2933f69be46fda28855c08134fc7f
18 June 2021, 09:57 AM
Allocations for The Welfare of Schedule Caste from 2019-20 to 2021-22

==================================================================================

Resource-ID:	2ef7903b77f04609af93bb54516c125c
18 June 2021, 09:57 AM
Allocations for The Welfare of Schedule Tribes from 2019-20 to 2021-22

==================================================================================

Resource-ID:	8a679d8db6d94605a1d160150fe22b77
18 June 2021, 09:57 AM
Allocations for the Welfare of Children from 2019-20 to 2021-22

==================================================================================

Resource-ID:	243825f60f304a10877dd1f86ad49598
18 June 2021, 09:27 AM
Monthly Range-wise Performance of Public Facilities for Deliveries conducted at facility for May 2013-14

==================================================================================

Resource-ID:	a5d0bd7d39e84392b65abe5e4737f865
18 June 2021, 09:26 AM
Monthly Range-wise Performance of Public Facilities for Deliveries conducted at facility for September 2018-19

==================================================================================
```
```json
# Returns:
[{"resourceid": "52d2933f69be46fda28855c08134fc7f",
  "timestamp": 1623990466,
  "title": "Allocations for The Welfare of Schedule Caste from 2019-20 to 2021-22"},
 {"resourceid": "2ef7903b77f04609af93bb54516c125c",
  "timestamp": 1623990466,
  "title": "Allocations for The Welfare of Schedule Tribes from 2019-20 to 2021-22"},
 {"resourceid": "8a679d8db6d94605a1d160150fe22b77",
  "timestamp": 1623990441,
  "title": "Allocations for the Welfare of Children from 2019-20 to 2021-22"},
 {"resourceid": "243825f60f304a10877dd1f86ad49598",
  "timestamp": 1623988620,
  "title": "Monthly Range-wise Performance of Public Facilities for Deliveries conducted at facility for May 2013-14"},
 {"resourceid": "a5d0bd7d39e84392b65abe5e4737f865",
  "timestamp": 1623988618,
  "title": "Monthly Range-wise Performance of Public Facilities for Deliveries conducted at facility for September 2018-19"}]
```

### 7. List of ***`recently updated resources`***
```python
datagovin.list_recently_updated(days=3,max_results=5,print_results=True)

```
```
# Prints:

5 of 303 results that were updated in the last - `3` days

==================================================================================

Resource-ID:	9ef84268d588465aa308a864a43d0070
21 June 2021, 02:05 PM
Current Daily Price of Various Commodities from Various Markets (Mandi)

==================================================================================

Resource-ID:	3b01bcb80b144abfb6f2c1bfd384ba69
21 June 2021, 12:03 PM
Real time Air Quality Index from various location

==================================================================================

Resource-ID:	d76a86b16a2a4ab39201cb9f6bc61fa4
21 June 2021, 08:50 AM
District Wise Total MSME Registered Service Enterprises till last date

==================================================================================

Resource-ID:	925bb7dd50f048768a1da5e45c4a989a
21 June 2021, 08:50 AM
District Wise Total MSME Registered Manufacturing and Service Enterprises till last date

==================================================================================

Resource-ID:	201b66f27fda40b8b613ffb7789c4341
21 June 2021, 08:50 AM
District Wise Total MSME Registered Manufacturing Enterprises till last date

==================================================================================
```

```json
# Returns:
[{"resourceid": "9ef84268d588465aa308a864a43d0070",
  "timestamp": 1624264506,
  "title": "Current Daily Price of Various Commodities from Various Markets (Mandi)"},
 {"resourceid": "3b01bcb80b144abfb6f2c1bfd384ba69",
  "timestamp": 1624257197,
  "title": "Real time Air Quality Index from various location"},
 {"resourceid": "d76a86b16a2a4ab39201cb9f6bc61fa4",
  "timestamp": 1624245637,
  "title": "District Wise Total MSME Registered Service Enterprises till last date"},
 {"resourceid": "925bb7dd50f048768a1da5e45c4a989a",
  "timestamp": 1624245633,
  "title": "District Wise Total MSME Registered Manufacturing and Service Enterprises till last date"},
 {"resourceid": "201b66f27fda40b8b613ffb7789c4341",
  "timestamp": 1624245629,
  "title": "District Wise Total MSME Registered Manufacturing Enterprises till last date"}]
```
## Searching for a dataset (API-Resource)
---
### 1. *Search* for resource using **`TITLE`**

```python
results = datagovin.search_by_title("MGNREGA",max_results=5,print_results=True)
```

```
# Returns:
5 of 45 results for : `MGNREGA`

==================================================================================

Resource-ID:    bf1da9fc565045c3be3b0ba006377869

Expenditure under MGNREGA on Schedule Caste (SC) Persondays during 2015-16 and 2018-19 (From: Ministry of Rural Development)

==================================================================================

Resource-ID:    9aa66b7abb1d4e20bd4be5e68539cdfc

Central Fund Released to Jammu and Kashmir under MGNREGA from 2016-17 to 2018-19 (From: Ministry of Rural Development)

==================================================================================

Resource-ID:    57bff16a642345b29700ebcde6709937

State/UT-wise Expenditure Reported in Management Information System (MIS) under MGNREGA from 2014-15 to 2018-19 (From: Ministry of Labour and Employment)

==================================================================================

Resource-ID:    8e7b41bec79044958339c8da0a7f287e

State/UT-wise Expenditure made on Water Related Works Taken up under MGNREGA from 2016-17 to 2019-20 (From: Ministry of Jal Shakti)

==================================================================================

Resource-ID:    7371da1e4c5e4c529223f85e1756d24d

District-wise expenditure under the Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA) in the state Punjab from 2017-18 to 2019-20 (From: Ministry of Rural Development)

==================================================================================
```

### 2. *Search* for resource using **`DESCRIPTION`**

```python
results = datagovin.search_by_description("Swachh Bharat Mission",max_results=5,print_results=True)
```

```
# Returns:
5 of 25 results for : `Swachh Bharat Mission`

==================================================================================

Resource-ID:    22f496bb32a84b6da4124f03c4b3ea62

District-wise Target vs Achievement of Construction of Toilets in State of Chhattisgarh under Swachh Bharat Mission (SBM) from 2013-14 to 2017-18 (From : Ministry of Tribal Affairs)

==================================================================================

Resource-ID:    673d72fc1c8a497d80477c3c72196e74

State/UT-wise Number of IHHLs Constructed under Swachh Bharat Mission - Gramin (SBM-G) from 02 October, 2014 to 17 July, 2019 (From : Ministry of Jal Shakti)

==================================================================================

Resource-ID:    2235bc9138cc4a4dbf5413e485596d5c

Funds Sanctioned, Allocated and Utilised under Swachh Bharat Mission (SBM) in Chhattisgarh from 2016-17 to 2018-19 (From: Ministry of Jal Shakti, Department of Drinking Water and Sanitation)

==================================================================================

Resource-ID:    45bb18686df44011b5fbbd5d74a01eda

Details of Fund (including Swachh Bharat Cess) Allocated & Released under Swachh Bharat Mission (Rural/Urban) from 2016-17 to 2018-19 (From: Ministry of Finance)

==================================================================================

Resource-ID:    5329bcc7f75f4a87be6a0bdaa6ebb4b4

Funds Allocated, Released, Balance and Utilization Certificate received under Swachh Bharat Mission (Urban) as on 30th November, 2019 (From: Ministry of Housing and Urban Affairs)

==================================================================================
```

### 3. ***Search*** for resources by `SOURCE`

```python
results = datagovin.search_by_source("tn.data.gov.in",max_results=3,print_results=True)
```

```
# Returns:
3 of 526 results for `source` : `tn.data.gov.in`

==================================================================================

Resource-ID:    952da80341cd41e990bcbcb760ffbf90

Area, Production & Productivity of Snake Gourd (Vegetables) by District-wise in Tamil Nadu for the Year 2015-16

==================================================================================

Resource-ID:    0bd2498df63c456a9f336e242e9abe82

Area, Production & Productivity of Chrysanthimum (Flowers) by District-wise in Tamil Nadu for the Year 2015-16

==================================================================================

Resource-ID:    921f5b1f093146399c96a00195e17881

Area, Production & Productivity of Jadhi Malli (Flowers) by District-wise in Tamil Nadu for the Year 2015-16

==================================================================================
```

### 4. ***Search for resources by*** `SECTOR`

```python
results = datagovin.search_by_sector("Banking",max_results=3,print_results=True)
```

```
# Returns:
3 of 45 results for `sector` : `Banking`

==================================================================================

Resource-ID:    4b9dd94d36be4f968578f8981857773c

Month-wise Progress Report of PMJDY by Public Sectors Banks/Regional Rural Banks/Private Banks upto 24-Feb-2016

==================================================================================

Resource-ID:    f719ee5c50254643aa54157d707d6077

Liabilities and assets of different classes of banks - scheduled commercial banks as on 31st March - State Bank of India from 2001 to 2014

==================================================================================

Resource-ID:    371020a7a43747df8946fbd030b53459

Liabilities And Assets Of State Financial Corporations (State-wise) upto 2012-13

==================================================================================
```

### 5. ***Search for resources by*** `ORG-NAME`

```python
results = datagovin.search_by_org_name("Ministry of Road Transport and Highways",max_results=5,print_results=True)
```

```
# Returns:
5 of 417 results for `organization` - `Ministry of Road Transport and Highways`

==================================================================================

Resource-ID:    37b1f841f44c490682fb2442b0f2bd25

State/UT-wise Length of Roads under Coal Fields/Coal units of Coal India Limited by Type of Surface as on 31st March, 2017

==================================================================================

Resource-ID:    b10ac9f5c1fd42c78c19e74a1fe64c04

State/UT-wise Length of Roads under Forest Departments by Type of Surface in India as on 31st March, 2017

==================================================================================

Resource-ID:    8ebce90f62e8421592672bf22bac7f94

State-wise Length of Roads in Major Ports by Type of Surface as on 31st March, 2017

==================================================================================

Resource-ID:    888f4d498c864f1c825feef9db674cc8

State/UT-wise Length of Military Engineering Service Roads by Type of Surface as on 31st March, 2017

==================================================================================

Resource-ID:    068ecf9440694838981b3529c3a48edc

State/UT-wise Length of PMGSY Roads by type of Surface as on 31st March, 2017

==================================================================================
```

### 6. *Search* for resources by `ORG-TYPE`

```python
results = datagovin.search_by_org_type("State",max_results=5,print_results=True)
```

```
# Returns:
5 of 645 results for `organization type` - `State`

==================================================================================

Resource-ID:    4200eb5f17294fee8477af5feb715b3c

Details of Vehicle Tax collected by Surat Municipal Corporation from Year 1989 onward

==================================================================================

Resource-ID:    fbdf3432b88a4592bbc4d0f60a0ac140

Surat City Bus and BRTS Passenger Information from April 2015 (daily)

==================================================================================

Resource-ID:    993acfe3b72e4e07895915aa34bc226d

Building Plan Applications at Surat Municipal Corporation from April 2015 onward (daily)

==================================================================================

Resource-ID:    8addc59332b54531a2346057209f35a0

Surat City Complaint Statistics from April 2015 onward (daily)

==================================================================================

Resource-ID:    3968cb03596842c9ac43cba988a964c7

Garbage Collection in Surat City (in KG) from April 2015 onward (daily)

==================================================================================
```

### 7. *Search* for resources with **`Multiple Filters`**

```python
results = datagovin.search(title="COVID",
                            description="Postiive Case",
                            org_name="Surat",
                            org_type="City",
                            sector="All",
                            source="smartcities.data.gov.in",
                            max_results=5,
                            print_results=True,
                          )
```

```
# Returns:
2 of 2 results        

==================================================================================

Resource-ID:    b9cfed4ca1a24f7aaffa88a8e1a2149c

COVID-19 Positive Case Details

==================================================================================

Resource-ID:    ee35f0724d804b418c17fd74414907be

COVID-19 Cluster / Containment Zone Details

==================================================================================
```


--------


> ## C. **Learn more about an API-resource.**

>> ### 1. Get all available `meta-data` for an API resource

> Meta-Data includes -
>
> - Resource-ID
> - Title
> - Description
> - Total records available
> - Date-Created
> - Data-Updated
> - Organization-Type
> - Organization-Name
> - Source
> - Sector
> - Fields

```python
datagovin.get_resource_info("b9cfed4ca1a24f7aaffa88a8e1a2149c")
```

```json
{"ResourceID": "b9cfed4ca1a24f7aaffa88a8e1a2149c",
 "Title": "COVID-19 Positive Case Details",
 "Description": "COVID-19 Positive Case Details",
 "TotalRecords": 3592,
 "DateCreated": "08 May 2020, 09:00 PM",
 "DateUdpated": "10 January 2021, 11:04 PM",
 "OrganizationNames": ["Gujarat", "Surat"],
 "OrganizationTypes": "City",
 "Sector": "All",
 "Source": "smartcities.data.gov.in",
 "Fields": ["sr_no",
            "city",
            "zone",
            "age",
            "gender",
            "latitude",
            "longitude",
            "result",
            "sample_result",
            "resultdate"]}
```            

>> ### 2. Get details of `fields` (variables) available for a resource.

```python
datagovin.get_resource_fields("b9cfed4ca1a24f7aaffa88a8e1a2149c")
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>field_code</th>
      <th>field_label</th>
      <th>field_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>sr_no</td>
      <td>Sr.No</td>
      <td>keyword</td>
    </tr>
    <tr>
      <th>1</th>
      <td>city</td>
      <td>City</td>
      <td>keyword</td>
    </tr>
    <tr>
      <th>2</th>
      <td>zone</td>
      <td>zone</td>
      <td>double</td>
    </tr>
    <tr>
      <th>3</th>
      <td>age</td>
      <td>age</td>
      <td>double</td>
    </tr>
    <tr>
      <th>4</th>
      <td>gender</td>
      <td>Gender</td>
      <td>keyword</td>
    </tr>
    <tr>
      <th>5</th>
      <td>latitude</td>
      <td>latitude</td>
      <td>double</td>
    </tr>
    <tr>
      <th>6</th>
      <td>longitude</td>
      <td>longitude</td>
      <td>double</td>
    </tr>
    <tr>
      <th>7</th>
      <td>result</td>
      <td>Result</td>
      <td>keyword</td>
    </tr>
    <tr>
      <th>8</th>
      <td>sample_result</td>
      <td>Sample_Result</td>
      <td>keyword</td>
    </tr>
    <tr>
      <th>9</th>
      <td>resultdate</td>
      <td>ResultDate</td>
      <td>date</td>
    </tr>
  </tbody>
</table>
</div>

--------

> ## D. **Download DATA**

```python
data = datagovin.get_data("b9cfed4ca1a24f7aaffa88a8e1a2149c")
data.head(20)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sr_no</th>
      <th>city</th>
      <th>zone</th>
      <th>age</th>
      <th>gender</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>result</th>
      <th>sample_result</th>
      <th>resultdate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Surat</td>
      <td>South West Zone</td>
      <td>21</td>
      <td>F</td>
      <td>21.1697</td>
      <td>72.7933</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>19/03/2020</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Surat</td>
      <td>Central Zone</td>
      <td>67</td>
      <td>M</td>
      <td>21.1869</td>
      <td>72.816</td>
      <td>Death</td>
      <td>Positive</td>
      <td>20/03/2020</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Surat</td>
      <td>East Zone - B</td>
      <td>50</td>
      <td>F</td>
      <td>21.21130173</td>
      <td>72.86820564</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>10/06/2020</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Surat</td>
      <td>South Zone</td>
      <td>26</td>
      <td>M</td>
      <td>21.1397</td>
      <td>72.8241</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>28/03/2020</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Surat</td>
      <td>West Zone</td>
      <td>55</td>
      <td>M</td>
      <td>21.2056124</td>
      <td>72.804538</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>11/06/2020</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>Surat</td>
      <td>North Zone</td>
      <td>47</td>
      <td>M</td>
      <td>21.2419426</td>
      <td>72.8287933</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>13/06/2020</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>Surat</td>
      <td>East Zone - B</td>
      <td>34</td>
      <td>M</td>
      <td>21.2225309</td>
      <td>72.8918084</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>17/06/2020</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>Surat</td>
      <td>North Zone</td>
      <td>39</td>
      <td>M</td>
      <td>21.2334082</td>
      <td>72.8046628</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>19/06/2020</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>20</td>
      <td>F</td>
      <td>21.1681</td>
      <td>72.8672</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>18/04/2020</td>
    </tr>
    <tr>
      <th>9</th>
      <td>10</td>
      <td>Surat</td>
      <td>West Zone</td>
      <td>32</td>
      <td>M</td>
      <td>21.2265</td>
      <td>72.7927</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>21/03/2020</td>
    </tr>
    <tr>
      <th>10</th>
      <td>11</td>
      <td>Surat</td>
      <td>Central Zone</td>
      <td>45</td>
      <td>M</td>
      <td>21.1852</td>
      <td>72.8209</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>22/03/2020</td>
    </tr>
    <tr>
      <th>11</th>
      <td>12</td>
      <td>Surat</td>
      <td>South Zone</td>
      <td>22</td>
      <td>M</td>
      <td>21.1613</td>
      <td>72.8305</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>01/04/2020</td>
    </tr>
    <tr>
      <th>12</th>
      <td>13</td>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>62</td>
      <td>M</td>
      <td>21.186</td>
      <td>72.863</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>23/03/2020</td>
    </tr>
    <tr>
      <th>13</th>
      <td>14</td>
      <td>Surat</td>
      <td>West Zone</td>
      <td>67</td>
      <td>M</td>
      <td>21.2212</td>
      <td>72.7954</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>29/03/2020</td>
    </tr>
    <tr>
      <th>14</th>
      <td>15</td>
      <td>Surat</td>
      <td>South West Zone</td>
      <td>23</td>
      <td>M</td>
      <td>21.1738</td>
      <td>72.8141</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>20/03/2020</td>
    </tr>
    <tr>
      <th>15</th>
      <td>16</td>
      <td>Surat</td>
      <td>North Zone</td>
      <td>29</td>
      <td>M</td>
      <td>21.2264</td>
      <td>72.8189</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>31/03/2020</td>
    </tr>
    <tr>
      <th>16</th>
      <td>17</td>
      <td>Surat</td>
      <td>West Zone</td>
      <td>61</td>
      <td>F</td>
      <td>21.2078</td>
      <td>72.7732</td>
      <td>Death</td>
      <td>Positive</td>
      <td>03/04/2020</td>
    </tr>
    <tr>
      <th>17</th>
      <td>18</td>
      <td>Surat</td>
      <td>South Zone</td>
      <td>40</td>
      <td>F</td>
      <td>21.1612</td>
      <td>72.8303</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>04/04/2020</td>
    </tr>
    <tr>
      <th>18</th>
      <td>19</td>
      <td>Surat</td>
      <td>Central Zone</td>
      <td>65</td>
      <td>M</td>
      <td>21.1956</td>
      <td>72.8353</td>
      <td>Death</td>
      <td>Positive</td>
      <td>04/04/2020</td>
    </tr>
    <tr>
      <th>19</th>
      <td>20</td>
      <td>Surat</td>
      <td>West Zone</td>
      <td>50</td>
      <td>M</td>
      <td>21.2015</td>
      <td>72.8085</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>05/04/2020</td>
    </tr>
  </tbody>
</table>
</div>


--------

> ## E. Filtering

```python
# First, let's take a look at valid `fields`.

datagovin.get_resource_fields("b9cfed4ca1a24f7aaffa88a8e1a2149c")
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>field_code</th>
      <th>field_label</th>
      <th>field_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>sr_no</td>
      <td>Sr.No</td>
      <td>keyword</td>
    </tr>
    <tr>
      <th>1</th>
      <td>city</td>
      <td>City</td>
      <td>keyword</td>
    </tr>
    <tr>
      <th>2</th>
      <td>zone</td>
      <td>zone</td>
      <td>double</td>
    </tr>
    <tr>
      <th>3</th>
      <td>age</td>
      <td>age</td>
      <td>double</td>
    </tr>
    <tr>
      <th>4</th>
      <td>gender</td>
      <td>Gender</td>
      <td>keyword</td>
    </tr>
    <tr>
      <th>5</th>
      <td>latitude</td>
      <td>latitude</td>
      <td>double</td>
    </tr>
    <tr>
      <th>6</th>
      <td>longitude</td>
      <td>longitude</td>
      <td>double</td>
    </tr>
    <tr>
      <th>7</th>
      <td>result</td>
      <td>Result</td>
      <td>keyword</td>
    </tr>
    <tr>
      <th>8</th>
      <td>sample_result</td>
      <td>Sample_Result</td>
      <td>keyword</td>
    </tr>
    <tr>
      <th>9</th>
      <td>resultdate</td>
      <td>ResultDate</td>
      <td>date</td>
    </tr>
  </tbody>
</table>
</div>

>> ### 1. Filtering with a *Single* ***`Field`*** - *Single* ***`Value`*** pair

```python
data = datagovin.get_data("b9cfed4ca1a24f7aaffa88a8e1a2149c",filters={"result":"Active"})
data
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sr_no</th>
      <th>city</th>
      <th>zone</th>
      <th>age</th>
      <th>gender</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>result</th>
      <th>sample_result</th>
      <th>resultdate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>511</td>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>25</td>
      <td>M</td>
      <td>21.179004</td>
      <td>72.808405</td>
      <td>Active</td>
      <td>Positive</td>
      <td>25/04/2020</td>
    </tr>
    <tr>
      <th>1</th>
      <td>951</td>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>35</td>
      <td>M</td>
      <td>21.1904773</td>
      <td>72.849517</td>
      <td>Active</td>
      <td>Positive</td>
      <td>13/05/2020</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1111</td>
      <td>Out City</td>
      <td>NA</td>
      <td>70</td>
      <td>F</td>
      <td>21.150554</td>
      <td>72.802457</td>
      <td>Active</td>
      <td>Positive</td>
      <td>18/05/2020</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1164</td>
      <td>Out City</td>
      <td>NA</td>
      <td>73</td>
      <td>M</td>
      <td>21.150554</td>
      <td>72.802457</td>
      <td>Active</td>
      <td>Positive</td>
      <td>19/05/2020</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1166</td>
      <td>Surat</td>
      <td>South Zone</td>
      <td>41</td>
      <td>M</td>
      <td>21.153726</td>
      <td>72.839782</td>
      <td>Active</td>
      <td>Positive</td>
      <td>20/05/2020</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1247</td>
      <td>Surat</td>
      <td>South Zone</td>
      <td>55</td>
      <td>M</td>
      <td>21.153215</td>
      <td>72.8267782</td>
      <td>Active</td>
      <td>Positive</td>
      <td>24/05/2020</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1361</td>
      <td>Surat</td>
      <td>South West Zone</td>
      <td>50</td>
      <td>F</td>
      <td>21.13268974</td>
      <td>72.74215644</td>
      <td>Active</td>
      <td>Positive</td>
      <td>24/05/2020</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1520</td>
      <td>Out City</td>
      <td>NA</td>
      <td>72</td>
      <td>M</td>
      <td>21.2217492</td>
      <td>72.7830429</td>
      <td>Active</td>
      <td>Positive</td>
      <td>28/05/2020</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1530</td>
      <td>Out City</td>
      <td>NA</td>
      <td>56</td>
      <td>F</td>
      <td>21.1577</td>
      <td>72.7768399</td>
      <td>Active</td>
      <td>Positive</td>
      <td>28/05/2020</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1594</td>
      <td>Out City</td>
      <td>NA</td>
      <td>53</td>
      <td>F</td>
      <td>21.1563151</td>
      <td>72.766301</td>
      <td>Active</td>
      <td>Positive</td>
      <td>30/05/2020</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2327</td>
      <td>Surat</td>
      <td>South Zone</td>
      <td>63</td>
      <td>M</td>
      <td>21.1223137</td>
      <td>72.8491477</td>
      <td>Active</td>
      <td>Positive</td>
      <td>10/06/2020</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2485</td>
      <td>Out City</td>
      <td>NA</td>
      <td>41</td>
      <td>M</td>
      <td>21.29079</td>
      <td>72.9001</td>
      <td>Active</td>
      <td>Positive</td>
      <td>13/06/2020</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2609</td>
      <td>Surat</td>
      <td>North Zone</td>
      <td>61</td>
      <td>M</td>
      <td>21.2366751</td>
      <td>72.8350334</td>
      <td>Active</td>
      <td>Positive</td>
      <td>14/06/2020</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2748</td>
      <td>Out City</td>
      <td>NA</td>
      <td>3</td>
      <td>F</td>
      <td>21.13488745</td>
      <td>72.76593804</td>
      <td>Active</td>
      <td>Positive</td>
      <td>16/06/2020</td>
    </tr>
  </tbody>
</table>
</div>

>> ### 2. Filtering with a *Single* ***`Field`*** - *Multiple* ***`Values`***

```python
datagovin.get_data("b9cfed4ca1a24f7aaffa88a8e1a2149c",filters={"result":["Active",'Cured/Discharged']})
```

<div>    
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sr_no</th>
      <th>city</th>
      <th>zone</th>
      <th>age</th>
      <th>gender</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>result</th>
      <th>sample_result</th>
      <th>resultdate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>511</td>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>25</td>
      <td>M</td>
      <td>21.179004</td>
      <td>72.808405</td>
      <td>Active</td>
      <td>Positive</td>
      <td>25/04/2020</td>
    </tr>
    <tr>
      <th>1</th>
      <td>951</td>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>35</td>
      <td>M</td>
      <td>21.1904773</td>
      <td>72.849517</td>
      <td>Active</td>
      <td>Positive</td>
      <td>13/05/2020</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1111</td>
      <td>Out City</td>
      <td>NA</td>
      <td>70</td>
      <td>F</td>
      <td>21.150554</td>
      <td>72.802457</td>
      <td>Active</td>
      <td>Positive</td>
      <td>18/05/2020</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1164</td>
      <td>Out City</td>
      <td>NA</td>
      <td>73</td>
      <td>M</td>
      <td>21.150554</td>
      <td>72.802457</td>
      <td>Active</td>
      <td>Positive</td>
      <td>19/05/2020</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1166</td>
      <td>Surat</td>
      <td>South Zone</td>
      <td>41</td>
      <td>M</td>
      <td>21.153726</td>
      <td>72.839782</td>
      <td>Active</td>
      <td>Positive</td>
      <td>20/05/2020</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>3009</th>
      <td>3189</td>
      <td>Surat</td>
      <td>North Zone</td>
      <td>50</td>
      <td>M</td>
      <td>21.226217</td>
      <td>72.817604</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>21/06/2020</td>
    </tr>
    <tr>
      <th>3010</th>
      <td>3190</td>
      <td>Surat</td>
      <td>North Zone</td>
      <td>42</td>
      <td>M</td>
      <td>21.2268099</td>
      <td>72.8256378</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>21/06/2020</td>
    </tr>
    <tr>
      <th>3011</th>
      <td>3191</td>
      <td>Surat</td>
      <td>West Zone</td>
      <td>52</td>
      <td>M</td>
      <td>21.205124</td>
      <td>72.776736</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>22/06/2020</td>
    </tr>
    <tr>
      <th>3012</th>
      <td>3193</td>
      <td>Surat</td>
      <td>North Zone</td>
      <td>26</td>
      <td>F</td>
      <td>21.2398084</td>
      <td>72.8500394</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>21/06/2020</td>
    </tr>
    <tr>
      <th>3013</th>
      <td>3194</td>
      <td>Surat</td>
      <td>North Zone</td>
      <td>49</td>
      <td>M</td>
      <td>21.2290168</td>
      <td>72.808571</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>21/06/2020</td>
    </tr>
  </tbody>
</table>
<p>3014 rows × 10 columns</p>
</div>

>> ### 3. Filtering with *Multiple* ***`Field(s)`*** - *Multiple* ***`Value(s)`***

```python
datagovin.get_data("b9cfed4ca1a24f7aaffa88a8e1a2149c",
                   filters={
                       "gender":["F","M"],
                       "result":['Cured/Discharged',"Death"],
                   })

# Note:
# Filtering returns a UNION of matching results, and NOT an INTERSECTION.
```
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sr_no</th>
      <th>city</th>
      <th>zone</th>
      <th>age</th>
      <th>gender</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>result</th>
      <th>sample_result</th>
      <th>resultdate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Surat</td>
      <td>South West Zone</td>
      <td>21</td>
      <td>F</td>
      <td>21.1697</td>
      <td>72.7933</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>19/03/2020</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3</td>
      <td>Surat</td>
      <td>East Zone - B</td>
      <td>50</td>
      <td>F</td>
      <td>21.21130173</td>
      <td>72.86820564</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>10/06/2020</td>
    </tr>
    <tr>
      <th>2</th>
      <td>9</td>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>20</td>
      <td>F</td>
      <td>21.1681</td>
      <td>72.8672</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>18/04/2020</td>
    </tr>
    <tr>
      <th>3</th>
      <td>17</td>
      <td>Surat</td>
      <td>West Zone</td>
      <td>61</td>
      <td>F</td>
      <td>21.2078</td>
      <td>72.7732</td>
      <td>Death</td>
      <td>Positive</td>
      <td>03/04/2020</td>
    </tr>
    <tr>
      <th>4</th>
      <td>18</td>
      <td>Surat</td>
      <td>South Zone</td>
      <td>40</td>
      <td>F</td>
      <td>21.1612</td>
      <td>72.8303</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>04/04/2020</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>5807</th>
      <td>3506</td>
      <td>Surat</td>
      <td>West Zone</td>
      <td>47</td>
      <td>M</td>
      <td>21.2057962</td>
      <td>72.7998015</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>23/06/2020</td>
    </tr>
    <tr>
      <th>5808</th>
      <td>3508</td>
      <td>Surat</td>
      <td>South Zone</td>
      <td>78</td>
      <td>M</td>
      <td>21.159747</td>
      <td>72.838655</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>23/06/2020</td>
    </tr>
    <tr>
      <th>5809</th>
      <td>3509</td>
      <td>Surat</td>
      <td>East Zone - A</td>
      <td>30</td>
      <td>M</td>
      <td>21.1975074</td>
      <td>72.8450123</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>24/06/2020</td>
    </tr>
    <tr>
      <th>5810</th>
      <td>3510</td>
      <td>Surat</td>
      <td>North Zone</td>
      <td>43</td>
      <td>M</td>
      <td>21.2284002</td>
      <td>72.8283048</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>23/06/2020</td>
    </tr>
    <tr>
      <th>5811</th>
      <td>3511</td>
      <td>Surat</td>
      <td>North Zone</td>
      <td>53</td>
      <td>M</td>
      <td>21.2440121</td>
      <td>72.8502404</td>
      <td>Cured/Discharged</td>
      <td>Positive</td>
      <td>23/06/2020</td>
    </tr>
  </tbody>
</table>
<p>3592 rows × 10 columns</p>
</div>


--------

> ## F. Restricting Variables/ Columns - `fields`

```python
datagovin.get_data("b9cfed4ca1a24f7aaffa88a8e1a2149c",
                    fields = ["city","zone","age","gender","result"],
                   )
# Get only the fields you need, by passing a list of valid fields in `fields`
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>zone</th>
      <th>age</th>
      <th>gender</th>
      <th>result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Surat</td>
      <td>South West Zone</td>
      <td>21</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Surat</td>
      <td>Central Zone</td>
      <td>67</td>
      <td>M</td>
      <td>Death</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Surat</td>
      <td>East Zone - B</td>
      <td>50</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Surat</td>
      <td>South Zone</td>
      <td>26</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Surat</td>
      <td>West Zone</td>
      <td>55</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>47</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Surat</td>
      <td>East Zone - B</td>
      <td>34</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>39</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>20</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Surat</td>
      <td>West Zone</td>
      <td>32</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Surat</td>
      <td>Central Zone</td>
      <td>53</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>45</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>60</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>65</td>
      <td>M</td>
      <td>Death</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>18</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Surat</td>
      <td>South Zone</td>
      <td>40</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Surat</td>
      <td>East Zone - A</td>
      <td>28</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>77</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Surat</td>
      <td>East Zone - A</td>
      <td>62</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Surat</td>
      <td>East Zone - A</td>
      <td>24</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>63</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>33</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>34</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Surat</td>
      <td>Central Zone</td>
      <td>24</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>34</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>34</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>27</th>
      <td>Surat</td>
      <td>South Zone</td>
      <td>43</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>28</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>52</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>30</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>33</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>31</th>
      <td>Surat</td>
      <td>West Zone</td>
      <td>46</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>32</th>
      <td>Surat</td>
      <td>East Zone - B</td>
      <td>38</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>33</th>
      <td>Surat</td>
      <td>South West Zone</td>
      <td>70</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>34</th>
      <td>Surat</td>
      <td>West Zone</td>
      <td>44</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>35</th>
      <td>Surat</td>
      <td>South West Zone</td>
      <td>45</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>36</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>36</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>37</th>
      <td>Surat</td>
      <td>Central Zone</td>
      <td>40</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>39</th>
      <td>Surat</td>
      <td>East Zone - A</td>
      <td>37</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
  </tbody>
</table>
</div>

--------

> ## G. Request data sorted by a valid `field`

```python
datagovin.get_data("b9cfed4ca1a24f7aaffa88a8e1a2149c",
                fields = ["city","zone","age","gender","result"],
                   sort_key = 'age',
                   sort_order = 'asc'
                   )

# Sort `field` in Ascending order using `asc`=`Ascending`
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>zone</th>
      <th>age</th>
      <th>gender</th>
      <th>result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>1</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Surat</td>
      <td>East Zone - A</td>
      <td>1</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Surat</td>
      <td>South Zone</td>
      <td>1</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>1</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>2</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Surat</td>
      <td>Central Zone</td>
      <td>2</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>2</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Surat</td>
      <td>East Zone - A</td>
      <td>2</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>2</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>3</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>34</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>34</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>34</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Surat</td>
      <td>East Zone - A</td>
      <td>34</td>
      <td>M</td>
      <td>Death</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>47</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Surat</td>
      <td>West Zone</td>
      <td>47</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Surat</td>
      <td>East Zone - B</td>
      <td>47</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Surat</td>
      <td>East Zone - A</td>
      <td>47</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>47</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Surat</td>
      <td>South West Zone</td>
      <td>47</td>
      <td>M</td>
      <td>Death</td>
    </tr>
    <tr>
      <th>30</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>60</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>31</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>60</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>33</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>60</td>
      <td>M</td>
      <td>Death</td>
    </tr>
    <tr>
      <th>35</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>60</td>
      <td>F</td>
      <td>Death</td>
    </tr>
    <tr>
      <th>36</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>60</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>37</th>
      <td>Surat</td>
      <td>South Zone</td>
      <td>60</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
  </tbody>
</table>
</div>

```python
datagovin.get_data("b9cfed4ca1a24f7aaffa88a8e1a2149c",
                   fields = ["city","zone","age","gender","result"],                   
                   sort_key = 'age',
                   sort_order = 'desc'
                   )
# Sort `field` in Descending order using `desc`=`Descending`
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>zone</th>
      <th>age</th>
      <th>gender</th>
      <th>result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>94</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>90</td>
      <td>F</td>
      <td>Death</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Surat</td>
      <td>East Zone - B</td>
      <td>89</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>88</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>88</td>
      <td>F</td>
      <td>Death</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>86</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>86</td>
      <td>M</td>
      <td>Death</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>85</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>85</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>54</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Surat</td>
      <td>North Zone</td>
      <td>54</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Surat</td>
      <td>South West Zone</td>
      <td>54</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Surat</td>
      <td>South Zone</td>
      <td>54</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Surat</td>
      <td>Central Zone</td>
      <td>54</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Surat</td>
      <td>South Zone</td>
      <td>54</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Surat</td>
      <td>Central Zone</td>
      <td>54</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Surat</td>
      <td>Central Zone</td>
      <td>42</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Surat</td>
      <td>Central Zone</td>
      <td>42</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Surat</td>
      <td>East Zone - A</td>
      <td>42</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Surat</td>
      <td>South West Zone</td>
      <td>42</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Surat</td>
      <td>South Zone</td>
      <td>42</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>27</th>
      <td>Surat</td>
      <td>East Zone - B</td>
      <td>42</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>28</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>42</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>30</th>
      <td>Surat</td>
      <td>Central Zone</td>
      <td>27</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>31</th>
      <td>Surat</td>
      <td>West Zone</td>
      <td>27</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>32</th>
      <td>Surat</td>
      <td>South East Zone</td>
      <td>27</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>33</th>
      <td>Surat</td>
      <td>South West Zone</td>
      <td>27</td>
      <td>F</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>35</th>
      <td>Surat</td>
      <td>Central Zone</td>
      <td>27</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
    <tr>
      <th>39</th>
      <td>Surat</td>
      <td>South Zone</td>
      <td>27</td>
      <td>M</td>
      <td>Cured/Discharged</td>
    </tr>
  </tbody>
</table>
</div>

--------

> ## H.  `ADVANCED` : Multi-Threading API-requests
>>
>> ### - Multi-Threading is disabled by default.
>> ### - You can enable multi-threading for faster performance on large datasets.
>>

```python
datagovin.get_resource_info("dad7a738fd3b437dad31e1f844e9a575")['TotalRecords']

# Returns:
# 20197
```

>> ### To Enable Multi-threading -
```python
datagovin.enable_multithreading()

# Returns:
# Multi-Threaded API requests enabled.
```

```python
%%timeit
datagovin.get_data("dad7a738fd3b437dad31e1f844e9a575",num_results='all')

# Returns:
# 258 ms ± 11.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

>> ### To Disable Multi-threading -

```python
datagovin.disable_multithreading()
# Returns:
# Multi-Threaded API requests disabled.
```

```python
%%timeit
datagovin.get_data("dad7a738fd3b437dad31e1f844e9a575",num_results='all')
# Returns:
# 2.74 s ± 194 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

--------

> ## **Documentation**
>
> - For the Python library, visit -
>   
>   > [pypi.org/project/datagovindia/](https://pypi.org/project/datagovindia/)
>
>   > [github.com/addypy/datagovindia](https://github.com/addypy/datagovindia)
>   
> - For the R/CRAN package, visit -
>   
>   > [cran.r-project.org/web/packages/datagovindia](https://cran.r-project.org/web/packages/datagovindia)
>
>   > [github.com/econabhishek/datagovindia](https://github.com/econabhishek/datagovindia)
>
> ### **Authors** :
>
> > - [Aditya Karan Chhabra](mailto:aditya0chhabra@gmail.com)
>
> > - [Abhishek Arora](mailto:abhishek.arora1996@gmail.com)
>
> ## **Meta-Data Updates** :
>
>  > Last Updated: **October 9, 2021**, `02:04 IST`
>
>  > Number of active APIs: **117186**
>