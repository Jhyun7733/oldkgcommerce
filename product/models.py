from django.db import models
from acc.models import User

# Create your models here.

class Product(models.Model):
    subject = models.CharField(max_length=200)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer")
    content = models.TextField()
    pubdate = models.DateTimeField()
    picture = models.ImageField(upload_to= "product/", blank=True, null=True)

    def summary(self):
        if len(self.content) > 20:
            return f"{self.content[:20]} ...자세히 보기"
        return self.content

    def __str__(self):
      return f"{self.subject}_{self.writer}"

    def getpic(self):
        if self.picture:
            return self.picture.url
        return "/media/noimage.jpg"


# class Reply(models.Model):
#     board = models.ForeignKey(Product, on_delete=models.CASCADE)
#     replyer = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.TextField()

#     def __str__(self):
#       return f"{self.product}_{self.replyer}"