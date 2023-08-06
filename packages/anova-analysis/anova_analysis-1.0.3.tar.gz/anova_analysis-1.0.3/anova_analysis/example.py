from anova_analysis import ANOVA_RBD

rep = 4
treat = 23
file = "data/MODEL_DATA.xlsx"
output = 'MODEL_DATA'

ANOVA_RBD.RBD(rep, treat, file, output)