from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify

from . import cpu, memory, launcher

# Create single page layout type
# (FullScreenPage, SinglePage, SinglePageWithDrawer)
def initialize(server):
    state = server.state
    state.trame__title = "trame monitor"

    with SinglePageLayout(server) as layout:
        # Toolbar
        layout.title.set_text("Resource Monitor")
        with layout.toolbar as tb:
            tb.dense = True
            vuetify.VSpacer()
            tb.add_child("{{refresh_rate}} s")
            vuetify.VSlider(
                v_model=("refresh_rate", 1),
                min=1,
                max=60,
                step=0.5,
                dense=True,
                hide_details=True,
                classes="ml-4",
                style="max-width: 200px;",
            )

        # Main content
        with layout.content:
            with vuetify.VContainer(fluid=True):
                with vuetify.VRow():
                    with vuetify.VCol(cols=6):
                        cpu.create_card()
                        memory.create_card(classes="mt-4")

                    with vuetify.VCol(cols=6):
                        launcher.create_card(server)
                        vuetify.VSpacer()
