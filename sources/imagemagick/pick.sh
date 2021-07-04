#!/data/data/com.termux/files/usr/bin/bash
## Generate a solid color wallpaper
## Based on https://github.com/adi1090x/canvas

filepath=$SCRIPT_DIR/downloads/"$(date +"%s").png"

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
	convert \( xc:"$color1" xc:"$color2" +append \) \( xc:"$color3" xc:"$color4" +append \) -append -filter triangle -resize "$size"\! "$filepath"
}

blurred_noise_paint() {
	convert -size "$size" xc: +noise Random "$filepath"
	convert "$filepath" -virtual-pixel tile -blur 0x"$blur" -auto-level -paint "$paint" "$filepath"
}

plasma_fractal() {
	get_random_number "360"
	swirl="$RNUM"
	convert -size "$size"  plasma:fractal \
	-blur 0x"$blur"  -swirl "$swirl"  "$filepath"
}

plasma_range() {
	get_random_color
	color1="$RCOLOR"
	get_random_color
	color2="$RCOLOR"
	convert -size "$size" plasma:$color1-$color2 "$filepath"
}

plasma_single() {
	get_random_color
	color1="$RCOLOR"
	convert -size "$size" plasma:$color1 "$filepath"
}

gradient_horizontal() {
	get_random_color
	color1="$RCOLOR"
	convert -size "$size" gradient: \( +clone \) \
	-background $color1 -compose ModulusAdd -flatten -blur 0x"$blur" \
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
	convert -size "$size" gradient:$color1-$color2 \( gradient:$color4-$color5 -rotate "$rotate" \) \
	-background $color3 -compose ModulusAdd -flatten  \
	"$filepath"
}

gradient_c() {
	get_random_color
	color1="$RCOLOR"
	get_random_color
	color2="$RCOLOR"
	get_random_color
	color3="$RCOLOR"
	get_random_color
	color4="$RCOLOR"
  convert \( xc:$color1 xc:$color2 +append \) \
          \( xc:$color3 xc:$color4 +append \) -append \
          -filter point -interpolate catrom \
          -define distort:viewport="100x100" \
          -distort Affine '.5,.5 .5,.5   1.5,1.5 99.5,99.5' \
          -resize "$size" "$filepath"

}

if [ "$pattern" = "random" ]; then
	get_random_number "10"
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
	plasma_fractal
	;;
	7|blurred)
	blurred_noise_paint
	;;
	8|gradient1)
	gradient_horizontal
	;;
	9|gradient2)
	gradient_angles
	;;
	10|plasma1)
	plasma_single
	;;
	11|plasma2)
	plasma_range
	;;
	12|gradient3)
	gradient_c
esac
