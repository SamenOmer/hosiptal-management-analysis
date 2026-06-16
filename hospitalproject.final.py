import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='sameen123',
    database='hospital_db'
)

patient= pd.read_sql("SELECT * FROM patients", conn)
doctor=pd.read_sql("Select * from doctors",conn)
pat_summary=pd.read_sql("select * from patient_summary",conn)
appointment=pd.read_sql("select * from appointments",conn)
billing=pd.read_sql("select * from billing",conn)
treatment=pd.read_sql("select * from treatments",conn)

##cleaning of data

#removing duplicates

patient = patient.drop_duplicates()
doctor= doctor.drop_duplicates()
appointment = appointment.drop_duplicates()
treatment= treatment.drop_duplicates()
pat_summary=pat_summary.drop_duplicates()

#adjusting data type and checking formatting
print(patient.isnull().sum())
print(patient.info())
patient["registration_date"]=pd.to_datetime(patient["registration_date"])
patient["date_of_birth"]=pd.to_datetime(patient["date_of_birth"])
print(patient.info())
print("other")
print(appointment.info())

print(appointment["status"].unique())
print(appointment.head())
appointment["appointment_date"]=pd.to_datetime(appointment["appointment_date"])
appointment["appointment_time"]=pd.to_datetime(appointment["appointment_time"],format="%H:%M:%S")

print(appointment.info())
print(billing.info())
billing["bill_date"]=pd.to_datetime(billing["bill_date"])
print(billing["payment_method"].unique())
print(billing["payment_status"].unique())

print(treatment.info())
treatment["treatment_date"]=pd.to_datetime(treatment["treatment_date"])
print(pat_summary.info())
pat_summary["appointment_date"]=pd.to_datetime(pat_summary["appointment_date"])
print(pat_summary.info())
#checking for null or mising values
print(patient.isnull().sum())
print(doctor.isnull().sum())
print(treatment.isnull().sum())
print(pat_summary.isnull().sum())
print(billing.isnull().sum())
print(appointment.isnull().sum())

#handling outliers
Q1 = treatment['cost'].quantile(0.25)
Q3 = treatment['cost'].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = treatment[
    (treatment['cost'] < lower_bound) |
    (treatment['cost'] > upper_bound)
]

print(outliers)
outliers.head()
print(doctor.head())
print(doctor["years_experience"].unique())

from datetime import datetime

patient['age'] = (
    datetime.now().year - patient['date_of_birth'].dt.year
)
print(patient['age'].describe())
print(billing.head())
print(treatment.columns)
merge_data=(appointment
            .merge (patient, on="patient_id")
            .merge(doctor, on="doctor_id")
            .merge (treatment, on="appointment_id")
            .merge (billing, on="treatment_id"))

print(merge_data.shape)

# exploratort data analysis

#gender distribution

gender_count=patient["gender"].value_counts()

plt.pie(gender_count,labels=gender_count.index,
        autopct="%1.1f%%")
plt.title("Gender Distibution")
plt.show()

#age distribition
print(patient["age"].describe())
age=patient["age"]
bin=np.arange(20,80,5)
plt.hist(age,bins=bin,color="purple",edgecolor="black")
plt.xlabel("age")
plt.ylabel("frequency")
plt.title("Age distribution")
plt.show()

#appointment status

app_status=appointment["status"].value_counts()
plt.pie(app_status,labels=app_status.index,colors=["blue","green","yellow","red"],autopct="%1.1f%%")
plt.xlabel("appointment status")
plt.ylabel("no of appointment")
plt.title("appointmnet status distribution")
plt.show()

#issurance provider 


print(merge_data['status'].value_counts())
print(appointment.shape)
print(billing.shape)
print(treatment.shape)
print(doctor.shape)
print(patient.shape)
print(appointment["appointment_id"].unique())

#insurance provider
#How many patients does each insurer cover?"
from matplotlib.ticker import MaxNLocator

insurance=patient["insurance_provider"].value_counts()
plt.bar(insurance.index,insurance.values,color="pink")
plt.xlabel("insurance provider")
plt.ylabel("Number of Patients")
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.title("Number of Patients Covered by Each Insurer")
plt.show()

#How many appointments came through each insurer?"
insurance1=merge_data["insurance_provider"].value_counts()
plt.bar(insurance1.index,insurance1.values,color="pink")
plt.xlabel("insurance provider")
plt.ylabel("Number of appointments")
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.title("Number of Appointments by Insurer”")
plt.show()

#doctor specilization count
doc_sp=doctor["specialization"].value_counts()
plt.bar(doc_sp.index,doc_sp.values)
plt.xlabel("specilization type")
plt.ylabel("count")
plt.title("doctor specialization count")
plt.show()

#treatment type distribution 
type=treatment["treatment_type"].value_counts()
type.plot(kind="barh",color="purple")
plt.xlabel("Count")
plt.ylabel("treatment type")
plt.title("Appointment count vs Treatment type")
plt.show()

#branch distribiution
branch=merge_data["hospital_branch"].value_counts()
plt.figure(figsize=(12,6))
branch.plot(kind="bar",color="green")
plt.ylabel("count")
plt.title("appointmnet count vs hospital branch")
plt.tight_layout()
plt.show()

#payment method distribution
pay=billing["payment_method"].value_counts()
plt.pie(pay.values,labels=pay.index,autopct="%1.1f%%")
plt.title("payment method distribution")
plt.show()

#payment_status distribution

print(billing.head())
data=merge_data[merge_data["status"]=="Completed"]
pay_status=data["payment_status"].value_counts()
plt.pie(pay_status,labels=pay_status.index,autopct="%1.1f%%")
plt.title("payment status distribution")
plt.show()

