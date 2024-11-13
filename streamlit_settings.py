import toml
import os

curr_dir = os.path.dirname(__file__)
streamlit_secrets_folder = os.path.join(curr_dir, ".streamlit")
if not os.path.exists(streamlit_secrets_folder):
    os.makedirs(streamlit_secrets_folder)

toml_file_path = os.path.abspath(os.path.join(streamlit_secrets_folder, "secrets.toml"))


def write_streamlit_secrets(input_data):
    with open(toml_file_path, "w") as out_file:
        toml.dump(input_data, out_file)
    print(f"Secrets file for Streamlit {out_file} was written.")
