from .models import ProjectTag, Tag, Project
from datetime import datetime


def get_recent_value_for_project_and_tag(project_id, tag_id):
    """
    Retorna o valor mais recente para um projeto e tag específicos.
    """
    resultado = ProjectTag.objects.filter(projeto__id=project_id, tag__tag_id=tag_id).order_by('-timestamp').first()

    return resultado



def get_oldest_value_for_project_and_tag(project_id, tag_id):
    """
    Retorna o valor mais antigo para um projeto e tag específicos.
    """
    resultado = ProjectTag.objects.filter(projeto__id=project_id, tag__tag_id=tag_id).order_by('timestamp').first()

    return resultado


def get_project_tag_values_older_than(timestamp):
    """
    Retorna todos os valores da tabela ProjectTag com timestamp mais antiga que a timestamp especificada.
    """
    values = ProjectTag.objects.filter(timestamp__lt=timestamp).values_list('value', flat=True)
    return values


def delete_project_tag_values_older_than(timestamp):
    """
    Exclui os registros da tabela ProjectTag com timestamp mais antiga que a timestamp especificada.
    """
    ProjectTag.objects.filter(timestamp__lt=timestamp).delete()


def get_all_tags():
    """
    Retorna uma lista com todas as tags.
    """
    return Tag.objects.all()


def get_all_projects():
    """
    Retorna todos os projetos.
    """
    return Project.objects.all()


def get_project_by_id(projeto_id):
    """
    Retorna um projeto pelo id.
    """
    return Project.objects.get(id=projeto_id)


def get_tag_by_id(tag_id):
    """
        Retorna uma tag pelo id.
        """
    return Tag.objects.get(tag_id=tag_id)


