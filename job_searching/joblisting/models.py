from django.db import models

class Job(models.Model):
    num = models.PositiveIntegerField(primary_key=True)  # 'num' as the primary key
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    summary = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title if self.title else str(self.num)
    class Meta:
        db_table = 'jobs'  # Set the MongoDB collection name

