# An insecure password manager

This program allow to store data in an JSON file. 

####  Usage:
All data is saved in the directory `locals/data.json`, and it is essential that you do not delete or modify the `locals/acc.json` directory, or you will be unable to decrypt your data even with your master password.

Run: 

```python pip install -r requirements.txt```

You can run the program `python project.py` or directly add data ```python project.py -a reddit -n myname -e myemail@exemple.com```. For searching, use the command `python project.py -s reddit -n myname -e myemail@exemple.com`, and for updating, use `python project.py -u reddit -n myname -e myemail@exemple.com`. Note that you do not need to add all the information if you are searching or updating data. You can add as much information as you remember for more precision.