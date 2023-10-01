<div align="center">

# datagovindia

[![MIT license](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/addypy/datagovindia/blob/master/LICENSE) ![PyPI - Version](https://img.shields.io/pypi/v/datagovindia?color=green) [![Downloads](https://static.pepy.tech/personalized-badge/datagovindia?period=total&units=international_system&left_color=gray&left_text=Downloads)](https://pepy.tech/project/datagovindia) 


## Python Client for Government of India’s [Open Government Data OGD platform](https://data.gov.in/) API

**`datagovindia`** is a Python client library for accessing resources from the Government of India’s Open Government Data OGD platform. It provides a simple and intuitive interface to search, discover and download data from the platform.

</div>

## Prerequisites

A data.gov.in API key is required to use this library. You can get your API key from [data.gov.in](https://data.gov.in).

## Setup

```sh
### Install from PyPI
pip install datagovindia
```
## Setting Up Your API Key
Saving your `API_KEY` as an environment variable named `DATAGOVINDIA_API_KEY` will allow the library to automatically detect your API key without the need to specify it in every command.

```bash
export DATAGOVINDIA_API_KEY=your_api_key_here ### Linux/Mac
```

or you can specify your API key in every command using the `--api-key` flag.


## Sync latest resource data from OGD (`Optional`)
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

### `Output`:

```
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

### `Output`:

<table>
    <thead>
        <tr>
            <th>resource_id</th>
            <th>title</th>
            <th>description</th>
            <th>org_type</th>
            <th>fields</th>
            <th>orgs</th>
            <th>source</th>
            <th>sectors</th>
            <th>date_created</th>
            <th>date_updated</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>ee03643a-ee4c-48c2-ac30-9f2ff26ab722</td>
            <td>District-wise MGNREGA Data at a Glance from 01.04.2023 to 31.08.2023</td>
            <td>District-wise MGNREGA Data at a Glance from 01.04.2023 to 31.08.2023</td>
            <td>Central</td>
            <td>[&#39;document_id&#39;, &#39;sno_&#39;, &#39;state_name&#39;, &#39;district_name&#39;, &#39;total_no__of_jobcards_issued&#39;, &#39;total_no__of_workers&#39;, &#39;total_no__of_active_job_cards&#39;, &#39;total_no__of_active_workers&#39;, &#39;sc_workers_against_active_workers&#39;, &#39;st_workers_against_active_workers&#39;, &#39;approved_labour_budget&#39;, &#39;persondays_of_central_liability_so_far&#39;, &#39;sc_persondays&#39;, &#39;st_persondays&#39;, &#39;women_persondays&#39;, &#39;average_days_of_employment_provided_per_household&#39;, &#39;average_wage_rate_per_day_per_person_rs__&#39;, &#39;total_no_of_hhs_completed_100_days_of_wage_employment&#39;, &#39;total_households_worked&#39;, &#39;total_individuals_worked&#39;, &#39;differently_abled_persons_worked&#39;, &#39;number_of_gps_with_nil_exp&#39;, &#39;total_no__of_works_takenup__new_spill_over_&#39;, &#39;number_of_ongoing_works&#39;, &#39;number_of_completed_works&#39;, &#39;__of_nrm_expenditure_public___individual_&#39;, &#39;__of_category_b_works&#39;, &#39;__of_expenditure_on_agriculture___agriculture_allied_works&#39;, &#39;total_exp_rs__in_lakhs__&#39;, &#39;wages_rs__in_lakhs_&#39;, &#39;material_and_skilled_wages_rs__in_lakhs_&#39;, &#39;total_adm_expenditure__rs__in_lakhs__&#39;, &#39;resource_uuid&#39;]</td>
            <td>[&#39;Ministry of Rural Development&#39;, &#39;Department of Land Resources (DLR)&#39;]</td>
            <td>data.gov.in</td>
            <td>[&#39;Rural&#39;, &#39;Land Resources&#39;]</td>
            <td>2023-09-19T06:43:03+00:00</td>
            <td>2023-09-19T10:39:44+00:00</td>
        </tr>
        <tr>
            <td>d1d29e37-1d60-46da-9902-52340abbfb13</td>
            <td>State/UTs-wise Expenditure on Water Related Works under Mahatma Gandhi National Rural Employment Guarantee Scheme (MGNREGA) from 2019-20 to 2021-22</td>
            <td>State/UTs-wise Expenditure on Water Related Works under Mahatma Gandhi National Rural Employment Guarantee Scheme (MGNREGA) from 2019-20 to 2021-22</td>
            <td>Central</td>
            <td>[&#39;document_id&#39;, &#39;sl__no_&#39;, &#39;state_ut&#39;, &#39;_2019_2020___water_conservation_and_water_harvesting___completed___number_of_works&#39;, &#39;_2019_2020___water_conservation_and_water_harvesting___completed___expenditure__rs__in_lakh_&#39;, &#39;_2019_2020___water_conservation_and_water_harvesting___ongoing___number_of_works&#39;, &#39;_2019_2020___water_conservation_and_water_harvesting___ongoing___expenditure__rs__in_lakh_&#39;, &#39;_2020_2021___water_conservation_and_water_harvesting___completed___number_of_works&#39;, &#39;_2020_2021___water_conservation_and_water_harvesting___completed___expenditure__rs__in_lakh_&#39;, &#39;_2020_2021___water_conservation_and_water_harvesting___ongoing___number&#39;, &#39;_2020_2021___water_conservation_and_water_harvesting___ongoing___expenditure__rs__in_lakh_&#39;, &#39;_2021_2022__as_on_10_03_2022____water_conservation_and_water_harvesting___completed___number_of_works&#39;, &#39;_2021_2022__as_on_10_03_2022____water_conservation_and_water_harvesting___completed___expenditure__rs__in_lakh_&#39;, &#39;_2021_2022__as_on_10_03_2022____water_conservation_and_water_harvesting___ongoing___number_of_works&#39;, &#39;_2021_2022__as_on_10_03_2022____water_conservation_and_water_harvesting___ongoing___expenditure__rs__in_lakh_&#39;, &#39;resource_uuid&#39;]</td>
            <td>[&#39;Rajya Sabha&#39;]</td>
            <td>data.gov.in</td>
            <td>[&#39;All&#39;]</td>
            <td>2022-09-15T07:24:33+00:00</td>
            <td>2022-09-15T12:37:43+00:00</td>
        </tr>
        <tr>
            <td>c0350589-65a7-4166-996a-ba5845c398fe</td>
            <td>State/UT-wise Central Funds Sanctioned/Released for Wage, Material &amp; Admin Component under MGNREGA from 2018-19 to 2021-22</td>
            <td>State/UT-wise Central Funds Sanctioned/Released for Wage, Material &amp; Admin Component under MGNREGA from 2018-19 to 2021-22</td>
            <td>Central</td>
            <td>[&#39;document_id&#39;, &#39;sl__no_&#39;, &#39;state_ut&#39;, &#39;fy_2018_19&#39;, &#39;fy_2019_20&#39;, &#39;fy_2020_21&#39;, &#39;fy_2021_22__as_on_26_07_2021_&#39;, &#39;resource_uuid&#39;]</td>
            <td>[&#39;Rajya Sabha&#39;]</td>
            <td>data.gov.in</td>
            <td>[&#39;All&#39;]</td>
            <td>2022-04-01T05:41:11+00:00</td>
            <td>2022-04-29T14:13:43+00:00</td>
        </tr>
        <tr>
            <td>0fecf99b-2c7c-46db-9f7d-c4bdacf040fc</td>
            <td>State/UT-wise List of Total Number of Active ST Worker and ST Person Days Generated under Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA) during 2019-20 and 2020-21 (From: Ministry of Tribal Affairs)</td>
            <td>State/UT-wise List of Total Number of Active ST Worker and ST Person Days Generated under Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA) during 2019-20 and 2020-21 (From: Ministry of Tribal Affairs)</td>
            <td>Central</td>
            <td>[&#39;document_id&#39;, &#39;_sl__no_&#39;, &#39;state_ut&#39;, &#39;total_number_of_active_st_worker__in_lakh_&#39;, &#39;st_person_days_generated__in_lakh___2019_20_&#39;, &#39;st_person_days_generated__in_lakhs___2020_21_&#39;, &#39;resource_uuid&#39;]</td>
            <td>[&#39;Rajya Sabha&#39;]</td>
            <td>data.gov.in</td>
            <td>[&#39;All&#39;]</td>
            <td>2021-12-15T14:23:27+00:00</td>
            <td>2022-02-28T10:15:14+00:00</td>
        </tr>
        <tr>
            <td>aeca8112-5fd4-4c91-92dc-d72b2c7b969e</td>
            <td>State/UT-wise Central Fund Released and Expenditure Reported under MGNREGA from 2017-18 to 2019-20 (From: Ministry of Rural Development)</td>
            <td>State/UT-wise Central Fund Released and Expenditure Reported under MGNREGA from 2017-18 to 2019-20 (From: Ministry of Rural Development)</td>
            <td>Central</td>
            <td>[&#39;document_id&#39;, &#39;_s__no_&#39;, &#39;state_ut&#39;, &#39;central_fund_released___2017_18__&#39;, &#39;central_fund_released___2018_19__&#39;, &#39;central_fund_released___2019_20&#39;, &#39;_expenditure___2017_18&#39;, &#39;_expenditure___2018_19&#39;, &#39;_expenditure___2019_20&#39;, &#39;resource_uuid&#39;]</td>
            <td>[&#39;Rajya Sabha&#39;]</td>
            <td>data.gov.in</td>
            <td>[&#39;All&#39;]</td>
            <td>2021-03-04T07:17:46+00:00</td>
            <td>2021-03-23T15:15:05+00:00</td>
        </tr>
        <tr>
            <td>7efb084d-b562-4b9f-8a3a-d0808a54d609</td>
            <td>State/UT-wise Persondays Generated under MGNREGA including West Bengal from 2017-18 to 2019-20 (From: Ministry of Rural Development)</td>
            <td>State/UT-wise Persondays Generated under MGNREGA including West Bengal from 2017-18 to 2019-20 (From: Ministry of Rural Development)</td>
            <td>Central</td>
            <td>[&#39;document_id&#39;, &#39;_sl_no&#39;, &#39;state_ut&#39;, &#39;_2017_18&#39;, &#39;_2018_19&#39;, &#39;_2019_20&#39;, &#39;resource_uuid&#39;]</td>
            <td>[&#39;Rajya Sabha&#39;]</td>
            <td>data.gov.in</td>
            <td>[&#39;All&#39;]</td>
            <td>2021-03-04T06:52:05+00:00</td>
            <td>2021-03-23T14:53:45+00:00</td>
        </tr>
        <tr>
            <td>6ae541ca-903e-4a6a-be62-48dedea02223</td>
            <td>Average Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA) wages from 2014-15 to 2018-19 (From : Ministry of Rural Development)</td>
            <td>Average Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA) wages from 2014-15 to 2018-19 (From : Ministry of Rural Development)</td>
            <td>Central</td>
            <td>[&#39;document_id&#39;, &#39;financial_year&#39;, &#39;average_wage_rate_per_day_per_person__rs__&#39;, &#39;resource_uuid&#39;]</td>
            <td>[&#39;Rajya Sabha&#39;]</td>
            <td>data.gov.in</td>
            <td>[&#39;All&#39;]</td>
            <td>2021-03-04T04:45:12+00:00</td>
            <td>2021-03-23T13:10:05+00:00</td>
        </tr>
    </tbody>
</table>


## Get information about a resource
```python
# In a python environment
datagovin.get_resource_info("5c2f62fe-5afa-4119-a499-fec9d604d5bd")
```

```sh
# From the command line
$ datagovindia get-resource-info 5c2f62fe-5afa-4119-a499-fec9d604d5bd
```

### `Output`:
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

## **Authors**:
- [Aditya Karan Chhabra](mailto:aditya0chhabra@gmail.com)

- [Abhishek Arora](https://econabhishek.github.io/)

- [Arijit Basu](https://arijitbasu.in/)