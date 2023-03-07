echo "Installing command dependencies"
pip install .

HOME_BIN="$HOME/bin"
COMMAND_NAME="kubectlpl"

if ! [ -d "$HOME_BIN" ]; then
  echo "Adding $HOME_BIN directory"
  mkdir -p "$HOME_BIN"
fi

case :$PATH: # notice colons around the value
  in *:$HOME_BIN:*) ;; # do nothing, it's there
     *)
        echo "Please Add $HOME_BIN to PATH variable"
        echo "e.g. export PATH=\$PATH:\$HOME/bin"
       ;;
esac

echo "Copying command $COMMAND_NAME to $HOME_BIN"
cp "commands/$COMMAND_NAME" "$HOME_BIN"
chmod +x "$HOME_BIN/$COMMAND_NAME"