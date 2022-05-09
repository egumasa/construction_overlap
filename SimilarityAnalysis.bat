@echo off
python "src\SimilarityAnalysis.py" -t trigram -d "sample_data" --begin-line 7 > "result.csv"