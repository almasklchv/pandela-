from django.conf import settings
from elasticsearch_dsl import Document, Text



from django.contrib.auth import get_user_model
# from .models import Profile

#это норм не вводить какие-то поля для документа
class ProfileDocument(Document):
    name = Text(analyzer='ik_max_word', search_analyzer='ik_smart')
    username = Text(analyzer='ik_max_word', search_analyzer='ik_smart')
    


    class Index:
        name = 'profiles'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }


    class Meta:
        doc_type = 'Profile'


class ProfileDocumentManager():

    def __init__(self):
        self.create_index()

    def create_index(self):
        ProfileDocument.init()

    def delete_index(self):
        from elasticsearch import Elasticsearch
        es = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
        es.indices.delete(index='profiles', ignore=[400, 404])

    def convert_to_doc(self, profiles): #если это не будет работать с сериалайзером, добавьобозначение моделей через class Django
        return [
            ProfileDocument(
                meta={
                    'id': profile.id},
                name=profile.name,
                username=profile.username,

            ) for profile in profiles]

    def rebuild(self, profiles=None):
        ProfileDocument.init()
        profiles = profiles if profiles else get_user_model().objects.all()
        docs = self.convert_to_doc(profiles)
        for doc in docs:
            doc.save()

    def update_docs(self, docs):
        for doc in docs:
            doc.save()

