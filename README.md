[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/4hPMH1rV)

# Zoo Management API in Python

[Link to the API](https://zoo-management-uzk7a2g7wa-et.a.run.app/)

This is an API that created using Flask in Python to simulate a zoo operation. Created by Owent Ovandy, 14 June 2024

## Application Details

### Library Used

- Flask
- Flassger
- NanoID
- Pytest
- Coverage
- Gunicorn
- Docker

### Apps Depedency

- flask = "*"
- flasgger = "*"
- gunicorn = "*"
- pytest = "*"
- nanoid = "*"
- coverage = "*"

## Function and Description

This API will manage an animal, employees, feeding schedule, enclosure, and report with adherance to RESTful API. It can do CRUD to animal, employees, enclosure and feeding schedules list. For now, it can only read the report data. For full API documentation, check /apidocs on run

## How to run

- Make sure python & pipenv is installed in your local
- cd to folder `src` & run `pipenv install`
- Instead of `flask run --debug` run `python app.py` instead
- Code should now run at port 5000
- Check API documentation at `localhost:5000/apidocs`

## Future Goals

- Add zoo entry function to manage zoo visit
- Integrate all the function to generate a full working report
