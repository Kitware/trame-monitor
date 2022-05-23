from trame.widgets import vuetify, html


def create_card(**kwargs):
    with vuetify.VCard(**kwargs):
        with vuetify.VCardTitle(classes="py-2"):
            html.Span("CPU", style="position: absolute;")
            with vuetify.VProgressLinear(
                v_model=("tmr_cpu_total", 0),
                height=20,
                style="margin-left: 60px;",
            ):
                html.Div("{{ tmr_cpu_total }} %", classes="text-subtitle-2")
        vuetify.VDivider()
        with vuetify.VCardText(classes="py-1"):
            with vuetify.VProgressLinear(
                v_for="v, i in tmr_cpu_per_core",
                key="i",
                value=("v",),
                height=12,
                label=("`#${i+1}`",),
                classes="my-1",
                color="green",
            ):
                html.Div("# {{ i + 1 }}", classes="text-overline")
                vuetify.VSpacer()
                html.Div("{{ v }} %", classes="text-overline")
