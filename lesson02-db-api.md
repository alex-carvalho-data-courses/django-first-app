# DB API - shell

Bellow there is a list of commands to interact with the db via the shell 
command line.  

To start with it, we'll the shell provided by Django instead of the direct 
**python shell**.

### Django shell
```shell
poetry run python manage.py shell
```

### Import the Polls app custom models
```shell
from polls.models import Question, Choice
```

### List all Questions
```shell
Question.objects.all()
```

### Insert a question
```shell
from django.utils import timezone
q = Question(question_text="What's new?", pub_date=timezone.now())
q.save()
```

### Retrieve field value
```shell
q.id
q.question_text
q.pub_date
```

### Update Model
```shell
q.question_text = "What's up?"
q.save()
```

### Search records by id
```shell
Question.objects.filter(id=1)
```

### Search field starting with
```shell
Question.objects.filter(question_text__startswith='What')
```

### Search by date/year
```shell
from django.utils import timezone
current_year = timezone.now().year
Question.objects.filter(pub_date__year=current_year)
```

### Get a specific record
```shell
Question.objects.get(id=2)
```

### Get specific record by pk
```shell
Question.objects.get(pk=1)
```

### Execute custom Model methods
```shell
q = Question.objects.get(pk=1)
q.was_published_recently()
```

### Retrieve all child records Set
```shell
q.choice_set.all()
```

### Create child record
```shell
q.choice_set.create(choice_text='Not much', votes=0)
q.choice_set.create(choice_text='The sky', votes=0)
```

### Count Child records
```shell
q.choice_set.count()
```

### Search Model by its Parent Model
```shell
current_year = timezone.now().year
Choice.objects.filter(question__pub_date__year=current_year)
```

### Delete Child record
```shell
c = q.choice_set.filter(choice_text__startswith='Not')
c.delete()
```