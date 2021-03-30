# -*- coding: utf-8 -*-
init:

    transform esdg_focus_sprite(x=900, k=1.0, h=.2):



        zoom float(k)
        #crop (0, (y-y*(1/k))*yk, x, y*(1/k))
        crop (0, esdg.y_size*h*k, esdg.x_size, esdg.y_size)

        xalign .5
        yalign 1.0

    transform esdg_transform(xalign=.5, # Заготовка для будующего окна
                             yalign=1.0):
        xalign xalign
        yalign yalign



    # default esdg = ESDG() # persistent

    # default esdg_collections = None # persistent

    image mikan_ds_intro:
        Text("Mikan-DS", size=190, slow_cps = 6)
        pause 1.9
        block:
            Text("Mikan-DS_", size=190)
            pause .5
            Text("Mikan-DS", size=190)
            pause .5
            repeat


label es_dev_gallery: # индекс

    jump .initialize пропускать заставку

    scene bg black

    show image Text(">>", size=190, color="#FC9") as code_mikan:
        xpos .14
        yalign .5
    show image Text("1.21.3.29", size=10) as mode_version:
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



    pause 2


    jump .initialize



label .initialize:

    $ initialize_everlasting_summer_dev_gallery()
    # pause #TODO

    jump .restart

label .restart:

    $ esdg.init()

    scene stars

    show screen esdg_settings

    show screen esdg_gallery

    show screen esdg_element_viewer

    with pixellate

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

label .massive_sprites:

    python:
        for sprite in reversed(esdg.sprites):
            renpy.hide(sprite.name)
            renpy.show(sprite.name, what=esdg.timed_sprite(sprite.create_displayable()), at_list=[esdg.POSITIONS[sprite.preference["position"]]])
    with dspr

    return
