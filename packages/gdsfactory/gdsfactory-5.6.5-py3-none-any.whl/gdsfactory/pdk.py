import pathlib
import warnings
from functools import partial

from omegaconf import DictConfig
from pydantic import BaseModel

from gdsfactory.components import cells
from gdsfactory.config import logger
from gdsfactory.containers import containers as containers_default
from gdsfactory.cross_section import cross_sections
from gdsfactory.types import (
    CellSpec,
    Component,
    ComponentFactory,
    ComponentSpec,
    CrossSection,
    CrossSectionFactory,
    CrossSectionSpec,
    Dict,
)


class Pdk(BaseModel):
    """Pdk Library to store cell and cross_section functions."""

    name: str
    cross_sections: Dict[str, CrossSectionFactory]
    cells: Dict[str, ComponentFactory]
    containers: Dict[str, ComponentFactory] = containers_default

    def activate(self) -> None:
        set_active_pdk(self)

    def register_cells(self, **kwargs) -> None:
        """Register cell factories."""
        for name, cell in kwargs.items():
            if not callable(cell):
                raise ValueError(
                    f"{cell} is not callable, make sure you register "
                    "cells functions that return a Component"
                )
            if name in self.cells:
                warnings.warn(f"Overwriting cell {name!r}")

            self.cells[name] = cell

    def register_containers(self, **kwargs) -> None:
        """Register container factories."""
        for name, cell in kwargs.items():
            if not callable(cell):
                raise ValueError(
                    f"{cell} is not callable, make sure you register "
                    "cells functions that return a Component"
                )
            if name in self.containers:
                warnings.warn(f"Overwriting container {name!r}")

            self.containers[name] = cell

    def register_cross_sections(self, **kwargs) -> None:
        """Register cross_sections factories."""
        for name, cross_section in kwargs.items():
            if not callable(cross_section):
                raise ValueError(
                    f"{cross_section} is not callable, make sure you register "
                    "cross_section functions that return a CrossSection"
                )
            if name in self.cross_sections:
                warnings.warn(f"Overwriting cross_section {name!r}")
            self.cross_sections[name] = cross_section

    def register_cells_yaml(self, dirpath: pathlib.Path) -> None:
        """Load *.pic.yml YAML files and register them as cells."""
        from gdsfactory.read.from_yaml import from_yaml

        if not dirpath.is_dir():
            raise ValueError(f"{dirpath} needs to be a directory.")

        for filepath in dirpath.glob("*/*.pic.yml"):
            name = filepath.stem.split(".")[0]
            logger.info(f"Add {name!r}")
            self.cells[name] = partial(from_yaml, filepath)

    def get_cell(self, cell: CellSpec, **kwargs) -> ComponentFactory:
        """Returns ComponentFactory from a cell spec."""
        cells_and_containers = set(self.cells.keys()).union(set(self.containers.keys()))

        if callable(cell):
            return cell
        elif isinstance(cell, str):
            if cell not in cells_and_containers:
                cells = list(self.cells.keys())
                containers = list(self.containers.keys())
                raise ValueError(
                    f"{cell!r} from PDK {self.name!r} not in cells: {cells} "
                    f"or containers: {containers}"
                )
            cell = self.cells[cell] if cell in self.cells else self.containers[cell]
            return cell
        elif isinstance(cell, (dict, DictConfig)):
            for key in cell.keys():
                if key not in ["function", "component", "settings"]:
                    raise ValueError(
                        f"Invalid setting {key!r} not in (component, function, settings)"
                    )
            settings = dict(cell.get("settings", {}))
            settings.update(**kwargs)

            cell_name = cell.get("function")
            if not isinstance(cell_name, str) or cell_name not in cells_and_containers:
                cells = list(self.cells.keys())
                containers = list(self.containers.keys())
                raise ValueError(
                    f"{cell_name!r} from PDK {self.name!r} not in cells: {cells} "
                    f"or containers: {containers}"
                )
            cell = (
                self.cells[cell_name]
                if cell_name in self.cells
                else self.containers[cell_name]
            )
            return partial(cell, **settings)
        else:
            raise ValueError(
                "get_cell expects a CellSpec (ComponentFactory, string or dict),"
                f"got {type(cell)}"
            )

    def get_component(self, component: ComponentSpec, **kwargs) -> Component:
        """Returns component from a component spec."""

        cells_and_containers = set(self.cells.keys()).union(set(self.containers.keys()))

        if isinstance(component, Component):
            if kwargs:
                raise ValueError(f"Cannot apply kwargs {kwargs} to {component.name!r}")
            return component
        elif callable(component):
            return component(**kwargs)
        elif isinstance(component, str):
            if component not in cells_and_containers:
                cells = list(self.cells.keys())
                containers = list(self.containers.keys())
                raise ValueError(
                    f"{component!r} not in PDK {self.name!r} cells: {cells} "
                    f"or containers: {containers}"
                )
            cell = (
                self.cells[component]
                if component in self.cells
                else self.containers[component]
            )
            return cell(**kwargs)
        elif isinstance(component, (dict, DictConfig)):
            for key in component.keys():
                if key not in ["function", "component", "settings"]:
                    raise ValueError(
                        f"Invalid setting {key!r} not in (component, function, settings)"
                    )
            settings = dict(component.get("settings", {}))
            settings.update(**kwargs)

            cell_name = component.get("component", None)
            cell_name = cell_name or component.get("function")
            if not isinstance(cell_name, str) or cell_name not in cells_and_containers:
                cells = list(self.cells.keys())
                containers = list(self.containers.keys())
                raise ValueError(
                    f"{cell_name!r} from PDK {self.name!r} not in cells: {cells} "
                    f"or containers: {containers}"
                )
            cell = (
                self.cells[cell_name]
                if cell_name in self.cells
                else self.containers[cell_name]
            )
            return cell(**settings)
        else:
            raise ValueError(
                "get_component expects a ComponentSpec (Component, ComponentFactory, string or dict),"
                f"got {type(component)}"
            )

    def get_cross_section(
        self, cross_section: CrossSectionSpec, **kwargs
    ) -> CrossSection:
        """Returns component from a cross_section spec."""
        if isinstance(cross_section, CrossSection):
            if kwargs:
                raise ValueError(f"Cannot apply {kwargs} to a defined CrossSection")
            return cross_section
        elif callable(cross_section):
            return cross_section(**kwargs)
        elif isinstance(cross_section, str):
            if cross_section not in self.cross_sections:
                cross_sections = list(self.cross_sections.keys())
                raise ValueError(f"{cross_section!r} not in {cross_sections}")
            cross_section_factory = self.cross_sections[cross_section]
            return cross_section_factory(**kwargs)
        elif isinstance(cross_section, (dict, DictConfig)):
            for key in cross_section.keys():
                if key not in ["function", "cross_section", "settings"]:
                    raise ValueError(
                        f"Invalid setting {key!r} not in (cross_section, function, settings)"
                    )
            cross_section_factory_name = cross_section.get("cross_section", None)
            cross_section_factory_name = (
                cross_section_factory_name or cross_section.get("function")
            )
            if (
                not isinstance(cross_section_factory_name, str)
                or cross_section_factory_name not in self.cross_sections
            ):
                cross_sections = list(self.cross_sections.keys())
                raise ValueError(
                    f"{cross_section_factory_name!r} not in {cross_sections}"
                )
            cross_section_factory = self.cross_sections[cross_section_factory_name]
            settings = dict(cross_section.get("settings", {}))
            settings.update(**kwargs)

            return cross_section_factory(**settings)
        else:
            raise ValueError(
                f"get_cross_section expects a CrossSectionSpec (CrossSection, CrossSectionFactory, string or dict), got {type(cross_section)}"
            )


GENERIC = Pdk(name="generic", cross_sections=cross_sections, cells=cells)
_ACTIVE_PDK = GENERIC


def get_component(component: ComponentSpec, **kwargs) -> Component:
    return _ACTIVE_PDK.get_component(component, **kwargs)


def get_cell(cell: CellSpec, **kwargs) -> ComponentFactory:
    return _ACTIVE_PDK.get_cell(cell, **kwargs)


def get_cross_section(cross_section: CrossSectionSpec, **kwargs) -> CrossSection:
    return _ACTIVE_PDK.get_cross_section(cross_section, **kwargs)


def get_active_pdk() -> Pdk:
    return _ACTIVE_PDK


def set_active_pdk(pdk: Pdk) -> None:
    global _ACTIVE_PDK
    _ACTIVE_PDK = pdk


if __name__ == "__main__":
    c = _ACTIVE_PDK.get_component("straight")
    print(c.settings)
