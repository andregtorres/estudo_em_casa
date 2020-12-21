mkdir -p "$1"
python3 parabolas.py "$1" "$2" "$3" "$4" "$5"
echo "making video"
ffmpeg -r 30  -f image2 -i "$1/frame_%04d.png" -vcodec libx264 -crf 25 "$1/$1.mp4"
echo "removing files"
rm "$1"/frame*
echo "DONE"
