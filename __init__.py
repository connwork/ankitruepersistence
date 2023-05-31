import os
import json
from aqt import mw, gui_hooks

config = mw.addonManager.getConfig(__name__)
inclusion_list = config["localstoragetopersist"]

def retrieve_local_storage():
    js_code = f"""
        var inclusion_list = {inclusion_list};
        var text = 'var key_value_pairs = [\\n';
        for (var i = 0; i < localStorage.length; i++) {{
            var key = localStorage.key(i);
            var value = localStorage.getItem(key);
            for (var j = 0; j < inclusion_list.length; j++) {{
                var inclusion_term = inclusion_list[j];
                if (key.startsWith(inclusion_term)) {{
                    text += '    ["' + key + '", "' + value + '"],\\n';
                }}
            }}
        }}
        text = text.slice(0, -2);
        text += '\\n];';
        text;
    """

    js_footer_code = f"""
        if (localStorage.getItem("ankipersistencerefresh") === null) {{
            localStorage.setItem("ankipersistencerefresh", 1);
            key_value_pairs.forEach(function(pair) {{
                var key = pair[0];
                var value = pair[1];
                if (localStorage.getItem(key) !== value) {{
                    localStorage.setItem(key, value);
                }}
            }});
        }}
    """

    def save_key_value_pairs(js_return):
        if js_return == "None":
            return
        js_persistentlocalstorage = f"{js_return}\n{js_footer_code}"
        media_folder = mw.col.media.dir()
        file_path = str(os.path.join(media_folder, "__persistentlocalstorage.js"))
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(js_persistentlocalstorage)

    mw.web.evalWithCallback(js_code, save_key_value_pairs)


def load_key_value_pairs():
    script_to_load_keys = '<script src="__persistentlocalstorage.js"></script>'
    note_types = mw.col.models.all()
    for note_type in note_types:
        templates = note_type["tmpls"]
        for templ in templates:
            for x in ["qfmt", "afmt"]:
                html = templ[x]
                if script_to_load_keys not in html:
                    html += "\n" + script_to_load_keys
                    templ[x] = html
                    mw.col.models.update(note_type)

# Hook into Anki's events
gui_hooks.profile_did_open.append(load_key_value_pairs)
gui_hooks.reviewer_will_end.append(retrieve_local_storage)
gui_hooks.profile_will_close.append(retrieve_local_storage)