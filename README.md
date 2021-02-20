# Project 1
Do these steps to make sure you have the correct packages. Also make sure you download gg2013.json and gg2015.json files into your local computer. The files are too large to push onto github.
```
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```
Make sure you are in your virtual environment when installing packages for this project! When you are ready to commit, make sure you run 
```
pip freeze > requirements.txt
```
to ensure that your requirements.txt is fully updated.

To get out of the virtual environment, simply type:
```
deactivate
```

#Team Members: Michael Kim
Feel free to reach out to me if there are some questions. The json output in main() inside the gg_api.py file will be in variable json_output. The human readable output will be printed out when main() is run.
