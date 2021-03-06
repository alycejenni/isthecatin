# is the cat in?

[![forthebadge](https://forthebadge.com/images/badges/contains-cat-gifs.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

[This is my cat](http://s3.eu-west-2.amazonaws.com/isthecatin-images/cat_1512635996_8505661-1.mp4).

His name is Tyson, and he is a bunny-murdering monster.

I've used a Raspberry Pi and opencv to detect when he uses his cat flap. When he does, he gets his picture taken and uploaded for the world to see on [isthecat.in](http://isthecat.in) - so we know if he's in or out, and if he's brought us any presents. The code in this repo is for that site (not for the RPi, though I will probably be uploading that soon).

Please report any issues and/or feel free to contribute!

## Contributing

If you want to contribute, you can check the issues for ideas or create your own if you've got something in mind already.

### Installing
*Note: this installation guide is a work in progress - it is very likely I have missed things out.*

**Dependencies:**
- [Python 3.6](https://www.python.org)
- [PostgreSQL](https://www.postgresql.org)

**Clone:**
```shell-script
git clone https://github.com/alycejenni/isthecatin.git
```

**Setup a PostgreSQL database - I like to call mine 'isthecatin' and have a dedicated user called 'kitty' with the password 'cat':**
```shell-script
createuser -P -d kitty
createdb -U kitty isthecatin
```

**Create a file called '.env' in the 'config' directory and fill it with this:**
```
SECRET_KEY=[YOUR-DJANGO-SECRET-KEY]
DJANGO_DEBUG=True
IMAGE_BUCKET=[AMAZON-S3-BUCKET-NAME]
AWS_KEY=[AMAZON-S3-KEY]
AWS_SECRET=[AMAZON-S3-SECRET]
DATABASE_URL=postgresql://kitty:cat@localhost:5432/isthecatin
SALT=[RANDOM-STRING]
```
*Note: obviously I'm not going to put the actual AWS details on here, so you'll have to use your own. It's pretty much free. I'm actually not sure how the Django secret key works so that might be a bit more difficult; I'll come back to this.*

**[recommended] Create a virtual Python environment for the project, e.g. using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest):**
```shell-script
mkvirtualenv isthecatin
setprojectdir C:\PATH\TO\PROJECT\ROOT
```

The following should be done from the project root:

**Install the Python packages:**
```shell-script
pip install -r requirements.txt
```

**Do the Django migrations:**
```shell-script
python manage.py migrate
```

**Then hopefully you can run it:**
```shell-script
python manage.py runserver localhost:8000
```

### Gulp
**Dependencies:**
- [Node.js](https://nodejs.org)

**Install the Node packages with npm:**
```shell-script
npm install
```

**Run the server:**
```shell-script
python manage.py runserver localhost:8000
```

**Run the default task in a different prompt:**
```shell-script
gulp
```

### Useful links

* [Fontawesome icon cheatsheet](http://fontawesome.io/cheatsheet/)
