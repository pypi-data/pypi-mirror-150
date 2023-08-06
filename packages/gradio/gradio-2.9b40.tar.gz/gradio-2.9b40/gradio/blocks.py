from __future__ import annotations

import getpass
import os
import sys
import time
import warnings
import webbrowser
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple

from gradio import encryptor, networking, queueing, strings, utils
from gradio.context import Context
from gradio.deprecation import check_deprecated_parameters
from gradio.utils import delete_none

if TYPE_CHECKING:  # Only import for type checking (is False at runtime).
    from fastapi.applications import FastAPI

    from gradio.components import Component, StatusTracker
    from gradio.routes import PredictBody


class Block:
    def __init__(self, *, render=True, css=None, visible=True, **kwargs):
        self._id = Context.id
        Context.id += 1
        self.css = css if css is not None else {}
        self.visible = visible
        if render:
            self.render()
        check_deprecated_parameters(self.__class__.__name__, **kwargs)

    def render(self):
        """
        Adds self into appropriate BlockContext
        """
        if Context.block is not None:
            Context.block.children.append(self)
        if Context.root_block is not None:
            Context.root_block.blocks[self._id] = self

    def unrender(self):
        """
        Removes self from BlockContext if it has been rendered (otherwise does nothing).
        Only deletes the first occurrence of self in BlockContext. Removes from the
        layout and collection of Blocks, but does not delete any event triggers.
        """
        if Context.block is not None:
            try:
                Context.block.children.remove(self)
            except ValueError:
                pass
        if Context.root_block is not None:
            try:
                del Context.root_block.blocks[self._id]
            except KeyError:
                pass
        return self

    def get_block_name(self) -> str:
        """
        Gets block's class name.

        If it is template component it gets the parent's class name.

        @return: class name
        """
        return (
            self.__class__.__base__.__name__.lower()
            if hasattr(self, "is_template")
            else self.__class__.__name__.lower()
        )

    def set_event_trigger(
        self,
        event_name: str,
        fn: Optional[Callable],
        inputs: Optional[Component | List[Component]],
        outputs: Optional[Component | List[Component]],
        preprocess: bool = True,
        postprocess: bool = True,
        js: Optional[str] = False,
        no_target: bool = False,
        status_tracker: Optional[StatusTracker] = None,
        queue: Optional[bool] = None,
    ) -> None:
        """
        Adds an event to the component's dependencies.
        Parameters:
            event_name: event name
            fn: Callable function
            inputs: input list
            outputs: output list
            preprocess: whether to run the preprocess methods of components
            postprocess: whether to run the postprocess methods of components
            js: Optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components
            no_target: if True, sets "targets" to [], used for Blocks "load" event
            status_tracker: StatusTracker to visualize function progress
        Returns: None
        """
        # Support for singular parameter
        if inputs is None:
            inputs = []
        if outputs is None:
            outputs = []
        if not isinstance(inputs, list):
            inputs = [inputs]
        if not isinstance(outputs, list):
            outputs = [outputs]

        Context.root_block.fns.append(BlockFunction(fn, preprocess, postprocess))
        Context.root_block.dependencies.append(
            {
                "targets": [self._id] if not no_target else [],
                "trigger": event_name,
                "inputs": [block._id for block in inputs],
                "outputs": [block._id for block in outputs],
                "backend_fn": fn is not None,
                "js": js,
                "status_tracker": status_tracker._id
                if status_tracker is not None
                else None,
                "queue": queue,
            }
        )

    def get_config(self):
        return {"css": self.css, "visible": self.visible}


class BlockContext(Block):
    def __init__(
        self,
        visible: bool = True,
        css: Optional[Dict[str, str]] = None,
        render: bool = True,
        **kwargs,
    ):
        """
        css: Css rules to apply to block.
        """
        self.children = []
        super().__init__(css=css, visible=visible, render=render, **kwargs)

    def __enter__(self):
        self.parent = Context.block
        Context.block = self
        return self

    def __exit__(self, *args):
        Context.block = self.parent

    def postprocess(self, y):
        return y


