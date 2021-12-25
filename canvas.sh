#!/data/data/com.termux/files/usr/bin/bash
# modified verion of canvas by adi1090x (https://github.com/adi1090x)
# original: https://github.com/adi1090x/canvas/blob/master/canvas
# licence: https://github.com/adi1090x/canvas/blob/master/LICENSE

## Generate a solid color wallpaper

size="1440x2560"
DIR="$PREFIX/tmp"
name="canvas.png"

solid() {
	get_random_color
	color="$RCOLOR"
	convert -size "$size" canvas:"$color" "$DIR/$name"
}

## Generate a linear gradient wallpaper
linear_gradient() {
	get_random_color
	color="$RCOLOR"

	get_random_number "360"
	angle="$RNUM"

	convert -size "$size" -define gradient:angle="${angle:-0}" gradient:"$color" "$DIR/$name"
}

## Generate a radial gradient wallpaper
radial_gradient() {
	get_random_color
	color1="$RCOLOR"
	get_random_color
	color="$color1-$RCOLOR"

	get_random_number "360"
	angle="$RNUM"

	getRandomShape
	shape="$RSHAPE"
	convert -size "$size" -define gradient:extent="${shape:-maximum}" -define gradient:angle="${angle:-0}" radial-gradient:"$color" "$DIR/$name"
}

## Generate a twisted gradient wallpaper
twisted_gradient() {
	get_random_color
	color1="$RCOLOR"
	get_random_color
	color="$color1-$RCOLOR"

	get_random_number "500"
	twist="$RNUM"
	convert -size "$size" gradient:"$color" -swirl "${twist:-150}" "$DIR/$name"
}

## Generate a 4 point gradient wallpaper
bilinear_gradient() {
	get_random_color
	color1="$RCOLOR"
	get_random_color
	color2="$RCOLOR"
	get_random_color
	color3="$RCOLOR"
	get_random_color
	color4="$RCOLOR"
	convert \( xc:"$color1" xc:"$color2" +append \) \( xc:"$color3" xc:"$color4" +append \) -append -filter triangle -resize "$size"\! "$DIR/$name"

}

## Generate a plasma wallpaper
plasma() {
	get_random_number "3"

	if [[ "$RNUM" == "1" ]]; then
		answer="r"
	elif [[ "$RNUM" == "2" ]]; then
		answer="t"
		get_random_number "500"
		twist="$RNUM"
	else
		answer="c"
		get_random_color
		color="$RCOLOR"
	fi
	if [[ $answer == "r" ]] || [[ $answer == "R" ]]; then
		convert -size "$size" plasma: "$DIR/$name"
	elif [[ $answer == "t" ]] || [[ $answer == "T" ]]; then
		convert -size "$size" plasma:fractal -swirl "${twist:-150}" "$DIR/$name"
		convert -size "$size" plasma:"$color" "$DIR/$name"
	fi
}

## Generate a random, multi-colored blurred/gradient wallpaper
blurred_noise() {
	get_random_number "30"
	blur="$RNUM"

	convert -size "$size" xc: +noise Random "$DIR/$name"
	convert "$DIR/$name" -virtual-pixel tile -blur 0x"${blur:-14}" -auto-level -resize "$size" "$DIR/$name"
}

## Generate random number lower than giver parameter
get_random_number() {
	RNUM=$(( ($RANDOM % $1) + 1 ))
}

## Generate random color
get_random_color() {
	RCOLOR="#"
	for ((i = 0 ; i < 6 ; i++)); do
		get_random_number "16"
		case $RNUM in
			"1") NEXTDIGIT="1";;
			"2") NEXTDIGIT="2";;
			"3") NEXTDIGIT="3";;
			"4") NEXTDIGIT="4";;
			"5") NEXTDIGIT="5";;
			"6") NEXTDIGIT="6";;
			"7") NEXTDIGIT="7";;
			"8") NEXTDIGIT="8";;
			"9") NEXTDIGIT="9";;
			"10") NEXTDIGIT="A";;
			"11") NEXTDIGIT="B";;
			"12") NEXTDIGIT="C";;
			"13") NEXTDIGIT="D";;
			"14") NEXTDIGIT="E";;
			"15") NEXTDIGIT="F";;
			"16") NEXTDIGIT="0";;
		esac
		RCOLOR="$RCOLOR$NEXTDIGIT"
	done
}

## Generate random shape option
getRandomShape() {
	get_random_number "4"
	case $RNUM in
		"1") RSHAPE="diagonal";;
		"2") RSHAPE="ellipse";;
		"3") RSHAPE="maximum";;
		"4") RSHAPE="minimum";;
	esac
}

## Generate random wallpaper
randomize() {
	get_random_number "7"
	case $RNUM in
		"1") solid;;
		"2") linear_gradient;;
		"3") radial_gradient;;
		"4") twisted_gradient;;
		"5") bilinear_gradient;;
		"6") plasma;;
		"7") blurred_noise;;
	esac
}
