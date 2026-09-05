# AI Usage Disclosure

This project was completed with assistance from Claude (Anthropic), used as
a coding and analysis assistant throughout the development process.

## How AI Was Used
- Writing and explaining Python/SQL code for data ingestion, staging, and
  mart-layer transformations
- Helping design and interpret data quality tests and statistical analyses
- Assisting with dashboard (Streamlit) code structure and debugging
- Helping draft documentation (README, this file, pilot design writeups)
- General guidance on environment setup (Python, Git, VS Code) as this was
  a new toolchain for me

## How AI Was NOT Used
- All queries were run against real, live public data sources (NYC TLC,
  Open-Meteo, MTA Open Data, NYC taxi zone lookup) - no data was invented,
  simulated, or hardcoded
- All findings, numbers, and statistical results in this project come from
  actually executing the code against the real dataset - I verified outputs
  at each stage rather than accepting generated code blindly
- Analytical decisions (which initiatives to select, which findings to
  highlight, how to interpret ambiguous results) were made by me, reviewing
  the actual query outputs
- The explainer video, executive memo framing, and final decisions on scope
  and priorities are my own

## My Role
I directed the project scope and priorities, ran every script personally,
reviewed and caught issues in the outputs (including a date-leakage bug in
an early aggregation, which I identified from an unexpected row count and
which we then corrected together), and made the final calls on data
handling, initiative selection, and interpretation throughout. 