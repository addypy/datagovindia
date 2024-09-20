# datagovindia

[![MIT license](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/addypy/datagovindia/blob/master/LICENSE) ![PyPI - Version](https://img.shields.io/pypi/v/datagovindia?color=green) [![Downloads](https://static.pepy.tech/personalized-badge/datagovindia?period=total&units=international_system&left_color=gray&left_text=Downloads)](https://pepy.tech/project/datagovindia)

## Python Client for Government of India’s [Open Government Data OGD platform](https://data.gov.in/) API

**`datagovindia`** is a Python client library for accessing resources from the Government of India’s Open Government Data OGD platform. It provides a simple and intuitive interface to search, discover and download data from the platform.

## Prerequisites

A data.gov.in API key is required to use this library. You can get your API key from [data.gov.in](https://data.gov.in).

## Setup

```sh
### Install from PyPI
pip install -U datagovindia
```

## Setting Up Your API Key

Saving your API key as an environment variable named `DATAGOVINDIA_API_KEY` will allow the library to automatically retrieve your API key when needed.

```bash
export DATAGOVINDIA_API_KEY=your_api_key_here
```

or you can specify your API key in every command using the `--api-key` flag.

## Sync latest resource data from OGD (`Optional`)

You can sync the latest metadata from data.gov.in to ensure that the library is up-to-date with the latest resources.

However, if you want to download data with resource IDs directly and don't need to search for resources, you can skip this step.

```python
# In a python environment
from datagovindia import DataGovIndia
datagovin = DataGovIndia() # Specify API key if not set as an environment variable
datagovin.sync_metadata()
```

**Note**: Updating the library's metadata from data.gov.in ensures synchronization with the latest data. While this step is optional (especially if you're focused only on data downloads), it's beneficial due to the OGD platform's lack of a search API for resources.

```sh
# To update metadata from the command line:
$ datagovindia sync-metadata # Specify API key if not set as an environment variable
```

Output:

```sh
Updated 198465/198465 resources: [===============================================>] - ETA: 0s         
Finished updating 198465 records in 62 seconds.
```

## Search for resources

```python
search_data = datagovin.search('mgnrega') # Returns a dataframe with search results. Searches in resource title by default

search_data = datagovin.search('mgnrega', search_fields=['title', 'description']) # Search in multiple fields
```

```sh
# Search for resources with the keyword 'mgnrega'
$ datagovindia search mgnrega # Returns a dataframe with search results

# Search for resources in the title and description fields only and save the results to a csv/xlsx/json file
$ datagovindia search mgnrega -f title -f description --output mgnrega.csv

# Preview the first n results of a search
$ datagovindia search mgnrega --preview --limit 5
```

Output:

| resource\_id | title | description | org\_type | fields | orgs | source | sectors | date\_created | date\_updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ee03643a-ee4c-48c2-ac30-9f2ff26ab722 | District-wise MGNREGA Data at a Glance from 01.04.2023 to 31.08.2023 | District-wise MGNREGA Data at a Glance from 01.04.2023 to 31.08.2023 | Central | \['document\_id', 'sno\_', 'state\_name', 'district\_name', 'total\_no\_\_of\_jobcards\_issued', 'total\_no\_\_of\_workers', 'total\_no\_\_of\_active\_job\_cards', 'total\_no\_\_of\_active\_workers', 'sc\_workers\_against\_active\_workers', 'st\_workers\_against\_active\_workers', 'approved\_labour\_budget', 'persondays\_of\_central\_liability\_so\_far', 'sc\_persondays', 'st\_persondays', 'women\_persondays', 'average\_days\_of\_employment\_provided\_per\_household', 'average\_wage\_rate\_per\_day\_per\_person\_rs\_\_', 'total\_no\_of\_hhs\_completed\_100\_days\_of\_wage\_employment', 'total\_households\_worked', 'total\_individuals\_worked', 'differently\_abled\_persons\_worked', 'number\_of\_gps\_with\_nil\_exp', 'total\_no\_\_of\_works\_takenup\_\_new\_spill\_over\_', 'number\_of\_ongoing\_works', 'number\_of\_completed\_works', '\_\_of\_nrm\_expenditure\_public\_\_\_individual\_', '\_\_of\_category\_b\_works', '\_\_of\_expenditure\_on\_agriculture\_\_\_agriculture\_allied\_works', 'total\_exp\_rs\_\_in\_lakhs\_\_', 'wages\_rs\_\_in\_lakhs\_', 'material\_and\_skilled\_wages\_rs\_\_in\_lakhs\_', 'total\_adm\_expenditure\_\_rs\_\_in\_lakhs\_\_', 'resource\_uuid'\] | \['Ministry of Rural Development', 'Department of Land Resources (DLR)'\] | data.gov.in | \['Rural', 'Land Resources'\] | 2023-09-19T06:43:03+00:00 | 2023-09-19T10:39:44+00:00 |
| d1d29e37-1d60-46da-9902-52340abbfb13 | State/UTs-wise Expenditure on Water Related Works under Mahatma Gandhi National Rural Employment Guarantee Scheme (MGNREGA) from 2019-20 to 2021-22 | State/UTs-wise Expenditure on Water Related Works under Mahatma Gandhi National Rural Employment Guarantee Scheme (MGNREGA) from 2019-20 to 2021-22 | Central | \['document\_id', 'sl\_\_no\_', 'state\_ut', '\_2019\_2020\_\_\_water\_conservation\_and\_water\_harvesting\_\_\_completed\_\_\_number\_of\_works', '\_2019\_2020\_\_\_water\_conservation\_and\_water\_harvesting\_\_\_completed\_\_\_expenditure\_\_rs\_\_in\_lakh\_', '\_2019\_2020\_\_\_water\_conservation\_and\_water\_harvesting\_\_\_ongoing\_\_\_number\_of\_works', '\_2019\_2020\_\_\_water\_conservation\_and\_water\_harvesting\_\_\_ongoing\_\_\_expenditure\_\_rs\_\_in\_lakh\_', '\_2020\_2021\_\_\_water\_conservation\_and\_water\_harvesting\_\_\_completed\_\_\_number\_of\_works', '\_2020\_2021\_\_\_water\_conservation\_and\_water\_harvesting\_\_\_completed\_\_\_expenditure\_\_rs\_\_in\_lakh\_', '\_2020\_2021\_\_\_water\_conservation\_and\_water\_harvesting\_\_\_ongoing\_\_\_number', '\_2020\_2021\_\_\_water\_conservation\_and\_water\_harvesting\_\_\_ongoing\_\_\_expenditure\_\_rs\_\_in\_lakh\_', '\_2021\_2022\_\_as\_on\_10\_03\_2022\_\_\_\_water\_conservation\_and\_water\_harvesting\_\_\_completed\_\_\_number\_of\_works', '\_2021\_2022\_\_as\_on\_10\_03\_2022\_\_\_\_water\_conservation\_and\_water\_harvesting\_\_\_completed\_\_\_expenditure\_\_rs\_\_in\_lakh\_', '\_2021\_2022\_\_as\_on\_10\_03\_2022\_\_\_\_water\_conservation\_and\_water\_harvesting\_\_\_ongoing\_\_\_number\_of\_works', '\_2021\_2022\_\_as\_on\_10\_03\_2022\_\_\_\_water\_conservation\_and\_water\_harvesting\_\_\_ongoing\_\_\_expenditure\_\_rs\_\_in\_lakh\_', 'resource\_uuid'\] | \['Rajya Sabha'\] | data.gov.in | \['All'\] | 2022-09-15T07:24:33+00:00 | 2022-09-15T12:37:43+00:00 |
| c0350589-65a7-4166-996a-ba5845c398fe | State/UT-wise Central Funds Sanctioned/Released for Wage, Material & Admin Component under MGNREGA from 2018-19 to 2021-22 | State/UT-wise Central Funds Sanctioned/Released for Wage, Material & Admin Component under MGNREGA from 2018-19 to 2021-22 | Central | \['document\_id', 'sl\_\_no\_', 'state\_ut', 'fy\_2018\_19', 'fy\_2019\_20', 'fy\_2020\_21', 'fy\_2021\_22\_\_as\_on\_26\_07\_2021\_', 'resource\_uuid'\] | \['Rajya Sabha'\] | data.gov.in | \['All'\] | 2022-04-01T05:41:11+00:00 | 2022-04-29T14:13:43+00:00 |
| 0fecf99b-2c7c-46db-9f7d-c4bdacf040fc | State/UT-wise List of Total Number of Active ST Worker and ST Person Days Generated under Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA) during 2019-20 and 2020-21 (From: Ministry of Tribal Affairs) | State/UT-wise List of Total Number of Active ST Worker and ST Person Days Generated under Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA) during 2019-20 and 2020-21 (From: Ministry of Tribal Affairs) | Central | \['document\_id', '\_sl\_\_no\_', 'state\_ut', 'total\_number\_of\_active\_st\_worker\_\_in\_lakh\_', 'st\_person\_days\_generated\_\_in\_lakh\_\_\_2019\_20\_', 'st\_person\_days\_generated\_\_in\_lakhs\_\_\_2020\_21\_', 'resource\_uuid'\] | \['Rajya Sabha'\] | data.gov.in | \['All'\] | 2021-12-15T14:23:27+00:00 | 2022-02-28T10:15:14+00:00 |
| aeca8112-5fd4-4c91-92dc-d72b2c7b969e | State/UT-wise Central Fund Released and Expenditure Reported under MGNREGA from 2017-18 to 2019-20 (From: Ministry of Rural Development) | State/UT-wise Central Fund Released and Expenditure Reported under MGNREGA from 2017-18 to 2019-20 (From: Ministry of Rural Development) | Central | \['document\_id', '\_s\_\_no\_', 'state\_ut', 'central\_fund\_released\_\_\_2017\_18\_\_', 'central\_fund\_released\_\_\_2018\_19\_\_', 'central\_fund\_released\_\_\_2019\_20', '\_expenditure\_\_\_2017\_18', '\_expenditure\_\_\_2018\_19', '\_expenditure\_\_\_2019\_20', 'resource\_uuid'\] | \['Rajya Sabha'\] | data.gov.in | \['All'\] | 2021-03-04T07:17:46+00:00 | 2021-03-23T15:15:05+00:00 |
| 7efb084d-b562-4b9f-8a3a-d0808a54d609 | State/UT-wise Persondays Generated under MGNREGA including West Bengal from 2017-18 to 2019-20 (From: Ministry of Rural Development) | State/UT-wise Persondays Generated under MGNREGA including West Bengal from 2017-18 to 2019-20 (From: Ministry of Rural Development) | Central | \['document\_id', '\_sl\_no', 'state\_ut', '\_2017\_18', '\_2018\_19', '\_2019\_20', 'resource\_uuid'\] | \['Rajya Sabha'\] | data.gov.in | \['All'\] | 2021-03-04T06:52:05+00:00 | 2021-03-23T14:53:45+00:00 |
| 6ae541ca-903e-4a6a-be62-48dedea02223 | Average Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA) wages from 2014-15 to 2018-19 (From : Ministry of Rural Development) | Average Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA) wages from 2014-15 to 2018-19 (From : Ministry of Rural Development) | Central | \['document\_id', 'financial\_year', 'average\_wage\_rate\_per\_day\_per\_person\_\_rs\_\_', 'resource\_uuid'\] | \['Rajya Sabha'\] | data.gov.in | \['All'\] | 2021-03-04T04:45:12+00:00 | 2021-03-23T13:10:05+00:00 |

