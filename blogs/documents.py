from django_elasticsearch_dsl.registries import registry
import time

import elasticsearch.client
from django.conf import settings
from elasticsearch_dsl import Document, InnerDoc, Date, Integer, Long, Text, Object, GeoPoint, Keyword, Boolean
from elasticsearch_dsl.connections import connections



# from django.contrib.auth import get_user_model
from .models import Blog #, Playlist

#сверить со всеми кодами в том гитхаб файле. я уверен что в моделях сто процентно может быть какое-то поле, которое я обязан добавить



ELASTICSEARCH_ENABLED = hasattr(settings, 'ELASTICSEARCH_DSL')


if ELASTICSEARCH_ENABLED: #короче если он включается, мы хосты включаем
    connections.create_connection(
        hosts=[settings.ELASTICSEARCH_DSL['default']['hosts']])
    from elasticsearch import Elasticsearch

    es = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
    from elasticsearch.client import IngestClient

    c = IngestClient(es)
    try:
        c.get_pipeline('geoip')
    except elasticsearch.exceptions.NotFoundError:
        c.put_pipeline('geoip', body='''{
              "description" : "Add geoip info",
              "processors" : [
                {
                  "geoip" : {
                    "field" : "ip"
                  }
                }
              ]
            }''')

class GeoIp(InnerDoc):
    continent_name = Keyword()
    country_iso_code = Keyword()
    country_name = Keyword()
    location = GeoPoint()


class UserAgentBrowser(InnerDoc):
    Family = Keyword()
    Version = Keyword()


class UserAgentOS(UserAgentBrowser):
    pass


class UserAgentDevice(InnerDoc):
    Family = Keyword()
    Brand = Keyword()
    Model = Keyword()


class UserAgent(InnerDoc):
    browser = Object(UserAgentBrowser, required=False)
    os = Object(UserAgentOS, required=False)
    device = Object(UserAgentDevice, required=False)
    string = Text()
    is_bot = Boolean()


#похоже что elapsedtime - модель которую нужно обработать с других файлов
class ElapsedTimeDocument(Document):
    url = Keyword()
    time_taken = Long()
    log_datetime = Date()
    ip = Keyword()
    geoip = Object(GeoIp, required=False)
    useragent = Object(UserAgent, required=False)

    class Index:
        name = 'performance'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Meta:
        doc_type = 'ElapsedTime'


class ElaspedTimeDocumentManager:
    @staticmethod
    def build_index():
        from elasticsearch import Elasticsearch
        client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
        res = client.indices.exists(index="performance")
        if not res:
            ElapsedTimeDocument.init()

    @staticmethod
    def delete_index():
        from elasticsearch import Elasticsearch
        es = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
        es.indices.delete(index='performance', ignore=[400, 404])

    @staticmethod
    def create(url, time_taken, log_datetime, useragent, ip):
        ElaspedTimeDocumentManager.build_index()
        ua = UserAgent()
        ua.browser = UserAgentBrowser()
        ua.browser.Family = useragent.browser.family
        ua.browser.Version = useragent.browser.version_string

        ua.os = UserAgentOS()
        ua.os.Family = useragent.os.family
        ua.os.Version = useragent.os.version_string

        ua.device = UserAgentDevice()
        ua.device.Family = useragent.device.family
        ua.device.Brand = useragent.device.brand
        ua.device.Model = useragent.device.model
        ua.string = useragent.ua_string
        ua.is_bot = useragent.is_bot

        doc = ElapsedTimeDocument(
            meta={
                'id': int(
                    round(
                        time.time() *
                        1000))
            },
            url=url,
            time_taken=time_taken,
            log_datetime=log_datetime,
            useragent=ua, ip=ip)
        doc.save(pipeline="geoip")


class BlogDocument(Document):
    title = Text(analyzer='ik_max_word', search_analyzer='ik_smart')
    description = Text(analyzer='ik_max_word', search_analyzer='ik_smart')
    author = Object(properties={
        'name': Text(analyzer='ik_max_word', search_analyzer='ik_smart'),
        'id': Integer(),
        'username': Text(analyzer='ik_max_word', search_analyzer='ik_smart'),
        'bio': Text(analyzer='ik_max_word', search_analyzer='ik_smart'),
    })
    playlist_setting = Object(properties={
        'name': Text(analyzer='ik_max_word', search_analyzer='ik_smart'),
        'description': Text(analyzer='ik_max_word', search_analyzer='ik_smart'),
        'id': Integer()
    })
    # tags = Object(properties={
    #     'name': Text(analyzer='ik_max_word', search_analyzer='ik_smart'),
    #     'id': Integer()
    # })

    pub_time = Date()
    mod_time = Date()
    # status = Text() ?? check his model https://github.com/liangliangyy/DjangoBlog/tree/44aceba6f94dcad5f8d4023aa91497a29f6f75a1
    # comment_status = Text()
    # type = Text()
    is_published = Boolean() #like type
    views = Integer()
    # article_order = Integer()

    class Index:
        name = 'blogs'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }


    class Meta:
        doc_type = 'Blog'


