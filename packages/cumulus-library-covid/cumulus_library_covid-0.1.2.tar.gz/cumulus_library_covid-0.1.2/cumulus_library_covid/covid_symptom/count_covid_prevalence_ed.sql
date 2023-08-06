CREATE TABLE covid_symptom__prevalence_ed AS
WITH from_period AS (
    SELECT DISTINCT
        encounter_ref,
        subject_ref,
        author_week,
        author_month,
        gender,
        race_display,
        age_at_visit,
        age_group,
        variant_era
    FROM covid_symptom__study_period
    WHERE ed_note
),

join_2020 AS (
    SELECT DISTINCT
        p.encounter_ref,
        p.subject_ref,
        p.author_week,
        p.author_month,
        p.gender,
        p.race_display,
        p.age_group,
        p.variant_era,
        COALESCE(pcr.covid_pcr_result_display, 'No PCR') AS covid_pcr_result,
        CASE
            WHEN dx.cond_code IS NOT NULL THEN 'COVID ICD10' ELSE 'No COVID ICD10'
        END AS covid_icd10,
        CASE
            WHEN
                (dx.cond_code IS NOT NULL OR pcr.covid_pcr_result_display = 'POSITIVE')
                THEN 'COVID DX'
            ELSE 'No COVID DX'
        END AS covid_dx,
        COALESCE(nlp.symptom_display, 'No Symptom') AS covid_symptom,
        COALESCE(icd10.icd10_display, 'No Symptom ICD10') AS symptom_icd10_display
    FROM from_period AS p
    LEFT JOIN covid_symptom__dx AS dx ON p.encounter_ref = dx.encounter_ref
    LEFT JOIN covid_symptom__pcr AS pcr ON p.encounter_ref = pcr.encounter_ref
    LEFT JOIN covid_symptom__symptom AS nlp ON p.encounter_ref = nlp.encounter_ref
    LEFT JOIN covid_symptom__symptom_icd10 AS icd10
        ON p.encounter_ref = icd10.encounter_ref
)

SELECT * FROM join_2020
ORDER BY author_week, variant_era;


CREATE OR REPLACE VIEW covid_symptom__count_prevalence_ed_month AS
WITH powerset AS (
    SELECT
        COUNT(DISTINCT encounter_ref) AS cnt,
        COUNT(DISTINCT subject_ref) AS cnt_subject,
        covid_dx,
        covid_icd10,
        covid_pcr_result,
        covid_symptom,
        symptom_icd10_display,
        variant_era,
        author_month,
        age_group
    FROM covid_symptom__prevalence_ed
    GROUP BY
        CUBE(
            covid_dx,
            covid_icd10,

            covid_pcr_result,
            covid_symptom,
            symptom_icd10_display,
            variant_era,
            author_month,
            age_group
        )
)

SELECT
    cnt,
    covid_dx,
    covid_icd10,
    covid_pcr_result,
    covid_symptom,
    symptom_icd10_display,
    variant_era,
    author_month,
    age_group
FROM powerset
WHERE cnt_subject >= 10
ORDER BY author_month ASC, cnt DESC;
