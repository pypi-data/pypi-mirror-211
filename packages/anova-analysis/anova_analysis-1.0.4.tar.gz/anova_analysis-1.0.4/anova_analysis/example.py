from anova_analysis import ANOVA_RBD

rep = 4
treat = 23
file = "data/MODEL_DATA.xlsx"
output = 'MODEL_DATA'

result = ANOVA_RBD.RBD(rep, treat, file, output)

CF = result["correction_factor"]
TSS = result["total_sum_of_square"]
RSS = result["replication_sum_of_square"]
TSS = result["treatment_sum_of_square"]
ESS = result["error_sum_of_square"]
Rdf = result["replication_df"]
Tdf = result["treatment_df"],
Edf = result["errors_df"],
RMSS = result["rep_mean_ss"],
TMSS = result["tre_mean_ss"],
EMSS = result["error_mean_ss"]

print("")