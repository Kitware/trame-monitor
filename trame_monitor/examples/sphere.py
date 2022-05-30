from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, vtk


def ui(server):
    server.state.trame__title = "Sphere"
    server.state.showRes = False
    server.state.client_only("thetaResolution", "phiResolution", "theta", "phi")
    with SinglePageLayout(server) as layout:
        layout.title.set_text("Sphere (vtk.js only)")
        layout.icon.click = "showRes = !showRes"
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                with vtk.VtkView(ref="view"):
                    with vtk.VtkGeometryRepresentation():
                        vtk.VtkAlgorithm(
                            vtk_class="vtkSphereSource",
                            state=(
                                "{ thetaResolution, phiResolution, startTheta: theta[0], endTheta: theta[1], startPhi: phi[0], endPhi: phi[1] }",
                            ),
                            __properties=[("vtk_class", "vtkClass")],
                        )

        with layout.toolbar:
            vuetify.VSpacer()
            vuetify.VSlider(
                v_if="showRes",
                dense=True,
                hide_details=True,
                v_model=("thetaResolution", 8),
                max=80,
                min=8,
                step=1,
                style="max-width: 300px;",
                classes="mx-4",
            )
            vuetify.VRangeSlider(
                v_if="!showRes",
                dense=True,
                hide_details=True,
                v_model=("theta", [0, 360]),
                max=360,
                min=0,
                step=1,
                style="max-width: 300px;",
                classes="mx-4",
            )
            vuetify.VSlider(
                v_if="showRes",
                hide_details=True,
                v_model=("phiResolution", 8),
                max=80,
                min=8,
                step=1,
                style="max-width: 300px;",
            )
            vuetify.VRangeSlider(
                v_if="!showRes",
                dense=True,
                hide_details=True,
                v_model=("phi", [0, 180]),
                max=180,
                min=0,
                step=1,
                style="max-width: 300px;",
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