class Row(BlockContext):
    def get_config(self):
        return {"type": "row", **super().get_config()}

    @staticmethod
    def update(
        css: Optional[Dict] = None,
        visible: Optional[bool] = None,
    ):
        return {
            "css": css,
            "visible": visible,
            "__type__": "update",
        }


class Column(BlockContext):
    def __init__(
        self,
        visible: bool = True,
        css: Optional[Dict[str, str]] = None,
        variant: str = "default",
    ):
        """
        css: Css rules to apply to block.
        variant: column type, 'default' (no background) or 'panel' (gray background color and rounded corners)
        """
        self.variant = variant
        super().__init__(visible=visible, css=css)

    def get_config(self):
        return {
            "type": "column",
            "variant": self.variant,
            **super().get_config(),
        }

    @staticmethod
    def update(
        variant: Optional[str] = None,
        css: Optional[Dict] = None,
        visible: Optional[bool] = None,
    ):
        return {
            "variant": variant,
            "css": css,
            "visible": visible,
            "__type__": "update",
        }


class Tabs(BlockContext):
    def change(self, fn: Callable, inputs: List[Component], outputs: List[Component]):
        """
        Parameters:
            fn: Callable function
            inputs: List of inputs
            outputs: List of outputs
        Returns: None
        """
        self.set_event_trigger("change", fn, inputs, outputs)


class TabItem(BlockContext):
    def __init__(self, label, **kwargs):
        super().__init__(**kwargs)
        self.label = label

    def get_config(self):
        return {"label": self.label, **super().get_config()}

    def select(self, fn: Callable, inputs: List[Component], outputs: List[Component]):
        """
        Parameters:
            fn: Callable function
            inputs: List of inputs
            outputs: List of outputs
        Returns: None
        """
        self.set_event_trigger("select", fn, inputs, outputs)


class BlockFunction:
    def __init__(self, fn: Optional[Callable], preprocess: bool, postprocess: bool):
        self.fn = fn
        self.preprocess = preprocess
        self.postprocess = postprocess
        self.total_runtime = 0
        self.total_runs = 0


