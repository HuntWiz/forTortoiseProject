from tortoise import fields, models



class Tag(models.Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=40)
    posts = fields.ManyToManyField('models.Post', related_name='tags')

    class Meta:
        table = 'Tags'

    def __str__(self):
        return self.title
