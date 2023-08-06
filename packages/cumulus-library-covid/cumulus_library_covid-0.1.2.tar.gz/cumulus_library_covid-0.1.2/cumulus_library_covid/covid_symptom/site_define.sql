-- ############################################################
-- Healthcare Site Specific

-- PCR test codes
--
CREATE OR REPLACE VIEW covid_symptom__site_pcr AS
SELECT
    t.from_system,
    t.from_code,
    t.analyte,
    t.code_system,
    t.code,
    t.display
FROM
    (
        VALUES
        (
            'BCH',
            'LAB:1043473617',
            'COVID',
            'http://loinc.org',
            '94500-6',
            'SARS-CoV-2 (COVID-19) RNA [Presence] in Respiratory specimen by NAA with probe detection' --noqa:LT05
        ),
        (
            'BCH',
            'LAB:1044804335',
            'COVID',
            'http://loinc.org',
            '94500-6',
            'SARS-CoV-2 (COVID-19) RNA [Presence] in Respiratory specimen by NAA with probe detection' --noqa:LT05
        ),
        (
            'BCH',
            'LAB:1044704735',
            'COVID',
            'http://loinc.org',
            '94500-6',
            'SARS-CoV-2 (COVID-19) RNA [Presence] in Respiratory specimen by NAA with probe detection' --noqa:LT05
        ),
        (
            'BCH',
            'LAB:1134792565',
            'COVID',
            'http://loinc.org',
            '95406-5',
            'SARS-CoV-2 (COVID-19) RNA [Presence] in Nose by NAA with probe detection'
        ),
        (
            'BCH',
            'LAB:1148157467',
            'COVID',
            'http://loinc.org',
            '95406-5',
            'SARS-CoV-2 (COVID-19) RNA [Presence] in Nose by NAA with probe detection'
        ),
        (
            'BCH',
            'LAB:467288722',
            'FLU',
            'http://loinc.org',
            '85477-8',
            'Influenza virus A RNA [Presence] in Upper respiratory specimen by NAA with probe detection' --noqa:LT05
        ),
        (
            'BCH',
            'LAB:152831642',
            'FLU',
            'http://loinc.org',
            '85476-0',
            'Influenza virus A and B and Respiratory syncytial virus RNA panel - Upper respiratory specimen by NAA with probe detection' --noqa:LT05
        ),
        (
            'BCH',
            'LAB:467288694',
            'FLU',
            'http://loinc.org',
            '85478-6',
            'Influenza virus B RNA [Presence] in Upper respiratory specimen by NAA with probe detection' --noqa:LT05
        ),
        (
            'BCH',
            'LAB:13815125',
            'FLU',
            'http://loinc.org',
            '62462-7',
            'Influenza virus A+B RNA [Presence] in Specimen by NAA with probe detection'
        ),
        (
            'BCH',
            'LAB:467288700',
            'RSV',
            'http://loinc.org',
            '85479-4',
            'Respiratory syncytial virus RNA [Presence] in Upper respiratory specimen by NAA with probe detection' --noqa:LT05
        )
    )
    AS t (from_system, from_code, analyte, code_system, code, display);

-- Emergency Department Notes
--
CREATE OR REPLACE VIEW covid_symptom__site_ed_note AS
SELECT
    t.from_system,
    t.from_code,
    t.from_display,
    t.code_system,
    t.code,
    t.display
FROM
    (
        VALUES
        (
            'BCH',
            'NOTE:149798455',
            'Emergency MD',
            'http://loinc.org',
            '34878-9',
            'Emergency medicine Note'
        ),
        (
            'BCH',
            'NOTE:159552404',
            'ED Note Scanned',
            'http://loinc.org',
            '34878-9',
            'Emergency medicine Note'
        ),
        (
            'BCH',
            'NOTE:3807712',
            'ED Note',
            'http://loinc.org',
            '34878-9',
            'Emergency medicine Note'
        ),
        (
            'BCH',
            'NOTE:189094644',
            'Emergency Dept Scanned Forms',
            'http://loinc.org',
            '34878-9',
            'Emergency medicine Note'
        ),
        (
            'BCH',
            'NOTE:189094576',
            'ED Scanned',
            'http://loinc.org',
            '34878-9',
            'Emergency medicine Note'
        ),
        (
            'BCH',
            'NOTE:3710480',
            'ED Consultation',
            'http://loinc.org',
            '51846-4',
            'Emergency department Consult note'
        )
    --    , ('BCH', 'NOTE:318198113', 'ED Social Work',                 'http://loinc.org','28653-4', 'Social work Note')
    --    , ('BCH', 'NOTE:318198110', 'ED Social Work Brief Screening', 'http://loinc.org','28653-4', 'Social work Note')
    --    , ('BCH', 'NOTE:318198107', 'ED Social Work Assessment',      'http://loinc.org','28653-4', 'Social work Note')
    --    , ('BCH', 'NOTE:189094619', 'Sexual Assault Nurse Exam (SANE) Report', 'http://loinc.org',  '57053-1', 'Nurse Emergency department Note')
    )
    AS t (from_system, from_code, from_display, code_system, code, display);
