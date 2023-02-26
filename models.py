from tortoise import fields
from tortoise.models import Model


class RealWordEN(Model):
    # id = fields.IntField(primary_key=True)
    string = fields.CharField(max_length=50, unique=True)
    type = fields.CharField(max_length=16, null=True)
    number = fields.CharField(max_length=1, null=True)
    tense = fields.CharField(max_length=16, null=True)

    class Meta:
        table = "real_words_EN"

    def __str__(self):
        return f"{self.string} ({self.id})"


class RealWordFR(Model):
    # id: = fields.IntField(primary_key=True)
    string = fields.CharField(max_length=100)
    type = fields.CharField(max_length=16, null=True)
    gender = fields.CharField(max_length=1, null=True)
    number = fields.CharField(max_length=1, null=True)
    tense = fields.CharField(max_length=16, null=True)
    proper = fields.data.BooleanField()
    complex = fields.data.BooleanField(null=True)

    class Meta:
        table = "real_words_FR"
        unique_together = ("string", "type")

    def __str__(self):
        return f"{self.string} ({self.id})"


class GeneratedWordEN(Model):
    # id = fields.IntField(primary_key=True)
    string = fields.CharField(max_length=100, unique=True)
    type = fields.CharField(max_length=16, null=True)
    number = fields.CharField(max_length=1, null=True)
    tense = fields.CharField(max_length=16, null=True)
    date = fields.DatetimeField()
    ip = fields.CharField(max_length=16)

    class Meta:
        table = "generated_words_EN"

    def __str__(self):
        return f"{self.string} ({self.id})"


class GeneratedWordFR(Model):
    # id = fields.IntField(primary_key=True)
    string = fields.CharField(max_length=100, unique=True)
    type = fields.CharField(max_length=16, null=True)
    gender = fields.CharField(max_length=1, null=True)
    number = fields.CharField(max_length=1, null=True)
    tense = fields.CharField(max_length=16, null=True)
    conjug = fields.CharField(max_length=16, null=True)
    date = fields.DatetimeField()
    ip = fields.CharField(max_length=16)

    class Meta:
        table = "generated_words_FR"

    def __str__(self):
        return f"{self.string} ({self.id})"


# class GeneratedDefinitionEN(Model):
#     # id = fields.IntField(primary_key=True)
#     generated_word_id = fields.ForeignKeyField(GeneratedWordEN)
#     text = fields.TextField()
#     date = fields.DatetimeField()
#     ip = fields.CharField(max_length=16)

#     class Meta:
#         table = "generated_definitions_EN"
#         unique_together = ("generated_word_id", "text")

#     def __str__(self):
#         return f"{self.text} ({self.id})"


# class GeneratedDefinitionFR(Model):
#     # id = fields.IntField(primary_key=True)
#     generated_word_id = fields.ForeignKeyField(GeneratedWordFR)
#     text = fields.TextField()
#     date = fields.DatetimeField()
#     ip = fields.CharField(max_length=16)

#     class Meta:
#         table = "generated_definitions_FR"
#         unique_together = ("generated_word_id", "text")

#     def __str__(self):
#         return f"{self.text} ({self.id})"
