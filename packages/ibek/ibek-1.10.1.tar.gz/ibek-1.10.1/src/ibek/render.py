"""
Functions for rendering lines in the boot script using Jinja2
"""

from typing import Callable, List, Optional, Union

from jinja2 import Template

from .ioc import IOC, Entity
from .support import Function, Once


class Render:
    """
    A class for generating snippets of startup script / EPICS DB
    by using Jinja to combine snippet templates from support module
    definition yaml with substitution values supplied in ioc entity yaml
    """

    def __init__(self: "Render"):
        self.once_done: List[str] = []

    def render_text(self, instance: Entity, text: str, once=False, suffix="") -> str:
        """
        Add in the next line of text, honouring the ``once`` flag which will
        only add the line once per IOC.

        Jinja rendering of values/args has already been done in Entity.__post_init__
        but we pass all strings though jinja again to render any other jinja
        in the IOC (e.g. database and function entries)

        ``once`` uses the name of the definition + suffix to track which lines
        have been rendered already. The suffix can be used where a given
        Entity has more than one element to render once (e.g. functions)
        """

        if once:
            name = instance.__definition__.name + suffix
            if name not in self.once_done:
                self.once_done.append(name)
            else:
                return ""

        # Render Jinja entries in the text
        jinja_template = Template(text)
        result = jinja_template.render(instance.__dict__)  # type: ignore

        if result == "":
            return ""

        return result + "\n"

    def render_function(self, instance: Entity, function: Function) -> str:
        """
        render a Function object that represents a function call in the IOC
        startup script
        """

        # initial function comment appears after newline for prettier formatting
        comment = f"\n# {function.name} "
        call = f"{function.name} "
        for name, value in function.args.items():
            comment += f"{name} "
            call += f"{value} "

        text = (
            self.render_text(instance, comment.strip(" "), once=True, suffix="func")
            + self.render_text(instance, function.header, once=True, suffix="func_hdr")
            + self.render_text(instance, call.strip(" "))
        )

        return text

    def render_script(self, instance: Entity) -> Optional[str]:
        """
        render the startup script by combining the jinja template from
        an entity with the arguments from an Entity
        """

        script = ""
        script_items = getattr(instance.__definition__, "script")
        for line in script_items:
            if isinstance(line, str):
                script += self.render_text(instance, line)
            elif isinstance(line, Once):
                script += self.render_text(instance, line.value, True)
            elif isinstance(line, Function):
                script += self.render_function(instance, line)

        return script

    def render_database(self, instance: Entity) -> Optional[str]:
        """
        render the lines required to instantiate database by combining the
        templates from the Entity's database list with the arguments from
        an Entity
        """
        templates = instance.__definition__.databases
        # The entity may not instantiate any database templates
        if not templates:
            return None
        jinja_txt = ""

        for template in templates:
            db_file = template.file.strip("\n")
            db_args = template.define_args.splitlines()

            include_list = []
            for arg in template.include_args:
                if arg in instance.__dict__:
                    include_list.append(f"{arg}={{{{ {arg} }}}}")
                else:
                    raise ValueError(
                        f"include arg '{arg}' in database template "
                        f"'{template.file}' not found in context"
                    )

            db_arg_string = ", ".join(db_args + include_list)

            jinja_txt += (
                f'msi -I${{EPICS_DB_INCLUDE_PATH}} -M"{db_arg_string}" "{db_file}"\n'
            )

        jinja_template = Template(jinja_txt)
        db_txt = jinja_template.render(instance.__dict__)  # type: ignore

        return db_txt + "\n"

    def render_environment_variables(self, instance: Entity) -> Optional[str]:
        """
        render the environment variable elements by combining the jinja template
        from an entity with the arguments from an Entity
        """
        variables = getattr(instance.__definition__, "env_vars")
        if not variables:
            return None

        env_var_txt = ""
        for variable in variables:
            # Substitute the name and value of the environment variable from args
            env_template = Template(f"epicsEnvSet {variable.name} {variable.value}")
            env_var_txt += env_template.render(instance.__dict__)
        return env_var_txt + "\n"

    def render_post_ioc_init(self, instance: Entity) -> Optional[str]:
        """
        render the post-iocInit entries by combining the jinja template
        from an entity with the arguments from an Entity
        """
        script = ""
        for line in getattr(instance.__definition__, "post_ioc_init"):
            script += self.render_text(instance, line)

        return script

    def render_elements(
        self, ioc: IOC, method: Callable[[Entity], Union[str, None]]
    ) -> str:
        """
        Render elements of a given IOC instance based on calling the correct method
        """
        elements = ""
        for instance in ioc.entities:
            if instance.entity_enabled:
                element = method(instance)
                if element:
                    elements += element
        return elements

    def render_script_elements(self, ioc: IOC) -> str:
        """
        Render all of the startup script entries for a given IOC instance
        """
        return self.render_elements(ioc, self.render_script)

    def render_database_elements(self, ioc: IOC) -> str:
        """
        Render all of the DBLoadRecords entries for a given IOC instance
        """
        return self.render_elements(ioc, self.render_database)

    def render_environment_variable_elements(self, ioc: IOC) -> str:
        """
        Render all of the environment variable entries for a given IOC instance
        """
        return self.render_elements(ioc, self.render_environment_variables)

    def render_post_ioc_init_elements(self, ioc: IOC) -> str:
        """
        Render all of the post-iocInit elements for a given IOC instance
        """
        return self.render_elements(ioc, self.render_post_ioc_init)
