mkdir -p "$1"
python3 reflexoes.py "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9"
echo "making video"
rm "$1/$1.mp4"
ffmpeg -r 30  -f image2 -i "$1/frame_%04d.png" -vcodec libx264 -pix_fmt yuv420p -crf 25 "$1/$1.mp4"
echo "removing files"
rm "$1"/frame*
echo "DONE"
