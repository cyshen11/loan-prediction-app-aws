# ℹ️ About

This loan prediction app, powered by Machine Learning predicts whether the loan will be paid off based on loan, account, transaction and owner information. The model is trained on the financial data from the <a href="https://web.archive.org/web/20180506061559/http://lisp.vse.cz/pkdd99/Challenge/chall.htm" target="_blank">Principles and Practice of Knowledge Discovery in Databases (PKDD’99) Challenge</a>. The training dataset consist of 202 loans while the test dataset has 87 loans. The model achieved 89% accuracy but only 0.57 ROC AUC score on the test dataset.

### Tech Stack:

- Frontend: Flask
- Database: AWS RDS (MariaDB)
- File Storage: AWS S3
- Machine Learning: AutoGluon
- Deployment: AWS SAM
- Integration: Pytest