#determining appoint id and patient_id where payents stus is pendinga and failed,and appoint stauta=completed


result=merge_data[
    (merge_data["status"]=="Completed")&
    (merge_data["payment_status"].isin(["Pending","Failed"]))]

print(result[["appointment_id","patient_id_x","status","payment_status"]])

print(result["payment_status"].value_counts())
list_failed=result[result["payment_status"]=="Failed"]
list_pending=result[result["payment_status"]=="Pending"]
print(list_failed[["appointment_id","patient_id_x","pat_fullname","status","payment_status"]])
print(list_pending[["appointment_id","patient_id_x","pat_fullname","status","payment_status"]])


revenue_risk=result["amount"].sum()
print("revenue at risk =",revenue_risk)
print(result["payment_method"].value_counts())

#A number of completed appointments had pending or failed payments, representing uncollected revenue.
#  Monitoring these cases can help improve the hospital's billing and collection process."
#total hsopital revenue and brach contribution
paid_data=merge_data[
    merge_data["payment_status"]=="Paid"]
total_revenue=paid_data["amount"].sum()

print("total hospital revenue=",round(total_revenue,2))

branch_revenue=paid_data.groupby(paid_data["hospital_branch"])["amount"].sum()
print(branch_revenue)

plt.pie(branch_revenue,labels=branch_revenue.index,autopct="%1.1f%%")
plt.title("Hospital branch share in total revenue")
plt.show()

#doctor and traetment type share in total revenue

doc_share=paid_data["amount"].groupby(paid_data["doc_fullname"]).sum().sort_values(ascending=False)
print(doc_share)

treatment_share=paid_data["amount"].groupby(paid_data["treatment_type"]).sum().sort_values(ascending=False)
print(treatment_share)


import seaborn as sns
sns.barplot(
    x=treatment_share.index,
    y=treatment_share.values,
    palette="viridis"
)
plt.title("Treatment type reveneue share")
plt.show()

sns.barplot(x=doc_share.values,
    y=doc_share.index,palette="viridis"
)
plt.title("Revenue share by doctor")
plt.show()

#revenue shre by insurance provider
print(appointment["appointment_date"].describe())

date_revenue=paid_data.groupby(paid_data["appointment_date"].dt.to_period("M"))["amount"].sum()
plt.plot(date_revenue.index.astype(str),date_revenue.values,marker="o")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.title("Revenue Trend Over Time")
plt.show()

#appointment 
print(treatment.head())

app_date=appointment.groupby(appointment["appointment_date"].dt.to_period("M"))["appointment_id"].count()
plt.plot(app_date.index.astype(str),app_date.values,marker="o")
plt.xlabel("Date")
plt.ylabel("Number of Appointments")
plt.title("Appointments by Date")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#weekday based
from datetime import datetime


paid_data["weekday"]=paid_data["appointment_date"].dt.day_name()
weekday_revenue=paid_data["amount"].groupby(paid_data["weekday"]).sum()

weekday_order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
weekday_revenue=weekday_revenue.reindex(weekday_order)
plt.bar(weekday_revenue.index,weekday_revenue.values)
plt.ylabel("Revenue")
plt.title("Revenue by Weekday")
plt.show()

#forcat monlthly fpor nect 3 months 
#montly appoinment forcast

from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings
warnings.filterwarnings("ignore")
monthly_app=appointment.groupby(appointment["appointment_date"].dt.to_period("M")).size()
monthly_app.index=monthly_app.index.to_timestamp()
print(monthly_app)

model=ExponentialSmoothing(monthly_app,trend="add",seasonal=None)
model_fit=model.fit()
forcast=model_fit.forecast(3)

monthly_app.plot(label="Actual")
forcast.plot(label="Forcast",linestyle="--")
plt.title("Monthly Appointment Volume Forecast")
plt.legend()
plt.savefig("Monthyl=app-forcast.png")
plt.show()

#monthly revenue fforcast

monthly_revenue=paid_data.groupby(paid_data["appointment_date"].dt.to_period("M"))["amount"].sum()
monthly_revenue.index=monthly_revenue.index.to_timestamp()
monthly_revenue.index = pd.DatetimeIndex(monthly_revenue.index, freq="MS")
print(monthly_revenue)

model=ExponentialSmoothing(monthly_revenue,trend="add",seasonal=None)
model_fit=model.fit()
forecast=model_fit.forecast(3)

monthly_revenue.plot(label="actual")
forecast.plot(label="forcast")
plt.title("Monthly revenue forcast")
plt.savefig("monthly_revenue_forcast.png")
plt.show()
#The model projects a continued upward/downward trend over the next 3 months based on the observed data. A straight-line forecast reflects the absence of strong seasonal patterns in 12 months of data."


#conclusion:

#patient overview:

import os

# This automatically finds your desktop path
desktop = os.path.join(os.path.expanduser("~"), "Desktop", "HospitalProject")

# Creates the folder if it doesnt exist
os.makedirs(desktop, exist_ok=True)

# Save all tables
merge_data.to_csv(os.path.join(desktop, "merge_data.csv"), index=False)
paid_data.to_csv(os.path.join(desktop, "paid_data.csv"), index=False)
branch_revenue.reset_index().to_csv(os.path.join(desktop, "branch_revenue.csv"), index=False)

print("Files Saved to Desktop → HospitalProject folder!")
patient.to_csv(os.path.join(desktop, "patient.csv"), index=False)
doctor.to_csv(os.path.join(desktop, "doctor.csv"), index=False)
