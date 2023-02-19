from django.db import models
from django.contrib.auth.models import User

class Title(models.Model):
    """titles of books"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)



    def __str__(self):
        """return the string of the title"""

        return f'{self.text}\t————from user "{self.owner}"'

class Entry(models.Model):
    """entries of the books"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        if len(self.text) <= 50:
            return self.text
        else:
            return f'{self.text[:50]}...'