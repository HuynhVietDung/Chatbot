from utils.connect import get_sheet, get_data
import re
import pandas as pd
import bcrypt


## Available Sheets name are "Account", "Appointerment", "Drug", "Doctor", "Patient", "Package"

######################## Account ########################
def create_account(id, email, password, role= "user") -> None:
    account_sheet = get_sheet("Account")

    idx = len(account_sheet.get_all_values()) + 1
    account_sheet.insert_row([id, email, password, 1, role], idx)


def update_account(id, email="", password="") -> None:
    account_sheet = get_sheet("Account")

    if len(account_sheet.get_all_values()) > 1:
        row_idx = account_sheet.find(id).row

        if email != "":
            account_sheet.update_cell(row_idx, 2, email)

        if password != "":
            account_sheet.update_cell(row_idx, 3, password)
            
def update_use(id, use) -> None:
    account_sheet = get_sheet("Account")

    if len(account_sheet.get_all_values()) > 1:
        row_idx = account_sheet.find(id).row
        account_sheet.update_cell(row_idx, 4, use)

def find_accountID(email: str) -> str:
    df = get_data("Account")
    return df[df["Email"] == email].iloc[0]["ID"]

def find_accountEmail(ID: str) -> str:
    df = get_data("Account")
    return df[df["ID"] == ID].iloc[0]["Email"]

def find_role(id:str) -> str:
    df = get_data("Account")
    return df[df["ID"] == id].iloc[0]["Role"]

def is_existed(email, df=pd.DataFrame()):
    df = get_data("Account") if df.empty else df
    return email in df["Email"].values

def is_valid_email(pw: str) -> bool:
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', pw)

def get_password(email):
    df = get_data("Account")
    return df[df["Email"] == email].iloc[0]["Password"]

def hash_pass(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_pass(new_pw: str, old_pw:str):
    return bcrypt.checkpw(new_pw.encode('utf-8'), old_pw.encode('utf-8'))

def delete_account(ID:str) -> None:
    account_sheet = get_sheet("Account")
    if len(account_sheet.get_all_values()) > 1:
        row_idx = account_sheet.find(ID).row
        if row_idx != None:
            account_sheet.delete_rows(row_idx)

######################## Patient ########################
def create_patient_record(
    id, email, name, age="", phone="", gender="Nam", image=""
) -> None:
    patient_sheet = get_sheet("Patient")
    idx = len(patient_sheet.get_all_values()) + 1
    patient_sheet.insert_row([id, email, name, age, phone, gender, image], idx)


def update_patient_record(
    id, email="", name="", age="", phone="", gender="", image=""
) -> None:
    patient_sheet = get_sheet("Patient")

    if len(patient_sheet.get_all_values()) > 1:
        row_idx = patient_sheet.find(id).row

        if email != "":
            patient_sheet.update_cell(row_idx, 2, email)
        if name != "":
            patient_sheet.update_cell(row_idx, 3, name)
        if age != "":
            patient_sheet.update_cell(row_idx, 4, age)
        if phone != "":
            patient_sheet.update_cell(row_idx, 5, phone)
        if gender != "":
            patient_sheet.update_cell(row_idx, 6, gender)
        if image != "":
            patient_sheet.update_cell(row_idx, 7, image)


######################## Appointment ########################
def create_appointment(ID, PatientID, DoctorID, Time, Description="") -> None:
    appointment_sheet = get_sheet("Appointment")
    idx = len(appointment_sheet.get_all_values()) + 1
    appointment_sheet.insert_row([ID, PatientID, DoctorID, Time, Description], idx)


def filter_appointment(PatientID: str) -> pd.DataFrame:
    appointment = get_data("Appointment")
    if not appointment.empty:
        patient_app = appointment[appointment["PatientID"] == PatientID]
        if not patient_app.empty:
            return patient_app

    return pd.DataFrame()


def update_appointment(id, DoctorID="", Time="", Description="") -> None:
    appointment_sheet = get_sheet("Appointment")

    if len(appointment_sheet.get_all_values()) > 1:
        row_idx = appointment_sheet.find(id).row

        if DoctorID != "":
            appointment_sheet.update_cell(row_idx, 3, DoctorID)
        if Time != "":
            appointment_sheet.update_cell(row_idx, 4, Time)
        if Description != "":
            appointment_sheet.update_cell(row_idx, 5, Description)


def cancel_appointment(ID: str) -> None:
    appointment_sheet = get_sheet("Appointment")
    if len(appointment_sheet.get_all_values()) > 1:
        row_idx = appointment_sheet.find(ID).row
        if row_idx != None:
            appointment_sheet.delete_rows(row_idx)


######################## Doctor ########################
def find_doctor_name(ID: str) ->  str:
    df = get_data("Doctor")
    return df[df["ID"] == ID].iloc[0]["Name"]

def create_doctor(id, name, title, spec, img, avai, time) -> None:
    doc_sheet = get_sheet("Doctor")

    idx = len(doc_sheet.get_all_values()) + 1
    doc_sheet.insert_row([id, name, title, spec, img, avai, time], idx)

def delete_doctor(ID: str) -> None:
    doctor_sheet = get_sheet("Doctor")
    if len(doctor_sheet.get_all_values()) > 1:
        row_idx = doctor_sheet.find(ID).row
        if row_idx != None:
            doctor_sheet.delete_rows(row_idx)
            
######################## Drug ########################



######################## Package ########################
def create_package(id: str, name:str, price: str, description: str, link: str)-> None:
    package_sheet = get_sheet("Package")

    idx = len(package_sheet.get_all_values()) + 1
    package_sheet.insert_row([id, name, price, description, link], idx)

def find_packageID(name: str) ->  str:
    df = get_data("Package")
    return df[df["Name"] == name].iloc[0]

def update_package(id: str, name:str, price: str, description: str, link: str)-> None:
    package_sheet = get_sheet("Package")

    if len(package_sheet.get_all_values()) > 1:
        row_idx = package_sheet.find(id).row

        if name != "":
            package_sheet.update_cell(row_idx, 2, name)
        if price != "":
            package_sheet.update_cell(row_idx, 3, price)
        if description != "":
            package_sheet.update_cell(row_idx, 4, description)
        if link != "":
            package_sheet.update_cell(row_idx, 5, link)

def delete_package(ID: str) -> None:
    package_sheet = get_sheet("Package")
    if len(package_sheet.get_all_values()) > 1:
        row_idx = package_sheet.find(ID).row
        if row_idx != None:
            package_sheet.delete_rows(row_idx)

######################## Payment ########################

def create_payment(id: str, PatientID: str, Email:str, PackageID: str, Time: str, link: str)-> None:
    package_sheet = get_sheet("Payment")

    idx = len(package_sheet.get_all_values()) + 1
    package_sheet.insert_row([id, PatientID, PackageID, Email, Time, link, 0], idx)

def update_flag(id: str)-> None:
    package_sheet = get_sheet("Payment")

    if len(package_sheet.get_all_values()) > 1:
        row_idx = package_sheet.find(id).row
        package_sheet.update_cell(row_idx, 7, 1)
