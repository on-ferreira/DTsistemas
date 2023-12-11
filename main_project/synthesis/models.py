from django.db import models


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    poco = models.CharField(max_length=255)
    um = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
        Armazenar todos os tipos de tag que existem no projeto
        Exemplo:
                id 1 - name: BLUE_GAL
                id 2 - name: YELLOW_GAL
    """
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=255)

    def __str__(self):
        return self.tag_name


class ProjectTag(models.Model):
    """
        Relação que irá salvar os valores e a timestamp de tags e projetos.
        Exemplo:
            Projeto_id 1 - tag_id 1 - value 10 - timestamp 21/11/2023 18:55
            Projeto_id 1 - tag_id 1 - value 0  - timestamp 21/11/2023 18:55
    """
    projeto = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"projeto_id: {self.projeto.id} - tag_name {self.tag.tag_name} - value {self.value} " \
               f"- timestamp {self.timestamp}"
