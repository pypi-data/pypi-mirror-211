""" utils for covid count verification """
from cumulus_library.schema import counts


def count_covid_prevalence_ed_month():
    """Convenience function for hand count verification"""
    view_name = "covid_symptom_count_prevalence_ed_month"
    from_table = "covid_symptom__prevalence_ed"
    cols = [
        "covid_icd10",
        "covid_pcr_result",
        "covid_symptom",
        "symptom_icd10_display",
        "variant_era",
        "author_month",
        "age_group",
    ]

    return counts.count_encounter(view_name, from_table, cols)
