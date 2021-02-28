mkdir -p "$2"
mkdir -p Arquivo/"$1"/"$2"
#python3 "$1".py ${@:2}
python3 "$1".py "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "${10}" "${11}" "${12}" "${13}" "${14}" "${15}" "${16}" "${17}"
echo "making video"
rm "$2/$2.mp4"
ffmpeg -r 30  -f image2 -i "$2/frame_%04d.png" -vcodec libx264 -pix_fmt yuv420p -crf 25 "$2/$2.mp4"
echo "removing files"
rm "$2"/frame*
cp -R "$2" Arquivo/"$1"/
rm -R "$2"
echo "copying files"
cp Arquivo/"$1"/"$2"/"$2".mp4 Arquivo/"$1"/_videos/"$2".mp4
cp Arquivo/"$1"/"$2"/ultimoFrame.png Arquivo/"$1"/_ultimos_frames/"$2".png
echo "DONE"
