from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, vtk


def ui(server):
    server.state.trame__title = "Cone"
    server.state.client_only("resolution")
    with SinglePageLayout(server) as layout:
        layout.title.set_text("Cone (vtk.js only)")
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                with vtk.VtkView(ref="view"):
                    with vtk.VtkGeometryRepresentation():
                        vtk.VtkAlgorithm(
                            vtkClass="vtkConeSource", state=("{ resolution }",)
                        )

        with layout.toolbar:
            vuetify.VSpacer()
            vuetify.VSlider(
                hide_details=True,
                v_model=("resolution", 6),
                max=60,
                min=3,
                step=1,
                style="max-width: 300px;",
            )
            vuetify.VSwitch(
                hide_details=True,
                v_model=("$vuetify.theme.dark",),
            )
            with vuetify.VBtn(icon=True, click="$refs.view.resetCamera()"):
                vuetify.VIcon("mdi-crop-free")


def main(server=None, **kwargs):
    # Get or create server
    if server is None:
        server = get_server()

    if isinstance(server, str):
        server = get_server(server)

    # Start server
    ui(server)
    server.start(**kwargs)


if __name__ == "__main__":
    main()
