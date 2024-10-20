from django.db import models


class Token(models.Model):
    unique_hash = models.CharField(max_length=255, unique=True)
    tx_hash = models.CharField(max_length=255, null=True)
    media_url = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)

    class Meta:
        db_table = 'tokens'
