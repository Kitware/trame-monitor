from trame.widgets import vuetify, html


def create_card(**kwargs):
    with vuetify.VCard(**kwargs):
        with vuetify.VCardTitle(classes="py-2"):
            html.Span("Memory", style="position: absolute;")
            with vuetify.VProgressLinear(
                v_model=("tmr_mem_percent", 0),
                height=20,
                style="margin-left: 100px;",
            ):
                html.Div("{{ tmr_mem_percent }} %", classes="text-subtitle-2")
        vuetify.VDivider()
        with vuetify.VCardText():
            with vuetify.VRow():
                with vuetify.VCol(cols=6, classes="pa-0"):
                    with vuetify.VList():
                        # Free
                        with vuetify.VListItem():
                            with vuetify.VProgressCircular(
                                value=("100*tmr_mem_free/tmr_mem_total",),
                                size=40,
                                width=8,
                                classes="mr-4",
                                color="green",
                            ):
                                html.Div(
                                    "{{ Math.round(100 * tmr_mem_free / tmr_mem_total) }}",
                                    classes="text-subtitle-2",
                                )
                            html.Div("Free", classes="text-subtitle-2")
                            vuetify.VSpacer()
                            html.Div(
                                "{{ utils.fmt.bytes(tmr_mem_free) }}",
                                classes="text-subtitle-2",
                            )

                        # Inactive
                        with vuetify.VListItem():
                            with vuetify.VProgressCircular(
                                value=("100*tmr_mem_inactive/tmr_mem_total",),
                                size=40,
                                width=8,
                                classes="mr-4",
                                color="light-blue",
                            ):
                                html.Div(
                                    "{{ Math.round(100 * tmr_mem_inactive / tmr_mem_total) }}",
                                    classes="text-subtitle-2",
                                )
                            html.Div("Inactive", classes="text-subtitle-2")
                            vuetify.VSpacer()
                            html.Div(
                                "{{ utils.fmt.bytes(tmr_mem_inactive) }}",
                                classes="text-subtitle-2",
                            )

                        # Active
                        with vuetify.VListItem():
                            with vuetify.VProgressCircular(
                                value=("100*tmr_mem_active/tmr_mem_total",),
                                size=40,
                                width=8,
                                classes="mr-4",
                                color="orange",
                            ):
                                html.Div(
                                    "{{ Math.round(100 * tmr_mem_active / tmr_mem_total) }}",
                                    classes="text-subtitle-2",
                                )
                            html.Div("Active", classes="text-subtitle-2")
                            vuetify.VSpacer()
                            html.Div(
                                "{{ utils.fmt.bytes(tmr_mem_active) }}",
                                classes="text-subtitle-2",
                            )

                        # Wired
                        with vuetify.VListItem():
                            with vuetify.VProgressCircular(
                                value=("100*tmr_mem_wired/tmr_mem_total",),
                                size=40,
                                width=8,
                                classes="mr-4",
                                color="red",
                            ):
                                html.Div(
                                    "{{ Math.round(100 * tmr_mem_wired / tmr_mem_total) }}",
                                    classes="text-subtitle-2",
                                )
                            html.Div("Wired", classes="text-subtitle-2")
                            vuetify.VSpacer()
                            html.Div(
                                "{{ utils.fmt.bytes(tmr_mem_wired) }}",
                                classes="text-subtitle-2",
                            )
                vuetify.VDivider(vertical=True, style="z-index: 1;")
                with vuetify.VCol(cols=6, classes="pa-0"):
                    with vuetify.VList():
                        # Available
                        with vuetify.VListItem():
                            html.Div("Available", classes="text-subtitle-2")
                            vuetify.VSpacer()
                            html.Div(
                                "{{ utils.fmt.bytes(tmr_mem_available, 1) }}",
                                classes="text-subtitle-2",
                            )

                        # Used
                        with vuetify.VListItem():
                            html.Div("Used", classes="text-subtitle-2")
                            vuetify.VSpacer()
                            html.Div(
                                "{{ utils.fmt.bytes(tmr_mem_used, 1) }}",
                                classes="text-subtitle-2",
                            )

                        # Total
                        with vuetify.VListItem():
                            html.Div("Total", classes="text-subtitle-2")
                            vuetify.VSpacer()
                            html.Div(
                                "{{ utils.fmt.bytes(tmr_mem_total, 1) }}",
                                classes="text-subtitle-2",
                            )

                        # Swap
                        with vuetify.VListItem():
                            html.Div("Swap", classes="text-subtitle-2")
                            vuetify.VSpacer()
                            html.Div(
                                "{{ utils.fmt.bytes(tmr_swap_used, 0) }} / {{ utils.fmt.bytes(tmr_swap_total, 0) }}",
                                classes="text-subtitle-2",
                            )
