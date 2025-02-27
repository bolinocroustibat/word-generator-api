from tortoise import fields
from tortoise.models import Model


class Language(Model):
    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=2, unique=True)  # e.g. 'en', 'es', 'it'
    name = fields.CharField(max_length=50)  # e.g. 'English', 'Spanish', 'Italian'

    class Meta:
        table = "languages"

    def __str__(self):
        return f"{self.name} ({self.code})"


class RealWord(Model):
    id = fields.IntField(pk=True)
    string = fields.CharField(max_length=100)
    language = fields.ForeignKeyField("models.Language", related_name="real_words")
    type = fields.CharField(max_length=16, null=True)
    gender = fields.CharField(max_length=1, null=True)  # For gendered languages
    number = fields.CharField(max_length=1, null=True)
    tense = fields.CharField(max_length=16, null=True)
    proper = fields.BooleanField(default=False)  # For proper nouns
    complex = fields.BooleanField(null=True)  # For complex words

    class Meta:
        table = "real_words"
        unique_together = ("string", "type", "language")

    def __str__(self):
        return f"{self.string} ({self.id})"


class GeneratedWord(Model):
    id = fields.IntField(pk=True)
    string = fields.CharField(max_length=100)
    language = fields.ForeignKeyField("models.Language", related_name="generated_words")
    type = fields.CharField(max_length=16, null=True)
    gender = fields.CharField(max_length=1, null=True)
    number = fields.CharField(max_length=1, null=True)
    tense = fields.CharField(max_length=16, null=True)
    conjug = fields.CharField(max_length=16, null=True)  # For conjugated forms
    date = fields.DatetimeField()
    ip = fields.CharField(max_length=16)

    class Meta:
        table = "generated_words"
        unique_together = ("string", "language")

    def __str__(self):
        return f"{self.string} ({self.id})"


class GeneratedDefinition(Model):
    id = fields.IntField(pk=True)
    generated_word = fields.ForeignKeyField(
        "models.GeneratedWord", related_name="generated_definitions"
    )
    text = fields.TextField()
    date = fields.DatetimeField()
    ip = fields.CharField(max_length=16)

    class Meta:
        table = "generated_definitions"
        unique_together = ("generated_word_id", "text")

    def __str__(self):
        return f"{self.text} ({self.id})"
