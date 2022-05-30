from trame.app import get_server, dev
from . import engine, ui


def _reload():
    server = get_server()
    dev.reload(ui)
    ui.initialize(server)


def main(server=None, **kwargs):
    # Get or create server
    if server is None:
        server = get_server()

    if isinstance(server, str):
        server = get_server(server)

    # CLI
    server.cli.add_argument(
        "--apps",
        help="Path to apps config file",
    )

    # Make UI auto reload
    server.controller.on_server_reload.add(_reload)

    # Init application
    args = server.cli.parse_known_args()[0]
    engine.initialize(server, apps=args.apps)
    ui.initialize(server)

    # Start server
    server.start(**kwargs)


if __name__ == "__main__":
    main()
