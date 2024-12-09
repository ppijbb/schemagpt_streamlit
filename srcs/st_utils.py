# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import mimetypes
import os
from pathlib import Path
from typing import Final

import tornado.web

import streamlit as st
from streamlit.logger import get_logger
import streamlit.components.v1 as components

_LOGGER: Final = get_logger(__name__)

# We agreed on these limitations for the initial release of static file sharing,
# based on security concerns from the SiS and Community Cloud teams
# The maximum possible size of single serving static file.
MAX_APP_STATIC_FILE_SIZE = 200 * 1024 * 1024  # 200 MB
# The list of file extensions that we serve with the corresponding Content-Type header.
# All files with other extensions will be served with Content-Type: text/plain
SAFE_APP_STATIC_FILE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".js", ".css", ".html")


class AppStaticFileHandler(tornado.web.StaticFileHandler):

    @staticmethod
    def check():
        return "Ok"

    def initialize(self, path: str, default_filename: str | None = None) -> None:
        super().initialize(path, default_filename)
        mimetypes.add_type("image/webp", ".webp")

    def validate_absolute_path(self, root: str, absolute_path: str) -> str | None:
        full_path = os.path.realpath(absolute_path)

        if os.path.isdir(full_path):
            # we don't want to serve directories, and serve only files
            raise tornado.web.HTTPError(404)

        if os.path.commonpath([full_path, root]) != root:
            # Don't allow misbehaving clients to break out of the static files directory
            _LOGGER.warning(
                "Serving files outside of the static directory is not supported"
            )
            raise tornado.web.HTTPError(404)

        if (
            os.path.exists(full_path)
            and os.path.getsize(full_path) > MAX_APP_STATIC_FILE_SIZE
        ):
            raise tornado.web.HTTPError(
                404,
                "File is too large, its size should not exceed "
                f"{MAX_APP_STATIC_FILE_SIZE} bytes",
                reason="File is too large",
            )

        return super().validate_absolute_path(root, absolute_path)

    def set_default_headers(self):
        # CORS protection is disabled because we need access to this endpoint
        # from the inner iframe.
        self.set_header("Access-Control-Allow-Origin", "*")

    def set_extra_headers(self, path: str) -> None:
        if Path(path).suffix == ".js":
            self.set_header("Content-Type", "text/javascript")
        elif Path(path).suffix == ".css":
            self.set_header("Content-Type", "text/css")
        elif Path(path).suffix not in SAFE_APP_STATIC_FILE_EXTENSIONS:
            self.set_header("Content-Type", "text/plain")
        self.set_header("X-Content-Type-Options", "nosniff")


def hide_radio_value_md():
    st.markdown(
        body="""
        <style>
        div[role="radiogroup"] div[data-testid="stMarkdownContainer"]:has(p){ visibility: hidden; height: 0px; }
        </style>
        """,
        unsafe_allow_html=True)


def colorize_multiselect_options() -> None:
    colors = ["blue", "green", "orange", "red", "violet", "gray", "rainbow"]
    rules = ""
    n_colors = len(colors)

    for i, color in enumerate(colors):
        rules += f""".stMultiSelect div[data-baseweb="select"] span[data-baseweb="tag"]:nth-child({n_colors}n+{i}){{background-color: {color};}}"""

    st.markdown(f"<style>{rules}</style>", unsafe_allow_html=True)


def draw_mermaid(code: str) -> None:
    st.html(
#         f"""<pre class="mermaid">
# {code}
# </pre>
# <script type="module">
#    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
#    mermaid.initialize({{ startOnLoad: true }});
# </script>
#         """,
        f"""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
        <script src="https://cdn.jsdelivr.net/npm/mermaid@latest/dist/mermaid.min.js"></script>
        <div class="mermaid-container" style="overflow-y: auto; max-height: 750px;">
            <div class="mermaid">
                {code}
            </div>
        </div>
        <script>
            mermaid.initialize({{
                startOnLoad: true,
                fontFamily: 'monospace, sans-serif',
                flowchart: {{
                    htmlLabels: true,
                    useMaxWidth: true,
                }},
                securityLevel: 'loose',
            }});
            mermaid.parseError = function(err, hash) {{
                console.error('Mermaid error:', err);
            }};
        </script>""",
        # scrolling=True,        
    )
