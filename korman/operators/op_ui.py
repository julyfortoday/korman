#    This file is part of Korman.
#
#    Korman is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Korman is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Korman.  If not, see <http://www.gnu.org/licenses/>.

import bpy
from bpy.props import *

class UIOperator:
    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == "PLASMA_GAME"


class CollectionAddOperator(UIOperator, bpy.types.Operator):
    bl_idname = "ui.plasma_collection_add"
    bl_label = "Add Item"
    bl_description = "Adds an item to the collection"

    context = StringProperty(name="ID Path",
                             description="Path to the relevant datablock from the current context",
                             options=set())
    group_path = StringProperty(name="Property Group Path",
                                description="Path to the property group from the ID",
                                options=set())
    collection_prop = StringProperty(name="Collection Property",
                                     description="Name of the collection property",
                                     options=set())
    index_prop = StringProperty(name="Index Property",
                                description="Name of the active element index property",
                                options=set())
    name_prefix = StringProperty(name="Name Prefix",
                                 description="Prefix for autogenerated item names",
                                 default="Item",
                                 options=set())
    name_prop = StringProperty(name="Name Property",
                               description="Attribute name of the item name property",
                               options=set())

    def execute(self, context):
        props = getattr(context, self.context).path_resolve(self.group_path)
        collection = getattr(props, self.collection_prop)
        idx = len(collection)
        collection.add()
        if self.name_prop:
            setattr(collection[idx], self.name_prop, "{} {}".format(self.name_prefix, idx+1))
        if self.index_prop:
            setattr(props, self.index_prop, idx)
        return {"FINISHED"}


class CollectionRemoveOperator(UIOperator, bpy.types.Operator):
    bl_idname = "ui.plasma_collection_remove"
    bl_label = "Remove Item"
    bl_description = "Removes an item from the collection"

    context = StringProperty(name="ID Path",
                             description="Path to the relevant datablock from the current context",
                             options=set())
    group_path = StringProperty(name="Property Group Path",
                                description="Path to the property group from the ID",
                                options=set())
    collection_prop = StringProperty(name="Collection Property",
                                     description="Name of the collection property",
                                     options=set())
    index_prop = StringProperty(name="Index Property",
                                description="Name of the active element index property",
                                options=set())

    def execute(self, context):
        props = getattr(context, self.context).path_resolve(self.group_path)
        collection = getattr(props, self.collection_prop)
        index = getattr(props, self.index_prop)
        if len(collection) > index:
            collection.remove(index)
            setattr(props, self.index_prop, index - 1)
            return {"FINISHED"}
        else:
            return {"CANCELLED"}