class BlogDocumentManager():

    def __init__(self):
        self.create_index()

    def create_index(self):
        BlogDocument.init()

    def delete_index(self):
        from elasticsearch import Elasticsearch
        es = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
        es.indices.delete(index='blogs', ignore=[400, 404])

    def convert_to_doc(self, blogs): #если это не будет работать с сериалайзером, добавьобозначение моделей через class Django
        return [
            BlogDocument(
                meta={
                    'id': blog.id},
                # body=blogs.body,
                title=blog.title,
                description=blog.description,
                author={
                    'name': blog.author.name,
                    'id': blog.author.id,
                    'username': blog.author.username,
                    'bio': blog.author.bio},
                playlist_setting={
                    'name': blog.playlist.name,
                    'description': blog.playlist.description,
                    'id': blog.category.id},
                # tags=[
                #     {
                #         'name': t.name,
                #         'id': t.id} for t in article.tags.all()],
                pub_time=blog.pub_time,
                mod_time=blog.mod_time,
                is_published=blog.is_published,
                # comment_status=blogs.comment_status,
                # type=blogs.type,
                views=blog.views,
                # article_order=blogs.article_order
            ) for blog in blogs]

    def rebuild(self, blogs=None):
        BlogDocument.init()
        blogs = blogs if blogs else Blog.videoobjects.all()
        docs = self.convert_to_doc(blogs)
        for doc in docs:
            doc.save()

    def update_docs(self, docs):
        for doc in docs:
            doc.save()



# class PlaylistDocument(Document): пока удален ненадолго
#     name = Text(analyzer='ik_max_word', search_analyzer='ik_smart')
#     description = Text(analyzer='ik_max_word', search_analyzer='ik_smart')
#     author = Object(properties={
#         'name': Text(analyzer='ik_max_word', search_analyzer='ik_smart'),
#         'id': Integer(),
#         'username': Text(analyzer='ik_max_word', search_analyzer='ik_smart'),
#         'bio': Text(analyzer='ik_max_word', search_analyzer='ik_smart'),
#     })
#     # tags = Object(properties={
#     #     'name': Text(analyzer='ik_max_word', search_analyzer='ik_smart'),
#     #     'id': Integer()
#     # })
#
#     pub_time = Date()
#     mod_time = Date()
#     # status = Text() ?? check his model https://github.com/liangliangyy/DjangoBlog/tree/44aceba6f94dcad5f8d4023aa91497a29f6f75a1
#     # comment_status = Text()
#     # type = Text()
#     # is_published = Boolean() #like type
#     # views = Integer()
#     # article_order = Integer()
#
#     class Index:
#         name = 'playlist'
#         settings = {
#             "number_of_shards": 1,
#             "number_of_replicas": 0
#         }
#
#
#     class Meta:
#         doc_type = 'Playlist'
#
#
# class PlaylistDocumentManager():
#
#     def __init__(self):
#         self.create_index()
#
#     def create_index(self):
#         PlaylistDocument.init()
#
#     def delete_index(self):
#         from elasticsearch import Elasticsearch
#         es = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
#         es.indices.delete(index='playlist', ignore=[400, 404])
#
#     def convert_to_doc(self, playlists): #если это не будет работать с сериалайзером, добавьобозначение моделей через class Django
#         return [
#             PlaylistDocument(
#                 meta={
#                     'id': playlist.id},
#                 # body=blogs.body,
#                 title=playlist.title,
#                 description=playlist.description,
#                 author={
#                     'name': playlist.author.name,
#                     'id': playlist.author.id,
#                     'username': playlist.author.username,
#                     'bio': playlist.author.bio},
#                 pub_time=playlist.pub_time,
#                 mod_time=playlist.mod_time,
#             ) for playlist in playlists]
#
#     def rebuild(self, playlists=None):
#         PlaylistDocument.init()
#         playlists = playlists if playlists else Playlist.objects.all()
#         docs = self.convert_to_doc(playlists)
#         for doc in docs:
#             doc.save()
#
#     def update_docs(self, docs):
#         for doc in docs:
#             doc.save()


# it's from absolutely another file with API elasticsearch, but without haystack
# class PlaylistDocument(Document):
#     author = fields.ObjectField(properties={
#         'id': fields.IntegerField(),
#         'name': fields.TextField(),
#         'username': fields.TextField(),
#         'bio': fields.TextField(),
#     })
#
#     class Index:
#         name = 'playlists'
#         settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 0,
#         }
#
#     class Django:
#         model = Playlist
#         fields = [
#             'name',
#             'description',
#             'pub_date',
#             'mod_date',
#             'id',
#             # 'author',
#         ]
#
#
# @registry.register_document
# class BlogDocument(Document):
#
#     author = fields.ObjectField(properties={
#         'id': fields.IntegerField(),
#         'name': fields.TextField(),
#         'username': fields.TextField(),
#         'bio': fields.TextField(),
#     })
#     playlist_setting = fields.ObjectField(properties={
#         'id': fields.IntegerField(),
#         'name': fields.TextField(),
#         'description': fields.TextField(),
#     })
#     # type = fields.TextField(attr='type_to_string')
#
#     class Index:
#         name = 'blogs'
#         settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 0,
#         }
#
#     class Django:
#         model = Blog
#         fields = [
#             'id',
#             'title',
#             'description',
#             'pub_date',
#             'mod_date',
#         ]