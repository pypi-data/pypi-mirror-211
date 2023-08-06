# ANOVA Analysis Package

The ANOVA Analysis Package is a Python package that provides functions for performing ``Two-Way ANOVA (Analysis of Variance) analysis`` on experimental data.
Currently it can perform RBD analysis only

## Installation

You can install the package using pip:
```
pip install anova_analysis
```
## Usage

- If you just want the output as a file:
```
from anova_analysis import ANOVA_RBD

 #Set the replication, treatment, input_file path and output_file_name

replication = 4
treatment = 23
input_file_path = "data/MODEL_DATA.xlsx"
output_file_name = "test"

 #Perform ANOVA analysis

ANOVA_RBD.RBD(replication, treatment, input_file_path, output_file_name )
```
- If you want the output to be used in for further analysis, 
you can then access the calculated values from the ``result`` dictionary:
```
result = ANOVA_RBD.RBD(replication, treatment, input_file_path, output_file_name)
```
- To access the ``result`` use the following
```
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

# Where CF, TSS,.. are variables
```
-  You can easily access them in your other Python file and use them as needed. Modify the returned data structure to suit your preferences and the specific values you want to access.

## Features

- Calculates the correction factor, total sum of squares, replication sum of squares, treatment sum of squares, and error sum of squares.
- Generates an ANOVA table with the source, degrees of freedom, sum of squares, mean square, F-values, and p-values at the 5% and 1% significance levels.
- Performs significance testing at the 5% and 1% levels to determine the statistical significance of the factors.
- Saves the ANOVA results in a text file for further analysis or reporting purposes.

## Example Dataset

- The package requires an Excel file containing the experimental data. The data should be arranged in a Randomized Block Design (RBD) format, with treatments (genotypes) in columns and replications in rows. 
- Please ensure that the excel file is in same format as it is given in this [repo](data/MODEL_DATA.xlsx) or below

                | Genotypes | R1    | R2     | R3     | R4     |
                |-----------|-------|--------|--------|--------|
                | 1x6       | 74.4  | 70.86  | 60.94  | 68     |
                | 1x7       | 91.82 | 99.18  | 118.88 | 120.68 |
                | 1x8       | 48.08 | 62.1   | 58.54  | 41.84  |
                | 2x6       | 59.06 | 65.62  | 81.62  | 86.76  |
                | 2x7       | 84.16 | 109.74 | 102.14 | 94.52  |

- If you have data in the below format, transform it to above said model (individual character) by using this [code](https://github.com/Insight-deviler/Folder-based-Character-Column-Transformation)

        | GENOTYPE | REPLICATION | Days to Maturity | PLANT HEIGHT (cm) |
        |----------|-------------|------------------|-------------------|
        | G1       | R1          | 4                | 5                 |
        | G1       | R2          | 5                | 6                 |
        | G1       | R3          | 4                | 9.3               |
        | G2       | R1          | 3                | 9.9               |
        | G2       | R2          | 6                | 7.5               |

## License
This package is licensed under the MIT License. See the [LICENSE](https://github.com/Insight-deviler/anova-analysis/blob/main/LICENSE.txt) file for more information.

## Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request on the GitHub repository.

## Authors
- Sarath S (insightagri10@gmail.com)
- Saranyadevi S

## Acknowledgements

- This package was developed as part of a research work. 
- This is based on ```Biometrical Methods in Quantitative Genetic Analysis by R.K. Singh and B.D. Chaudhary```
- I would like to thank all contributors and supporters.