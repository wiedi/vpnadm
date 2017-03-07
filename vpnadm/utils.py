from django.db import models

class SingletonModel(models.Model):
	class Meta:
		abstract = True

	def save(self, *args, **kwargs):
		self.pk = 1
		super(SingletonModel, self).save(*args, **kwargs)
	
	@classmethod
	def get(cls):
		obj, c = cls.objects.get_or_create(pk = 1)
		return obj






