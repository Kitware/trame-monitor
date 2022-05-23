from trame.widgets import vuetify, html


def create_card(server, **kwargs):
    with vuetify.VCard(**kwargs):
        with vuetify.VCardTitle(classes="py-2"):
            html.Span("Processes")
            vuetify.VSpacer()
            with vuetify.VBtn(
                icon=True,
                click=(server.controller.launcher_start, "['trame_app.app.main']"),
            ):
                vuetify.VIcon("mdi-plus")
        vuetify.VDivider()
        with vuetify.VCardText(classes="py-1"):
            with vuetify.VList(dense=True):
                with vuetify.VListItem(v_for="p, i in processes", key="i"):
                    with vuetify.VRow():
                        html.Div(
                            "{{ get(p).status }}",
                            classes="text-subtitle-2 py-1 text-capitalize",
                        )
                        vuetify.VSpacer()
                        with vuetify.VBtn(
                            v_if="get(p).status === 'ready'",
                            icon=True,
                            small=True,
                            click="open(`http://localhost:${get(p).port}/`, '_blank')",
                        ):
                            vuetify.VIcon("mdi-open-in-new")
