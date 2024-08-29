from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
import requests


class Extension(Extension):

    def __init__(self):
        super(Extension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument() or str()
        if len(query.strip()) == 0:
            return RenderResultListAction([
                ExtensionResultItem(icon='images/icon.png',
                                    name='No input',
                                    on_enter=HideWindowAction())
            ])
        else:
            result = requests.get("https://www.wikidata.org/w/api.php?action=wbsearchentities&search="+query+"&language=en&uselang=en&type=item&limit=10&format=json").json()
            items = []

            for i in result["search"]:
                desc = "No description"
                if "description" in i:
                    desc = i["description"]

                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name=i["label"],
                                                 description=desc,
                                                 on_enter=OpenUrlAction(i["concepturi"])))

            return RenderResultListAction(items)

if __name__ == '__main__':
    Extension().run()