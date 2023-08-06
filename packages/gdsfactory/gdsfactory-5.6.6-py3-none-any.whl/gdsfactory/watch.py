import logging
import pathlib
import sys
import time
from functools import partial

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from gdsfactory.config import cwd
from gdsfactory.pdk import get_active_pdk
from gdsfactory.read.from_yaml import from_yaml


class YamlEventHandler(FileSystemEventHandler):
    """Logs captured events."""

    def __init__(self, logger=None):
        super().__init__()

        self.logger = logger or logging.root

    def update_cell(self, src_path) -> None:
        """Register new file into active pdk."""

        pdk = get_active_pdk()
        filepath = pathlib.Path(src_path)
        cell_name = filepath.stem
        function = partial(from_yaml, filepath)
        pdk.register_cells_yaml(**{cell_name: function})

    def on_moved(self, event):
        super().on_moved(event)

        what = "directory" if event.is_directory else "file"
        self.logger.info(
            "Moved %s: from %s to %s", what, event.src_path, event.dest_path
        )

    def on_created(self, event):
        super().on_created(event)

        what = "directory" if event.is_directory else "file"
        if what == "file" and event.src_path.endswith(".pic.yml"):
            self.logger.info("Created %s: %s", what, event.src_path)
            c = from_yaml(event.src_path)
            c.show()

            self.update_cell(event.src_path)

    def on_deleted(self, event):
        super().on_deleted(event)

        what = "directory" if event.is_directory else "file"
        self.logger.info("Deleted %s: %s", what, event.src_path)

        pdk = get_active_pdk()
        filepath = pathlib.Path(event.src_path)
        cell_name = filepath.stem
        pdk.remove_cell(cell_name)

    def on_modified(self, event):
        super().on_modified(event)

        what = "directory" if event.is_directory else "file"
        if what == "file" and event.src_path.endswith(".pic.yml"):
            self.logger.info("Modified %s: %s", what, event.src_path)
            try:
                c = from_yaml(event.src_path)
                c.show()
                self.update_cell(event.src_path)
            except Exception as e:
                print(e)


def watch(path=str(cwd)) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    event_handler = YamlEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    watch(path)