## Get information about a resource

```python
# In a python environment
datagovin.get_resource_info("5c2f62fe-5afa-4119-a499-fec9d604d5bd")
```

```sh
# From the command line
$ datagovindia get-resource-info 5c2f62fe-5afa-4119-a499-fec9d604d5bd
```

Output:

```json
{
    "index_name": "5c2f62fe-5afa-4119-a499-fec9d604d5bd",
    "title": "All India Pincode Directory till last month",
    "desc": "All India Pincode Directory till last month",
    "org_type": "Central",
    "org": [
        "Ministry of Communications",
        "Department of Posts"
    ],
    "sector": [
        "Post"
    ],
    "source": "data.gov.in",
    "catalog_uuid": "709e9d78-bf11-487d-93fd-d547d24cc0ef",
    "visualizable": false,
    "active": false,
    "created": 1608423011,
    "updated": 1659003955,
    "created_date": "2020-12-20",
    "updated_date": "2022-07-28T10:25:55Z",
    "field": [
        {
            "id": "circlename",
            "name": "circlename",
            "type": "keyword"
        },
        {
            "id": "regionname",
            "name": "regionname",
            "type": "keyword"
        },
        {
            "id": "divisionname",
            "name": "divisionname",
            "type": "keyword"
        },
        {
            "id": "officename",
            "name": "officename",
            "type": "keyword"
        },
        {
            "id": "pincode",
            "name": "pincode",
            "type": "double"
        },
        {
            "id": "officetype",
            "name": "officetype",
            "type": "keyword"
        },
        {
            "id": "delivery",
            "name": "delivery",
            "type": "keyword"
        },
        {
            "id": "district",
            "name": "district",
            "type": "keyword"
        },
        {
            "id": "statename",
            "name": "statename",
            "type": "keyword"
        },
        {
            "id": "latitude",
            "name": "latitude",
            "type": "keyword"
        },
        {
            "id": "longitude",
            "name": "longitude",
            "type": "keyword"
        }
    ],
    "total": 165307
}
```

## Download data from a resource

```python
# In a python environment
data = datagovin.get_data("5c2f62fe-5afa-4119-a499-fec9d604d5bd")
```

```sh
# Download data as a json, csv or xlsx file by specifying the --output filepath
$ datagovindia get-data 5c2f62fe-5afa-4119-a499-fec9d604d5bd --output pincode.csv 
```

## License

`datagovindia` is licensed under the MIT License. See the [LICENSE](https://github.com/addypy/datagovindia/blob/master/LICENSE) file for more details.

## **Authors**

- [Aditya Karan Chhabra](mailto:aditya0chhabra@gmail.com)

- [Abhishek Arora](https://econabhishek.github.io/)

- [Arijit Basu](https://arijitbasu.in/)