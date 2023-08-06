/*This is a restriced access only table that contains the raw UIDs that can be used to
 connect the data in MedQuery to PACS or other hospital systems
 */
 CREATE TABLE IF NOT EXISTS restricted.r_uids_table (
    r_series_uid TEXT NOT NULL,
    r_study_uid TEXT NOT NULL,
    r_patient_uid TEXT NOT NULL,
    series_uid TEXT NOT NULL,
    study_uid TEXT NOT NULL,
    patient_uid TEXT NOT NULL,
    patient_name TEXT,
    FOREIGN KEY (series_uid) REFERENCES multimodal_image_table (series_uid),
    FOREIGN KEY (patient_uid) REFERENCES patient_table (patient_uid)
);
