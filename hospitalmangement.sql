create DATABASE hospital_db;
use hospital_db;
select * from appointments;
select * from billing;
select * from doctors;
select * from treatments;
select * from patients;
select p.patient_id,p.first_name,p.last_name,d.doctor_id,d.first_name,d.last_name,
a.appointment_date From appointments a JOIN patients p 
ON a.patient_id=p.patient_id
JOIN doctors d ON a.doctor_id=d.doctor_id;



ALTER TABLE doctors 
ADD column doc_fullname CHAR(100);
UPDATE doctors 
set doc_fullname=concat(first_name," ",last_name);
select*from doctors;

#doctorwith the most appointmnets?
select a.doctor_id,d.doc_fullname,count(*) as total_appointments
FROM appointments a
join doctors d 
ON a.doctor_id=d.doctor_id group by a.doctor_id,d.doc_fullname ORDER BY total_appointments DESC;

#which treatment generate the high revenue?

select treatment_type,sum(cost) as total_amount
FROM treatments
GROUP BY treatment_type ORDER BY total_amount DESC;

ALTER TABLE patients
add column pat_fullname char(100);
UPDATE patients
SET pat_fullname=CONCAT(first_name," " ,last_name);
select * from patients;

Create VIEW patient_summary AS
(select a.appointment_id,a.appointment_date,a.patient_id,
p.pat_fullname,a.doctor_id,d.doc_fullname
from appointments a
join patients p ON a.patient_id=p.patient_id
join doctors d ON  a.doctor_id=d.doctor_id);
select * from patient_summary;
















