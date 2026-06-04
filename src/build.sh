PYTHON_VERSION="3.12.3"
LLPYR_VERSION="1.0"
TARGET_NAME="Lifeline.PYR-v$LLPYR_VERSION"

# Intro text
echo "You may take as long as you need to read this. There is no time limit."
echo ""
echo "Lifeline.PYR v$LLPYR_VERSION build script."
echo "This is for Python v$PYTHON_VERSION."
echo "If the resulting program is not running in that version, something has gone wrong with it." 
echo "This script itself is under the MIT License,"
echo "however the program that you are about to compile is under the GNU General Public License v3.0."
echo "That means that with the resulting program, you MUST comply to the terms of the GPLv3."
echo ""
echo "Here are links to those licenses:"
echo "MIT: https://opensource.org/license/mit"
echo "GPL: https://www.gnu.org/licenses/gpl-3.0.html"
echo ""
echo "Now, to use the build script."
echo "It is assumed that you are in the project's source directory."
echo "If not, exit now with Ctrl+C and cd into it."
read -p "Press Enter to continue..."

# Check prequisites
echo "Checking for prequisites..."
if ! command -v pyenv &>/dev/null; then
    echo "Error: pyenv is not installed. Please install it."
    exit 1
fi
if ! pyenv versions --bare | grep -qx "$PYTHON_VERSION"; then
    echo "Warning: Python $PYTHON_VERSION is not installed. Install it now via pyenv? [y/n]"
    read -p ">" yn
    yn=$(echo "$yn" | xargs)
    case $yn in
        [Yy]* ) pyenv install "$PYTHON_VERSION";;
        [Nn]* ) echo "Exiting." && exit 0;;
        * ) echo "Error: Could not parse your response. Please use [y/n]." && exit 1;; 
    esac
fi
echo "All prequisites installed!"

# Build
echo "Starting build..."
# Set up enviornment
PYTHON_BIN="$HOME/.pyenv/versions/$PYTHON_VERSION/bin/python"
echo "In case of error, look at the Python version below this in case they give any information."
"$PYTHON_BIN" --version
"$PYTHON_BIN" -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install PyInstaller
pyinstaller --onefile --clean --name $TARGET_NAME --collect-submodules=pygame main.py
mv dist/$TARGET_NAME ./$TARGET_NAME
deactivate
rm -r build dist venv # rm commands scare me. don't be scared of this one though, it's safe probably
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -type f -delete

# Confirm removal of .spec
read -p "Do you want to delete the .spec file? (y/n) " yn
case $yn in
  [yY] ) rm $TARGET_NAME.spec;;
  [nN] ) echo "Deletion skipped.";;
  * ) echo "Invalid response. Deletion automatically skipped.";;
esac
echo "Build done!"