class Blocks(BlockContext):
    def __init__(
        self,
        theme: str = "default",
        analytics_enabled: Optional[bool] = None,
        mode: str = "blocks",
        **kwargs,
    ):

        # Cleanup shared parameters with Interface #TODO: is this part still necessary after Interface with Blocks?
        self.save_to = None
        self.api_mode = False
        self.theme = theme
        self.requires_permissions = False  # TODO: needs to be implemented
        self.encrypt = False

        # For analytics_enabled and allow_flagging: (1) first check for
        # parameter, (2) check for env variable, (3) default to True/"manual"
        self.analytics_enabled = (
            analytics_enabled
            if analytics_enabled is not None
            else os.getenv("GRADIO_ANALYTICS_ENABLED", "True") == "True"
        )

        super().__init__(render=False, **kwargs)
        self.blocks: Dict[int, Block] = {}
        self.fns: List[BlockFunction] = []
        self.dependencies = []
        self.mode = mode

        self.is_running = False
        self.share_url = None

        self.ip_address = utils.get_local_ip_address()
        self.is_space = True if os.getenv("SYSTEM") == "spaces" else False
        self.favicon_path = None
        self.auth = None

    def render(self):
        if Context.root_block is not None:
            Context.root_block.blocks.update(self.blocks)
            Context.root_block.fns.extend(self.fns)
            Context.root_block.dependencies.extend(self.dependencies)
        if Context.block is not None:
            Context.block.children.extend(self.children)

    def process_api(
        self,
        data: PredictBody,
        username: str = None,
        state: Optional[Dict[int, any]] = None,
    ) -> Dict[str, Any]:
        """
        Processes API calls from the frontend.
        Parameters:
            data: data recieved from the frontend
            username: name of user if authentication is set up
            state: data stored from stateful components for session
        Returns: None
        """
        raw_input = data.data
        fn_index = data.fn_index
        block_fn = self.fns[fn_index]
        dependency = self.dependencies[fn_index]

        if block_fn.preprocess:
            processed_input = []
            for i, input_id in enumerate(dependency["inputs"]):
                block = self.blocks[input_id]
                if getattr(block, "stateful", False):
                    processed_input.append(state.get(input_id))
                else:
                    processed_input.append(block.preprocess(raw_input[i]))
        else:
            processed_input = raw_input
        start = time.time()
        predictions = block_fn.fn(*processed_input)
        duration = time.time() - start
        block_fn.total_runtime += duration
        block_fn.total_runs += 1
        if len(dependency["outputs"]) == 1:
            predictions = (predictions,)
        if block_fn.postprocess:
            output = []
            for i, output_id in enumerate(dependency["outputs"]):
                block = self.blocks[output_id]
                if getattr(block, "stateful", False):
                    state[output_id] = predictions[i]
                    output.append(None)
                else:
                    prediction_value = predictions[i]
                    if type(
                        prediction_value
                    ) is dict and "update" in prediction_value.get("__type__"):
                        if prediction_value["__type__"] == "generic_update":
                            del prediction_value["__type__"]
                            prediction_value = block.__class__.update(
                                **prediction_value
                            )
                        prediction_value = delete_none(prediction_value)
                        if "value" in prediction_value:
                            prediction_value["value"] = (
                                block.postprocess(prediction_value["value"])
                                if prediction_value["value"] is not None
                                else None
                            )
                        output_value = prediction_value
                    else:
                        output_value = (
                            block.postprocess(prediction_value)
                            if prediction_value is not None
                            else None
                        )
                    output.append(output_value)

        else:
            output = predictions
        return {
            "data": output,
            "duration": duration,
            "average_duration": block_fn.total_runtime / block_fn.total_runs,
        }

    def get_config(self):
        return {"type": "column"}

    def get_config_file(self):
        config = {
            "mode": "blocks",
            "components": [],
            "theme": self.theme,
            "enable_queue": getattr(
                self, "enable_queue", False
            ),  # attribute set at launch
        }

        for _id, block in self.blocks.items():
            config["components"].append(
                {
                    "id": _id,
                    "type": (block.get_block_name()),
                    "props": utils.delete_none(block.get_config())
                    if hasattr(block, "get_config")
                    else {},
                }
            )

        def getLayout(block):
            if not isinstance(block, BlockContext):
                return {"id": block._id}
            children = []
            for child in block.children:
                children.append(getLayout(child))
            return {"id": block._id, "children": children}

        config["layout"] = getLayout(self)
        config["dependencies"] = self.dependencies
        return config

    def __enter__(self):
        if Context.block is None:
            Context.root_block = self
        self.parent = Context.block
        Context.block = self
        return self

    def __exit__(self, *args):
        Context.block = self.parent
        if self.parent is None:
            Context.root_block = None
        else:
            self.parent.children.extend(self.children)
        self.config = self.get_config_file()

    def load(
        self, fn: Callable, inputs: List[Component], outputs: List[Component]
    ) -> None:
        """
        Adds an event for when the demo loads in the browser.

        Parameters:
            fn: Callable function
            inputs: input list
            outputs: output list
        Returns: None
        """
        self.set_event_trigger(
            event_name="load", fn=fn, inputs=inputs, outputs=outputs, no_target=True
        )

    def clear(self):
        """Resets the layout of the Blocks object."""
        self.blocks = {}
        self.fns = []
        self.dependencies = []
        self.children = []
        return self

    def launch(
        self,
        inline: bool = None,
        inbrowser: bool = None,
        share: bool = False,
        debug: bool = False,
        enable_queue: bool = None,
        auth: Optional[Callable | Tuple[str, str] | List[Tuple[str, str]]] = None,
        auth_message: Optional[str] = None,
        private_endpoint: Optional[str] = None,
        prevent_thread_lock: bool = False,
        show_error: bool = True,
        server_name: Optional[str] = None,
        server_port: Optional[int] = None,
        show_tips: bool = False,
        height: int = 500,
        width: int = 900,
        encrypt: bool = False,
        favicon_path: Optional[str] = None,
        ssl_keyfile: Optional[str] = None,
        ssl_certfile: Optional[str] = None,
        ssl_keyfile_password: Optional[str] = None,
    ) -> Tuple[FastAPI, str, str]:
        """
        Launches the webserver that serves the UI for the interface.
        Parameters:
        inline (bool): whether to display in the interface inline on python notebooks.
        inbrowser (bool): whether to automatically launch the interface in a new tab on the default browser.
        share (bool): whether to create a publicly shareable link from your computer for the interface.
        debug (bool): if True, and the interface was launched from Google Colab, prints the errors in the cell output.
        auth (Callable, Union[Tuple[str, str], List[Tuple[str, str]]]): If provided, username and password (or list of username-password tuples) required to access interface. Can also provide function that takes username and password and returns True if valid login.
        auth_message (str): If provided, HTML message provided on login page.
        private_endpoint (str): If provided, the public URL of the interface will be this endpoint (should generally be unchanged).
        prevent_thread_lock (bool): If True, the interface will block the main thread while the server is running.
        show_error (bool): If True, any errors in the interface will be printed in the browser console log
        server_port (int): will start gradio app on this port (if available). Can be set by environment variable GRADIO_SERVER_PORT.
        server_name (str): to make app accessible on local network, set this to "0.0.0.0". Can be set by environment variable GRADIO_SERVER_NAME.
        show_tips (bool): if True, will occasionally show tips about new Gradio features
        width (int): The width in pixels of the iframe element containing the interface (used if inline=True)
        height (int): The height in pixels of the iframe element containing the interface (used if inline=True)
        encrypt (bool): If True, flagged data will be encrypted by key provided by creator at launch
        favicon_path (str): If a path to a file (.png, .gif, or .ico) is provided, it will be used as the favicon for the web page.
        ssl_keyfile (str): If a path to a file is provided, will use this as the private key file to create a local server running on https.
        ssl_certfile (str): If a path to a file is provided, will use this as the signed certificate for https. Needs to be provided if ssl_keyfile is provided.
        ssl_keyfile_password (str): If a password is provided, will use this with the ssl certificate for https.
        Returns:
        app (FastAPI): FastAPI app object that is running the demo
        local_url (str): Locally accessible link to the demo
        share_url (str): Publicly accessible link to the demo (if share=True, otherwise None)
        """
        if (
            auth
            and not callable(auth)
            and not isinstance(auth[0], tuple)
            and not isinstance(auth[0], list)
        ):
            auth = [auth]
        self.auth = auth
        self.auth_message = auth_message
        self.show_tips = show_tips
        self.show_error = show_error
        self.height = height
        self.width = width
        self.favicon_path = favicon_path
        if self.is_space and enable_queue is None:
            self.enable_queue = True
        else:
            self.enable_queue = enable_queue or False

        self.config = self.get_config_file()

        self.encrypt = encrypt
        if self.encrypt:
            self.encryption_key = encryptor.get_key(
                getpass.getpass("Enter key for encryption: ")
            )

        if self.is_running:
            self.server_app.launchable = self
            print(
                "Rerunning server... use `close()` to stop if you need to change `launch()` parameters.\n----"
            )
        else:
            server_port, path_to_local_server, app, server = networking.start_server(
                self,
                server_name,
                server_port,
                ssl_keyfile,
                ssl_certfile,
                ssl_keyfile_password,
            )
            self.local_url = path_to_local_server
            self.server_port = server_port
            self.server_app = app
            self.server = server
            self.is_running = True

        utils.launch_counter()

        # If running in a colab or not able to access localhost,
        # automatically create a shareable link.
        is_colab = utils.colab_check()
        if is_colab or not (networking.url_ok(self.local_url)):
            share = True
            if is_colab:
                if debug:
                    print(strings.en["COLAB_DEBUG_TRUE"])
                else:
                    print(strings.en["COLAB_DEBUG_FALSE"])
        else:
            print(strings.en["RUNNING_LOCALLY"].format(self.local_url))
        if is_colab and self.requires_permissions:
            print(strings.en["MEDIA_PERMISSIONS_IN_COLAB"])

        if private_endpoint is not None:
            share = True

        if share:
            if self.is_space:
                raise RuntimeError("Share is not supported when you are in Spaces")
            try:
                if self.share_url is None:
                    share_url = networking.setup_tunnel(
                        self.server_port, private_endpoint
                    )
                    self.share_url = share_url
                print(strings.en["SHARE_LINK_DISPLAY"].format(self.share_url))
                if private_endpoint:
                    print(strings.en["PRIVATE_LINK_MESSAGE"])
                else:
                    print(strings.en["SHARE_LINK_MESSAGE"])
            except RuntimeError:
                if self.analytics_enabled:
                    utils.error_analytics(self.ip_address, "Not able to set up tunnel")
                self.share_url = None
                share = False
                print(strings.en["COULD_NOT_GET_SHARE_LINK"])
        else:
            print(strings.en["PUBLIC_SHARE_TRUE"])
            self.share_url = None

        self.share = share

        if inbrowser:
            link = self.share_url if share else self.local_url
            webbrowser.open(link)

        # Check if running in a Python notebook in which case, display inline
        if inline is None:
            inline = utils.ipython_check() and (auth is None)
        if inline:
            if auth is not None:
                print(
                    "Warning: authentication is not supported inline. Please"
                    "click the link to access the interface in a new tab."
                )
            try:
                from IPython.display import IFrame, display  # type: ignore

                if share:
                    while not networking.url_ok(self.share_url):
                        time.sleep(1)
                    display(
                        IFrame(self.share_url, width=self.width, height=self.height)
                    )
                else:
                    display(
                        IFrame(self.local_url, width=self.width, height=self.height)
                    )
            except ImportError:
                pass

        data = {
            "launch_method": "browser" if inbrowser else "inline",
            "is_google_colab": is_colab,
            "is_sharing_on": share,
            "share_url": self.share_url,
            "ip_address": self.ip_address,
            "enable_queue": self.enable_queue,
            "show_tips": self.show_tips,
            "server_name": server_name,
            "server_port": server_port,
            "is_spaces": self.is_space,
            "mode": self.mode,
        }
        if hasattr(self, "analytics_enabled") and self.analytics_enabled:
            utils.launch_analytics(data)

        utils.show_tip(self)

        # Block main thread if debug==True
        if debug or int(os.getenv("GRADIO_DEBUG", 0)) == 1:
            self.block_thread()
        # Block main thread if running in a script to stop script from exiting
        is_in_interactive_mode = bool(getattr(sys, "ps1", sys.flags.interactive))
        if not prevent_thread_lock and not is_in_interactive_mode:
            self.block_thread()

        return self.server_app, self.local_url, self.share_url

    def close(self, verbose: bool = True) -> None:
        """
        Closes the Interface that was launched and frees the port.
        """
        try:
            self.server.close()
            self.is_running = False
            if verbose:
                print("Closing server running on port: {}".format(self.server_port))
        except (AttributeError, OSError):  # can't close if not running
            pass

    def block_thread(
        self,
    ) -> None:
        """Block main thread until interrupted by user."""
        try:
            while True:
                time.sleep(0.1)
        except (KeyboardInterrupt, OSError):
            print("Keyboard interruption in main thread... closing server.")
            self.server.close()
            if self.enable_queue:
                queueing.close()
