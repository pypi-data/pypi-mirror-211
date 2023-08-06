jlpm  # Install npm package dependencies

# Clone the repo to your local environment
# Change directory to the proper directory
# Install package in development mode
printf "\n\n***** pip install -e . \n\n"
pip install -e .

# Link your development version of the extension with JupyterLab
printf "\n\n***** jupyter labextension develop . --overwrite \n\n"
jupyter labextension develop . --overwrite

# Server extension must be manually installed in develop mode
#jupyter server extension list
printf "\n\n***** jupyter server extension enable opensarlab-oslnotify \n\n"
jupyter server extension enable opensarlab-oslnotify

printf "\n\n***** jupyter labextension enable \n\n"
jupyter labextension enable opensarlab-oslnotify

# Compile the TypeScript sources to Javascript
# Rebuild extension Typescript source after making changes
printf "\n\n***** jlpm run build \n\n"
jlpm run build

# Run Jupyter Lab
printf "\n\n***** jupyter lab \n\n"
OPENSARLAB_PROFILE_NAME='SAR 1' \
OPENSCIENCELAB_LAB_SHORT_NAME='opensarlab-test' \
OPENSCIENCELAB_PORTAL_DOMAIN='https://opensciencelab-test.asf.alaska.edu' \
jupyter lab