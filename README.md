# Flask_Simple_App

this is my project for this subject

# setup:

for anaconda users


```
conda create -n flask_app_env python=3.8 

```


```
conda activate flask_app_env
```


```
pip install -r requirments.txt
```

- open up xammp server or wamp set a data base name to "flaskdb" importent
- run this commands :

```
python migrations.py db init 
```

```
python migrations.py db migrate 
```

```
python migrations.py db upgrade 

```
- finally 

```
flask run  
```

