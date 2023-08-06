# Locass - Simple and easy to use localization library written on Python
![Locass Logo](https://user-images.githubusercontent.com/94710002/163729049-7bace2a6-4fb4-4b1a-8eff-5390dba23529.png)
### LoCalization As So Simple - simple, light-weight, and simple to use library which help you to localizate your apps on different languages. 
> Note: This project is unstable because of the first releases not tested. We are asking you to report any bugs you found.
## How to use
#### Step 1: Create a folder with your localization files, for example locals.
>We recommend you to create it in the root of your project or in the same directory with your executable because we recommend you to use RELATIVE paths like```./locals/```

#### Step 2: Create localization files using your own markers or use default, markdown is:```KEYMARKER(keyvalue)VALUEMARKER(value)```, consider that spaces between markers and values are forbidden. For example:
```
[k]HW![v]Привет Мир!
```
#### Step 3: Install and import this module in your project. Details about installing is on Installing page. Next, create a LocalManager object. Use expression like this:
```python
man = locass.LocalManager()
```
#### Step 4: configure localization manager, using 
```python
man.configure() 
```
#### function. First argument is the path, where your localization files are, for example "./locals/"
> NOTE: Please, don't lose "/" symbols!
#### Second argument is the dictionary, which contains the localization name as a key and name of file as a value, for example {"RU": "ru.lang", "EN": "en.lang"} 
#### Third is the Keymarker of your markdown you used in localization files, for example "[k]"
#### Last is the Valuemarker of your markdown, for example "[v]"
#### So if you used next markdown of localization flies:
#### file ru.lang in ./locals/ with inside
```[k]HW![v]Привет Мир!```
#### and file en.lang in the same directory with inside
```[k]HW![v]Hello World!```
#### your call will be like:
```python
man.configure("./locals/",{"RU": "ru.lang", "EN":"en.lang"},"[k]","[v]")
```
#### Step 5: Load language to use, using ```loadLang(key)``` where key is localization name from previous step, for example "RU":
```python
man.loadLang("RU")
```
#### Step 6: Use it in your code, and when you need string from selected localization, only call ```g(key)```, where key from your localization file. For example after steps above we can call next:
```python
man.g("HW!") #Returns Привет Мир!
```
> Note: To change the loaded language, only call loadLang again with new argument, for example 
> ```python
> man2.configure("./locals/",{"RU": "ru.lang", "EN":"en.lang"},"[k]","[v]")
> man2.loadLang("RU")
> man2.g("HW!") #Returns Привет Мир!
> man2.loadLang("EN")
> man2.g("HW!") #Returns Hello World!
>```
## Installing
#### Get it form PyPi: https://pypi.org/project/locass/ or in terminal run
```pip install locass```
#### or
```pip3 install locass```
## Tests
#### Try and see how the library works only running ```tests/test.py```. Run it only after installing the library or it won't work.
## Bugs and errors
#### Now library is under development so we asking you to tell us about every bug or error you found. You should consider that library is unstable and can cause some errors.
