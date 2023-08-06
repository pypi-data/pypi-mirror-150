import json
import time


class SocketMethods:

    def __init__(self, sio, sid):
        self.sio = sio
        self.sid = sid

    def emit_menu(self, id, title, nav_link, icon):
        """
        Sends menu layer from server to the client side
        """
        menu = {
            "id": id,
            "title": title,
            "navLink": nav_link,
            "icon": icon
        }
        message = {
            "layers": [
                {
                    "id": "menu-%s" % (id),
                    "collectionName": "menus",
                    "set": [menu],
                    "timestamp": int(time.time())
                }
            ]
        }
        self.sio.emit('add-layers', json.dumps(message), room=self.sid)

    def emit_page(self, id, element):
        """
        Sends main page content from server to the client side
        """
        page = {
            "id": id,
            "element": element
        }
        message = {
            "layers": [
                {
                    "id": f'page-{id}',
                    "collectionName": "pages",
                    "set": [page],
                    "timestamp": int(time.time())
                }
            ]
        }
        self.sio.emit('add-layers', json.dumps(message), room=self.sid)

    def emit_busy(self, collection_name):
        message = {
            "layers": [
                {
                    "id": f'busy-{collection_name}',
                    "collectionName": "busy",
                    "set": [{"id": collection_name}],
                    "timestamp": int(time.time())
                }
            ]
        }
        self.sio.emit('add-layers', json.dumps(message), room=self.sid)

    def emit_done(self, collection_name):
        message = {
            "query": {
                "id": f'busy-{collection_name}',
            }
        }
        self.sio.emit('remove-layers', json.dumps(message), room=self.sid)

    def emit_documents(self, collection_name, documents):
        """
        Sends the main content of the plugin to the client,
        which displays the Fusion Cost Calculator datatable
        """
        message = {
            "layers": [
                {
                    "id": collection_name,
                    "collectionName": collection_name,
                    "set": documents,
                    "timestamp": int(time.time())
                }
            ]
        }
        self.sio.emit('add-layers', json.dumps(message), room=self.sid)

