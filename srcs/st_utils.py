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

import streamlit as st


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
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
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
