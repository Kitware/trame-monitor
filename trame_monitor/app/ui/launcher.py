from trame.widgets import vuetify, html


def create_card(server, **kwargs):
    with vuetify.VCard(**kwargs):
        with vuetify.VCardTitle(classes="py-2"):
            html.Span("Processes ({{ processes_available }})")
            vuetify.VSpacer()

            with vuetify.VBtn(
                icon=True,
                click=server.controller.launcher_clear,
            ):
                vuetify.VIcon("mdi-autorenew")

            with vuetify.VMenu(offset_y=True):
                with vuetify.Template(v_slot_activator="{ on, attrs}"):
                    with vuetify.VBtn(
                        icon=True,
                        v_show="processes_available > 0",
                        v_bind="attrs",
                        v_on="on",
                    ):
                        vuetify.VIcon("mdi-plus")
                with vuetify.VList():
                    with vuetify.VListItem(
                        v_for="(name, idx) in apps",
                        key="name",
                        click=(server.controller.launcher_start, "[name]"),
                    ):
                        vuetify.VListItemTitle("{{ name }}")

        vuetify.VDivider()
        with vuetify.VCardText(classes="py-1"):
            with vuetify.VList(dense=True):
                with vuetify.VListItem(v_for="p, i in processes", key="i"):
                    with vuetify.VRow():
                        html.Div(
                            "{{ get(p).name }}",
                            classes="text-subtitle-2 py-1 text-capitalize",
                        )
                        vuetify.VSpacer()
                        html.Div(
                            "{{ get(p).status }}",
                            v_if="get(p).status !== 'ready'",
                            classes="text-subtitle-2 py-1 text-capitalize",
                        )
                        with vuetify.VBtn(
                            v_if="get(p).status === 'ready'",
                            icon=True,
                            small=True,
                            click="open(`http://localhost:${get(p).port}/`, '_blank')",
                        ):
                            vuetify.VIcon("mdi-open-in-new")
