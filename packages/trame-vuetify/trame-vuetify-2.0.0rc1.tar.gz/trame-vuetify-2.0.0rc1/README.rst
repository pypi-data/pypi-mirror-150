trame-vuetify
===========================================================================

Trame-vuetify extend trame **widgets** and **ui** with all the beautiful Vuetify UI components.
Vuetify is a UI Library with beautifully handcrafted Material Components. No design skills required — everything you need to create amazing applications is at your fingertips.

This package is under the same MIT License as the `Vuetify <https://github.com/vuetifyjs/vuetify/blob/master/LICENSE.md>`_ library that it expose for its usage in trame.

`The original Vuetify components documentation <https://vuetifyjs.com/en/>`_ provide a great resource for interactive visualization of those widgets.


How to use it?
-----------------------------------------------------------

trame wraps Vuetify as it's primary UI Component Library. The `Vuetify website <https://vuetifyjs.com/en/>`_ is very well made for exploring components and understanding components' parameters and controls, while a reference to our wrapper API is available `here <https://trame-vuetify.readthedocs.io/en/latest/trame.html.vuetify.html>`_.
The way trame translate Vue templates into plain Python code is by doing the following.


Material Components
```````````````````````````````````````````````````````````

First you need to import the `vuetify` module so you can instantiate the various Material Components like illustrated below. Moreover, in the documentation the component names use dashes as separators while in Python we use the Camelcase notation for the class name.

.. code-block:: python

    from trame.widgets import vuetify

    # <v-btn>Hello World</v-btn>
    btn = vuetify.VBtn("Hello World")

Boolean attributes
```````````````````````````````````````````````````````````

Implicit attribute values must be made explicit in Python by assigning `True` to them.

.. code-block:: python

    # <v-text-field disabled />
    vuetify.VTextField(disabled=True)


Dash and colon separators
```````````````````````````````````````````````````````````

Any special characters (`-` and `:`) become `_` in Python.

.. code-block:: python

    # <v-text-field v-model="myText" />
    vuetify.VTextField(v_model=("myText",))


Events
```````````````````````````````````````````````````````````

Events in vue are prefixed with a `@` but in Python we declare them the same way we declare regular attributes.

.. code-block:: python

    def runMethod():
        pass

    # <v-btn @click="runMethod" />
    vuetify.VBtn(click=runMethod)


Trame Community
-----------------------------------------------------------

* `WebSite <https://kitware.github.io/trame/>`_
* `Discussions <https://github.com/Kitware/trame/discussions>`_
* `Issues <https://github.com/Kitware/trame/issues>`_
* `RoadMap <https://github.com/Kitware/trame/projects/1>`_
* `Contact Us <https://www.kitware.com/contact-us/>`_
* .. image:: https://zenodo.org/badge/410108340.svg
    :target: https://zenodo.org/badge/latestdoi/410108340
