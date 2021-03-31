# -*- coding: utf-8 -*-
init python:

    mods["es_dev_gallery"] =  u"{font=fonts/timesi.ttf}{size=40}Галерея мододела{/size}{/font}"

    import pygame.scrap
    from renpy.display.layout import Composite as dComposite #TODO
    import re, os

    class ESDG(object):
        """Специальный класс для хранения переменных, что бы было меньше путаницы."""

        def __init__(self):
            object.__setattr__(self, "__dict__", {})

            global esdg
            esdg = self

            # Default

            self.POSITIONS = {"fleft": fleft, "left": left, "cleft": cleft, "center": center, "cright": cright, "right": right, "fright": fright}
            self.SPRITES_DISTANCE_XSIZES = {"close": 1125, "normal": 900, "far": 630}


            self.TRANSLATE_INTO_RUSSIAN = {
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
                "semen": "Комната Семёна",
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


                "sprites": "Спрайты",
                "bg": "Фоны",
                "cg": "Иллюстрации",
                "CG": "Иллюстрация",





                "emotion": "Эмоции",
                "dress": "Одежда",
                "accessory": "Аксессуар",
                "distance": "Дальность",
                "position": "Позиция",

                "close": "Близко",
                "normal": "Обычно",
                "far": "Далеко",
            }



            if renpy.variant("large"):

                self.xpreview_size = 336
                self.ypreview_size = 196

                self.x_preview_size = 320
                self.y_preview_size = 180

                self.x_size = 1920
                self.y_size = 1080

                self.element_viewer_bg_crop = (370, 110, 1388, 890)
                self.element_viewer_viewport_area = (0, 0, 660, 800)

            else:
                self.xpreview_size = 244
                self.ypreview_size = 131

                self.x_preview_size = 213
                self.y_preview_size = 120

                self.x_size = 1280
                self.y_size = 720

                self.element_viewer_bg_crop = (247, 73, 925, 593)
                self.element_viewer_viewport_area = (0, 0, 440, 600)

            self.preview_size = self.xpreview_size, self.ypreview_size

            self._size = self.x_size, self.y_size

            self.elements_background = im.Scale(im.Blur("images/bg/ext_camp_entrance_day.jpg", 2.5), self.x_preview_size, self.y_preview_size)

            self.galleries = {}# {"Number": EsdgGallery(20)}

            # По возможности все переводить в константы ради оптимизации
            renpy.const("esdg.POSITIONS")
            renpy.const("esdg.TRANSLATE_INTO_RUSSIAN")
            renpy.const("esdg.SPRITES_DISTANCE_XSIZES")

            # renpy.const("esdg.galleries")

            renpy.const("esdg.xpreview_size")
            renpy.const("esdg.ypreview_size")
            renpy.const("esdg.preview_size")

            renpy.const("esdg.x_preview_size")
            renpy.const("esdg.y_preview_size")

            renpy.const("esdg.x_size")
            renpy.const("esdg.y_size")
            renpy.const("esdg._size")

            renpy.const("esdg.element_viewer_bg_crop")
            renpy.const("esdg.element_viewer_viewport_area")

            renpy.pure("esdg.translate")

            self.settings = self.element_viewer = self.gallery = None
            self.bg = None
            self.sprites = []



            # self.init()

        def init(self):

            self.settings = False
            self.element_viewer = self.gallery = EsdgScreen
            self.day_time()

            self.bg = None
            self.sprites = []


        def __setattr__(self, key, value):
            self.__dict__[key] = value


        def __delattr__(self, key):
            del self.__dict__[key]


        def create_galleries(self):

            self.galleries = {}

            sprites = esdg_get_sprites()
            sprites_objects = []

            for sprite in sprites:
                sprite_data = sprites[sprite]

                sprites_objects.append(EsdgSprite(sprite, sprite_data))

            self.galleries["sprites"] = EsdgGallery("sprites", sprites_objects)


            bgs = esdg_get_bg()
            bg_objects = []

            for bg in bgs:

                bg_data = bgs[bg]

                bg_objects.append(EsdgBg(bg, bg_data))

            self.galleries["bg"] = EsdgGallery("bg", bg_objects)

            cgs = esdg_get_cg()
            cg_objects = []

            for cg in cgs:

                cg_data = cgs[cg]

                cg_objects.append(EsdgCg(cg_data))

            self.galleries["cg"] = EsdgGallery("cg", cg_objects)

        def exception(self, check, message=""):
            """
            Так как трейсбек перестает работать, приходится отдельно
            проверять.

            assert тоже не работает, в итоге приходится вот так извращатся.

            """

            if not check:
                raise Exception(message+"""\n\n
Если вы это видите эту ошибку то пожайлуста
пришлите лог сюда
https://vk.com/topic-203508980_47492565
или
https://github.com/Mikan-DS/Everlasting_Summer_Development_Gallery/issues
                """)

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


        def timer_action(self, time, action, name="timer_action"):
            renpy.show_screen("esdg_delay", time, action, tag_=name, _tag=name)

        def timed_sprite(self, sprite):

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

        def zoom_to_preview(self, img):
            """
            Метод для упрощения адаптирование изображения
            из размера экрана по коэффиценту размеру стандартного
            превью.
            """
            # assert not isinstance(img, Displayable) #
            return At(img, esdg_zoom_image(k=.1666))


        # Методы для работы с выводом кода
        def code_all(self):
            """Собирает код со всех элементов"""

            code = "# Время суток\n$ " + time_of_day + '_time()\n$ persistent.sprite_time = "' + time_of_day +'"\n\n'

            add_transition = False

            if self.bg:
                add_transition = True
                code += "# Фон\n" + self.bg.code + (" # " + self.translate(self.bg.name) if self.bg.name != "cg" else "") + "\n\n"

            if len(self.sprites) > 1:
                code += "# Спрайты\n"
            for sprite in reversed(self.sprites):
                add_transition = True
                code += sprite.code + " # " + self.translate(sprite.name) + "\n"

            if add_transition:
                code += "\n\nwith " + renpy.random.choice(["dspr", "dissolve_fast", "dissolve", "fade"]) + " # Переход от фирмы :)\n"

            return code

        def color_code(self, code):

            code = re.sub(r"(#[^\n]*)", r"{color=#a56870}\1{/color}", code)
            code = re.sub(r'("[^\n]*")', r"{color=#446e41}\1{/color}", code)

            for i in ["show", "scene", "with", "at", "$"]:
                #code = re.sub(r'(show|scene|$)', r"{color=#a78e66}\1{/color}", code)
                code = code.replace(i, "{color=#fc6}"+i+"{/color}" )
            return code




        # Методы галереи

        def show_gallery(self, gallery):
            # assert isinstance(gallery, EsdgGallery) # Если вы это видите в ошибке то пожайлуста пришлите лог сюда https://vk.com/topic-203508980_47492565 или https://github.com/Mikan-DS/Everlasting_Summer_Development_Gallery/issues
            self.exception(isinstance(gallery, EsdgGallery), "in show gallery "+str(gallery))

            self.gallery = gallery
            gallery.state = True
            renpy.restart_interaction()

        def hide_gallery(self):
            self.gallery.state = False

            self.timer_action(.7, self.remove_gallery, "remove_gallery")
            renpy.restart_interaction()

        def remove_gallery(self):
            self.gallery = EsdgScreen


        # Методы манипуляции спрайтами

        def add_element(self, element):

            self.exception(isinstance(element, EsdgElement), "in adding new element "+str(element))

            element = element.copy() # Копируется для того что бы значения обновлялись



            if element.collection in ["bg", "cg"]:

                self.bg = None
                self.bg = element

                self.hide_gallery()

                self.timer_action(.7, Function(self.select_element, element), "show_background_"+element.name)

                element()

            else:
                if element in self.sprites: # Если предмет уже добавлен,
                    self.sprites.remove(element) # то его аналог удаляется (типо перезапуска)

                self.sprites.insert(0, element) # Он всегда добавляется наверх

                self.hide_gallery()

                self.timer_action(.7, Function(self.select_element, element), "show_sprite_"+element.name)

                self.refresh_sprites()
            # element()

        def select_element(self, element):

            self.element_viewer = element
            element.state = True

        def deselect_element(self):
            self.element_viewer.state = False

            self.timer_action(.7, self.remove_element, "remove_element")
            renpy.restart_interaction()

        def remove_element(self):
            self.element_viewer = EsdgScreen

        def remove_sprite(self):

            element = self.element_viewer

            self.deselect_element()

            if isinstance(element, EsdgSprite): # Только для спрайтов (в том числе и пользовательских)

                if element in self.sprites: # Если предмет еще есть
                    self.sprites.remove(element) # то он удаляется

                element.remove()

        def move_element(self, i, direction):

            if direction == "down":
                if i+1 < len(self.sprites):
                    self.sprites.insert(i+1, self.sprites.pop(i))

            else:
                if i > 0:
                    self.sprites.insert(i-1, self.sprites.pop(i))

            self.refresh_sprites()

        def refresh_sprites(self):

            renpy.call("es_dev_gallery.massive_sprites")

        # Методы настроек быстрых настроек

        def show_settings(self):
            self.settings = True
            renpy.restart_interaction()

        def hide_settings(self):
            self.settings = False
            renpy.restart_interaction()







    class CopyCode(Action):
        """Действие для копирования текста в буфер обмена."""
        def __init__(self, code):
            self.code = code

        def __eq__(self, other):

            if not isinstance(other, CopyCode):
                return False

            return self.code is other.code

        def __call__(self):
            pygame.scrap.put(pygame.SCRAP_TEXT, self.code.encode("utf-8"))
            renpy.notify(_("Строчка кода скопирована в буфер обмена"))

    class OpenFileCode(Action):
        """Действие для копирования кода в файл."""
        def __init__(self, code):
            self.code = code

        def __eq__(self, other):

            if not isinstance(other, CopyCode):
                return False

            return self.code is other.code

        def __call__(self):
            with open("ESDG_SCENE_OUTPUT.txt", "w") as file:
                file.write(self.code)
            renpy.notify(_("Открытие файла ESDG_SCENE_OUTPUT.txt"))
            os.startfile("ESDG_SCENE_OUTPUT.txt")


    class EsdgScreen(object):

        state = False

    class EsdgGallery(EsdgScreen):

        def __init__(self, name, elements):

            self.name = name
            self._page = 0


            self.elements = elements# [EsdgElementData(i) for i in range(1, i+1)]

            self.page_maximum = (len(elements)-1)//9

        def page(self):

            return self.elements[self._page*9:self._page*9+9]

        def next_page(self):
            if self._page < self.page_maximum:
                self._page += 1
            else:
                self._page = 0
            renpy.restart_interaction()

        def back_page(self):
            if self._page > 0:
                self._page -= 1
            else:
                self._page = self.page_maximum

            renpy.restart_interaction()

    # class EsdgElementData:
    #
    #     def __init__(self, *args, **kwargs):
    #
    #         self.preview = Null()#Crop((-50, -5, esdg.xpreview_size, esdg.ypreview_size), Text(str(i), size=200))
    #
    #         self.name = ""
    #         self.collection = "None"
    #         self.element_class = EsdgElementData


    class EsdgElement(object):

        def __init__(self, *args, **kwargs):

            self.name = ""
            self.collection = ""
            self.extra = {}

            self.actions = {}

            self.default_preference = {}

            self.preference = self.default_preference.copy()

            self.preview = Null()

            self._cash = []
            self.__copy_req = {}

            self.state = False


        def create_displayable(self, _preference=None):
            return Null()


        def create_preview(self, _preference=None):
            return self.create_displayable(_preference)

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
            return self.__class__(**self.__copy_req)

        def __call__(self, *args, **kwargs):
            pass

        def __eq__(self, other):
            if not isinstance(other, self.__class__):
                return False
            return self.name == other.name


    class EsdgCg(EsdgElement):

        def __init__(self, data, _settings=None, preview=None, default_preference=None):

            self.name = "CG"
            self.collection = "bg"
            self.extra = {"Вариаций": str(len(data))}

            self.state = False

            self.actions = {}

            self._data = data

            if _settings and default_preference:
                self._settings = _settings
                self.default_preference = default_preference

            else:
                self._settings = {"zvariants":[]}

                default_cg = None

                for cg in data:
                    default_cg = cg

                    self._settings["zvariants"].append((cg, self.create_preview({"zvariants": cg})))


                self.default_preference = {"zvariants": default_cg}

            self.preference = self.default_preference.copy()

            self.preview = preview or self.create_preview({"zvariants":default_cg})#self._data[default_bg]

            self.__copy_req = {
                "data": self._data,
                "_settings": self._settings,
                "preview": self.preview,
                "default_preference": self.default_preference

            }

        def create_displayable(self, _preference=None):
            cg = _preference["zvariants"] if _preference else self.default_preference["zvariants"]

            return self._data[cg]

        def create_preview(self, _preference=None):
            return self.create_displayable(_preference) # esdg.zoom_to_preview()

        def get_settings(self):
            return {"image": self._settings, "text": {}}

        def set_preference(self, value):
            self.preference["zvariants"] = value

        def callback(self, *callback):
            self.set_preference(callback[1])

            self()

        @property
        def code(self):
            return "scene cg "+self.preference["zvariants"]


        def __call__(self, *args, **kwargs):


            esdg.sprites.clear()

            renpy.call("es_dev_gallery.show_scene", bg=self.create_displayable(self.preference))

        def __eq__(self, other):
            if not isinstance(other, self.__class__):
                return False
            return self._data == other._data




    class EsdgBg(EsdgElement):

        def __init__(self, name, data, cash=None, preview=None, _settings=None, default_preference=None):

            self.name = name
            self.collection = "bg"
            self.extra = {"Вариаций": "0+"}

            self.state = False

            self.actions = {}

            if _settings and default_preference and cash:
                self._data = cash
                self._settings = _settings
                self._data = cash
                self.default_preference = default_preference

            else:
                self._settings = {}
                self._data = {}

                default_bg = None

                for setting in data:
                    self._settings[setting] = []
                    for bg in data[setting]:
                        self._data[bg[0]] = bg[1]
                        self._settings[setting].append((bg[0], self.create_preview({"name": bg[0]})))


                    if setting in ["ext", "int"] or not default_bg:
                        default_bg = self._settings[setting][0][0]


                self.default_preference = {"name": default_bg, "int": default_bg, "ext": default_bg,"zvariants": default_bg}

            self.preference = self.default_preference.copy()

            self.preview = preview or self.create_preview({"name":default_bg})#self._data[default_bg]

            self.extra["Вариаций"] = str(len(self._data))

            self.__copy_req = {
                "name": name,
                "data": self._data,
                "cash": self._data,
                "preview": self.preview,
                "_settings": self._settings,
                "default_preference": self.default_preference

            }

        def create_displayable(self, _preference=None):
            bg = _preference["name"] if _preference else self.default_preference["name"]

            return self._data[bg]

        def create_preview(self, _preference=None):
            return self.create_displayable(_preference) # esdg.zoom_to_preview(

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


            if "day" in self.preference["name"]:
                esdg.day_time()

            elif "sunset" in self.preference["name"]:
                esdg.sunset_time()
            elif "night" in self.preference["name"]:
                esdg.night_time()
            elif "black" in self.preference["name"]:
                esdg.night_time()

            else:
                esdg.day_time()

            renpy.call("es_dev_gallery.show_scene", bg=self.create_displayable(self.preference))


    class EsdgSprite(EsdgElement):

        def __init__(self, name, data, cash=None, _emotions=None, default_preference=None, preview=None,  *args, **kwargs):

            self.state = True # Нужно только для показа экрана

            self.name = name
            self.collection = "sprite"
            self.extra = {"Тег": name}

            self.actions = {"Убрать спрайт": esdg.remove_sprite}

            self._data = data

            self.cash = cash or {} # cache занят
            self._emotions = _emotions or {}

            self._k = 1.0


            if _emotions and default_preference:# Если все уже найдено, то просто присваивает значения

                self.default_preference = default_preference

            else:

                # Заполняет словарь эмоций и заодно ищет подходящую дефолтную

                default_emotion = None

                for distance in data:
                    distance_data = data[distance]
                    for pose in distance_data:
                        pose_data = distance_data[pose]

                        for emotion in pose_data["emotions"]:

                            if emotion == "normal" or (not default_emotion and emotion != None):
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


                # Дефолтная позиция, как правило, normal
                default_distance = self._distance(self._emotions[default_emotion])

                # Дефолтная одежда если есть
                default_dress = self._dress(self._base(default_distance, self._pose(default_emotion)))

                # Составляет словарь с дефолтными значениями

                self.default_preference = {
                                            "emotion": default_emotion,

                                            "dress": default_dress,

                                            "accessory": None, # Для аксессура нет смысла искать дефолт


                                            "distance": default_distance,
                                            "position": "center" # Это не относится к спрайту напрямую, потому все варианты всегда доступны для всех спрайтов
                                            }


            # Изначально настройки должны быть установлены по умолчанию
            # и впоследтсвие быть независимы от дефолтных и настроек другого
            # экземпляра спрайта
            self.preference = self.default_preference.copy()


            # Если уже есть превью - присваивается, в ином случае вызывает
            # метод для создания
            self.preview = preview or self.create_preview()


            # создание буфера для настроек
            self._settings_buffer = [{"emotion": None, "distance": None}, {"image": {}, "text":{}}]

            # создание словаря с необходимыми аттрибутами для копирования

            self.__copy_req = {
                            "name":name,
                            "data":data,
                            "cash":self.cash,
                            "_emotions":self._emotions,
                            "default_preference":self.default_preference,
                            "preview":self.preview
            }


        def create_displayable(self, _preference=None):

            preference = self.default_preference.copy()
            preference.update(_preference or self.preference)

            base = self._base(preference["distance"], self._pose(preference["emotion"]))

            composite_data = [(esdg.SPRITES_DISTANCE_XSIZES[ preference["distance"] ], esdg.y_size)]

            if "body" in base:
                composite_data += [(0, 0), base["body"] ]

            composite_data += [(0, 0), base["emotions"][ preference["emotion"] ], ]

            if preference["dress"]:
                composite_data += [(0, 0), base["dresses"][ preference["dress"] ], ]

            if preference["accessory"]:
                composite_data += [(0, 0), base["accessories"][ preference["accessory"] ], ]

            return im.Composite(*composite_data)



        def create_preview(self, name=None, value=None):



            preference = self.default_preference.copy()

            preference = self.change_preference(preference, "emotion", self.preference["emotion"])


            preference = self.change_preference(preference, name, value)

            cash = self._pose(preference["emotion"])+str(name)+"_"+str(value)

            if cash in self.cash:
                img = self.cash[cash]
            else:

                k = 2.2
                chk = 1.0
                h=0


                if self.name == "us":
                    chk = 1.55
                elif self.name == "uv":
                    chk = 1.3
                elif self.name in ["mi", "mz"]:
                    chk = 1.2
                elif self.name in ["sl", "dv", "un"]:
                    chk = 1.1


                if name == "dress":
                    h = 0
                    k = 1.6
                else:
                    h = -1.1

                k*=chk

                h+=(k)-1

                img = At(self.create_displayable(preference), esdg_focus_sprite(self._width(preference["distance"]), k, h))


                self.cash[cash] = img


            return img





        def get_settings(self):


            if self._settings_buffer[0]["emotion"] != self.preference["emotion"] or self._settings_buffer[0]["distance"]  != self.preference["distance"]:
                setting = {"image": {}, "text":{}}

                emotions = []

                for emotion in self._emotions:
                    emotions.append(
                                    (emotion, self.create_preview("emotion", emotion))

                                    )
                setting["image"]["emotion"] = emotions

                pose = self._emotions[self.preference["emotion"]][0]
                base = self._data[self.preference["distance"]][pose]


                if "dresses" in base:
                    dresses = []

                    for dress in base["dresses"]:
                        dresses.append(
                                    (dress, self.create_preview("dress", dress))
                                    )

                    setting["image"]["dress"] = dresses

                if "accessories" in base:
                    accessories = []

                    for accessory in  base["accessories"]:
                        accessories.append(
                                        (accessory, self.create_preview("accessory", accessory))
                                        )

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



        # Help

        def _distance(self, emotion_data):
            """Находит наиболее подходящую дистанцию из возможных для эмоции."""
            for i in emotion_data[1]:
                if i == "normal":
                    return i
            return i

        def _pose(self, emotion):
            """Находит позу от эмоции."""
            return self._emotions[emotion][0]

        def _base(self, distance, pose):
            """Находит базу под позу для определенной дистанции."""
            return self._data[distance][pose]

        def _dress(self, base):
            """
            Находит наиболее подходящую одежду из доступной
            в базе, если её нет, возвращает None.
            """
            dress = None

            if "dresses" in base:
                for _dress in base["dresses"]:
                    if _dress == "pioneer":
                        return _dress
                    elif not dress and _dress:
                        dress = _dress

            return dress

        def _width(self, distance):
            return esdg.SPRITES_DISTANCE_XSIZES[distance]


        @property
        def code(self):
            name = " "+self.name
            emotion = (" "+self.preference["emotion"] if self.preference["emotion"] else "")
            dress = (" "+self.preference["dress"] if self.preference["dress"] else " body" if "body" in self._data[self.preference["distance"]][ self._emotions[ self.preference["emotion"]][0]] else"")
            accessory = (" "+self.preference["accessory"] if self.preference["accessory"] else "")
            distance = (" "+self.preference["distance"] if self.preference["distance"] != "normal" else "")
            position = (" at "+self.preference["position"] if self.preference["position"] else "")
            return "show"+name+emotion+dress+accessory+distance+position

        def callback(self, *callback):

            # renpy.notify(str(args).replace("{", "<"))
            self.preference.update(self.change_preference(name=callback[0], value=callback[1], log=True))
            self()

        def __call__(self, trans=dissolve, *args, **kwargs):
            renpy.call("es_dev_gallery.show_displayable", displayable=esdg.timed_sprite(self.create_displayable()), name = self.name, pos_at = esdg.POSITIONS[self.preference["position"]], trans=trans)

        def remove(self):
            renpy.call("es_dev_gallery.hide_displayable", self.name)


    def esdg_get_cg():#FIXME

        cgs = {}

        for file in renpy.list_files():
            if file.startswith("images/cg/") and not "cards_contest" in file and not "d2_2ch_beach" in file:

                name = file.split("/")[-1][:-4]


                #cgs[name.split("_", 1)[1]] = (name.split("_", 1)[0], file)

                info = []#name


                file_tags = name.split("_")


                itime = file_tags[0]

                rname = name.replace(itime+"_","")

                info += [rname, itime]

                tag = itime+"_"+file_tags[1]

                if tag in ["d3_dv", "d3_un", "d3_sl", "d4_us", "d5_un", "d5_us", "d5_dv", "d6_dv", "d6_sl", "d6_un", "d7_un"]:
                    tag += "_"+file_tags[2]

                elif tag == "day4_us":
                    tag = "d4_us_morning"
                elif tag == "epilogue_mi":
                    if file_tags[2] in ["1", "9"]:
                        tag = "epilogue_mi_romantic"
                    else:
                        tag = "epilogue_mi_horror"
                elif tag == "d3_us":
                    if file_tags[2] == "library" and file_tags[3] in ["3", "4"]:
                        tag = "d4_us_morning"
                    else:
                        tag += "_"+file_tags[1]
                elif tag == "d6_us":
                    if file_tags[2] == "night":
                        tag = "d4_us_morning"
                elif tag in ["d7_dv", "d6_uv"]:
                    if len(file_tags) > 2:
                        tag += "_2"


                if not tag in cgs:
                    cgs[tag] = {}

                cgs[tag][name] = file

        return cgs



    def esdg_get_bg(): #FIXME

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


    def initialize_everlasting_summer_dev_gallery():

        global esdg

        esdg = ESDG()

        esdg.create_galleries()
