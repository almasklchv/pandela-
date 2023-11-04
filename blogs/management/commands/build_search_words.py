from django.core.management.base import BaseCommand

from blogs.models import Playlist #, Tag


# TODO параметризация
class Command(BaseCommand):
    help = 'build search words'

    def handle(self, *args, **options):
        datas = set([t.name for t in Playlist.objects.all()]) #+ плюсик поставить и потом тут ")" убрать с появлением тегов
                    #[t.name for t in Tag.objects.all()])
        print('\n'.join(datas))