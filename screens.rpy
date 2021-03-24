# -*- coding: utf-8 -*-
init offset = 998
init:

    screen esdg_delay(t=1, a=NullAction(), tag_="esdg_delay"):
        timer t action [a, Hide(tag_)]
        vbox:
            text "Загрузка..."
            text "("+tag_+")"

    screen esdg_settings:

        zorder 800

        showif esdg.settings_state:

            hbox:
                at transform:
                    yalign 0.5
                    xalign 0.0
                    xoffset -70
                    on show:
                        xalign -1.0
                        ease .5 xalign 0.0
                    on hide:
                        ease .5 xalign -1.0

                frame:

                    background Frame(get_image("gui/ingame_menu/"+persistent.sprite_time+"/ingame_menu.png"), 125, 140)

                    frame:
                        background Null()
                        padding (170, 80)

                        ysize 1080
                        xminimum 400


                        vbox:
                            yalign .0
                            xalign .0
                            first_spacing 30
                            spacing 20

                            text "Настройки вида" style "settings_text" size 50 xalign .5

                            vbox:
                                first_spacing 6
                                text "Время суток для спрайтов" style "settings_text" size 40
                                hbox:
                                    spacing 20
                                    hbox:
                                        spacing 6
                                        if persistent.sprite_time == "day":
                                            add get_image("gui/settings/leaf.png") ypos 0.12
                                        else:
                                            add Null(width=22, height=29) ypos 0.12
                                        textbutton "День" style "log_button" text_style "settings_text"  action esdg.day_time

                                    hbox:
                                        spacing 6
                                        if persistent.sprite_time == "sunset":
                                            add get_image("gui/settings/leaf.png") ypos 0.12
                                        else:
                                            add Null(width=22, height=29) ypos 0.12
                                        textbutton "Закат" style "log_button" text_style "settings_text"  action esdg.sunset_time

                                    hbox:
                                        spacing 6
                                        if persistent.sprite_time == "night":
                                            add get_image("gui/settings/leaf.png") ypos 0.12
                                        else:
                                            add Null(width=22, height=29) ypos 0.12
                                        textbutton "Ночь" style "log_button" text_style "settings_text"  action esdg.night_time


                            if esdg.bg:
                                vbox:
                                    first_spacing 6
                                    text "Фон" style "settings_text" size 40

                                    textbutton esdg.translate(esdg.bg.name) style "log_button" text_style "settings_text" text_size 30 xpos .1 action Function(esdg.show_element, esdg.bg)

                            if esdg.sprites:
                                vbox:
                                    first_spacing 6
                                    spacing 16
                                    text "Спрайты" style "settings_text" size 40

                                    for sprite in esdg.sprites:
                                        textbutton esdg.translate(sprite) style "log_button" text_style "settings_text" text_size 30 xpos .1 action Function(esdg.show_element, esdg.sprites[sprite])



                imagebutton:
                    auto "images/gui/dialogue_box/day/backward_%s.png"

                    yalign 0.5
                    xoffset -100

                    action esdg.hide_settings



        else:

            imagebutton:
                auto "images/gui/dialogue_box/day/forward_%s.png"

                at transform:

                    xalign 0.0
                    yalign 0.5

                    on show:
                        alpha 0
                        pause .4
                        alpha 1


                action esdg.show_settings

        textbutton "R" action Jump("es_dev_gallery.initialize") yalign 0.99 xalign 0.99 text_size 30




    screen esdg_element_viewer:

        zorder 790

        showif esdg.selected_element[0]:

            hbox:

                at transform:
                    yalign 0.5
                    xalign 1.0
                    on show:
                        xalign 2.0
                        ease .5 xalign 1.0
                    on hide:
                        ease .5 xalign 2.0
                imagebutton:
                    auto "images/gui/dialogue_box/day/forward_%s.png"

                    yalign 0.5

                    action esdg.hide_element

                frame:
                    xmaximum 668
                    ymaximum 1041

                    background Null()

                    add get_image("gui/settings/history_bg.jpg"):
                        crop (370, 110, 1388, 890)
                        zoom .75

                        rotate 90
                        rotate_pad False

                    if esdg.selected_element[1]:
                        vbox:

                            spacing 20
                            first_spacing 40


                            ypos .03

                            add Null(height=1, width=668)

                            hbox:

                                xpos .05
                                spacing 10

                                frame:
                                    xsize 336
                                    ysize 196
                                    background esdg.elements_background

                                    if esdg.elements_background_2 and not esdg.selected_element[1].collection in ["bg", "cg"]:
                                        add esdg.elements_background_2 align (.5, .5)

                                    add esdg.selected_element[1].preview:
                                        zoom .166
                                        xalign .5
                                        yalign 1.0

                                vbox:
                                    spacing 10
                                    first_spacing 20
                                    xsize 200

                                    text esdg.translate(esdg.selected_element[1].name)  style "settings_text" size 40 bold True xalign .5


                                    text "Тип: " + esdg.selected_element[1].collection  style "settings_text" size 34
                                    for info in esdg.selected_element[1].extra:

                                        text info+": " + esdg.selected_element[1].extra[info]  style "settings_text" size 34

                            hbox:

                                xpos .05


                                viewport id "element_settings":
                                    mousewheel True

                                    area (0, 0, 640, 580) # 540, 530


                                    # add Solid("AAA", ysize=3000)

                                    vbox:

                                        spacing 20

                                        # frame:
                                        #     background Solid("AAA") #"1A1A77"

                                        # hbox:
                                        #     spacing 4
                                        #
                                        #     text "{font=fonts/corbelb.ttf}{color=#1A1A77}"+esdg.selected_element[1].code+"{/color}{/font}" yalign .5
                                        #
                                        #     text " | " yalign .5

                                        textbutton "Копировать код" style "log_button" text_style "settings_text" action CopyCode(esdg.selected_element[1].code) yalign .5

                                        for button_ in esdg.selected_element[1].actions:
                                            textbutton button_ style "log_button" text_style "settings_text" action esdg.selected_element[1].actions[button_] yalign .5

                                        $ settings = esdg.selected_element[1].get_settings()

                                        $ image_settings = settings["image"]

                                        for setting in image_settings:

                                            $ setting_data = image_settings[setting]

                                            vbox:
                                                spacing 3

                                                add get_image("gui/settings/bar_null.png") xzoom 1.67 xpos .07

                                                text esdg.translate(setting) style "settings_text" size 37 bold True xalign .1

                                                frame:
                                                    area (0, 0, 696, 196)
                                                    background Null()

                                                    at transform:
                                                        zoom .8
                                                    viewport id setting:
                                                        mousewheel "horizontal"

                                                        hbox:
                                                            spacing 5

                                                            for button_ in setting_data:
                                                                frame:
                                                                    xsize 336
                                                                    ysize 196
                                                                    background esdg.elements_background

                                                                    if esdg.elements_background_2 and not esdg.selected_element[1].collection in ["bg", "cg"]:
                                                                        add esdg.elements_background_2 align (.5, .5)

                                                                    if button_[0]:
                                                                        add button_[1]:
                                                                            zoom .166
                                                                            xalign .5
                                                                            yalign 1.0
                                                                    else:
                                                                        add Text("X", color="F00", bold=True, size=800):
                                                                            zoom .166
                                                                            xalign .5
                                                                            yalign .5

                                                                    if esdg.selected_element[1].preference[setting] == button_[0]:
                                                                        add Solid("#4C4", xsize=30, ysize=196) yalign .5
                                                                    else:
                                                                        add Null(width=30, height=196) yalign .5

                                                                        imagebutton:
                                                                            align (.5, .5)
                                                                            idle get_image("gui/gallery/blank.png")
                                                                            hover Solid("#FFF3", xsize=320, ysize=180)

                                                                            action Function(esdg.selected_element[1].callback, setting, button_[0])


                                                bar value XScrollValue(setting) ysize 36 xmaximum 556 left_bar "images/misc/none.png" right_bar "images/misc/none.png" thumb "images/gui/settings/htumb.png"

                                        $ text_settings = settings["text"]

                                        for setting in text_settings:

                                            $ setting_data = text_settings[setting]
                                            vbox:
                                                spacing 3

                                                add get_image("gui/settings/bar_null.png") xzoom 1.67 xpos .07

                                                text esdg.translate(setting) style "settings_text" size 37 bold True xalign .1

                                                for i in range(len(setting_data)//3):
                                                    hbox:
                                                        spacing 4
                                                        xalign .5
                                                        for k in range(3):
                                                            $ button_ = setting_data[i*3+k]
                                                            hbox:
                                                                spacing 6
                                                                if esdg.selected_element[1].preference[setting] == button_:
                                                                    add get_image("gui/settings/leaf.png") ypos 0.12
                                                                else:
                                                                    add Null(width=22, height=29) ypos 0.12

                                                                textbutton (esdg.translate(button_) or "X") style "log_button" text_style "settings_text" text_size 38 action Function(esdg.selected_element[1].callback, setting, button_)
                                                if len(setting_data)%3:
                                                    $ i += 1
                                                    hbox:
                                                        spacing 4
                                                        xalign .5
                                                        for k in range(len(setting_data)%3):
                                                            $ button_ = setting_data[i*3+k]
                                                            hbox:
                                                                spacing 6
                                                                if esdg.selected_element[1].preference[setting] == button_:
                                                                    add get_image("gui/settings/leaf.png") ypos 0.12
                                                                else:
                                                                    add Null(width=22, height=29) ypos 0.12

                                                                textbutton (esdg.translate(button_) or "X") style "log_button" text_style "settings_text" text_size 38 action Function(esdg.selected_element[1].callback, setting, button_)


                                add get_image("gui/settings/vbar_null.png") yzoom 1.9 xoffset -80

                                vbar value YScrollValue("element_settings") ymaximum 430 yalign .5 bottom_bar "images/misc/none.png" top_bar "images/misc/none.png" thumb "images/gui/settings/vthumb.png" thumb_offset -92 xoffset -60


    screen esdg_gallery:

        zorder 900



        showif esdg.gallery_state:

            imagebutton:
                idle Solid("0004")
                at transform:
                    on show:
                        alpha 0
                        ease .5 alpha 1.0
                    on hide:
                        ease .5 alpha 0.0

                action NullAction()


            frame:

                xmaximum 1388
                ymaximum 890

                at transform:

                    align (.5, 1.0)

                    on show:
                        yalign 8.0
                        ease .5 yalign 1.0
                    on hide:
                        ease .5 yalign 8.0


                background Crop((370, 110, 1388, 890), get_image("gui/settings/history_bg.jpg"))

                if esdg.gallery_collection:
                    $ gallery_data = esdg_collections[esdg.gallery_collection]
                    $ gallery_tags = list(gallery_data)

                    text esdg.gallery_collection style "settings_text" size 45 bold True xalign .5 yalign .0
                    frame:
                        background Null()

                    imagebutton:
                        auto "images/gui/dialogue_box/day/backward_%s.png"

                        xalign .99 yalign .01

                        action esdg.hide_gallery

                    hbox:
                        xpos .05
                        ypos .05

                        viewport id "gallery":
                            mousewheel True

                            area (0, 0, 1050, 790)

                            #add Solid("AAA", ysize=5000)
                            vbox:
                                spacing 20

                                for i in range(len(gallery_tags)//3):
                                    hbox:
                                        spacing 5
                                        for k in range(3):
                                            $ button_ = gallery_data[gallery_tags[i*3+k]]
                                            frame:
                                                xsize 336
                                                ysize 196
                                                background esdg.elements_background

                                                if esdg.elements_background_2 and not esdg.gallery_collection in ["bg", "cg"]:
                                                    add esdg.elements_background_2 align (.5, .5)

                                                add button_.preview:
                                                    zoom .166
                                                    xalign .5
                                                    yalign 1.0

                                                imagebutton:
                                                    align (.5, .5)
                                                    idle get_image("gui/gallery/blank.png")
                                                    hover Solid("#FFF3", xsize=320, ysize=180)

                                                    action Function(esdg.add_element, button_)

                                $ i += 1
                                for k in range(len(gallery_tags)%3):
                                    $ button_ = gallery_data[gallery_tags[i*3+k]]
                                    frame:
                                        xsize 336
                                        ysize 196
                                        background esdg.elements_background

                                        if esdg.elements_background_2 and not esdg.gallery_collection in ["bg", "cg"]:
                                            add esdg.elements_background_2 align (.5, .5)

                                        add button_.preview:
                                            zoom .166
                                            xalign .5
                                            yalign 1.0

                                        imagebutton:
                                            align (.5, .5)
                                            idle get_image("gui/gallery/blank.png")
                                            hover Solid("#FFF3", xsize=320, ysize=180)

                                            action Function(esdg.add_element, button_)

                        vbar value YScrollValue("gallery") yalign .5 ymaximum 790 bottom_bar "images/misc/none.png" top_bar "images/misc/none.png" thumb "images/gui/settings/vthumb.png" thumb_offset -12

        hbox:
            xalign 0.5
            yalign 1.0

            textbutton "bg" text_size 36 action Function(esdg.show_gallery, "bg")
            textbutton "sprites" text_size 36 action Function(esdg.show_gallery, "sprites")
            # textbutton "cg" text_size 36 action Function(esdg.show_gallery, "cg")
