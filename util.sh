#!/data/data/com.termux/files/usr/bin/bash

get_input() {
  if [[ $1 = "text" ]]; then
    input=$(termux-dialog "$1" -t "$2" -i "$3")
  else
    input=$(termux-dialog "$1" -t "$2" -v "$3")
  fi
  code=$(echo "$input" | jq --raw-output ".code")
  if [ "$code" = "-2" ]; then
    echo "<CANCEL>"
  else
    echo "$input" | jq --raw-output ".text"
  fi
}

get_random_number() {
	RNUM=$(( ("$RANDOM" % $1) + 1 ))
}

### config editor ###
# https://stackoverflow.com/a/60116613
# https://stackoverflow.com/a/2464883
# https://unix.stackexchange.com/a/331965/312709
# thanks to ixz in #bash on irc.freenode.net

function config_set() {
  if [[ $2 == *"<CANCEL>"* ]]; then
    exit 0
  fi
  local file=$CONFIG_FILE
  local key=$1
  local val=${@:2}

  ensureConfigFileExists "${file}"

  # create key if not exists
  if ! grep -q "^${key}=" "$file"; then
    # insert a newline just in case the file does not end with one
    printf "\n${key}=" >> "$file"
  fi

  chc "$file" "$key" "$val"
}

function ensureConfigFileExists() {
  if [ ! -e "$1" ] ; then
    if [ -e "$1.example" ]; then
      cp "$1.example" "$1";
    else
      touch "$1"
    fi
  fi
}

function chc() {
    gawk -v OFS== -v FS== -e \
    'BEGIN { ARGC = 1 } $1 == ARGV[2] { print ARGV[4] ? ARGV[4] : $1, ARGV[3]; next } 1' \
    "$@" <"$1" >"$1.1"; mv "$1"{.1,};
}

function config_get() {
    val="$(config_read_file "$CONFIG_FILE" "${1}")";
    if [ "${val}" = "__UNDEFINED__" ]; then
        val="$(config_read_file "$CONFIG_FILE".example "${1}")";
    fi
    printf -- "%s" "${val}";
}

function config_read_file() {
    (grep -E "^${2}=" -m 1 "${1}" 2>/dev/null || echo "VAR=__UNDEFINED__") | head -n 1 | cut -d '=' -f 2-;
}
### ### ###
