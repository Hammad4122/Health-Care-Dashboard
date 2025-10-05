# Importing modules
import pandas as pd
import streamlit as st
import os
from streamlit_option_menu import option_menu
import altair as alt

#----------------------------------------

def run_app():
    bill,department,doctor,patient,treatment = import_data()
    # ------------------
    # Dashboard
    # ------------------
    st.title("🏥 Healthcare Dashboard")
    st.markdown('<style>div.block-container{padding-top:50px;}</style>',unsafe_allow_html=True)
    datasets = ["Bills","Department","Doctors","Patient"]
    st.divider()
    # ____SideBar____
    with st.sidebar:
        title = st.title("📃 Select Dataset")
        selected_dataset = st.selectbox(
            "Choose a Dataset",
            datasets,
            label_visibility='collapsed'
        )
        st.success(f"{selected_dataset} dataset has been selected")

    #----------------------------------------------
    #              Doctors
    #----------------------------------------------
    if selected_dataset == "Bills":
        st.header("Bills Dataset")
        st.divider()
        paid_bills = len(bill.loc[bill["paid_status"] == "Paid","paid_status"])
        unpaid_bills = len(bill.loc[bill["paid_status"] == "Unpaid","paid_status"])
        total_bills = bill['paid_status'].count()
        payment_status = bill.groupby('paid_status').size().reset_index(name='Counts')

        #---------------------------------------
        #           Visualization
        #---------------------------------------
        st.subheader("Bills Status",divider=True,width='content')
        st.bar_chart(data = payment_status,
                        x='paid_status',y='Counts',
                        x_label='',y_label='',
                        color="#37FF4475"
                        )
        #-------------------------------------------
        #              Metrics
        #-------------------------------------------
        st.divider()
        st.subheader("🔢Metrics",width='content',divider=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Bills", total_bills)
        col2.metric("Paid Bills", paid_bills)
        col3.metric("Unpaid Bills", unpaid_bills)


    #-----------------------------------------
    #           Department Data
    #-----------------------------------------
    elif selected_dataset == "Department":
        st.header("Department Dataset")
        st.divider()
        grouped_department_total_beds = department.groupby('department')['total_beds'].sum().reset_index(name = 'total_beds')
        grouped_department_occupied_beds = department.groupby('department')['occupied_beds'].sum().reset_index(name = 'occupied_beds')
        #---------------------------------------
        #           Visualization
        #---------------------------------------
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Total Number of beds in each Department",divider=True,width='content')
            st.bar_chart(data=grouped_department_total_beds,
                         x = 'department',
                         y = 'total_beds',
                         x_label="Department",
                         y_label="Total Beds",
                         color="#D7B635AB")
        with col2:
            st.subheader("Number of Occupied Beds in each Department",divider=True,width='content')
            st.bar_chart(data=grouped_department_occupied_beds,
                         x='department',
                         y='occupied_beds',
                         x_label='Department',
                         y_label='Occupied Beds',
                         color="#21FFCFBC")
            
        #-------------------------------------------
        #              Metrics
        #-------------------------------------------
        st.divider()
        st.subheader("🔢Metrics",width='content',divider=True)
        st.subheader(f"Total Beds : {department['total_beds'].sum()}")   
        st.subheader(f"Occupied Beds : {department['occupied_beds'].sum()}")  
        st.subheader(f"Non-Occupied Beds : {(department['total_beds'].sum()) - (department['occupied_beds'].sum())}")

    #----------------------------------------------
    #              Doctors
    #----------------------------------------------
    elif selected_dataset == 'Doctors':
        st.header("Doctors Dataset")
        st.divider()
        #-------------------------------------------------------------------------------
        #        User can search for a doctor by giving the required information
        #-------------------------------------------------------------------------------
        user_search_input = st.text_input("Enter the Doctor ID or his/her name : ")
        user_department_search_input = st.text_input("Enter the department : ")
        search_button = st.button("Search")
        if search_button:
            if not(user_search_input and user_department_search_input):
                if user_search_input or user_department_search_input:
                    if user_search_input.isdigit():
                        search_result = doctor.loc[(doctor['doctor_id'] == int(user_search_input))]
                    else : 
                        search_result = doctor.loc[(doctor['name'].str.lower() == user_search_input.lower())]
                    if user_department_search_input:
                        dept_search_result = doctor.loc[doctor['department'].str.lower() == user_department_search_input.lower()]
                        st.dataframe(dept_search_result)
                    if user_search_input:
                        st.dataframe(search_result,use_container_width=True)
            else :
                if user_search_input.isdigit():
                    search_result = doctor.loc[(doctor["doctor_id"] == int(user_search_input)) & (doctor["department"].str.lower() == user_department_search_input.lower())]
                else :
                    search_result = doctor.loc[(doctor['name'].str.lower() == user_search_input.lower()) & (doctor["department"].str.lower() == user_department_search_input.lower())]
                st.dataframe(search_result,use_container_width=True)
        
        selected_option = option_menu(menu_title=None,
                                options=['Graph 1',"Graph 2","Graph 3"],
                                default_index=0,
                                orientation="horizontal",
                                menu_icon='cast',icons=['bar-chart-fill','bar-chart-fill','bar-chart-fill'])
        #-----------------------------------------------------------------------
        #                          Visualizations
        #-----------------------------------------------------------------------
        if selected_option == 'Graph 1':
            avg_experience = doctor.groupby('department')['years_experience'].mean().reset_index()
            st.subheader("Average Experience of Doctors from each Department",divider='green',width='content')
            st.bar_chart(data=avg_experience,
                         x='department',
                         y='years_experience',
                         x_label='Department',
                         y_label='AVG Experience',
                         color="#AEFF57CB")
        elif selected_option == 'Graph 2':
            seen_patients_dept = doctor.groupby('department')['patients_seen'].sum().reset_index()
            st.subheader("Total Patients seen by each Department",divider='blue',width='content')
            st.bar_chart(data = seen_patients_dept,
                         x='department',
                         y='patients_seen',
                         x_label='Department',
                         y_label='Patients Seen',
                         color= "#3EF2FFC7")
        elif selected_option == 'Graph 3':
            docs_in_dept = doctor.groupby('department')['doctor_id'].count().reset_index()
            st.subheader("Doctors in each Department",divider="violet",width='content')
            st.scatter_chart(data=docs_in_dept,
                          x='department',
                          y='doctor_id',
                          x_label='Department',
                          y_label='No. of Doctors',
                          color="#BDA8FFEF")
        #------------------------------
        #         <- No-Metrics
        #------------------------------


    elif selected_dataset == 'Patient':
        st.header("Patient Dataset")
        st.divider()

        #--------------------------------------------------------------
        #           Searching Logic for Patient data search
        #--------------------------------------------------------------
        user_patient_search_input = st.text_input("Enter the name or id of the patient : ")
        user_patient_department_search_input = st.text_input("Enter the department : ")
        search_button = st.button("Search")
        if search_button:
            if not(user_patient_search_input and user_patient_department_search_input):
                if user_patient_search_input or user_patient_department_search_input:
                    if user_patient_search_input.isdigit():
                        search_result = patient.loc[(patient['patient_id'] == int(user_patient_search_input))]
                    else : 
                        search_result = patient.loc[(patient['name'].str.lower() == user_patient_search_input.lower())]
                    if user_patient_department_search_input:
                        dept_search_result = patient.loc[patient['department'].str.lower() == user_patient_department_search_input.lower()]
                        st.dataframe(dept_search_result)
                    if user_patient_search_input:
                        st.dataframe(search_result,use_container_width=True)
            else :
                if user_patient_search_input.isdigit():
                    search_result = patient.loc[(patient["patient_id"] == int(user_patient_search_input)) & (patient["department"].str.lower() == user_patient_department_search_input.lower())]
                else :
                    search_result = patient.loc[(patient['name'].str.lower() == user_patient_search_input.lower()) & (patient["department"].str.lower() == user_patient_department_search_input.lower())]
                st.dataframe(search_result,use_container_width=True)
        #-------------------------------------
        #           Visualizations
        #-------------------------------------
        selected_option = option_menu(menu_title=None,
                                options=['Graph 1',"Graph 2","Graph 3"],
                                default_index=0,
                                orientation="horizontal",
                                menu_icon='cast',icons=['bar-chart-fill','bar-chart-fill','bar-chart-fill'])
        if selected_option == 'Graph 1':
            patient_status = patient.groupby('outcome').size().reset_index(name='Amount')
            st.subheader("Patients Status",divider='orange',width='content')
            st.bar_chart(data = patient_status,
                         x='outcome',
                         y='Amount',
                         x_label='Status',
                         y_label='Number')
        elif selected_option == 'Graph 2':
            patients_in_each_dept = patient.groupby('department')['patient_id'].count().reset_index()
            st.subheader("Patients in each Department",divider='orange',width='content')
            st.bar_chart(data=patients_in_each_dept,
                         x='department',
                         y='patient_id',
                         x_label='Department',
                         y_label='Patients',
                         color="#FFFFFFCB")
        elif selected_option == 'Graph 3':
            patients_gender = patient.groupby('gender').size().reset_index(name='count')
            color_scale = alt.Scale(
                domain=['Male', 'Female', 'Other'],
                range=['#1E90FF', '#FF69B4', '#9B59B6']  # Blue, Pink, Purple
            )

            chart = alt.Chart(patients_gender).mark_bar().encode(
                x=alt.X('gender', title='Gender'),
                y=alt.Y('count', title='Number of Patients'),
                color=alt.Color('gender', scale=color_scale, legend=alt.Legend(title='Gender'))
            ).properties(
                title='Patients Gender Distribution'
            )

            st.altair_chart(chart, use_container_width=True)


def import_data():
    BASE_DIR = os.path.dirname(__file__)

    bill = pd.read_csv(os.path.join(BASE_DIR,"..", "cleaned_datasets", "cleaned_bill_data.csv"))
    department = pd.read_csv(os.path.join(BASE_DIR,"..", "cleaned_datasets", "cleaned_department_status_data.csv"))
    doctor = pd.read_csv(os.path.join(BASE_DIR,"..", "cleaned_datasets", "cleaned_doctor_data.csv"))
    patient = pd.read_csv(os.path.join(BASE_DIR,"..", "cleaned_datasets", "cleaned_patient_data.csv"))
    treatment = pd.read_csv(os.path.join(BASE_DIR,"..", "cleaned_datasets", "cleaned_treatment_data.csv"))
    return bill,department,doctor,patient,treatment


#*************************************************
if __name__ == "__main__":
    run_app()
