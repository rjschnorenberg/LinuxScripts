#!/usr/bin/env bash
YEAR="2017"
START_DATE="${YEAR}-01-01"
END_DATE="${YEAR}-12-31"
RESOLUTION="1920x1080"

i=0
for repo in `find /home/user/git -mindepth 1 -maxdepth 1 -type d`; do
	echo "Generating log for $repo"
	# 1. Generate a Gource custom log files for each repo. This can be facilitated by the --output-custom-log FILE option of Gource as of 0.29:
	logfile="$(mktemp /tmp/gource.XXXXXX)"
	gource --start-date "$START_DATE" --stop-date "$END_DATE" --output-custom-log "${logfile}" ${repo}
	# 2. If you want each repo to appear on a separate branch instead of merged onto each other (which might also look interesting), you can use a 'sed' regular expression to add an extra parent directory to the path of the files in each project:
	sed -i -E "s#(.+)\|#\1|/${repo}#" ${logfile}
	logs[$i]=$logfile
	let i=$i+1
done

combined_log="$(mktemp /tmp/gource.XXXXXX)"
cat ${logs[@]} | sort -n > $combined_log
rm ${logs[@]}

echo "Committers:"
cat $combined_log | awk -F\| {'print  $2'} | sort | uniq
echo "======================"

time gource $combined_log \
	--seconds-per-day 1 \
	-$RESOLUTION \
	--highlight-users \
	--date-format "%Y-%m-%d" \
	--hide mouse \
	--key \
	--stop-at-end \
	--output-ppm-stream - | ffmpeg -y -r 30 -f image2pipe -vcodec ppm -i - -vcodec libx264 -x264opts crf=16 -r 30 -pix_fmt yuv420p "gource${YEAR}.mp4"
rm $combined_log
