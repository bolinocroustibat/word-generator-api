from tortoise import fields
from tortoise.models import Model


class RealWordEN(Model):
    # id: int = fields.IntField(primary_key=True)
    string: str = fields.CharField(max_length=50, unique=True)
    type: str = fields.CharField(max_length=16, null=True)
    number: str = fields.CharField(max_length=1, null=True)
    tense: str = fields.CharField(max_length=16, null=True)

    class Meta:
        table = "real_words_EN"

    def __str__(self):
        return f"{self.string} ({self.id})"


class RealWordFR(Model):
    # id: int = fields.IntField(primary_key=True)
    string: str = fields.CharField(max_length=100)
    type: str = fields.CharField(max_length=16, null=True)
    gender: str = fields.CharField(max_length=1, null=True)
    number: str = fields.CharField(max_length=1, null=True)
    tense: str = fields.CharField(max_length=16, null=True)
    proper: bool = fields.data.BooleanField()
    complex: bool = fields.data.BooleanField(null=True)

    class Meta:
        table = "real_words_FR"
        unique_together = ("string", "type")

    def __str__(self):
        return f"{self.string} ({self.id})"


class GeneratedWordEN(Model):
    # id: int = fields.IntField(primary_key=True)
    string: str = fields.CharField(max_length=100, unique=True)
    type: str = fields.CharField(max_length=16, null=True)
    number: str = fields.CharField(max_length=1, null=True)
    tense: str = fields.CharField(max_length=16, null=True)
    date = fields.DatetimeField()
    ip: str = fields.CharField(max_length=16)

    class Meta:
        table = "generated_words_EN"

    def __str__(self):
        return f"{self.string} ({self.id})"


class GeneratedWordFR(Model):
    # id: int = fields.IntField(primary_key=True)
    string: str = fields.CharField(max_length=100, unique=True)
    type: str = fields.CharField(max_length=16, null=True)
    gender: str = fields.CharField(max_length=1, null=True)
    number: str = fields.CharField(max_length=1, null=True)
    tense: str = fields.CharField(max_length=16, null=True)
    conjug: str = fields.CharField(max_length=16, null=True)
    date = fields.DatetimeField()
    ip: str = fields.CharField(max_length=16)

    class Meta:
        table = "generated_words_FR"

    def __str__(self):
        return f"{self.string} ({self.id})"


# class GeneratedDefinitionEN(Model):
#     # id: int = fields.IntField(primary_key=True)
#     generated_word_id = fields.ForeignKeyField(GeneratedWordEN)
#     text: str = fields.TextField()
#     date = fields.DatetimeField()
#     ip: str = fields.CharField(max_length=16)

#     class Meta:
#         table = "generated_definitions_EN"
#         unique_together = ("generated_word_id", "text")

#     def __str__(self):
#         return f"{self.text} ({self.id})"


# class GeneratedDefinitionFR(Model):
#     # id: int = fields.IntField(primary_key=True)
#     generated_word_id = fields.ForeignKeyField(GeneratedWordFR)
#     text: str = fields.TextField()
#     date = fields.DatetimeField()
#     ip: str = fields.CharField(max_length=16)

#     class Meta:
#         table = "generated_definitions_FR"
#         unique_together = ("generated_word_id", "text")

#     def __str__(self):
#         return f"{self.text} ({self.id})"
