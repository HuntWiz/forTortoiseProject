from tortoise import fields, models


class Post(models.Model):

    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    tags: fields.ManyToManyRelation["Tag"]

    class Meta:
        table = 'Posts'


    def __str__(self):
        return self.title