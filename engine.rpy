# -*- coding: utf-8 -*-
init offset = 997
init python:


    mods["es_dev_gallery"] =  u"{font=fonts/timesi.ttf}{size=40}Галерея мододела{/size}{/font}"

    import pygame.scrap
    from renpy.display.layout import Composite as dComposite #TODO
    # from copy import copy as copy_instance

    class ESDG(object):
        """Специальный класс для хранения переменных, что бы было меньше путаницы."""

        SPRITES_DISTANCE_XSIZES = {"close": 1125, "normal": 900, "far": 630}
        POSITIONS = {"fleft": fleft, "left": left, "cleft": cleft, "center": center, "cright": cright, "right": right, "fright": fright}

        TRANSLATE_INTO_RUSSIAN = {
            "cs": "Виола",
            "dv": "Алиса",
            "el": "Электроник",
            "mi": "Мику",
            "mt": "Ольга Дмитриевна",
            "mz": "Женя",
            "pi": "Пионер",
            "sh": "Шурик",
            "sl": "Славя",
            "un": "Лена",
            "us": "Ульяна",
            "uv": "Юля",


            "square": "Площадь",
            "liaz": "Лиаз",
            "mine": "Шахта",
            "library": "Библиотека",
            "clubs": "Клубы",
            "intro": "Интро",
            "semen": "Комната Семёнв",
            "catacombs": "Катакомбы",
            "dining": "Столовая",
            "playground": "Спортплощадка",
            "camp_entrance": "Вход в лагерь",
            "stage": "Сцена",
            "beach": "Пляж",
            "bus": "Автобус",
            "houses": "Домики",
            "house_of_dv": "Дом Алисы",
            "boathouse": "Лод. Станция",
            "path": "Тропинка",
            "polyana": "Поляна",
            "path2": "Лес",
            "musclub": "Музклуб",
            "island": "Остров",
            "house_of_sl": "Дом Слави",
            "old_building": "Старое здание",
            "bathhouse": "Баня",
            "aidpost": "Медпункт",
            "house_of_un": "Дом Лены",
            "washstand": "Умывальники",
            "house_of_mt": "Дом Ольги",
            "road": "Дорога",

            "int": "Интерьер",
            "ext": "Экстерьер",
            "zvariants": "Другие варианты",



            "emotion": "Эмоции",
            "dress": "Одежда",
            "accessory": "Аксессуар",
            "distance": "Дальность",
            "position": "Позиция",

            "close": "Близко",
            "normal": "Обычно",
            "far": "Далеко",


            # "fleft": fleft,
            # "left": left,
            # "cleft": cleft,
            # "center": center,
            # "cright": cright,
            # "right": right,
            # "fright": fright



        }

        def __init__(self):
            object.__setattr__(self, "__dict__", {})

            # Default

            self.selected_element = [None, None]
            self.elements_background = "images/gui/gallery/not_opened_idle.png"
            self.elements_background_2 = None
            self.collections = {}

            self.settings_state = False
            self.gallery_state = False
            self.gallery_collection = None

            self.sprites = {}
            self.bg = None

        def __setattr__(self, key, value):
            self.__dict__[key] = value


        def __delattr__(self, key):
            del self.__dict__[key]


        # Методы полезные для мода
        def day_time(self):
            day_time()
            persistent.sprite_time = "day"
            renpy.restart_interaction()

        def sunset_time(self):
            sunset_time()
            persistent.sprite_time = "sunset"
            renpy.restart_interaction()

        def night_time(self):
            night_time()
            persistent.sprite_time = "night"
            renpy.restart_interaction()

        def translate(self, variable):

            if variable in self.TRANSLATE_INTO_RUSSIAN:
                return self.TRANSLATE_INTO_RUSSIAN[variable]
            return variable


        def hide_settings(self):
            self.settings_state  = False
            renpy.restart_interaction()

        def show_settings(self):
            self.settings_state = True
            renpy.restart_interaction()


        def add_element(self, element):

            element = element.copy()

            self.gallery_state  = False
            # self.show_element(element)
            #
            # element()

            # renpy.restart_interaction()



            if not element.collection in ["bg", "cg"]:
                self.sprites[element.name] = element
            else:
                self.bg = element
            # renpy.notify(str(self.sprites).replace("{", "<("))

            renpy.show_screen("esdg_delay", .7, Function(self.show_element, element), tag_="show_element_"+element.name, _tag="show_element_"+element.name)
            #self.show_element(element)

            element()

        def hide_element(self):
            self.selected_element[0] = False
            renpy.restart_interaction()

        def show_element(self, element):

            self.selected_element = [True, element]
            renpy.restart_interaction()

        def remove_sprite(self):
            element = self.selected_element[1]
            if element and element.name in self.sprites:
                self.sprites.pop(element.name)

            self.hide_element()

            if element:
                element.remove()


        def hide_gallery(self):
            self.gallery_state  = False
            renpy.restart_interaction()

        def show_gallery(self, collection):
            self.gallery_state = True

            self.gallery_collection = collection
            renpy.restart_interaction()


        def refresh_sprites(self):

            renpy.call("es_dev_gallery.massive_sprites", self.sprites.values())


    class CopyCode(Action):
        """Действие для копирования текста в буфер обмена."""
        def __init__(self, code):
            self.code = code

        def __call__(self):
            pygame.scrap.put(pygame.SCRAP_TEXT, self.code.encode("utf-8"))
            renpy.notify(_("Строчка кода скопирована в буфер обмена"))



    class EsdgElement:

        def __init__(self, *args, **kwargs):

            self.name = ""
            self.collection = ""
            self.extra = {}

            self.actions = {}

            self.default_preference = {}

            self.preference = self.default_preference.copy()

            self.preview = Null()

            self.__copy_req = []



        def create_diplayable(self, _preference=None):
            return Null()


        def create_preview(self, _preference=None):
            return self.create_diplayable(_preference)

        def get_settings(self):
            setting = {"image": {}, "text":{}}
            return setting

        def set_preference(self, name, value):
            pass

        def callback(self, *callback):
            pass

        @property
        def code(self):
            return ""

        def copy(self, *args, **kwargs):
            # return copy_instance(self)
            return self.__class__(*self.__copy_req)


        def __call__(self, *args, **kwargs):
            pass


    class EsdgCg(EsdgElement):


        def __init__(self, name, data, *args, **kwargs):

            self.name = name
            self.collection = "cg"
            self.extra = {"Появление": data[0]}

            self._time = data[0]

            self.actions = {}

            self.default_preference = {}

            self.preference = self.default_preference.copy()

            self.preview = data[1]

            self.__copy_req = [name, data]



        def create_diplayable(self, _preference=None):
            return self.preview


        def create_preview(self, _preference=None):
            return self.create_diplayable(_preference)

        def get_settings(self):
            setting = {"image": {}, "text":{}}
            return setting

        def set_preference(self, name, value):
            pass

        def callback(self, *callback):
            pass

        @property
        def code(self):
            return "scene cg "+self._time+"_"+self.name


        def __call__(self, *args, **kwargs):
            renpy.call("es_dev_gallery.show_scene", bg=self.preview)



    class EsdgBg(EsdgElement):

        def __init__(self, name, data, *args, **kwargs):

            self.name = name
            self.collection = "bg"
            self.extra = {"Вариаций": "0+"}

            self.actions = {}

            self._settings = {}
            self._data = {}

            default_bg = None

            for setting in data:
                self._settings[setting] = []
                for bg in data[setting]:
                    self._data[bg[0]] = bg[1]
                    self._settings[setting].append((bg[0], self.create_diplayable({"name": bg[0]})))


                if setting in ["ext", "int"] or not default_bg:
                    default_bg = self._settings[setting][0][0]


            self.default_preference = {"name": default_bg, "int": default_bg, "ext": default_bg,"zvariants": default_bg}

            self.preference = self.default_preference.copy()

            self.preview = self._data[default_bg]

            self.extra["Вариаций"] = str(len(self._data))

            self.__copy_req = [self.name, data]



        def create_diplayable(self, _preference=None):
            bg = _preference["name"] if _preference else self.default_preference["name"]

            return self._data[bg]


        def create_preview(self, _preference=None):
            return self.create_diplayable(_preference)

        def get_settings(self):
            return {"image": self._settings, "text": {}}

        def set_preference(self, name, value):
            for pref in ["name", "int", "ext", "zvariants"]:
                self.preference[pref] = value

        def callback(self, *callback):
            self.set_preference(callback[0], callback[1])

            self()

        @property
        def code(self):
            return "scene bg "+self.preference["name"]


        def __call__(self, *args, **kwargs):
            renpy.call("es_dev_gallery.show_scene", bg=self.create_diplayable(self.preference))


    class EsdgSprite(EsdgElement):

        def __init__(self, name, data, *args, **kwargs):

            self.name = name
            self.collection = "sprite"
            self.extra = {"Тег": name}

            self.actions = {"Убрать спрайт": esdg.remove_sprite}

            self._data = data

            self._emotions = {}

            self.__copy_req = [self.name, self._data]

            default_emotion = None

            for distance in data:
                distance_data = data[distance]
                for pose in distance_data:
                    pose_data = distance_data[pose]

                    for emotion in pose_data["emotions"]:

                        if emotion == "normal" or (not default_emotion and emotion):
                            default_emotion = emotion

                        if not emotion in self._emotions:
                            self._emotions[emotion] = [pose, []]

                        if distance == "close":
                            self._emotions[emotion][1].insert(0, distance)
                        elif distance == "normal":
                            if "close" in self._emotions[emotion][1]:
                                self._emotions[emotion][1].insert(1, distance)
                            else:
                                self._emotions[emotion][1].insert(0, distance)
                        else:
                            self._emotions[emotion][1].append(distance)


            default_dress = None

            if "dresses" in data["normal"]["1"]:
                for dress in data["normal"]["1"]["dresses"]:
                    if dress == "pioneer" or (not default_dress and dress):
                        default_dress = dress

            self.default_preference = {
                                        "emotion": default_emotion,

                                        "dress": default_dress,

                                        "accessory": None,


                                        "distance": "normal",
                                        "position": "center"


                                        }

            self.preference = self.default_preference.copy()


            self.preview = self.create_preview(self.default_preference)

            self._settings_buffer = [{"emotion": None, "distance": None}, {"image": {}, "text":{}}]

        def create_diplayable(self, _preference=None):

            preference = self.default_preference.copy()

            preference.update(_preference or self.preference)

            pose = self._emotions[preference["emotion"]][0]
            base = self._data[preference["distance"]][pose]

            composite_data = [(esdg.SPRITES_DISTANCE_XSIZES[ preference["distance"] ], 1080)]

            if "body" in base:
                composite_data += [(0, 0), base["body"] ]

            composite_data += [(0, 0), base["emotions"][ preference["emotion"] ], ]

            if preference["dress"]:
                composite_data += [(0, 0), base["dresses"][ preference["dress"] ], ]

            if preference["accessory"]:
                composite_data += [(0, 0), base["accessories"][ preference["accessory"] ], ]

            sprite = im.Composite(*composite_data)

            return ConditionSwitch(
                "persistent.sprite_time=='sunset'",
                    im.MatrixColor(
                        sprite,
                        im.matrix.tint(0.94, 0.82, 1.0)
                    ),
                "persistent.sprite_time=='night'",
                    im.MatrixColor(
                        sprite,
                        im.matrix.tint(0.63, 0.78, 0.82)
                    ),
                True,
                    sprite
            )

        def create_preview(self, _preference=None, k=2.2, h=.2):
            preference = self.default_preference.copy()

            preference.update(_preference or self.preference)

            preference = self.change_preference(preference, "distance", "normal")

            if self.name in ["us", "uv"]:
                h=.55+.67*(-.2+h)
                k=3.08+1.2*(-2.2+k)

            return At(self.create_diplayable(_preference), esdg_focus_sprite(k, esdg.SPRITES_DISTANCE_XSIZES[ preference["distance"] ], 1080, h))

        def get_settings(self):

            if self._settings_buffer[0]["emotion"] != self.preference["emotion"] or self._settings_buffer[0]["distance"]  != self.preference["distance"]:
                setting = {"image": {}, "text":{}}

                emotions = []

                for emotion in self._emotions:
                    emotions.append((emotion, self.create_preview(self.change_preference(self.default_preference,name="emotion", value=emotion, log=False))))
                setting["image"]["emotion"] = emotions

                pose = self._emotions[self.preference["emotion"]][0]
                base = self._data[self.preference["distance"]][pose]


                if "dresses" in base:
                    dresses = []

                    for dress in base["dresses"]:
                        dresses.append((dress, self.create_preview(self.change_preference(self.default_preference,name="dress", value=dress, log=False), 1.5, .9)))

                    setting["image"]["dress"] = dresses

                if "accessories" in base:
                    accessories = []

                    for accessory in  base["accessories"]:
                        accessories.append((accessory, self.create_preview(self.change_preference(self.default_preference,name="accessory", value=accessory, log=False), 1.6, .1)))

                    setting["image"]["accessory"] = accessories



                distances = self._emotions[self.preference["emotion"]][1]
                if len(distances) > 1:
                    setting["text"]["distance"] = distances

                setting["text"]["position"] = ["fleft", "left", "cleft", "center", "cright", "right", "fright"]

                self._settings_buffer[0]["emotion"] = self.preference["emotion"]
                self._settings_buffer[0]["distance"] = self.preference["distance"]

                self._settings_buffer[1] = setting

            else:
                setting = self._settings_buffer[1]


            return setting

        def change_preference(self, _preference=None, name="", value=None, log=False):

            assert name, "Name must be written!"

            if _preference=="default":
                preference = self.default_preference.copy()
            elif type(_preference) == dict:
                preference = _preference.copy()
            else:
                preference = self.preference.copy()

            preference[name] = value

            if name != "distance" and not self._emotions[ preference["emotion"] ][0] in self._data[preference["distance"]]:
                if log:
                    renpy.notify("Не возможно применить дистанцию к одной из настроек, потому она установлена по умолчанию")
                preference["distance"] = "normal"


            if name != "emotion" and not preference["distance"] in self._emotions[ preference["emotion"] ][1]:
                if log:
                    renpy.notify("Не возможно применить эмоцию к одной из настроек, потому она установлена по умолчанию")
                for emotion in self._emotions:
                    if preference["distance"] in self._emotions[ preference["emotion"] ][1]:
                        preference["emotion"] = emotion

            base = self._data[preference["distance"]][ self._emotions[ preference["emotion"] ][0]]

            if not "dresses" in base or not preference["dress"] in base["dresses"]:
                if log and preference["dress"] != None:
                    renpy.notify("Не возможно применить одежду к одной из настроек, потому она установлена по умолчанию")

                preference["dress"] = None

                if "dresses" in base:
                    for dress in base["dresses"]:
                        if dress == "pioneer" or (not preference["dress"] and dress):
                            preference["dress"] = dress

            if not "accessories" in base or not preference["accessory"] in base["accessories"]:
                if log and preference["accessory"] != None:
                    renpy.notify("Не возможно применить аксессуар к одной из настроек, потому она установлена по умолчанию")

                preference["accessory"] = None

            return preference

        def set_preference(self, name, value):
            self.preference.update(self.change_preference(name=name, value=value, log=True))

        def callback(self, *callback):
            #renpy.notify(str(callback))

            self.set_preference(callback[0], callback[1])

            # renpy.restart_interaction()

            self()


        @property
        def code(self):
            name = " "+self.name
            emotion = (" "+self.preference["emotion"] if self.preference["emotion"] else "")
            dress = (" "+self.preference["dress"] if self.preference["dress"] else " body" if "body" in self._data[self.preference["distance"]][ self._emotions[ self.preference["emotion"]][0]] else"")
            accessory = (" "+self.preference["accessory"] if self.preference["accessory"] else "")
            distance = (" "+self.preference["distance"] if self.preference["distance"] != "normal" else "")
            position = (" at "+self.preference["position"] if self.preference["position"] else "")
            return "show"+name+emotion+dress+accessory+distance+position

        def __call__(self, trans=dissolve, *args, **kwargs):
            renpy.call("es_dev_gallery.show_displayable", displayable=self.create_diplayable(), name = self.name, pos_at = esdg.POSITIONS[self.preference["position"]], trans=trans)

        def remove(self):
            renpy.call("es_dev_gallery.hide_displayable", self.name)


    def esdg_create_collections():

        global esdg_collections

        esdg_collections = {}

        sprites = esdg_get_sprites()
        sprites_objects = {}

        for sprite in sprites:
            sprite_data = sprites[sprite]

            sprites_objects[sprite] = EsdgSprite(sprite, sprite_data)

        esdg_collections["sprites"] = sprites_objects

        bgs = esdg_get_bg()
        bg_objects = {}

        for bg in bgs:

            bg_data = bgs[bg]

            bg_objects[bg] = EsdgBg(bg, bg_data)

        esdg_collections["bg"] = bg_objects



        # cgs = esdg_get_cg()
        # cg_objects = {}
        #
        # for cg in cgs:
        #
        #     cg_data = cgs[cg]
        #
        #     cg_objects[cg] = EsdgCg(cg, cg_data)
        #
        # esdg_collections["cg"] = cg_objects



    def esdg_get_cg():

        cgs = {}

        for file in renpy.list_files():
            if file.startswith("images/cg/") and not "cards_contest" in file:

                name = file.split("/")[-1][:-4]

                cgs[name.split("_", 1)[1]] = (name.split("_", 1)[0], file)

        return cgs

    def esdg_get_bg(): # Hope it'll work...

        groups = {}

        for file in renpy.list_files():
            if file.startswith("images/bg/"):

                info = []

                name = file.split("/")[-1][:-4]
                file_tags = name.split("_")

                info.append(name)


                itype = False

                if file_tags[0] in ["int", "ext"]:
                    info.append(file_tags[0])
                    itype = True
                else:
                    info.append(None)


                itime = False
                if file_tags[-1] in ["day", "sunset", "night"]:
                    info.append(file_tags[-1])
                    itime = True
                else:
                    info.append(None)

                bg = name.replace(info[1]+"_" if itype else "", "").replace("_"+info[2] if itime else "", "")
                # info.append(bg)

                tag = bg.split("_")[0]

                if tag == "old":
                    tag = "old_building"

                elif tag == "house":
                    tag = "house_of_"+bg.split("_")[2]

                elif tag == "washstand2":
                    tag = "washstand"

                elif tag == "no": #TODO
                    tag = "bus"

                elif tag == "camp":
                    tag = "camp_entrance"

                if not tag in groups:
                    groups[tag] = {}


                collection = info[1] or "zvariants"
                if not collection in groups[tag]:
                    groups[tag][collection] = []



                groups[tag][collection].append([name, file])

                #print(info)

        tfile = open("bgs.txt", "w")
        for bg in groups:

            tfile.write('"'+bg+'": " '+'",\n')

        tfile.close()

        return groups







    def esdg_get_sprites():

        emotions = [
            "normal",
            "normal_smile",

            "surp1",
            "surp2",
            "surp3",
            "surprise",
            "surprise2",

            "smile",
            "smile2",
            "smile3",

            "grin",
            "happy",
            "laugh",
            "laugh2",

            "evil_smile",
            "cry_smile",

            "shy",
            "shy2",

            "serious",

            "dontlike",
            "angry",
            "angry2",
            "rage",

            "tender",
            "guilty",

            "upset",

            "sad",
            "cry",
            "cry2",

            "fingal",
            "bukal",
            "calml",

            "scared",
            "fear",
            "shocked",
        ]

        dresses = [
            "swim",
            "pioneer2",
            "dress",
            "sport",
            "pioneer",

            "coat", # Эта одежда вырезана из игры и осталась только в качестве файла,
                    # потому если вы хотите её использовать - вам придется обьявит её заново

            # "pioneer_smile", исключение для пионера
        ]

        accessories = [
            "stethoscope",
            "panama",
            "glasses",
        ]

        ifnull = None#Null(width=900, heigh=1080)

        sprites = {}

        for file in renpy.list_files():
            if file.startswith("images/sprites/") and not "pi/" in file:
                file_pos = file.split("/")
                name = file_pos[-1][:-4]
                file_tokens = name.split("_", 2)

                if file_tokens[0] in sprites:
                    sprite = sprites[file_tokens[0]]
                else:
                    sprite = sprites[file_tokens[0]] = {"close": {}, "normal": {}, "far": {}}

                sprite = sprite[file_pos[2]]

                if file_tokens[1] in sprite:
                    pose = sprite[file_tokens[1]]
                else:
                    pose = sprite[file_tokens[1]] = {}

                if file_tokens[2] == "body":
                    pose["body"] = file
                    if "dresses" in pose:
                        pose["dresses"][None] = ifnull

                elif file_tokens[2] in emotions:
                    if not "emotions" in pose:
                        pose["emotions"] = {}
                    pose["emotions"][file_tokens[2]] = file

                elif file_tokens[2] in dresses:
                    if not "dresses" in pose:
                        pose["dresses"] = {}
                    pose["dresses"][file_tokens[2]] = file
                    if "body" in pose:
                        pose["dresses"][None] = ifnull

                elif file_tokens[2] in accessories:
                    if not "accessories" in pose:
                        pose["accessories"] = {None : ifnull}
                    pose["accessories"][file_tokens[2]] = file

                else:
                    raise Exception("Файл с неопределенным аттрибутом \""+file_tokens[2]+"\"!: "+file)


        sprites["pi"] = { # Исключение
        i: {"1": {"emotions": {
                                "": "images/sprites/"+i+"/pi/pi_1_pioneer.png",
                                "smile":  "images/sprites/"+i+"/pi/pi_1_pioneer_smile.png"
                              }
                 }
            } for i in ["far", "normal", "close"]
        }

        return sprites

    def prepare_everlasting_summer_dev_gallery():
        #global esdg_collections

        esdg_create_collections()

    def initialize_everlasting_summer_dev_gallery():

        global esdg

        esdg = ESDG()



        # default

        # esdg.selected_element = [True, EsdgElement()]

        # esdg.selected_element = [True, esdg_collections["sprites"]["us"]]

        # esdg.selected_element = [True, esdg_collections["bg"]["library"]]

        esdg.day_time()

        esdg.elements_background = "images/gui/gallery/not_opened_idle.png"
        esdg.elements_background_2 = im.Scale(im.Blur("images/bg/ext_camp_entrance_day.jpg", 2.5), 320, 180)
        esdg.elements_background_2 = ConditionSwitch(
            "persistent.sprite_time=='sunset'",
                im.Scale(im.Blur("images/bg/ext_beach_sunset.jpg", 2.5), 320, 180),
            "persistent.sprite_time=='night'",
                im.Scale(im.Blur("images/bg/ext_beach_night.jpg", 2.5), 320, 180),
            True,
                im.Scale(im.Blur("images/bg/ext_beach_day.jpg", 2.5), 320, 180)
        )
