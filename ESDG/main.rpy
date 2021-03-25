# -*- coding: utf-8 -*-
init:

    transform esdg_focus_sprite(k=1.0, x=1920, y=1080, yk=.2):

        zoom float(k)


        crop (0, (y-y*(1/k))*yk, x, y*(1/k))


    default esdg = ESDG()

    default esdg.selected_element = [None, None]
    default esdg.elements_background = Null()#"images/gui/gallery/not_opened_idle.png"

    default esdg_collections = None

    image mikan_ds_intro:
        # Text(">>", size=190)
        # pause .8
        Text("Mikan-DS", size=190, slow_cps = 6)
        pause 1.9
        block:
            Text("Mikan-DS_", size=190)
            pause .5
            Text("Mikan-DS", size=190)
            pause .5
            repeat


label es_dev_gallery: # индекс

    # show image Text("{size=70}RedHead Team представляет{/size}", slow_cps = 25) at truecenter

    jump .indev

    scene bg black

    show image Text(">>", size=190, color="#FC9") as code_mikan:
        xpos .14
        yalign .5
    show image Text("1.21.3.24", size=10) as mode_version:
        xalign 1.0
        yalign 1.0
    with dissolve
    pause .1
    play sound sfx_keyboard_mouse
    show mikan_ds_intro as mikan:
        xpos .3
        yalign .5

    pause 2
    stop sound

    pause 3

    hide code_mikan
    hide mikan
    hide mode_version
    with fade2

    $ prepare_everlasting_summer_dev_gallery()

    pause 2


    #jump es_dev_gallery

    jump .initialize

label .indev:

    $ prepare_everlasting_summer_dev_gallery()
    jump .initialize


label .initialize:

    $ initialize_everlasting_summer_dev_gallery()

    scene stars

    show screen esdg_settings

    show screen esdg_gallery

    show screen esdg_element_viewer

    with pixellate

    # pause #TODO

    jump .cycle

label .cycle: # цикл галлереи

    $ renpy.block_rollback()

    pause

    jump .cycle

label .show_displayable(displayable=Null(), name = "sprite", pos_at = center, trans=dissolve):

    $ renpy.show(name, what=displayable, at_list=[pos_at])
    with trans

    return

label .hide_displayable(name="sprite"):

    #hide expression name
    $ renpy.hide(name)
    with dissolve

    return

label .show_scene(bg="black"):

    scene expression bg
    # with dspr

    $ esdg.refresh_sprites()

    return

label .massive_sprites(sprites):

    python:
        for sprite in sprites:
            renpy.show(sprite.name, what=sprite.create_diplayable(sprite.preference), at_list=[esdg.POSITIONS[sprite.preference["position"]]])
    with dspr

    return
