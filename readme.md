# Requirements
*python3.6 or above (i used python 3.7)

# Installation 
 * Install python3.6 or above (https://www.python.org/downloads/)
 * Install virtual environment (https://docs.python.org/3.6/library/venv.html)
 * Install pip (https://pip.pypa.io/en/stable/installing/)
 * create virtualenv(```virtualenv venv -p python3.6```)
 * Install dependencies(```pip install -r requirements.txt```)

# How to use
   * ```python manage.py --help```
      * and follow the instructions
# Commands
## manage.py command
```python 
python manage.py --help
Usage: manage.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  assign-bed        Assign a bed to the patient, inputs: name - name of the...
  bed-status        check the status of the bed input: bed_number
  list-beds         Lists the beds which are free or occupied inputs:...
  list-patients     list the patients which opt for the specific type of
                    the...

  patient-checkout  patient checkout free the occupied bed input: patient_id
```

## assign-bed command
```python
python manage.py assign-bed --help
Usage: manage.py assign-bed [OPTIONS]

  Assign a bed to the patient,

  inputs:

      name - name of the patient,

      bed_number - bed numbers choosen by the patient

Options:
  --help  Show this message and exit.
```

## list-beds command
```python
python manage.py list-beds --help  
Usage: manage.py list-beds [OPTIONS]

  Lists the beds which are free or occupied

  inputs:  type_of_bed -

       enter 0 for general,

       enter 1 for semi-private,

       enter 2 for private,

       enter 3 for all,

Options:
  -t, --type_of_bed INTEGER  type of the bed, 3 is default
  --help                     Show this message and exit.

```

## list-patients command
```python
python manage.py list-patients --help
Usage: manage.py list-patients [OPTIONS]

  list the patients which opt for the specific type of the bed

  inputs:

      type_of_bed -

          enter 0 for general,

          enter 1 for semi-private,

          enter 2 for private

Options:
  -t, --type_of_bed INTEGER  type of the bed, 3 is default
  --help                     Show this message and exit.
```

## bed-status command
```python
python manage.py bed-status --help
Usage: manage.py bed-status [OPTIONS]

  check the status of the bed input: bed_number

Options:
  -b, --bed_number TEXT
  --help                 Show this message and exit.
```
