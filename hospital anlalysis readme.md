

# &#x20;**Hospital MANGEMENT Analysis**





A multi-tool data analysis project built using SQL, Python, and Power BI to explore patient behaviour, doctor performance, billing trends, and revenue insights across a hospital network.





###### **Tools Used:**



* SQL — database design and querying
* Python (Pandas, Matplotlib) — data cleaning and exploratory analysis
* Power BI — interactive dashboard 





###### &#x20;**Conclusion:**





###### &#x20;**Patient Overview:**



* Male patients accounted for **62%** and female patients **38%** of total patients.
* **51.5%** of appointments had a status of *Cancelled* or *No-Show*.
* Insurance was provided by four companies, ranked by coverage:

&#x20;   **Medcare Plus > Wellness Corp > Plus Secure > Health India**





###### &#x20;**Doctor Overview:**



* Total of 10 doctors across departments.
* Specialists per department:



| Department  | Count |

|-------------|-------|

| Pediatrics  | 5     |

| Dermatology | 3     |

| Oncology    | 2     |







###### &#x20;**Treatment Overview:**



**Chemotherapy** had the highest number of appointments scheduled.





###### &#x20;**Billing Overview:**



* Most common payment method is Credit Card, accounting for 37.5% of total payments
* Only 32% of appointments have a Paid billing status; the remaining are Pending or Failed



&#x20;***Note:*** Some paid billing records are associated with appointments marked as Cancelled, Scheduled, or No-Show. This appears to be a limitation of the synthetic dataset and may not reflect real-world hospital operations.



###### 

###### &#x20;**Revenue Analysis**





|      Metric            |     Value      |

|------------------------|----------------|

| Total Hospital Revenue |  173,424.90    |

| Revenue at Risk        |  93,037.19     |





&#x20;**Revenue by Branch**



| Hospital Branch | Revenue       |

|-----------------|---------------|

| Central Hospital|  86,460.11    |

| Eastside Clinic |  54,397.45    |

| Westside Clinic |  32,567.34    |



&#x20;**Revenue by Treatment**



|   Treatment |    Revenue    |

|-------------|---------------|

|   X-Ray     |    47,978.78  |

|   MRI       |    43,064.42  |

|Chemotherapy |    32,607.26  |

|Physiotherapy|    32,251.38  |

|   ECG       |    17,523.06  |





&#x20;**Key Insights:**



* **Central Hospital** contributes **\~50%** of total network revenue
* Despite having the most appointments, Chemotherapy did not lead in revenue , **X-Ray** generated the highest revenue, while ECG had the lowest.
* **Dr. Sarah Taylor** was the highest revenue-contributing doctor
* Revenue peaked in **June**, while appointment volume peaked in **April** .Showing the two do not always move together
* Months with fewer appointments sometimes generated higher revenue, suggesting treatment mix and cost have a greater impact than appointment count alone
* The hospital generates the highest revenue on **Wednesday**, followed by **Sunday**



###### **Forecast**



* A downward trend in revenue is predicted from January to March
* Appointment count is expected to remain relatively stable with only a slight upward tilt





###### **What I Learned:**



* Learned that appointment volume and revenue don't always move

&#x20;  together — treatment type has a bigger impact

* Realised how messy real billing data can be when payments don't

&#x20;  match appointment statuses

* Understood how to connect multiple tables in SQL before

&#x20;  visualising in Power BI







###### **Dataset**



**Source:** https://www.kaggle.com/datasets/kanakbaghel/hospital-management-dataset



This is a synthetic dataset with 5 CSV files covering patients, doctors, appointments, treatments, and billing. It was used for learning purposes only and does not represent any real hospital or patient records.







