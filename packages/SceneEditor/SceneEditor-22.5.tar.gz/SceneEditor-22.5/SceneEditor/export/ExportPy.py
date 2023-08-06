#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import os
import logging
from panda3d.core import ConfigVariableBool
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectDialog import YesNoDialog
from panda3d.core import LVecBase2f, LVecBase3f, LVecBase4f, LPoint2f, LPoint3f, LPoint4f, LVector3f
from panda3d.core import LVecBase2, LVecBase3, LVecBase4, LPoint2, LPoint3, LPoint4
from panda3d.core import LPlane

from DirectFolderBrowser.DirectFolderBrowser import DirectFolderBrowser

class ExporterPy:
    def __init__(self, save_path, save_file, scene_root, scene_objects, tooltip):
        self.objects = scene_objects

        self.content = "#!/usr/bin/python\n"
        self.content += "# -*- coding: utf-8 -*-\n"
        self.content += "# This file was created using the Scene Editor\n\n"

        includes = [
            "LPoint3f",
            "LVector3f",
            "LVecBase3f",
            "LPlane",
            "NodePath",
            "CollisionNode",
            "CollisionSphere",
            "CollisionCapsule",
            "CollisionInvSphere",
            "CollisionPlane",
            "CollisionRay",
            "CollisionLine",
            "CollisionSegment",
            "CollisionParabola",
            "CollisionBox",
            "ActorNode",
            "PointLight",
            "DirectionalLight",
            "AmbientLight",
            "Spotlight",
            "Camera",
            "PerspectiveLens"]

        self.content += "from panda3d.core import (\n"
        for inc in includes:
            self.content += f"    {inc},\n"
        self.content += ")\n\n"

        self.content += "class Scene:\n"
        self.content += "    def __init__(self, rootParent=base.render):\n"

        self.write_scene_element(scene_root, "rootParent")


        self.browser = DirectFolderBrowser(
            self.save,
            True,
            save_path,
            save_file,
            [".py"],
            tooltip)
        self.browser.show()

        #self.dlgPathSelect = PathSelect(
        #    self.save, "Save Python File", "Save file path", "Save", saveFile, tooltip)

    def write_scene_element(self, root, root_name):
        if hasattr(root, "get_children"):
            for obj in root.get_children():
                if obj in self.objects and not obj.is_stashed():
                    obj_name = self.get_save_object_name(obj.get_name())
                    if obj.get_tag("object_type") == "model":
                        model_path = f"'{obj.get_tag('filepath')}'"
                        self.content += " "*8 + f"self.{obj_name} = loader.load_model({model_path})\n"
                        self.content += " "*8 + f"self.{obj_name}.set_pos({obj.get_pos()})\n"
                        self.content += " "*8 + f"self.{obj_name}.set_hpr({obj.get_hpr()})\n"
                        self.content += " "*8 + f"self.{obj_name}.set_scale({obj.get_scale()})\n"
                        self.content += " "*8 + f"self.{obj_name}.reparent_to({root_name})\n\n"

                    if obj.get_tag("object_type") == "empty":
                        self.content += " "*8 + f"self.{obj_name} = NodePath('{obj_name}')\n"
                        self.content += " "*8 + f"self.{obj_name}.set_pos({obj.get_pos()})\n"
                        self.content += " "*8 + f"self.{obj_name}.set_hpr({obj.get_hpr()})\n"
                        self.content += " "*8 + f"self.{obj_name}.set_scale({obj.get_scale()})\n"
                        self.content += " "*8 + f"self.{obj_name}.reparent_to({root_name})\n\n"

                    elif obj.get_tag("object_type") == "collision":
                        self.content += " "*8 + f"col = {obj.get_tag('collision_solid_type')}(\n"
                        for key, value in eval(obj.get_tag('collision_solid_info')).items():
                            if key == "plane":
                                # BUG https://github.com/panda3d/panda3d/issues/1248
                                valueStr = repr(value).replace(" ", ", ")
                                self.content += " "*12 + f"{valueStr},\n"
                            else:
                                self.content += " "*12 + f"{value},\n"
                        self.content += " "*8 + f")\n"
                        self.content += " "*8 + f"cn = CollisionNode('{obj.get_name()}')\n"
                        self.content += " "*8 + f"cn.addSolid(col)\n"
                        self.content += " "*8 + f"self.{obj_name} = {root_name}.attachNewNode(cn)\n"
                        self.content += " "*8 + f"self.{obj_name}.set_pos({obj.get_pos()})\n"
                        self.content += " "*8 + f"self.{obj_name}.set_hpr({obj.get_hpr()})\n"
                        self.content += " "*8 + f"self.{obj_name}.set_scale({obj.get_scale()})\n\n"

                    elif obj.get_tag("object_type") == "physics":
                        self.content += " "*8 + f"actor_node = ActorNode('{obj.get_name()}')\n"
                        self.content += " "*8 + f"base.physicsMgr.attach_physical_node(actor_node)\n"
                        self.content += " "*8 + f"self.{obj_name} = {root_name}.attachNewNode(actor_node)\n\n"

                    elif obj.get_tag("object_type") == "light":
                        self.content += " "*8 + f"light = {obj.get_tag('light_type')}('{obj.get_name()}')\n"
                        if obj.get_tag('light_type') == "Spotlight":
                            self.content += " "*8 + f"lens = PerspectiveLens()\n"
                            self.content += " "*8 + f"light.setLens(lens)\n"
                        self.content += " "*8 + f"self.{obj_name} = {root_name}.attachNewNode(light)\n"
                        self.content += " "*8 + f"self.{obj_name}.set_pos({obj.get_pos()})\n"
                        self.content += " "*8 + f"self.{obj_name}.set_hpr({obj.get_hpr()})\n"
                        self.content += " "*8 + f"self.{obj_name}.set_scale({obj.get_scale()})\n"
                        self.content += " "*8 + f"{root_name}.setLight(self.{obj_name})\n\n"

                    elif obj.get_tag("object_type") == "camera":
                        self.content += " "*8 + f"self.{obj_name} = Camera('{obj_name}', {obj.get_tag('camera_type')}())\n\n"

                self.write_scene_element(obj, obj.get_name())

    def get_save_object_name(self, name):
        unsave_characters = [
            ",", ".",  ";", ":", "+", "-", "/", "\\","<", ">", "\"", "\'", "#",
            "*", "~", "!", "§", "$", "%", "&", "(", ")", "[", "]", "{", "}",
            "?", "`", "'", "|", "^", "°"]
        for unsave_char in unsave_characters:
            name = name.replace(unsave_char, "_")
        return name

    def save(self, doSave):
        if doSave:
            self.dlgOverwrite = None
            self.dlgOverwriteShadow = None
            path = self.browser.get()
            path = os.path.expanduser(path)
            path = os.path.expandvars(path)
            if os.path.exists(path):
                self.dlgOverwrite = YesNoDialog(
                    text="File already Exist.\nOverwrite?",
                    relief=DGG.RIDGE,
                    frameColor=(1,1,1,1),
                    frameSize=(-0.5,0.5,-0.3,0.2),
                    sortOrder=1,
                    button_relief=DGG.FLAT,
                    button_frameColor=(0.8, 0.8, 0.8, 1),
                    command=self.__executeSave,
                    extraArgs=[path],
                    scale=300,
                    pos=(base.getSize()[0]/2, 0, -base.getSize()[1]/2),
                    parent=base.pixel2d)
                self.dlgOverwriteShadow = DirectFrame(
                    pos=(base.getSize()[0]/2 + 10, 0, -base.getSize()[1]/2 - 10),
                    sortOrder=0,
                    frameColor=(0,0,0,0.5),
                    frameSize=self.dlgOverwrite.bounds,
                    scale=300,
                    parent=base.pixel2d)
            else:
                self.__executeSave(True, path)
            base.messenger.send("setLastPath", [path])
        self.browser.destroy()
        del self.browser

    def __executeSave(self, overwrite, path):
        if self.dlgOverwrite is not None: self.dlgOverwrite.destroy()
        if self.dlgOverwriteShadow is not None: self.dlgOverwriteShadow.destroy()
        if not overwrite: return
        with open(path, 'w') as outfile:
            outfile.write(self.content)
