import pandas as pd
import numpy as np
import random

n = 1000

data = {
    "Patient_ID":[f"P{i}" for i in range(1,n+1)],
    "Age":np.random.randint(1,90,n),
    "Gender":np.random.choice(["Male","Female"],n),
    "Arrival_Time":np.random.randint(0,24,n),
    "Heart_Rate":np.random.randint(50,180,n),
    "Oxygen_Level":np.random.randint(75,100,n),
    "Temperature":np.round(np.random.uniform(97,105,n),1),
    "Blood_Pressure":np.random.randint(90,180,n),
    "Severity_Score":np.random.randint(1,11,n),
    "Waiting_Time":np.random.randint(1,180,n),
    "Treatment_Required":np.random.choice(["Yes","No"],n)
}

df = pd.DataFrame(data)

df.to_csv("hospital_patients.csv",index=False)

print("Dataset Created")

validation_report = {}

validation_report["Invalid Age"] = len(df[df["Age"]<0])

validation_report["Invalid Oxygen"] = len(
    df[(df["Oxygen_Level"]<0) |
       (df["Oxygen_Level"]>100)]
)

validation_report["Invalid Heart Rate"] = len(
    df[(df["Heart_Rate"]<20) |
       (df["Heart_Rate"]>250)]
)

validation_report["Missing Values"] = df.isnull().sum().sum()

print(validation_report)

def priority(row):

    score = 0

    if row["Oxygen_Level"] < 90:
        score += 30

    if row["Heart_Rate"] > 120:
        score += 20

    if row["Temperature"] > 102:
        score += 15

    if row["Age"] > 65:
        score += 10

    score += row["Severity_Score"] * 5

    return score

df["Priority_Score"] = df.apply(priority,axis=1)

def category(score):

    if score <= 25:
        return "Normal"

    elif score <= 50:
        return "Moderate"

    elif score <= 75:
        return "High Priority"

    else:
        return "Critical"

df["Priority_Category"] = df["Priority_Score"].apply(category)

df.to_csv("hospital_patients.csv",index=False)

queue_analysis = df["Priority_Category"].value_counts()

avg_wait = df.groupby(
    "Priority_Category"
)["Waiting_Time"].mean()

print(queue_analysis)
print(avg_wait)

total_patients = len(df)

doctors_daily = np.ceil(total_patients/20)

peak_hour_patients = df.groupby(
    "Arrival_Time"
).size().max()

peak_doctors = np.ceil(
    peak_hour_patients/20
)

print("Doctors Daily:",doctors_daily)
print("Peak Doctors:",peak_doctors)

beds_daily = int(total_patients*0.30)

beds_weekly = beds_daily*7

print("Beds Daily:",beds_daily)
print("Beds Weekly:",beds_weekly)

hourly = df.groupby(
    "Arrival_Time"
).size()

busiest = hourly.idxmax()

least = hourly.idxmin()

average = hourly.mean()

print("Busiest Hour:",busiest)
print("Least Busy Hour:",least)

print("Mean Age:",df["Age"].mean())

print("Median Age:",
      df["Age"].median())

print("Age Std:",
      df["Age"].std())

print("Average Oxygen:",
      df["Oxygen_Level"].mean())

print("Average Heart Rate:",
      df["Heart_Rate"].mean())

print("Average Temperature:",
      df["Temperature"].mean())

print("Average Waiting:",
      df["Waiting_Time"].mean())

print("Maximum Waiting:",
      df["Waiting_Time"].max())

print("Minimum Waiting:",
      df["Waiting_Time"].min())

critical = len(
    df[df["Priority_Category"]=="Critical"]
)

if critical < 20:
    alert = "GREEN"

elif critical <= 50:
    alert = "YELLOW"

elif critical <= 100:
    alert = "ORANGE"

else:
    alert = "RED"

print("Alert Level:",alert)

import matplotlib.pyplot as plt
import seaborn as sns

sns.histplot(df["Age"],bins=20)

plt.title("Age Distribution")

plt.show()

sns.histplot(df["Oxygen_Level"])

plt.show()

sns.countplot(
    x=df["Priority_Category"]
)

plt.show()

hourly.plot(kind="bar")

plt.title("Hourly Arrivals")

plt.show()

sns.boxplot(
    y=df["Waiting_Time"]
)

plt.show()

plt.bar(
    ["Daily","Weekly"],
    [beds_daily,beds_weekly]
)

plt.show()

forecast_patients = int(
    total_patients*1.10
)

future_doctors = np.ceil(
    forecast_patients/20
)

future_beds = int(
    forecast_patients*0.30
)

future_staff = int(
    forecast_patients*0.10
)

print(future_doctors)
print(future_beds)
print(future_staff)

kpi = {
    "Total Patients":total_patients,
    "Critical Patients":critical,
    "Average Waiting":
        round(df["Waiting_Time"].mean(),2),

    "Bed Utilization":
        round((beds_daily/500)*100,2),

    "Doctor Utilization":
        round((total_patients/
              (doctors_daily*20))*100,2)
}

with pd.ExcelWriter(
    "hospital_analytics_report.xlsx"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Patient Records",
        index=False
    )

    queue_analysis.to_excel(
        writer,
        sheet_name="Priority Analysis"
    )

    pd.DataFrame({
        "Doctors Daily":
        [doctors_daily],

        "Peak Doctors":
        [peak_doctors]
    }).to_excel(
        writer,
        sheet_name="Doctor Requirement"
    )

    pd.DataFrame({
        "Beds Daily":[beds_daily],
        "Beds Weekly":[beds_weekly]
    }).to_excel(
        writer,
        sheet_name="Bed Occupancy"
    )

    pd.DataFrame(kpi,index=[0]).to_excel(
        writer,
        sheet_name="Summary Dashboard"
    )

print("Excel Report Created")

recommendations = []

if critical > 100:
    recommendations.append(
        "Increase ICU beds immediately."
    )

recommendations.append(
    "Increase doctors during peak hours."
)

recommendations.append(
    "Reduce waiting time using triage."
)

recommendations.append(
    "Hire additional emergency nurses."
)

recommendations.append(
    "Improve patient routing."
)

recommendations.append(
    "Allocate more beds."
)

recommendations.append(
    "Monitor oxygen critical patients."
)

recommendations.append(
    "Use predictive scheduling."
)

recommendations.append(
    "Improve ambulance coordination."
)

recommendations.append(
    "Automate emergency alerts."
)

print(recommendations)
