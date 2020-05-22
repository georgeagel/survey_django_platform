from django.db import models
from django.contrib.auth.models import User



# class Survey(models.Model):
#     name = models.CharField(("Name"), max_length=400)
#     description = models.TextField(("Description"), )
#     is_published = models.BooleanField(("Users can see it and answer it"),)
#     need_logged_user = models.BooleanField(("Only authenticated users can see it and answer it"),)
#     display_by_question = models.BooleanField(("Display by question"),)
#     template = models.CharField(("Template"), max_length=255, null=True, blank=True)

#     class Meta(object):
#         verbose_name = ('survey')
#         verbose_name_plural = ('surveys')

#     def __str__(self):
#         return self.name

#     def latest_answer_date(self):
#         """ Return the latest answer date.
#         Return None is there is no response. """
#         min_ = None
#         for response in self.responses.all():
#             if min_ is None or min_ < response.updated:
#                 min_ = responses.updated
#         return min_

#     def get_absolute_url(self):
#         return reverse("survey-detail", kwargs={"id": self.pk})







class Survey(models.Model):
    name = models.CharField(("Name"), max_length=400)
    description = models.TextField(("Description"), )
    is_published = models.BooleanField(("Users can see it and answer it"),)
    need_logged_user = models.BooleanField(("Only authenticated users can see it and answer it"),)
    display_by_question = models.BooleanField(("Display by question"),)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=("Survey"), related_name="Survey" ) 
    #template = models.CharField(("Template"), max_length=255, null=True, blank=True)

    class Meta(object):
        verbose_name = ('survey')
        verbose_name_plural = ('surveys')

    def __str__(self):
        return self.name

    def latest_answer_date(self):
        """ Return the latest answer date.
        Return None is there is no response. """
        min_ = None
        for response in self.responses.all():
            if min_ is None or min_ < response.updated:
                min_ = responses.updated
        return min_

    def get_absolute_url(self):
        return reverse("survey-detail", kwargs={"id": self.pk})



class Category(models.Model):
    name = models.CharField(("Name"), max_length=400)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name=("Survey"), related_name="categories")
    order = models.IntegerField(("Display order"), blank=True, null=True)
    description = models.CharField(("Description"), max_length=2000, blank=True, null=True)

    class Meta:
        # pylint: disable=too-few-public-methods
        verbose_name = ("category")
        verbose_name_plural = ("categories")

    def __str__(self):
        return self.name

    def slugify(self):
        return slugify(str(self))


def validate_choices(choices):
    """  Verifies that there is at least two choices in choices
    :param String choices: The string representing the user choices.
    """
    values = choices.split(',')
    empty = 0
    for value in values:
        if value.replace(" ", "") == "":
            empty += 1
    if len(values) < 2 + empty:
        msg = "The selected field requires an associated list of choices."
        msg += " Choices must contain more than one item."
        raise Exception(msg)


CHOICES_HELP_TEXT = (
    """The choices field is only used if the question type
if the question type is 'radio', 'select', or
'select multiple' provide a comma-separated list of
options for this question ."""
)


class Question(models.Model):
    TEXT = "text"
    SHORT_TEXT = "short-text"
    RADIO = "radio"
    SELECT = "select"
    SELECT_IMAGE = "select_image"
    SELECT_MULTIPLE = "select-multiple"
    INTEGER = "integer"
    FLOAT = "float"
    DATE = "date"

    QUESTION_TYPES = (
        (TEXT, ("text (multiple line)")),
        (SHORT_TEXT, ("short text (one line)")),
        (RADIO, ("radio")),
        (SELECT, ("select")),
        (SELECT_MULTIPLE, ("Select Multiple")),
        (SELECT_IMAGE, ("Select Image")),
        (INTEGER, ("integer")),
        (FLOAT, ("float")),
        (DATE, ("date")),
    )



    type = models.CharField(("Type"), max_length=200, choices=QUESTION_TYPES, default=TEXT)
    question_text = models.CharField(("header"), max_length=300)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name=("Survey"), related_name="questions")
    choices = models.TextField(("Choices"), blank=True, null=True, help_text=CHOICES_HELP_TEXT)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, verbose_name=("Category"), blank=True, null=True, related_name="questions"
    )

    def save(self, *args, **kwargs):
        if self.type in [Question.RADIO, Question.SELECT, Question.SELECT_MULTIPLE]:
            validate_choices(self.choices)
        super(Question, self).save(*args, **kwargs)


    def get_clean_choices(self):
            """ Return split and stripped list of choices with no null values. """
            if self.choices is None:
                return []
            choices_list = []
            for choice in self.choices.split(','):
                choice = choice.strip()
                if choice:
                    choices_list.append(choice)
            return choices_list





class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=("Question"), related_name="answers")
    
    created = models.DateTimeField(("Creation date"), auto_now_add=True)
    updated = models.DateTimeField(("Update date"), auto_now=True)
    body = models.TextField(("Content"), blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=("Survey"), related_name="questions" ) 


    def __init__(self, *args, **kwargs):
        try:
            question = Question.objects.get(pk=kwargs["question_id"])
        except KeyError:
            question = kwargs.get("question")
        body = kwargs.get("body")
        if question and body:
            self.check_answer_body(question, body)
        super(Answer, self).__init__(*args, **kwargs)

    def check_answer_body(self, question, body):
        if question.type in [Question.RADIO, Question.SELECT, Question.SELECT_MULTIPLE]:
            choices = question.get_clean_choices()
            if body:
                if body[0] == "[":
                    answers = []
                    for i, part in enumerate(body.split("'")):
                        if i % 2 == 1:
                            answers.append(part)
                else:
                    answers = [body]
            for answer in answers:
                if answer not in choices:
                    msg = "Impossible answer '{}'".format(body)
                    msg += " should be in {} ".format(choices)
                    raise Exception(msg)