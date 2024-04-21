from django import forms
from django.db import models

class GitHubDepo(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url
    
  

class JavaClass(models.Model):
    github_repo = models.ForeignKey(GitHubDepo, on_delete=models.CASCADE, null=True)
    class_name = models.CharField(max_length=100)
    javadoc_lines_count = models.IntegerField()
    comment_lines_count = models.IntegerField()
    code_line_count = models.IntegerField()
    loc_count = models.IntegerField()
    function_count = models.IntegerField()
    comment_deviation_perc = models.FloatField()

    def __str__(self):
        return self.class_name
    
