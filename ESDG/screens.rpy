# -*- coding: utf-8 -*-
init:

    screen esdg_delay(t=1, a=NullAction(), tag_="esdg_delay"):
        timer t action [a, Hide(tag_)]

        if "show" in tag_:
            vbox:
                text "Загрузка..."
                text "("+tag_+")"

    screen esdg_settings():

        zorder 800

        # textbutton "R" action Jump("es_dev_gallery.initialize") yalign 0.99 xalign 0.99 text_size 30

        hbox:
            spacing 4
            yalign 0.99
            xalign 0.99

            # textbutton "R" action Jump("es_dev_gallery") yalign 0.99 xalign 0.99 text_size 30 # for debug

            textbutton "Спрятать (H)":
                text_size 30
                at transform:
                    on hover:
                        linear .4 alpha 1.0
                    on idle:
                        linear .4 alpha 0.2
                action HideInterface()

            textbutton "Сцена":
                text_size 30
                at transform:
                    on hover:
                        linear .4 alpha 1.0
                    on idle:
                        linear .4 alpha 0.2
                action Show("esdg_scene_preference", dissolve_fast)


        showif esdg.settings:

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


                    frame: #TODO Not adapted
                        background Null()
                        padding (170, 80)

                        ysize 1080
                        xminimum 400


                        vbox:
                            yalign .0
                            xalign .0
                            spacing 20

                            vbox:
                                first_spacing 6
                                xalign .5
                                text "Время суток для спрайтов" style "settings_text" size 40
                                hbox:
                                    spacing 20
                                    hbox:
                                        spacing 6
                                        if persistent.sprite_time == "day":
                                            add get_image("gui/settings/leaf.png") ypos 0.12
                                        else:
                                            add Null(width=22, height=29) ypos 0.12
                                        textbutton "День" style "log_button" text_style "settings_text" text_size 30 action esdg.day_time

                                    hbox:
                                        spacing 6
                                        if persistent.sprite_time == "sunset":
                                            add get_image("gui/settings/leaf.png") ypos 0.12
                                        else:
                                            add Null(width=22, height=29) ypos 0.12
                                        textbutton "Закат" style "log_button" text_style "settings_text"  text_size 30 action esdg.sunset_time

                                    hbox:
                                        spacing 6
                                        if persistent.sprite_time == "night":
                                            add get_image("gui/settings/leaf.png") ypos 0.12
                                        else:
                                            add Null(width=22, height=29) ypos 0.12
                                        textbutton "Ночь" style "log_button" text_style "settings_text" text_size 30  action esdg.night_time

                            if esdg.bg:
                                vbox:
                                    first_spacing 6
                                    text "Фон" style "settings_text" size 40

                                    textbutton esdg.translate(esdg.bg.name) style "log_button" text_style "settings_text" text_size 30 xpos .1 action Function(esdg.select_element, esdg.bg)

                            if esdg.sprites:
                                vbox:
                                    first_spacing 6
                                    spacing -10

                                    text "Спрайты" style "settings_text" size 35


                                    for i, sprite in enumerate(esdg.sprites):
                                        add get_image("gui/settings/bar_null.png") xzoom 1.6 xalign .5 yoffset -15

                                        textbutton esdg.translate(sprite.name) style "log_button" text_style "settings_text" text_size 30 xpos .1 action Function(esdg.select_element, sprite)
                                        hbox:
                                            xalign 1.0
                                            yoffset -30
                                            at transform:
                                                zoom .6
                                            imagebutton:
                                                idle "images/misc/up.png"
                                                action Function(esdg.move_element, i, "up")

                                            imagebutton:
                                                idle "images/misc/down.png"
                                                action Function(esdg.move_element, i, "down")


                                        # hbox:
                                        #     text str(i)
                                        #     textbutton esdg.translate(sprite.name) style "log_button" text_style "settings_text" text_size 30 xpos .1 action Function(esdg.select_element, sprite)
                                        #
                                        #     imagebutton:
                                        #         idle "images/misc/up.png"
                                        #         action Function(esdg.move_element, i, "up")
                                        #
                                        #     imagebutton:
                                        #         idle "images/misc/down.png"
                                        #         action Function(esdg.move_element, i, "down")


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


    screen esdg_element_viewer():

        zorder 790

        style_prefix "esdg_element_viewer"


        showif esdg.element_viewer.state:
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

                    action esdg.deselect_element

                frame:


                    add get_image("gui/settings/history_bg.jpg"):

                        crop esdg.element_viewer_bg_crop
                        zoom .75

                        rotate 90
                        rotate_pad False



                    hbox:
                        xpos .01
                        ypos .05
                        viewport id "element_settings":

                            mousewheel True
                            pagekeys True


                            scrollbars None
                            if renpy.mobile:
                                draggable True


                            area esdg.element_viewer_viewport_area




                            vbox:
                                spacing 20


                                xfill True



                                if isinstance(esdg.element_viewer, EsdgElement):


                                    hbox:


                                        spacing 10
                                        xpos .05

                                        # frame:
                                        #     xsize esdg.x_preview_size ysize esdg.y_preview_size
                                        #
                                        #
                                        #     add Solid("#6d4e39F0", xysize=esdg.preview_size):
                                        #         anchor (.5, .5)
                                        #         xalign .5
                                        #         yalign .5
                                        #
                                        #     if esdg.element_viewer.collection != "bg":
                                        #         add esdg.elements_background align (.5, .5)
                                        #
                                        #     add esdg.element_viewer.preview  align (.5, 1.0)
                                        #
                                        #
                                        frame:
                                            xysize esdg.preview_size
                                            background Solid("#6d4e39F0")
                                            frame:
                                                background None
                                                xalign .5 yalign .5
                                                xsize esdg.x_preview_size ysize esdg.y_preview_size
                                                if esdg.element_viewer.collection != "bg":
                                                    add esdg.elements_background align (.5, .5)

                                                add esdg.element_viewer.preview:
                                                    zoom .166
                                                    align (.5, 1.0)
                                        #
                                        # frame:
                                        #     xysize esdg.preview_size
                                        #     background Solid("#6d4e39F0")
                                        #     frame:
                                        #         xalign .5 yalign .5
                                        #         xsize esdg.x_preview_size ysize esdg.y_preview_size
                                        #         background esdg.elements_background # Solid("#48C")
                                        #
                                        #         add esdg.element_viewer.preview

                                        vbox:
                                            spacing 10
                                            first_spacing 20
                                            xsize 200

                                            text esdg.translate(esdg.element_viewer.name) size 40 bold True xalign .5


                                            text "Тип: " + esdg.element_viewer.collection
                                            for info in esdg.element_viewer.extra:

                                                text info+": " + esdg.element_viewer.extra[info]

                                    textbutton "Копировать код" style "log_button" text_style "settings_text" action CopyCode(esdg.element_viewer.code) xpos .05 yalign .5

                                    for button_ in esdg.element_viewer.actions:
                                        textbutton button_ style "log_button" text_style "settings_text" action esdg.element_viewer.actions[button_] xpos .05 yalign .5



                                    vbox:

                                        spacing 10

                                        xpos .05

                                        $ settings = esdg.element_viewer.get_settings()

                                        for setting in settings["image"]:

                                            $ setting_data = settings["image"][setting]

                                            add get_image("gui/settings/bar_null.png") xzoom 1.9 yzoom 1.3 xpos .02

                                            text esdg.translate(setting) style "esdg_element_viewer_text"

                                            hbox:


                                                box_wrap True
                                                xpos .07

                                                spacing 4
                                                box_wrap_spacing 4



                                                for button_ in setting_data:

                                                    frame:
                                                        xsize esdg.x_preview_size ysize esdg.y_preview_size

                                                        at transform:
                                                            zoom .75

                                                        add Solid("#6d4e39D0", xysize=esdg.preview_size) align (.5, .5)

                                                        if esdg.element_viewer.collection != "bg":
                                                            add esdg.elements_background align (.5, .5)

                                                        if button_[0]:
                                                            add button_[1]:
                                                                zoom .166
                                                                xalign .5
                                                                yalign 1.0
                                                        else:
                                                            add Text("X", color="F00", bold=True, size=esdg.y_size):
                                                                zoom .166
                                                                xalign .5
                                                                yalign .5
                                                        imagebutton:
                                                            align (.5, .5)
                                                            idle get_image("gui/gallery/blank.png")
                                                            hover Solid("#FFF3")
                                                            action Function(esdg.element_viewer.callback, setting, button_[0])

                                                    # frame:
                                                    #
                                                    #     xysize esdg.preview_size
                                                    #     background Solid("#6d4e39D0")
                                                    #     at transform:
                                                    #         zoom .75
                                                    #
                                                    #     # frame:
                                                    #     #     xalign .5 yalign .5
                                                    #     #     background esdg.elements_background
                                                    #     #
                                                    #     #     add button_[1] xalign .5 yalign 1.0
                                                    #     #
                                                    #     # imagebutton:
                                                    #     #     align (.5, .5)
                                                    #     #     idle get_image("gui/gallery/blank.png")
                                                    #     #     hover_foreground Solid("#FFF3")
                                                    #
                                                    #
                                                    #     imagebutton:
                                                    #         xalign .5 yalign .5
                                                    #         xsize esdg.x_preview_size ysize esdg.y_preview_size
                                                    #         background esdg.elements_background
                                                    #         idle button_[1]
                                                    #         hover_foreground Solid("#AAA5")
                                                    #         action Function(esdg.element_viewer.callback, setting, button_[0])

                                        for setting in settings["text"]:

                                            $ setting_data = settings["text"][setting]

                                            add get_image("gui/settings/bar_null.png") xzoom 1.9 yzoom 1.3 xpos .02

                                            text esdg.translate(setting) style "esdg_element_viewer_text"

                                            hbox:


                                                box_wrap True
                                                xpos .01

                                                xmaximum int(esdg.element_viewer_viewport_area[2]*.8)

                                                spacing 4
                                                box_wrap_spacing 4

                                                for button_ in setting_data:
                                                    hbox:
                                                        spacing 3
                                                        if esdg.element_viewer.preference[setting] == button_:
                                                            add get_image("gui/settings/leaf.png") ypos 0.12
                                                        else:
                                                            add Null(width=22, height=29) ypos 0.12

                                                        textbutton (esdg.translate(button_) or "X") style "log_button" text_style "settings_text" text_size 38 action Function(esdg.element_viewer.callback, setting, button_)



                        vbar value YScrollValue("element_settings"):

                            style "esdg_element_viewer_vbar"


                            bar_invert True

                            yalign .5

                            ymaximum esdg.element_viewer_viewport_area[3]

                            bottom_bar "images/misc/none.png"
                            top_bar "images/misc/none.png"
                            thumb "images/gui/settings/vthumb.png"

    style esdg_element_viewer_text is text:

        color "#4d2e19"
        size 34

    style esdg_element_viewer_frame is default:

        xmaximum 668
        ymaximum 1041

        background Null()

    style esdg_element_viewer_frame:

        variant "mobile"

        xmaximum 445
        ymaximum 694

        background Null()


    style esdg_element_viewer_vbar:

        # thumb_offset -92
        xoffset -40

    style esdg_element_viewer_vbar:

        variant "mobile"

        # thumb_offset -92
        xoffset -27

    screen esdg_gallery():

        zorder 900

        style_prefix "esdg_gallery"

        showif esdg.gallery.state:
            imagebutton: # Блокировка остальных окон
                idle Solid("0004")
                at transform:
                    on show:
                        alpha 0
                        ease .5 alpha 1.0
                    on hide:
                        ease .5 alpha 0.0

                action NullAction()

            frame:

                at transform:
                    align (.5, 1.0)
                    on show:
                        yalign 8.0
                        ease .5 yalign 1.0
                    on hide:
                        ease .5 yalign 8.0



                imagebutton:
                    auto "images/gui/dialogue_box/day/backward_%s.png"

                    xalign .99 yalign .01

                    action esdg.hide_gallery

                if esdg.gallery.__class__ == EsdgGallery:

                    text esdg.translate(esdg.gallery.name) xalign .5 yalign .07 style "settings_text" size 70

                    hbox:

                        style "esdg_gallery_gallerylist"


                        for i in esdg.gallery.page():

                            frame:
                                style "default"
                                xsize esdg.x_preview_size ysize esdg.y_preview_size

                                add Solid("#6d4e39D0", xysize=esdg.preview_size) align (.5, .5)

                                if i.collection != "bg":
                                    add esdg.elements_background align (.5, .5)
                                add i.preview:
                                    zoom .166
                                    xalign .5
                                    yalign 1.0

                                imagebutton:
                                    align (.5, .5)
                                    idle get_image("gui/gallery/blank.png")
                                    hover Solid("#FFF3")
                                    action Function(esdg.add_element, i)

                            # frame:
                            #
                            #     xysize esdg.preview_size
                            #     background Solid("#6d4e39D0")
                            #     imagebutton:
                            #         xalign .5 yalign .5
                            #         xsize esdg.x_preview_size ysize esdg.y_preview_size
                            #         background esdg.elements_background # Solid("#48C")
                            #         idle i.preview
                            #         hover_foreground Solid("#AAA5")
                            #         action Function(esdg.add_element, i)

                    hbox:

                        yalign .92
                        xalign .5

                        textbutton "<" style "log_button" text_size 50 action esdg.gallery.back_page
                        text "Страница №"+str(esdg.gallery._page+1)+"/"+str(esdg.gallery.page_maximum+1) style "settings_text" size 50
                        textbutton ">" style "log_button" text_size 50 action esdg.gallery.next_page




        hbox:
            xalign 0.5
            yalign 1.0

            # textbutton "N" action Function(esdg.show_gallery, esdg.galleries["Number"])

            # textbutton "bg":
            #     at transform:
            #         on hover:
            #             linear .4 alpha 1.0
            #         on idle:
            #             linear .4 alpha 0.7
            #     action Function(esdg.show_gallery, esdg.galleries["bg"])
            # textbutton "sprites":
            #     at transform:
            #         on hover:
            #             linear .4 alpha 1.0
            #         on idle:
            #             linear .4 alpha 0.7
            #     action Function(esdg.show_gallery, esdg.galleries["sprites"])
            # textbutton "cg":
            #     at transform:
            #         on hover:
            #             linear .4 alpha 1.0
            #         on idle:
            #             linear .4 alpha 0.7
            #     action Function(esdg.show_gallery, esdg.galleries["cg"])

            for gallery in esdg.galleries:
                textbutton gallery action Function(esdg.show_gallery, esdg.galleries[gallery]) at esdg_gallery_textbutton_transform

    transform esdg_gallery_textbutton_transform:
        on hover:
            linear .4 alpha 1.0
        on idle:
            linear .4 alpha 0.7

    style esdg_gallery_frame is default:

        xsize 1388 # .723
        ysize 890 # .824


        background Crop((370, 110, 1388, 890), get_image("gui/settings/history_bg.jpg"))

    style esdg_gallery_frame:
        variant "small"
        xsize 925
        ysize 593

        background Crop((246, 110, 925, 593), get_image("gui/settings/history_bg.jpg"))


    style esdg_gallery_button is button

    style esdg_gallery_button_text is settings_text:
        size 36

    style esdg_gallery_gallerylist is default:

        xpos .05
        ypos .15


        spacing 36 #20

        box_wrap True
        box_wrap_spacing 26 #10

    style esdg_gallery_gallerylist:

        variant "mobile"

        xpos .05
        ypos .15

        spacing 27#11

        box_wrap True
        box_wrap_spacing 22#6


    screen esdg_scene_preference():

        zorder 999

        imagebutton: # Блокировка остальных окон
            idle Solid("0002")
            at transform:
                on show:
                    alpha 0
                    ease .5 alpha 1.0
                on hide:
                    ease .5 alpha 0.0
            action Hide("esdg_scene_preference", dissolve_fast)

        frame:
            background Solid("#ebe3b8")

            xysize (.7, .7)

            align (.5, .5)

            add Solid("#1e1f21", xysize=(.4, .6)) align (.01, .05)

            $ code = esdg.code_all()

            viewport:
                align (.01, .05)
                xysize (.4, .6)
                scrollbars True

                text esdg.color_code(code)# align (.5, .5)

            vbox:
                align (.57, .3)
                spacing 20
                textbutton "Копировать в буфер обмена" style "log_button"  text_style "settings_text"  action CopyCode(code) text_size 30
                textbutton "Открыть в текстовом файле" style "log_button"  text_style "settings_text"  action OpenFileCode(code) text_size 30
                textbutton "{color=#a56870}Обнулить сцену{/color}" style "log_button"  action Jump("es_dev_gallery.initialize") text_size 30

                null
                null

                textbutton "{color=#39f}Написать отзыв =){/color}" style "log_button"  action OpenURL("https://vk.com/topic-203508980_47492565") text_size 30
