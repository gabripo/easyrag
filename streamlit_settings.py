import toml

toml_file_path = ".streamlit/secrets.toml"


def write_streamlit_secrets(input_data):
    with open(toml_file_path, "w") as out_file:
        toml.dump(input_data, out_file)
    print(f"Secrets file for Streamlit {out_file} was written.")
