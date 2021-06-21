#!/data/data/com.termux/files/usr/bin/bash
## Generate a solid color wallpaper
## Based on https://github.com/adi1090x/canvas

. "$SCRIPT_DIR/imagemagick/config"

filepath=$SCRIPT_DIR/downloads/"$(date +"%s").png"
get_random_number() {
	RNUM=$(( ("$RANDOM" % $1) + 1 ))
}

getRandomShape() {
	get_random_number "4"
	case $RNUM in
		"1") RSHAPE="diagonal";;
		"2") RSHAPE="ellipse";;
		"3") RSHAPE="maximum";;
		"4") RSHAPE="minimum";;
	esac
}

get_random_color() {
	RCOLOR="#"
	for i in 1 2 3 4 5 6
	do
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

solid() {
	get_random_color
	color="$RCOLOR"
	convert -size "$size" canvas:"$color" "$filepath"
}

## Generate a linear gradient wallpaper
linear_gradient() {
		get_random_color
		color1="$RCOLOR"
		get_random_color
		color2="$RCOLOR"
		get_random_number "360"
		angle="$RNUM"
	convert -size "$size" -define gradient:angle="$angle" gradient:"$color1-$color2" "$filepath"
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
	convert -size "$size" -define gradient:extent="$shape" -define gradient:angle="$angle" radial-gradient:"$color" "$filepath"
}

## Generate a twisted gradient wallpaper
twisted_gradient() {
		get_random_color
		color1="$RCOLOR"
		get_random_color
		color="$color1-$RCOLOR"

		get_random_number "500"
		twist="$RNUM"
	convert -size "$size" gradient:"$color" -swirl "${twist}" "$filepath"
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

		get_random_number "2"
		if [[ "$RNUM" == "1" ]]; then
			answer="s"
		else
			answer="r"
		fi

	if [[ $answer == "s" ]] || [[ $answer == "S" ]]; then
		convert \( xc:"$color1" xc:"$color2" +append \) \( xc:"$color3" xc:"$color4" +append \) -append -size "$size" xc: +swap  -fx 'v.p{i/(w-1),j/(h-1)}' "$filepath"
	else
		convert \( xc:"$color1" xc:"$color2" +append \) \( xc:"$color3" xc:"$color4" +append \) -append -filter triangle -resize "$size"\! "$filepath"
	fi
}

blurred_noise() {
		get_random_number "30"
		blur="$RNUM"
	convert -size "100x56" xc: +noise Random "/tmp/noise.png"
	convert "/tmp/noise.png" -virtual-pixel tile -blur 0x30 -auto-level -resize "$size" "$filepath"
}

plasma() {
	get_random_number "360"
	swirl="$RNUM"
		get_random_number "15"
	blur="$RNUM"
	convert -size "$size"  plasma:fractal \
				 -blur 0x$blur  -swirl $swirl  "$filepath"
}

gradient_horizontal() {
		get_random_color
		color1="$RCOLOR"
		get_random_color
		color2="$RCOLOR"
		get_random_color
		color3="$RCOLOR"
			get_random_number "60"
		blur="$RNUM"
	  convert -size "$size" gradient:$color1-$color2 \( +clone +clone \) \
	          -background $color3 -compose ModulusAdd -blur 0x$blur -flatten \
	          "$filepath"
}

gradient_angles() {
		get_random_color
		color1="$RCOLOR"
		get_random_color
		color2="$RCOLOR"
		get_random_color
		color3="$RCOLOR"
		get_random_color
		color4="$RCOLOR"
		get_random_color
		color5="$RCOLOR"
			get_random_number "360"
		rotate="$RNUM"
			get_random_number "60"
		blur="$RNUM"

  convert -size "$size" gradient:$color1-$color2 \( gradient:$color4-$color5 -rotate $rotate \) \
					-background $color3 -compose ModulusAdd -blur 0x$blur -flatten \
          "$filepath"
}

layered_levels() {
		get_random_color
		color1="$RCOLOR"
	convert -size "$size" xc: +noise Random "/tmp/noise.png"
	convert "/tmp/noise.png" -blur 0x12 -normalize \
     \( -size 1x9 xc: -draw 'color 0,4 point' \) \
     -fx '(.5+.3*v.p{0,u*(v.h-1)})' \
     \( +clone -normalize -edge .3 -fx 'R+G+B' \) \
     -fx 'intensity+v'  -fill $color1 -tint 100 "$filepath"
}

edged_level() {
		get_random_color
		color1="$RCOLOR"
convert -size "$size" xc: +noise Random "/tmp/noise.png"
	convert "/tmp/noise.png" -blur 0x12 -normalize \
	 \( -size 1x9 xc: -draw 'color 0,4 point' \) \
	 -fx '(.6+.2*v.p{0,G*(v.h-1)})' \
	 \( +clone -normalize -edge 1 \) -fill $color1 -tint 100 -fx 'u+v' "$filepath"
}

if [ "$pattern" = "random" ]; then
	get_random_number "11"
	pattern="$RNUM"
fi

case "$pattern" in
		1|solid)
			solid
			;;
		2|linear)
				linear_gradient
				;;
		3|radial)
				radial_gradient
				;;
		4|twisted)
				twisted_gradient
				;;
		5|bilinear)
				bilinear_gradient
				;;
		6|plasma)
				plasma
				;;
		7|blurred)
				blurred_noise
				;;
		8|gradient1)
				gradient_horizontal
				;;
		9|gradient2)
				gradient_angles
				;;
		10|layered)
				layered_levels
				;;
		11|edged)
				edged_level
				;;
esac
