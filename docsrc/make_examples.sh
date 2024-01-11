#!/bin/bash
#
# Generate the example outputs used in the Gurita documentation.
# These are typically images and text files.
#
# The purpose is to make sure that the Gurita documentation uses up-to-date
# outputs from Gurita, and that Gurita can successfully generate all the examples
# without errors.
#
# This script requires that the gurita command is in your PATH.
#
# Each example has a "tag", which is typically the text of the command as presented in the documents.
#
# If no command line arguments are given to this script then it will generate
# all example outputs.
#
#     ./make_examples.sh
#
# However, you can also get the script to generate exactly one of the examples by
# giving the tag on the command line: 
#
#     ./make_examples.sh 'gurita hist -x tip --xlim 3 8 < tips.csv'  

NUMBER_CMD_LINE_ARGS="$#"
CMD_LINE_ARG_1="$1"
DATA_DIR=../data
IMG_OUT_DIR=../docs/_images
FILE_OUT_DIR=example_outputs
SUCCESS_COUNT=0
FAIL_COUNT=0

if ! command -v gurita &> /dev/null
then
    echo "gurita was not executable in your PATH, exiting"
    exit 1
fi

postscript () {
   echo
   echo "${SUCCESS_COUNT} examples have been successfully run" 
   echo "${FAIL_COUNT} examples failed" 
}

trap postscript EXIT

# arg1: the UUID of the command to run
# arg2: a message to display on output when the command is running
# arg3: the bash command to run

run_example () {
    TAG="$1"
    COMMAND="$2"

    if [[ ($NUMBER_CMD_LINE_ARGS -eq 0 || ($NUMBER_CMD_LINE_ARGS -eq 1 && $CMD_LINE_ARG_1 == $TAG)) ]]; then
	echo
        echo "$TAG"
        eval "$COMMAND"
	eval_exit_status=$?
        if [ ${eval_exit_status} -ne 0 ]; then
            echo
            echo "**** $TAG failed ****" 
	    FAIL_COUNT=$((FAIL_COUNT+1))
        else
	    SUCCESS_COUNT=$((SUCCESS_COUNT+1))
        fi
    fi
}

################################################################################

run_example \
 'gurita box -x species -y sepal_length' \
 'cat "${DATA_DIR}/iris.csv" | gurita box -x species -y sepal_length --out "${IMG_OUT_DIR}/box.species.sepal_length.png"'

################################################################################

run_example \
 'cat iris.csv | gurita pretty' \
 'cat "${DATA_DIR}/iris.csv" | gurita pretty > "${FILE_OUT_DIR}/iris_pretty.txt"'

################################################################################

run_example \
 'cat iris.csv | gurita groupby --key species --val sepal_length --fun median' \
 'cat "${DATA_DIR}/iris.csv" | gurita groupby --key species --val sepal_length --fun median > "${FILE_OUT_DIR}/iris_groupby_species_sepal_length_median.txt"'

################################################################################

run_example \
 'gurita filter '\''species != "virginica"'\'' + sample 0.9 + pca + scatter -x pc1 -y pc2 --hue species' \
 "cat ${DATA_DIR}/iris.csv | gurita filter 'species != \"virginica\"' + sample 0.9 + pca + scatter -x pc1 -y pc2 --hue species --out ${IMG_OUT_DIR}/scatter.pc1.pc2.species.png"

################################################################################

run_example \
 'gurita count -x class < titanic.csv' \
 'gurita count -x class --out "${IMG_OUT_DIR}/count.class.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita box -y age -x class --fcol sex < titanic.csv' \
 'gurita box -y age -x class --fcol sex --out "${IMG_OUT_DIR}/box.class.age.sex.facet.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita box -y age -x class --frow sex < titanic.csv' \
 'gurita box -y age -x class --frow sex --out "${IMG_OUT_DIR}/box.class.age.sex.facet.row.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita box -y age -x class --fcol deck < titanic.csv' \
 'gurita box -y age -x class --fcol deck --out "${IMG_OUT_DIR}/box.class.age.deck.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita box -y age -x class --fcol deck --fcolwrap 4 < titanic.csv' \
 'gurita box -y age -x class --fcol deck --fcolwrap 4 --out "${IMG_OUT_DIR}/box.class.age.deck.fcolwrap4.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita in iris.csv + head' \
 'gurita in "${DATA_DIR}/iris.csv" + head > "${FILE_OUT_DIR}/iris_head.txt"'

################################################################################

run_example \
 'gurita bar -y age -x class < titanic.csv' \
 'gurita bar -y age -x class --out "${IMG_OUT_DIR}/bar.class.age.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita bar -x age -y class --orient h < titanic.csv' \
 'gurita bar -x age -y class --orient h --out "${IMG_OUT_DIR}/bar.age.class.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita bar -y age -x class --estimator max < titanic.csv' \
 'gurita bar -y age -x class --estimator max --out "${IMG_OUT_DIR}/bar.class.age.max.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita bar -y age -x class --sd < titanic.csv' \
 'gurita bar -y age -x class --sd --out "${IMG_OUT_DIR}/bar.class.age.std.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita bar -y age -x class --ci 98 < titanic.csv' \
 'gurita bar -y age -x class --ci 98 --out "${IMG_OUT_DIR}/bar.class.age.ci.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita bar -y age -x class --order First Second Third < titanic.csv' \
 'gurita bar -y age -x class --order First Second Third --out "${IMG_OUT_DIR}/bar.class.age.order.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita bar -y age -x class --hue class < titanic.csv' \
 'gurita bar -y age -x class --hue class --out "${IMG_OUT_DIR}/bar.class.age.sex.hue.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita bar -y age -x class --hue sex < titanic.csv' \
 'gurita bar -y age -x class --hue sex --out "${IMG_OUT_DIR}/bar.class.age.sex.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita bar -y age -x class --hue sex --hueorder female male < titanic.csv' \
 'gurita bar -y age -x class --hue sex --hueorder female male --out "${IMG_OUT_DIR}/bar.class.age.sex.hueorder.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita bar -y age -x class --order First Second Third --hue sex --hueorder female male < titanic.csv' \
 'gurita bar -y age -x class --order First Second Third --hue sex --hueorder female male --out "${IMG_OUT_DIR}/bar.class.age.sex.hueorder.png" < "${DATA_DIR}/titanic.csv"'


################################################################################

run_example \
 'gurita bar -y age -x class --logy < titanic.csv' \
 'gurita bar -y age -x class --logy --out "${IMG_OUT_DIR}/bar.class.age.logy.png" < "${DATA_DIR}/titanic.csv"'


################################################################################

run_example \
 'gurita bar -y age -x class --ylim 10 30 < titanic.csv' \
 'gurita bar -y age -x class --ylim 10 30 --out "${IMG_OUT_DIR}/bar.class.age.ylim.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita bar -y age -x class --fcol sex < titanic.csv' \
 'gurita bar -y age -x class --fcol sex --out "${IMG_OUT_DIR}/bar.class.age.sex.facet.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita box -y age < titanic.csv' \
 'gurita box -y age --out "${IMG_OUT_DIR}/box.age.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita box -y age -x class < titanic.csv' \
 'gurita box -y age -x class --out "${IMG_OUT_DIR}/box.class.age.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita box -x age -y class --orient h < titanic.csv' \
 'gurita box -x age -y class --orient h --out "${IMG_OUT_DIR}/box.age.class.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita box -y age -x class --nooutliers < titanic.csv' \
 'gurita box -y age -x class --nooutliers --out "${IMG_OUT_DIR}/box.class.age.nooutliers.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita box -y age -x class --strip --nooutliers < titanic.csv' \
 'gurita box -y age -x class --strip --nooutliers --out "${IMG_OUT_DIR}/box.class.age.strip.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita box -y age -x class --order First Second Third < titanic.csv' \
 'gurita box -y age -x class --order First Second Third --out "${IMG_OUT_DIR}/box.class.age.order.png" < "${DATA_DIR}/titanic.csv"'
 
################################################################################

run_example \
 'gurita box -y age -x class --hue class < titanic.csv' \
 'gurita box -y age -x class --hue class --out "${IMG_OUT_DIR}/box.class.age.hue.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita box -y age -x class --hue sex < titanic.csv' \
 'gurita box -y age -x class --hue sex --out "${IMG_OUT_DIR}/box.class.age.sex.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita box -y age -x class --hue sex --hueorder female male < titanic.csv' \
 'gurita box -y age -x class --hue sex --hueorder female male --out "${IMG_OUT_DIR}/box.class.age.sex.hueorder.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita box -y age -x class --order First Second Third --hue sex --hueorder female male < titanic.csv' \
 'gurita box -y age -x class --order First Second Third --hue sex --hueorder female male --out "${IMG_OUT_DIR}/box.class.age.sex.order.hueorder.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita box -y age -x class --logy < titanic.csv' \
 'gurita box -y age -x class --logy --out "${IMG_OUT_DIR}/box.class.age.logy.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita box -y age -x class --ylim 10 30 < titanic.csv' \
 'gurita box -y age -x class --ylim 10 30 --out "${IMG_OUT_DIR}/box.class.age.limy.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita boxen -y age < titanic.csv' \
 'gurita boxen -y age --out "${IMG_OUT_DIR}/boxen.age.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita boxen -y age -x class < titanic.csv' \
 'gurita boxen -y age -x class --out "${IMG_OUT_DIR}/boxen.class.age.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita boxen -x age -y class --orient h < titanic.csv' \
 'gurita boxen -x age -y class --orient h --out "${IMG_OUT_DIR}/boxen.age.class.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita boxen -y age -x class --order First Second Third < titanic.csv' \
 'gurita boxen -y age -x class --order First Second Third --out "${IMG_OUT_DIR}/boxen.age.class.order.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita boxen -y age -x class --hue class < titanic.csv' \
 'gurita boxen -y age -x class --hue class --out "${IMG_OUT_DIR}/boxen.class.age.hue.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita boxen -y age -x class --hue sex < titanic.csv' \
 'gurita boxen -y age -x class --hue sex --out "${IMG_OUT_DIR}/boxen.class.age.sex.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita boxen -y age -x class --hue sex --hueorder female male < titanic.csv' \
 'gurita boxen -y age -x class --hue sex --hueorder female male --out "${IMG_OUT_DIR}/boxen.class.age.sex.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita boxen -y age -x class --order First Second Third --hue sex --hueorder female male < titanic.csv' \
 'gurita boxen -y age -x class --order First Second Third --hue sex --hueorder female male --out "${IMG_OUT_DIR}/boxen.age.class.sex.order.hueorder.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita boxen -y age -x class --logy < titanic.csv' \
 'gurita boxen -y age -x class --logy --out "${IMG_OUT_DIR}/boxen.class.age.logy.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita boxen -y age -x class --ylim 10 30 < titanic.csv' \
 'gurita boxen -y age -x class --ylim 10 30 --out "${IMG_OUT_DIR}/boxen.class.age.limy.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita boxen -y age -x class --fcol sex < titanic.csv' \
 'gurita boxen -y age -x class --fcol sex --out "${IMG_OUT_DIR}/boxen.class.age.sex.facet.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita count -x embark_town < titanic.csv' \
 'gurita count -x embark_town --out "${IMG_OUT_DIR}/count.embark_town.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita count -y embark_town < titanic.csv' \
 'gurita count -y embark_town --out "${IMG_OUT_DIR}/count.embark_town.y.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita count -x embark_town --order Cherbourg Queenstown Southampton < titanic.csv' \
 'gurita count -x embark_town --order Cherbourg Queenstown Southampton --out "${IMG_OUT_DIR}/count.embark_town.order.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita count -x embark_town --hue class < titanic.csv' \
 'gurita count -x embark_town --hue class --out "${IMG_OUT_DIR}/count.embark_town.class.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita count -x embark_town --hue class --hueorder First Second Third < titanic.csv' \
 'gurita count -x embark_town --hue class --hueorder First Second Third --out "${IMG_OUT_DIR}/count.embark_town.class.hueorder.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita count -x embark_town --hue class --order Cherbourg Queenstown Southampton --hueorder First Second Third < titanic.csv' \
 'gurita count -x embark_town --hue class --order Cherbourg Queenstown Southampton --hueorder First Second Third --out "${IMG_OUT_DIR}/count.embark_town.class.order.hueorder.png" < "${DATA_DIR}/titanic.csv"' \

################################################################################

run_example \
 'gurita count -x embark_town --logy < titanic.csv' \
 'gurita count -x embark_town --logy --out "${IMG_OUT_DIR}/count.embark_town.logy.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita count -x embark_town --ylim 100 300 < titanic.csv' \
 'gurita count -x embark_town --ylim 100 300 --out "${IMG_OUT_DIR}/count.embark_town.limy.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
  'gurita count -x embark_town --fcol sex < titanic.csv' \
  'gurita count -x embark_town --fcol sex --out "${IMG_OUT_DIR}/count.embark_town.sex.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita count -x embark_town --hue embark_town < titanic.csv' \
 'gurita count -x embark_town --hue embark_town --out "${IMG_OUT_DIR}/count.embark_town.hue.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita heatmap -y year -x month -v passengers < flights.csv' \
 'gurita heatmap -y year -x month -v passengers --out "${IMG_OUT_DIR}/heatmap.month.year.png" < "${DATA_DIR}/flights.csv"'
	
################################################################################

run_example \
 'gurita heatmap -y month -x year -v passengers < flights.csv' \
 'gurita heatmap -y month -x year -v passengers --out "${IMG_OUT_DIR}/heatmap.year.month.png" < "${DATA_DIR}/flights.csv"'
	
################################################################################

run_example \
 'gurita heatmap -y year -x month -v passengers --cmap YlOrRd < flights.csv' \
 'gurita heatmap -y year -x month -v passengers --cmap YlOrRd --out "${IMG_OUT_DIR}/heatmap.month.year.cmap.png" < "${DATA_DIR}/flights.csv"' 
	
################################################################################

run_example \
 'gurita heatmap -y year -x month -v passengers --annot < flights.csv' \
 'gurita heatmap -y year -x month -v passengers --annot --out "${IMG_OUT_DIR}/heatmap.month.year.annot.png" < "${DATA_DIR}/flights.csv"'
	
################################################################################

run_example \
 'gurita heatmap -y year -x month -v passengers --vmin 250 --vmax 550 < flights.csv' \
 'gurita heatmap -y year -x month -v passengers --vmin 250 --vmax 550 --out "${IMG_OUT_DIR}/heatmap.month.year.vmin.vmax.png" < "${DATA_DIR}/flights.csv"'
	
################################################################################

run_example \
 'gurita heatmap -y year -x month -v passengers --robust < flights.csv' \
 'gurita heatmap -y year -x month -v passengers --robust --out "${IMG_OUT_DIR}/heatmap.month.year.robust.png" < "${DATA_DIR}/flights.csv"'
	
################################################################################

run_example \
 'gurita heatmap -y year -x month -v passengers --sorty d < flights.csv' \
 'gurita heatmap -y year -x month -v passengers --sorty d --out "${IMG_OUT_DIR}/heatmap.month.year.sorty.png" < "${DATA_DIR}/flights.csv"'
	
################################################################################

run_example \
 'gurita heatmap -y year -x month -v passengers --orderx January February March April < flights.csv' \
 'gurita heatmap -y year -x month -v passengers --orderx January February March April --out "${IMG_OUT_DIR}/heatmap.month.year.orderx.png" < "${DATA_DIR}/flights.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip < tips.csv' \
 'gurita hist -x tip --out "${IMG_OUT_DIR}/hist.tip.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x day < tips.csv' \
 'gurita hist -x day --out "${IMG_OUT_DIR}/hist.day.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -y tip < tips.csv' \
 'gurita hist -y tip --out "${IMG_OUT_DIR}/hist.tip.y.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip -y total_bill < tips.csv' \
 'gurita hist -x tip -y total_bill --out "${IMG_OUT_DIR}/hist.tip.total_bill.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --bins 5 < tips.csv' \
 'gurita hist -x tip --bins 5 --out "${IMG_OUT_DIR}/hist.tip.bins5.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --binwidth 3 < tips.csv' \
 'gurita hist -x tip --binwidth 3 --out "${IMG_OUT_DIR}/hist.tip.binwidth3.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --cumulative < tips.csv' \
 'gurita hist -x tip --cumulative --out "${IMG_OUT_DIR}/hist.tip.cumulative.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --hue smoker < tips.csv' \
 'gurita hist -x tip --hue smoker --out "${IMG_OUT_DIR}/hist.tip.smoker.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --hue smoker --multiple stack < tips.csv' \
 'gurita hist -x tip --hue smoker --multiple stack --out "${IMG_OUT_DIR}/hist.tip.smoker.stacked.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --hue smoker --multiple dodge < tips.csv' \
 'gurita hist -x tip --hue smoker --multiple dodge --out "${IMG_OUT_DIR}/hist.tip.smoker.dodge.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --hue smoker --multiple fill < tips.csv' \
 'gurita hist -x tip --hue smoker --multiple fill --out "${IMG_OUT_DIR}/hist.tip.smoker.fill.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --stat proportion < tips.csv' \
 'gurita hist -x tip --stat proportion --out "${IMG_OUT_DIR}/hist.tip.proportion.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --hue smoker --stat proportion --multiple dodge < tips.csv' \
 'gurita hist -x tip --hue smoker --stat proportion --multiple dodge --out "${IMG_OUT_DIR}/hist.tip.proportion.smoker.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --hue smoker --stat proportion --multiple dodge --indnorm < tips.csv' \
 'gurita hist -x tip --hue smoker --stat proportion --multiple dodge --indnorm --out "${IMG_OUT_DIR}/hist.tip.proportion.smoker.indnorm.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --kde < tips.csv' \
 'gurita hist -x tip --kde --out "${IMG_OUT_DIR}/hist.tip.kde.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --nofill < tips.csv' \
 'gurita hist -x tip --nofill --out "${IMG_OUT_DIR}/hist.tip.nofill.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --element step < tips.csv' \
 'gurita hist -x tip --element step --out "${IMG_OUT_DIR}/hist.tip.step.png" < "${DATA_DIR}/tips.csv"'

	
################################################################################

run_example \
 'gurita hist -x tip --element poly < tips.csv' \
 'gurita hist -x tip --element poly --out "${IMG_OUT_DIR}/hist.tip.poly.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --logy < tips.csv' \
 'gurita hist -x tip --logy --out "${IMG_OUT_DIR}/hist.tip.logy.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --xlim 3 8 < tips.csv' \
 'gurita hist -x tip --xlim 3 8 --out "${IMG_OUT_DIR}/hist.tip.xlim.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita hist -x tip --fcol day < tips.csv' \
 'gurita hist -x tip --fcol day --out "${IMG_OUT_DIR}/hist.tip.day.png" < "${DATA_DIR}/tips.csv"'

################################################################################

run_example \
 'gurita line -x timepoint -y signal < fmri.csv' \
 'gurita line -x timepoint -y signal --out "${IMG_OUT_DIR}/line.timepoint.signal.png" < "${DATA_DIR}/fmri.csv"'
	
################################################################################

run_example \
 'gurita line -x timepoint -y signal --hue event < fmri.csv' \
 'gurita line -x timepoint -y signal --hue event --out "${IMG_OUT_DIR}/line.timepoint.signal.event.png" < "${DATA_DIR}/fmri.csv"'
	
################################################################################

run_example \
 'gurita line -x timepoint -y signal --hue event --hueorder cue stim < fmri.csv' \
 'gurita line -x timepoint -y signal --hue event --hueorder cue stim --out "${IMG_OUT_DIR}/line.timepoint.signal.event.hue.png" < "${DATA_DIR}/fmri.csv"'
	
################################################################################

run_example \
 'gurita line -x timepoint -y signal --logx < fmri.csv' \
 'gurita line -x timepoint -y signal --logx --out "${IMG_OUT_DIR}/line.timepoint.signal.logx.png" < "${DATA_DIR}/fmri.csv"'
 
################################################################################

run_example \
 'gurita line -x timepoint -y signal --xlim 5 15.5 < fmri.csv' \
 'gurita line -x timepoint -y signal --xlim 5 15.5 --out "${IMG_OUT_DIR}/line.timepoint.signal.xlim.png" < "${DATA_DIR}/fmri.csv"'
	
################################################################################

run_example \
 'gurita line -x timepoint -y signal --fcol event < fmri.csv' \
 'gurita line -x timepoint -y signal --fcol event --out "${IMG_OUT_DIR}/line.timepoint.signal.event.facet.png" < "${DATA_DIR}/fmri.csv"'

################################################################################

run_example \
 'gurita lmplot -x sepal_length -y petal_length < iris.csv' \
 'gurita lmplot -x sepal_length -y petal_length --out "${IMG_OUT_DIR}/lmplot.sepal_length.petal_length.png" < "${DATA_DIR}/iris.csv"'
	
################################################################################

run_example \
 'gurita lmplot -x sepal_length -y petal_length --hue species < iris.csv' \
 'gurita lmplot -x sepal_length -y petal_length --hue species --out "${IMG_OUT_DIR}/lmplot.sepal_length.petal_length.species.png" < "${DATA_DIR}/iris.csv"'
	
################################################################################

run_example \
 'gurita lmplot -x sepal_length -y petal_length --fcol species < iris.csv' \
 'gurita lmplot -x sepal_length -y petal_length --fcol species --out "${IMG_OUT_DIR}/lmplot.sepal_length.petal_length.species.facets.png" < "${DATA_DIR}/iris.csv"'
	
################################################################################

run_example \
 'gurita pair < iris.csv' \
 'gurita pair --out "${IMG_OUT_DIR}/pair.png" < "${DATA_DIR}/iris.csv"'
	
################################################################################

run_example \
 'gurita pair -c sepal_length petal_length species < iris.csv' \
 'gurita pair -c sepal_length petal_length species --out "${IMG_OUT_DIR}/pair.columns.png" < "${DATA_DIR}/iris.csv"'
	
################################################################################

run_example \
 'gurita pair -c sepal_length petal_length species --rxtl 90 < iris.csv' \
 'gurita pair -c sepal_length petal_length species --rxtl 90 --out "${IMG_OUT_DIR}/pair.columns.rxtl.png" < "${DATA_DIR}/iris.csv"'
	
################################################################################

run_example \
 'gurita pair --hue species < iris.csv' \
 'gurita pair --hue species --out "${IMG_OUT_DIR}/pair.species.png" < "${DATA_DIR}/iris.csv"'
	
################################################################################

run_example \
 'gurita pair --corner < iris.csv' \
 'gurita pair --corner --out "${IMG_OUT_DIR}/pair.corner.png" < "${DATA_DIR}/iris.csv"'
	
################################################################################

run_example \
 'gurita pair --kind kde < iris.csv' \
 'gurita pair --kind kde --out "${IMG_OUT_DIR}/pair.kde.png" < "${DATA_DIR}/iris.csv"'
	
################################################################################

run_example \
 'gurita pair --kind hist < iris.csv' \
 'gurita pair --kind hist --out "${IMG_OUT_DIR}/pair.hist.png" < "${DATA_DIR}/iris.csv"'
	
################################################################################

run_example \
 'gurita pair --kind reg < iris.csv' \
 'gurita pair --kind reg --out "${IMG_OUT_DIR}/pair.reg.png" < "${DATA_DIR}/iris.csv"'
	
################################################################################

run_example \
 'gurita point -y age -x class < titanic.csv' \
 'gurita point -y age -x class --out "${IMG_OUT_DIR}/point.class.age.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita point -x age -y class --orient h < titanic.csv' \
 'gurita point -x age -y class --orient h --out "${IMG_OUT_DIR}/point.age.class.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita point -y age -x class --order First Second Third < titanic.csv' \
 'gurita point -y age -x class --order First Second Third --out "${IMG_OUT_DIR}/point.class.age.order.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita point -y age -x class --hue sex < titanic.csv' \
 'gurita point -y age -x class --hue sex --out "${IMG_OUT_DIR}/point.class.age.sex.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita point -y age -x class --hue sex --hueorder female male < titanic.csv' \
 'gurita point -y age -x class --hue sex --hueorder female male --out "${IMG_OUT_DIR}/point.class.age.sex.hueorder.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita point -y age -x class --order First Second Third --hue sex --hueorder female male < titanic.csv' \
 'gurita point -y age -x class --order First Second Third --hue sex --hueorder female male --out "${IMG_OUT_DIR}/point.class.age.sex.order.hueorder.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita point -y age -x class --logy < titanic.csv' \
 'gurita point -y age -x class --logy --out "${IMG_OUT_DIR}/point.class.age.logx.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita point -y age -x class --ylim 10 30 < titanic.csv' \
 'gurita point -y age -x class --ylim 10 30 --out "${IMG_OUT_DIR}/point.class.age.ylim.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita point -y age -x class --fcol sex < titanic.csv' \
 'gurita point -y age -x class --fcol sex --out "${IMG_OUT_DIR}/point.class.age.sex.facets.png" < "${DATA_DIR}/titanic.csv"'
	
################################################################################

run_example \
 'gurita scatter -x total_bill -y tip < tips.csv' \
 'gurita scatter -x total_bill -y tip --out "${IMG_OUT_DIR}/scatter.total_bill.tip.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita scatter -x day -y tip < tips.csv' \
 'gurita scatter -x day -y tip --out "${IMG_OUT_DIR}/scatter.day.tip.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita scatter -x total_bill -y tip --hue day < tips.csv' \
 'gurita scatter -x total_bill -y tip --hue day --out "${IMG_OUT_DIR}/scatter.total_bill.tip.day.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita scatter -x total_bill -y tip --hue size < tips.csv' \
 'gurita scatter -x total_bill -y tip --hue size --out "${IMG_OUT_DIR}/scatter.total_bill.tip.size.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita scatter -x total_bill -y tip --hue day --dotstyle sex < tips.csv' \
 'gurita scatter -x total_bill -y tip --hue day --dotstyle sex --out "${IMG_OUT_DIR}/scatter.total_bill.tip.day.dotstyle.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita scatter -x sepal_length -y sepal_width --dotsize petal_length < iris.csv' \
 'gurita scatter -x sepal_length -y sepal_width --dotsize petal_length --out "${IMG_OUT_DIR}/scatter.sepal_length.sepal_width.png" < "${DATA_DIR}/iris.csv"'
	
################################################################################

run_example \
 'gurita scatter -x sepal_length -y sepal_width --dotsize petal_length --dotsizerange 10 200 < iris.csv' \
 'gurita scatter -x sepal_length -y sepal_width --dotsize petal_length --dotsizerange 10 200 --out "${IMG_OUT_DIR}/scatter.sepal_length.sepal_width.sizerange.png" < "${DATA_DIR}/iris.csv"'
	
################################################################################

run_example \
 'gurita scatter -x total_bill -y tip --dotalpha 1 --dotlinewidth 0.5 --dotlinecolour black < tips.csv' \
 'gurita scatter -x total_bill -y tip --dotalpha 1 --dotlinewidth 0.5 --dotlinecolour black --out "${IMG_OUT_DIR}/scatter.total_bill.tip.alpha.width.colour.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita scatter -x total_bill -y tip --logx < tips.csv' \
 'gurita scatter -x total_bill -y tip --logx --out "${IMG_OUT_DIR}/scatter.total_bill.tip.logx.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita scatter -x total_bill -y tip --xlim 20 40 < tips.csv' \
 'gurita scatter -x total_bill -y tip --xlim 20 40 --out "${IMG_OUT_DIR}/scatter.total_bill.tip.xlim.png" < "${DATA_DIR}/tips.csv"'
	
################################################################################

run_example \
 'gurita scatter -x total_bill -y tip --fcol smoker < tips.csv' \
 'gurita scatter -x total_bill -y tip --fcol smoker --out "${IMG_OUT_DIR}/scatter.total_bill.tip.smoker.png" < "${DATA_DIR}/tips.csv"'

################################################################################

run_example \
 'gurita strip -y age < titanic.csv' \
 'gurita strip -y age --out "${IMG_OUT_DIR}/strip.age.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita strip -y age -x class < titanic.csv' \
 'gurita strip -y age -x class --out "${IMG_OUT_DIR}/strip.class.age.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita strip -x age -y class --orient h < titanic.csv' \
 'gurita strip -x age -y class --orient h --out "${IMG_OUT_DIR}/strip.age.class.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita strip -y age -x class --order First Second Third < titanic.csv' \
 'gurita strip -y age -x class --order First Second Third --out "${IMG_OUT_DIR}/strip.class.age.order.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita strip -y age -x class --hue sex < titanic.csv' \
 'gurita strip -y age -x class --hue sex --out "${IMG_OUT_DIR}/strip.class.age.sex.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita strip -y age -x class --hue sex --dodge < titanic.csv' \
 'gurita strip -y age -x class --hue sex --dodge --out "${IMG_OUT_DIR}/strip.class.age.sex.dodge.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita strip -y age -x class --hue sex --hueorder female male < titanic.csv' \
 'gurita strip -y age -x class --hue sex --hueorder female male --out "${IMG_OUT_DIR}/strip.class.age.sex.hueorder.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita strip -y age -x class --order First Second Third --hue sex --hueorder female male < titanic.csv' \
 'gurita strip -y age -x class --order First Second Third --hue sex --hueorder female male --out "${IMG_OUT_DIR}/strip.class.age.sex.order.hueorder.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita strip -y age -x class --logy < titanic.csv' \
 'gurita strip -y age -x class --logy --out "${IMG_OUT_DIR}/strip.class.age.logy.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita strip -y age -x class --ylim 10 30 < titanic.csv' \
 'gurita strip -y age -x class --ylim 10 30 --out "${IMG_OUT_DIR}/strip.class.age.ylim.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita strip -y age -x class --fcol sex < titanic.csv' \
 'gurita strip -y age -x class --fcol sex --out "${IMG_OUT_DIR}/strip.class.age.sex.facet.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita strip -y age -x class --hue class < titanic.csv' \
 'gurita strip -y age -x class --hue class --out "${IMG_OUT_DIR}/strip.class.age.hue.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita swarm -y age < titanic.csv' \
 'gurita swarm -y age --out "${IMG_OUT_DIR}/swarm.age.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita swarm -y age -x class < titanic.csv' \
 'gurita swarm -y age -x class --out "${IMG_OUT_DIR}/swarm.class.age.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita swarm -x age -y class --orient h < titanic.csv' \
 'gurita swarm -x age -y class --orient h --out "${IMG_OUT_DIR}/swarm.age.class.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita swarm -y age -x class --order First Second Third < titanic.csv' \
 'gurita swarm -y age -x class --order First Second Third --out "${IMG_OUT_DIR}/swarm.class.age.order.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita swarm -y age -x class --hue sex < titanic.csv' \
 'gurita swarm -y age -x class --hue sex --out "${IMG_OUT_DIR}/swarm.class.age.sex.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita swarm -y age -x class --hue sex --dodge < titanic.csv' \
 'gurita swarm -y age -x class --hue sex --dodge --out "${IMG_OUT_DIR}/swarm.class.age.sex.dodge.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita swarm -y age -x class --hue sex --hueorder female male < titanic.csv' \
 'gurita swarm -y age -x class --hue sex --hueorder female male --out "${IMG_OUT_DIR}/swarm.class.age.sex.hueorder.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita swarm -y age -x class --order First Second Third --hue sex --hueorder female male < titanic.csv' \
 'gurita swarm -y age -x class --order First Second Third --hue sex --hueorder female male --out "${IMG_OUT_DIR}/swarm.class.age.sex.order.hueorder.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita swarm -y age -x class --logy < titanic.csv' \
 'gurita swarm -y age -x class --logy --out "${IMG_OUT_DIR}/swarm.class.age.logy.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita swarm -y age -x class --ylim 10 30 < titanic.csv' \
 'gurita swarm -y age -x class --ylim 10 30 --out "${IMG_OUT_DIR}/swarm.class.age.logy.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita swarm -y age -x class --fcol sex < titanic.csv' \
 'gurita swarm -y age -x class --fcol sex --out "${IMG_OUT_DIR}/swarm.class.age.sex.facets.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita swarm -y age -x class --hue class < titanic.csv' \
 'gurita swarm -y age -x class --hue class --out "${IMG_OUT_DIR}/swarm.class.age.hue.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita violin -y age < titanic.csv' \
 'gurita violin -y age --out "${IMG_OUT_DIR}/violin.age.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita violin -y age -x class < titanic.csv' \
 'gurita violin -y age -x class --out "${IMG_OUT_DIR}/violin.class.age.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita violin -x age -y class --orient h < titanic.csv' \
 'gurita violin -x age -y class --orient h --out "${IMG_OUT_DIR}/violin.age.class.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita violin -y age -x class --order First Second Third < titanic.csv' \
 'gurita violin -y age -x class --order First Second Third --out "${IMG_OUT_DIR}/violin.class.age.order.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita violin -y age -x class --hue sex < titanic.csv' \
 'gurita violin -y age -x class --hue sex --out "${IMG_OUT_DIR}/violin.class.age.sex.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita violin -y age -x class --hue sex --hueorder female male < titanic.csv' \
 'gurita violin -y age -x class --hue sex --hueorder female male --out "${IMG_OUT_DIR}/violin.class.age.sex.hueorder.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita violin -y age -x class --order First Second Third --hue sex --hueorder female male < titanic.csv' \
 'gurita violin -y age -x class --order First Second Third --hue sex --hueorder female male --out "${IMG_OUT_DIR}/violin.class.age.sex.order.hueorder.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita violin -y age -x class --logy < titanic.csv' \
 'gurita violin -y age -x class --logy --out "${IMG_OUT_DIR}/violin.class.age.logy.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita violin -y age -x class --ylim 10 30 < titanic.csv' \
 'gurita violin -y age -x class --ylim 10 30 --out "${IMG_OUT_DIR}/violin.class.age.limy.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita violin -y age -x class --fcol sex < titanic.csv' \
 'gurita violin -y age -x class --fcol sex --out "${IMG_OUT_DIR}/violin.class.age.sex.facet.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita violin -y age -x class --hue class < titanic.csv' \
 'gurita violin -y age -x class --hue class --out "${IMG_OUT_DIR}/violin.class.age.hue.png" < "${DATA_DIR}/titanic.csv"'

################################################################################

run_example \
 'gurita corr -c sepal_length sepal_width < iris.csv' \
 'gurita corr -c sepal_length sepal_width < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.corr.sepal_length.sepal_width.txt"'

################################################################################

run_example \
 'gurita corr < iris.csv' \
 'gurita corr < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.corr.txt"'

################################################################################

run_example \
 'gurita corr -c sepal_length petal_length petal_width < iris.csv' \
 'gurita corr -c sepal_length petal_length petal_width < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.sepal_length.petal_length.petal_width.txt"'

################################################################################

run_example \
 'gurita corr --col sepal_length sepal_width --method spearman < iris.csv' \
 'gurita corr --col sepal_length sepal_width --method spearman < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.corr.sepal_length.sepal_width.spearman.txt"'

################################################################################

run_example \
 'gurita corr + heatmap -x col1 -y col2 -v corr < iris.csv' \
 'gurita corr + heatmap -x col1 -y col2 -v corr --out "${IMG_OUT_DIR}/iris.corr.heatmap.png" < "${DATA_DIR}/iris.csv"'

################################################################################

run_example \
 'gurita cut -c sepal_length species < example.csv' \
 'gurita cut -c sepal_length species > "${FILE_OUT_DIR}/example.cut.sepal_length.species.txt" <<EOF
sepal_length,sepal_width,petal_length,petal_width,species
6.3,3.4,5.6,2.4,virginica
6.3,2.5,5.0,1.9,virginica
4.8,3.4,1.9,0.2,setosa
6.3,3.3,4.7,1.6,versicolor
6.4,3.2,4.5,1.5,versicolor
4.7,3.2,1.3,0.2,setosa
6.4,2.8,5.6,2.1,virginica
5.4,3.9,1.7,0.4,setosa
5.9,3.0,4.2,1.5,versicolor
5.2,3.5,1.5,0.2,setosa
EOF'

################################################################################

run_example \
 'gurita cut -c sepal_length species --invert < example.csv' \
 'gurita cut -c sepal_length species --invert > "${FILE_OUT_DIR}/example.cut.invert.sepal_length.species.txt" <<EOF
sepal_length,sepal_width,petal_length,petal_width,species
6.3,3.4,5.6,2.4,virginica
6.3,2.5,5.0,1.9,virginica
4.8,3.4,1.9,0.2,setosa
6.3,3.3,4.7,1.6,versicolor
6.4,3.2,4.5,1.5,versicolor
4.7,3.2,1.3,0.2,setosa
6.4,2.8,5.6,2.1,virginica
5.4,3.9,1.7,0.4,setosa
5.9,3.0,4.2,1.5,versicolor
5.2,3.5,1.5,0.2,setosa
EOF'

################################################################################

run_example \
 'gurita dropna < missing.csv' \
 'gurita dropna > "${FILE_OUT_DIR}/missing.dropna.txt" <<EOF 
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,
4.9,3.0,1.4,0.2,virginica
4.7,,1.3,0.2,setosa
EOF'

################################################################################

run_example \
 'gurita dropna --axis columns < missing.csv' \
 'gurita dropna --axis columns > "${FILE_OUT_DIR}/missing.dropna.axis.txt" <<EOF 
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,
4.9,3.0,1.4,0.2,virginica
4.7,,1.3,0.2,setosa
EOF'

################################################################################

run_example \
 'gurita dropna --col species < missing.csv' \
 'gurita dropna --col species > "${FILE_OUT_DIR}/missing.dropna.species.txt" <<EOF 
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,
4.9,3.0,1.4,0.2,virginica
4.7,,1.3,0.2,setosa
EOF'
 

################################################################################

run_example \
 "gurita eval 'sepal_area = sepal_length * sepal_width * 0.5' + head < iris.csv" \
 "gurita eval 'sepal_area = sepal_length * sepal_width * 0.5' + head < ${DATA_DIR}/iris.csv > ${FILE_OUT_DIR}/iris.eval.head.txt"

################################################################################

run_example \
 "gurita eval 'dist = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)' < points.csv" \
 "gurita eval 'dist = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)' > ${FILE_OUT_DIR}/points.eval.sqrt.txt <<EOF
x1,y1,x2,y2
0,0,3,4
10,0,10,0
18,12,-4,55
EOF"

################################################################################

run_example \
 'gurita gmm + head < iris.csv' \
 'gurita gmm + head < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.gmm.head.txt"'

################################################################################

run_example \
 'gurita gmm + describe -c cluster < iris.csv' \
 'gurita gmm + describe -c cluster < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.gmm.describe.cluster.txt"'

################################################################################

run_example \
 'gurita gmm + box -x cluster -y petal_length < iris.csv' \
 'gurita gmm + box -x cluster -y petal_length --out "${IMG_OUT_DIR}/box.cluster.petal_length.png" < "${DATA_DIR}/iris.csv"'

################################################################################

run_example \
 'gurita gmm -n 3 + groupby -k cluster < iris.csv' \
 'gurita gmm -n 3 + groupby -k cluster < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.gmm.groupby.cluster.txt"'

################################################################################

run_example \
 'gurita gmm --name grouping + head < iris.csv' \
 'gurita gmm --name grouping + head < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.gmm.name.head.txt"'

################################################################################

run_example \
 'gurita groupby --key embark_town < titanic.csv' \
 'gurita groupby --key embark_town < "${DATA_DIR}/titanic.csv" > "${FILE_OUT_DIR}/titanic.groupby.embark_town.txt"'

################################################################################

run_example \
 'gurita groupby --key embark_town class < titanic.csv' \
 'gurita groupby --key embark_town class < "${DATA_DIR}/titanic.csv" > "${FILE_OUT_DIR}/titanic.groupby.embark_town.class.txt"'

################################################################################

run_example \
 'gurita groupby --key embark_town class sex < titanic.csv' \
 'gurita groupby --key embark_town class sex < "${DATA_DIR}/titanic.csv" > "${FILE_OUT_DIR}/titanic.groupby.embark_town.class.sex.txt"'

################################################################################

run_example \
 'gurita groupby --key embark_town --val age --fun mean < titanic.csv' \
 'gurita groupby --key embark_town --val age --fun mean < "${DATA_DIR}/titanic.csv" > "${FILE_OUT_DIR}/titanic.groupby.embark_town.age.mean.txt"'

################################################################################

run_example \
 'gurita groupby --key embark_town --val age --fun mean max min < titanic.csv' \
 'gurita groupby --key embark_town --val age --fun mean max min < "${DATA_DIR}/titanic.csv" > "${FILE_OUT_DIR}/titanic.groupby.embark_town.age.mean.max.min.txt"' 

################################################################################

run_example \
 'gurita groupby --key embark_town --val age fare --fun mean max min < titanic.csv' \
 'gurita groupby --key embark_town --val age fare --fun mean max min < "${DATA_DIR}/titanic.csv" > "${FILE_OUT_DIR}/titanic.groupby.embark_town.age.fare.mean.max.min.txt"'

################################################################################

run_example \
 'gurita groupby --key embark_town class --val age fare --fun mean max min < titanic.csv' \
 'gurita groupby --key embark_town class --val age fare --fun mean max min < "${DATA_DIR}/titanic.csv" > "${FILE_OUT_DIR}/titanic.groupby.embark_town.class.age.fare.mean.max.min.txt"' 

################################################################################

run_example \
 'gurita head 5 < example.csv' \
 'gurita head 5 > "${FILE_OUT_DIR}/example.head.txt" <<EOF
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
4.6,3.1,1.5,0.2,setosa
5.0,3.6,1.4,0.2,setosa
5.4,3.9,1.7,0.4,setosa
4.6,3.4,1.4,0.3,setosa
5.0,3.4,1.5,0.2,setosa
4.4,2.9,1.4,0.2,setosa
4.9,3.1,1.5,0.1,setosa
EOF'

################################################################################

run_example \
 'gurita head 5 + tail 3 < example.csv' \
 'gurita head 5 + tail 3 > "${FILE_OUT_DIR}/example.head.tail.txt" <<EOF
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
4.6,3.1,1.5,0.2,setosa
5.0,3.6,1.4,0.2,setosa
5.4,3.9,1.7,0.4,setosa
4.6,3.4,1.4,0.3,setosa
5.0,3.4,1.5,0.2,setosa
4.4,2.9,1.4,0.2,setosa
4.9,3.1,1.5,0.1,setosa
EOF'

################################################################################

run_example \
 'gurita head 1 < example.csv' \
 'gurita head 1 > "${FILE_OUT_DIR}/example.head.1.txt" <<EOF
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
4.6,3.1,1.5,0.2,setosa
5.0,3.6,1.4,0.2,setosa
5.4,3.9,1.7,0.4,setosa
4.6,3.4,1.4,0.3,setosa
5.0,3.4,1.5,0.2,setosa
4.4,2.9,1.4,0.2,setosa
4.9,3.1,1.5,0.1,setosa
EOF'

################################################################################

run_example \
 'gurita head -3 < example.csv' \
 'gurita head -3 > "${FILE_OUT_DIR}/example.head.negative.3.txt" <<EOF
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
4.6,3.1,1.5,0.2,setosa
5.0,3.6,1.4,0.2,setosa
5.4,3.9,1.7,0.4,setosa
4.6,3.4,1.4,0.3,setosa
5.0,3.4,1.5,0.2,setosa
4.4,2.9,1.4,0.2,setosa
4.9,3.1,1.5,0.1,setosa
EOF'

################################################################################

run_example \
 'gurita kmeans + head < iris.csv' \
 'gurita kmeans + head < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.kmeans.head.txt"'

################################################################################

run_example \
 'gurita kmeans + describe -c cluster < iris.csv' \
 'gurita kmeans + describe -c cluster < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.kmeans.describe.cluster.txt"' 

################################################################################

run_example \
 'gurita kmeans + box -x cluster -y petal_length < iris.csv' \
 'gurita kmeans + box -x cluster -y petal_length --out "${IMG_OUT_DIR}/box.cluster.petal_length.png" < "${DATA_DIR}/iris.csv"'

################################################################################

run_example \
 'gurita kmeans -n 3 + groupby -k cluster < iris.csv' \
 'gurita kmeans -n 3 + groupby -k cluster < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.kmeans.groupby.cluster.txt"'

################################################################################

run_example \
 'gurita kmeans --name grouping + head < iris.csv' \
 'gurita kmeans --name grouping + head < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.kmeans.name.head.txt"'

################################################################################

run_example \
 'gurita melt + head 15 < example.csv' \
 'gurita melt + head 15 > "${FILE_OUT_DIR}/example.melt.head.15.txt" <<EOF
person,level,sun,mon,tue,wed,thu,fri,sat
Alice,A1,0,8,8,4,1,4,3
Bob,B3,4,0,0,4,6,0,3
Wei,B1,0,0,8,8,8,4,3
Imani,A2,0,8,8,8,4,5,0
Diego,C2,3,7,7,2,1,1,4
EOF'

################################################################################

run_example \
 'gurita melt -i person + head 15 < example.csv' \
 'gurita melt -i person + head 15 > "${FILE_OUT_DIR}/example.melt.index.person.head.15.txt" <<EOF
person,level,sun,mon,tue,wed,thu,fri,sat
Alice,A1,0,8,8,4,1,4,3
Bob,B3,4,0,0,4,6,0,3
Wei,B1,0,0,8,8,8,4,3
Imani,A2,0,8,8,8,4,5,0
Diego,C2,3,7,7,2,1,1,4
EOF'

################################################################################

run_example \
 'gurita melt -i person level + head 15 < example.csv' \
 'gurita melt -i person level + head 15 > "${FILE_OUT_DIR}/example.melt.index.person.level.head.15.txt" <<EOF
person,level,sun,mon,tue,wed,thu,fri,sat
Alice,A1,0,8,8,4,1,4,3
Bob,B3,4,0,0,4,6,0,3
Wei,B1,0,0,8,8,8,4,3
Imani,A2,0,8,8,8,4,5,0
Diego,C2,3,7,7,2,1,1,4
EOF'


################################################################################

run_example \
 'gurita melt -i person -v level sat sun < example.csv' \
 'gurita melt -i person -v level sat sun > "${FILE_OUT_DIR}/example.melt.person.level.sat.sun.txt" << EOF
person,level,sun,mon,tue,wed,thu,fri,sat
Alice,A1,0,8,8,4,1,4,3
Bob,B3,4,0,0,4,6,0,3
Wei,B1,0,0,8,8,8,4,3
Imani,A2,0,8,8,8,4,5,0
Diego,C2,3,7,7,2,1,1,4
EOF'

################################################################################

run_example \
 'gurita melt --varname key + head 10 < example.csv' \
 'gurita melt --varname key + head 10 > "${FILE_OUT_DIR}/example.melt.varname.key.head.10.txt" <<EOF 
person,level,sun,mon,tue,wed,thu,fri,sat
Alice,A1,0,8,8,4,1,4,3
Bob,B3,4,0,0,4,6,0,3
Wei,B1,0,0,8,8,8,4,3
Imani,A2,0,8,8,8,4,5,0
Diego,C2,3,7,7,2,1,1,4
EOF'

################################################################################

run_example \
 'gurita melt --valname data + head 10 < example.csv' \
 'gurita melt --valname data + head 10 > "${FILE_OUT_DIR}/example.melt.valname.data.head.10.txt" <<EOF
person,level,sun,mon,tue,wed,thu,fri,sat
Alice,A1,0,8,8,4,1,4,3
Bob,B3,4,0,0,4,6,0,3
Wei,B1,0,0,8,8,8,4,3
Imani,A2,0,8,8,8,4,5,0
Diego,C2,3,7,7,2,1,1,4
EOF'

################################################################################

run_example \
 'gurita melt --varname key --valname data + head 10 < example.csv' \
 'gurita melt --varname key --valname data + head 10 > "${FILE_OUT_DIR}/example.melt.varname.key.valname.data.head.10.txt" <<EOF
person,level,sun,mon,tue,wed,thu,fri,sat
Alice,A1,0,8,8,4,1,4,3
Bob,B3,4,0,0,4,6,0,3
Wei,B1,0,0,8,8,8,4,3
Imani,A2,0,8,8,8,4,5,0
Diego,C2,3,7,7,2,1,1,4
EOF'

################################################################################

run_example \
 'gurita normtest < iris.csv' \
 'gurita normtest < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.normtest.txt"' 

################################################################################

run_example \
 'gurita normtest -c sepal_length < iris.csv' \
 'gurita normtest -c sepal_length < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.normtest.sepal_length.txt"'

################################################################################

run_example \
 'gurita normtest -c sepal_length petal_length < iris.csv' \
 'gurita normtest -c sepal_length petal_length < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.normtest.sepal_length.petal_length.txt"' 

################################################################################

run_example \
 'gurita normtest -c species < iris.csv' \
 'gurita normtest -c species < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.normtest.species.txt"' 

################################################################################

run_example \
 'gurita normtest --alpha 0.06 < iris.csv' \
 'gurita normtest --alpha 0.06 < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.normtest.alpha.txt"' 

################################################################################

run_example \
 'gurita normtest --pvalue --stat < iris.csv' \
 'gurita normtest --pvalue --stat < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.normtest.pvalue.stat.txt"' 

################################################################################

run_example \
 'gurita normtest --method shapiro < iris.csv' \
 'gurita normtest --method shapiro < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.normtest.method.shapiro.txt"' 

################################################################################

run_example \
 'gurita outlier -c sepal_width + head < iris.csv' \
 'gurita outlier -c sepal_width + head < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.outlier.sepal_width.head.txt"' 


################################################################################

run_example \
 'gurita outlier -c sepal_length petal_width + head < iris.csv' \
 'gurita outlier -c sepal_length petal_width + head < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.outlier.sepal_width.petal_width.txt"' 

################################################################################

run_example \
 'gurita outlier --suffix out + head < iris.csv' \
 'gurita outlier --suffix out + head < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.outlier.suffix.out.head.txt"' 

################################################################################

run_example \
 'gurita pca + head < iris.csv' \
 'gurita pca + head < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.pca.head.txt"' 

################################################################################

run_example \
 'gurita pca + scatter -x pc1 -y pc2 < iris.csv' \
 'gurita pca + scatter -x pc1 -y pc2 --out "${IMG_OUT_DIR}/scatter.pc1.pc2.png" < "${DATA_DIR}/iris.csv"' 

################################################################################

run_example \
 'gurita pca -n 3 + head < iris.csv' \
 'gurita pca -n 3 + head < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.pca.n.3.head.txt"' 

################################################################################

run_example \
 'gurita pca --prefix comp + head < iris.csv' \
 'gurita pca --prefix comp + head < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.pca.prefix.comp.head.txt"'

################################################################################

run_example \
 'gurita pivot -i person -c feature -v val < example.csv' \
 'gurita pivot -i person -c feature -v val > "${FILE_OUT_DIR}/example.pivot.person.feature.val.txt" <<EOF
person,feature,val
Alice,level,A1
Bob,level,B3
Alice,mon,8
Bob,mon,0
Alice,tue,8
Bob,tue,0
Alice,wed,4
Bob,wed,4
Alice,thu,1
Bob,thu,6
Alice,fri,4
Bob,fri,0
EOF'


################################################################################

run_example \
 'gurita pivot -i feature -c person -v val < example.csv' \
 'gurita pivot -i feature -c person -v val > "${FILE_OUT_DIR}/example.pivot.feature.person.val.txt" <<EOF
person,feature,val
Alice,level,A1
Bob,level,B3
Alice,mon,8
Bob,mon,0
Alice,tue,8
Bob,tue,0
Alice,wed,4
Bob,wed,4
Alice,thu,1
Bob,thu,6
Alice,fri,4
Bob,fri,0
EOF'

################################################################################

run_example \
 'gurita pivot -i person -c feature -v val + melt -i person -v mon tue wed thu fri level --varname feature --valname val < example.csv' \
 'gurita pivot -i person -c feature -v val + melt -i person -v mon tue wed thu fri level --varname feature --valname val > "${FILE_OUT_DIR}/example.pivot.person.feature.val.melt.txt" <<EOF
person,feature,val
Alice,level,A1
Bob,level,B3
Alice,mon,8
Bob,mon,0
Alice,tue,8
Bob,tue,0
Alice,wed,4
Bob,wed,4
Alice,thu,1
Bob,thu,6
Alice,fri,4
Bob,fri,0
EOF'

################################################################################

run_example \
 'gurita pivot -i feature -c person -v val + melt -i feature -v Alice Bob --varname person --valname val < example.csv' \
 'gurita pivot -i feature -c person -v val + melt -i feature -v Alice Bob --varname person --valname val > "${FILE_OUT_DIR}/example.pivot.person.feature.val.melt.alice.bob.txt" <<EOF
person,feature,val
Alice,level,A1
Bob,level,B3
Alice,mon,8
Bob,mon,0
Alice,tue,8
Bob,tue,0
Alice,wed,4
Bob,wed,4
Alice,thu,1
Bob,thu,6
Alice,fri,4
Bob,fri,0
EOF'

################################################################################

run_example \
 'gurita pivot -i person -c feature -v val < missing.csv' \
 'gurita pivot -i person -c feature -v val > "${FILE_OUT_DIR}/example.pivot.person.feature.val.missing.txt" <<EOF
person,feature,val
Bob,level,B3
Alice,mon,8
Bob,mon,0
Alice,tue,8
Bob,tue,0
Alice,wed,4
Bob,wed,4
Alice,thu,1
Bob,thu,6
Alice,fri,4
Bob,fri,0
EOF'

################################################################################

run_example \
 'gurita pivot -i person level -c variable -v value < example.csv' \
 'gurita pivot -i person level -c variable -v value > "${FILE_OUT_DIR}/example.pivot.person.level.variable.value.txt" <<EOF
person,level,variable,value
Alice,A1,sun,0
Bob,B3,sun,4
Wei,B1,sun,0
Imani,A2,sun,0
Diego,C2,sun,3
Alice,A1,mon,8
Bob,B3,mon,0
Wei,B1,mon,0
Imani,A2,mon,8
Diego,C2,mon,7
Alice,A1,tue,8
Bob,B3,tue,0
Wei,B1,tue,8
Imani,A2,tue,8
Diego,C2,tue,7
EOF'


################################################################################

run_example \
 'gurita pivot -i level variable -c person -v value < example.csv' \
 'gurita pivot -i level variable -c person -v value > "${FILE_OUT_DIR}/example.pivot.level.variable.person.value.txt" <<EOF
person,level,variable,value
Alice,A1,sun,0
Bob,B3,sun,4
Wei,B1,sun,0
Imani,A2,sun,0
Diego,C2,sun,3
Alice,A1,mon,8
Bob,B3,mon,0
Wei,B1,mon,0
Imani,A2,mon,8
Diego,C2,mon,7
Alice,A1,tue,8
Bob,B3,tue,0
Wei,B1,tue,8
Imani,A2,tue,8
Diego,C2,tue,7
EOF'

################################################################################

run_example \
 'gurita pivot -i person -c feature -v val -f sample < example.csv' \
 'gurita pivot -i person -c feature -v val -f sample > "${FILE_OUT_DIR}/example.pivot.person.feature.val.sample.txt" <<EOF 
person,feature,val
Alice,level,B2
Alice,level,A1
Bob,level,B3
Alice,mon,8
Bob,mon,0
Alice,tue,8
Bob,tue,0
Alice,wed,4
Bob,wed,4
Alice,thu,1
Bob,thu,6
Alice,fri,4
Bob,fri,0
EOF'

################################################################################

run_example \
 'gurita sample 10 < iris.csv' \
 'gurita sample 10 < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.sample.10.txt"'

################################################################################

run_example \
 'gurita sample 0.05 < iris.csv' \
 'gurita sample 0.05 < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.sample.05.txt"'

################################################################################

run_example \
 'gurita sort -c sepal_width < example.csv' \
 'gurita sort -c sepal_width > "${FILE_OUT_DIR}/example.sort.sepal_width.txt" <<EOF
sepal_length,sepal_width,petal_length,petal_width,species
6.3,3.4,5.6,2.4,virginica
6.3,2.5,5.0,1.9,virginica
4.8,3.4,1.9,0.2,setosa
6.3,3.3,4.7,1.6,versicolor
6.4,3.2,4.5,1.5,versicolor
4.7,3.2,1.3,0.2,setosa
6.4,2.8,5.6,2.1,virginica
5.4,3.9,1.7,0.4,setosa
5.9,3.0,4.2,1.5,versicolor
5.2,3.5,1.5,0.2,setosa
EOF'

################################################################################

run_example \
 'gurita sort -c species < example.csv' \
 'gurita sort -c species > "${FILE_OUT_DIR}/example.sort.species.txt" <<EOF 
sepal_length,sepal_width,petal_length,petal_width,species
6.3,3.4,5.6,2.4,virginica
6.3,2.5,5.0,1.9,virginica
4.8,3.4,1.9,0.2,setosa
6.3,3.3,4.7,1.6,versicolor
6.4,3.2,4.5,1.5,versicolor
4.7,3.2,1.3,0.2,setosa
6.4,2.8,5.6,2.1,virginica
5.4,3.9,1.7,0.4,setosa
5.9,3.0,4.2,1.5,versicolor
5.2,3.5,1.5,0.2,setosa
EOF'

################################################################################

run_example \
 'gurita sort -c sepal_width species < example.csv' \
 'gurita sort -c sepal_width species > "${FILE_OUT_DIR}/example.sort.sepal_width.species.txt" <<EOF
sepal_length,sepal_width,petal_length,petal_width,species
6.3,3.4,5.6,2.4,virginica
6.3,2.5,5.0,1.9,virginica
4.8,3.4,1.9,0.2,setosa
6.3,3.3,4.7,1.6,versicolor
6.4,3.2,4.5,1.5,versicolor
4.7,3.2,1.3,0.2,setosa
6.4,2.8,5.6,2.1,virginica
5.4,3.9,1.7,0.4,setosa
5.9,3.0,4.2,1.5,versicolor
5.2,3.5,1.5,0.2,setosa
EOF'

################################################################################

run_example \
 'gurita sort -c sepal_width --order d < example.csv' \
 'gurita sort -c sepal_width --order d > "${FILE_OUT_DIR}/example.sort.sepal_width.order.d.txt" <<EOF
sepal_length,sepal_width,petal_length,petal_width,species
6.3,3.4,5.6,2.4,virginica
6.3,2.5,5.0,1.9,virginica
4.8,3.4,1.9,0.2,setosa
6.3,3.3,4.7,1.6,versicolor
6.4,3.2,4.5,1.5,versicolor
4.7,3.2,1.3,0.2,setosa
6.4,2.8,5.6,2.1,virginica
5.4,3.9,1.7,0.4,setosa
5.9,3.0,4.2,1.5,versicolor
5.2,3.5,1.5,0.2,setosa
EOF'

################################################################################

run_example \
 'gurita sort -c sepal_width species --order d a < example.csv' \
 'gurita sort -c sepal_width species --order d a > "${FILE_OUT_DIR}/example.sort.sepal_width.species.order.d.a.txt" <<EOF
sepal_length,sepal_width,petal_length,petal_width,species
6.3,3.4,5.6,2.4,virginica
6.3,2.5,5.0,1.9,virginica
4.8,3.4,1.9,0.2,setosa
6.3,3.3,4.7,1.6,versicolor
6.4,3.2,4.5,1.5,versicolor
4.7,3.2,1.3,0.2,setosa
6.4,2.8,5.6,2.1,virginica
5.4,3.9,1.7,0.4,setosa
5.9,3.0,4.2,1.5,versicolor
5.2,3.5,1.5,0.2,setosa
EOF'

################################################################################

run_example \
 'gurita sort -c sepal_length < missing.csv' \
 'gurita sort -c sepal_length > "${FILE_OUT_DIR}/example.sort.sepal_width.missing.txt" <<EOF
sepal_length,sepal_width,petal_length,petal_width,species
4.7,3.2,1.3,0.2,setosa
4.8,3.4,1.9,0.2,setosa
5.4,3.9,1.7,0.4,setosa
5.9,3.0,4.2,1.5,versicolor
6.3,2.5,5.0,1.9,virginica
6.3,3.3,4.7,1.6,versicolor
6.4,3.2,4.5,1.5,versicolor
6.4,2.8,5.6,2.1,virginica
,3.4,5.6,2.4,virginica
,3.5,1.5,0.2,setosa
EOF'

################################################################################

run_example \
 'gurita sort -c sepal_length --napos first < missing.csv' \
 'gurita sort -c sepal_length --napos first > "${FILE_OUT_DIR}/example.sort.sepal_length.napos.first.txt" <<EOF
sepal_length,sepal_width,petal_length,petal_width,species
4.7,3.2,1.3,0.2,setosa
4.8,3.4,1.9,0.2,setosa
5.4,3.9,1.7,0.4,setosa
5.9,3.0,4.2,1.5,versicolor
6.3,2.5,5.0,1.9,virginica
6.3,3.3,4.7,1.6,versicolor
6.4,3.2,4.5,1.5,versicolor
6.4,2.8,5.6,2.1,virginica
,3.4,5.6,2.4,virginica
,3.5,1.5,0.2,setosa
EOF'

################################################################################

run_example \
 'gurita tail 5 < example.csv' \
 'gurita tail 5 > "${FILE_OUT_DIR}/example.tail.5.txt" <<EOF 
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
4.6,3.1,1.5,0.2,setosa
5.0,3.6,1.4,0.2,setosa
5.4,3.9,1.7,0.4,setosa
4.6,3.4,1.4,0.3,setosa
5.0,3.4,1.5,0.2,setosa
4.4,2.9,1.4,0.2,setosa
4.9,3.1,1.5,0.1,setosa
EOF'

################################################################################

run_example \
 'gurita tail 5 + head 3 < example.csv' \
 'gurita tail 5 + head 3 > "${FILE_OUT_DIR}/example.tail.5.head.3.txt" <<EOF  
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
4.6,3.1,1.5,0.2,setosa
5.0,3.6,1.4,0.2,setosa
5.4,3.9,1.7,0.4,setosa
4.6,3.4,1.4,0.3,setosa
5.0,3.4,1.5,0.2,setosa
4.4,2.9,1.4,0.2,setosa
4.9,3.1,1.5,0.1,setosa
EOF'

################################################################################

run_example \
 'gurita tail 1 < example.csv' \
 'gurita tail 1 > "${FILE_OUT_DIR}/example.tail.1.txt" <<EOF 
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
4.6,3.1,1.5,0.2,setosa
5.0,3.6,1.4,0.2,setosa
5.4,3.9,1.7,0.4,setosa
4.6,3.4,1.4,0.3,setosa
5.0,3.4,1.5,0.2,setosa
4.4,2.9,1.4,0.2,setosa
4.9,3.1,1.5,0.1,setosa
EOF'

################################################################################

run_example \
 'gurita tail -3 < example.csv' \
 'gurita tail -3 > "${FILE_OUT_DIR}/example.tail.neg.3.txt" <<EOF
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
4.6,3.1,1.5,0.2,setosa
5.0,3.6,1.4,0.2,setosa
5.4,3.9,1.7,0.4,setosa
4.6,3.4,1.4,0.3,setosa
5.0,3.4,1.5,0.2,setosa
4.4,2.9,1.4,0.2,setosa
4.9,3.1,1.5,0.1,setosa
EOF'

################################################################################

run_example \
 'gurita unique -c species < iris.csv' \
 'gurita unique -c species < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.unique.species.txt"'

################################################################################

run_example \
 'gurita unique -c species + sort -c species_unique --order d < iris.csv' \
 'gurita unique -c species + sort -c species_unique --order d < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.unique.species.sort.species_unique.order.d.txt"' 

################################################################################

run_example \
 'gurita unique -c class < titanic.csv' \
 'gurita unique -c class < "${DATA_DIR}/titanic.csv" > "${FILE_OUT_DIR}/titanic.unique.class.txt"'

################################################################################

run_example \
 'gurita zscore -c sepal_width + head < iris.csv' \
 'gurita zscore -c sepal_width + head < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.zscore.sepal_width.head.txt"' 

################################################################################

run_example \
 'gurita zscore -c sepal_length petal_width + head < iris.csv' \
 'gurita zscore -c sepal_length petal_width + head < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.zscore.sepal_length.petal_width.txt"' 

################################################################################

run_example \
 'gurita zscore --suffix z + head < iris.csv' \
 'gurita zscore --suffix z + head < "${DATA_DIR}/iris.csv" > "${FILE_OUT_DIR}/iris.zscore.suffix.z.head.txt"' 

################################################################################

run_example \
 'gurita describe < titanic.csv' \
 'gurita describe < "${DATA_DIR}/titanic.csv" > "${FILE_OUT_DIR}/titanic.describe.txt"' 

################################################################################

run_example \
 'gurita describe --col age class < titanic.csv' \
 'gurita describe --col age class < "${DATA_DIR}/titanic.csv" > "${FILE_OUT_DIR}/titanic.describe.age.txt"' 

################################################################################

run_example \
 "gurita filter 'age >= 30' + describe < titanic.csv" \
 "gurita filter 'age >= 30' + describe < ${DATA_DIR}/titanic.csv > ${FILE_OUT_DIR}/titanic.filter.30.describe.txt"

################################################################################

run_example \
 'gurita pretty < titanic.csv' \
 'gurita pretty < "${DATA_DIR}/titanic.csv" > "${FILE_OUT_DIR}/titanic.pretty.txt"' 

################################################################################

run_example \
 'gurita pretty --col age class < titanic.csv' \
 'gurita pretty --col age class < "${DATA_DIR}/titanic.csv" > "${FILE_OUT_DIR}/titanic.pretty.age.class.txt"' 

################################################################################

run_example \
 'gurita pretty --maxrows 20 --maxcols 6 < titanic.csv' \
 'gurita pretty --maxrows 20 --maxcols 6 < "${DATA_DIR}/titanic.csv" > "${FILE_OUT_DIR}/titanic.pretty.maxrows.20.maxcols.6.txt"' 

################################################################################

run_example \
 "gurita filter 'age >= 30' + pretty < titanic.csv" \
 "gurita filter 'age >= 30' + pretty < ${DATA_DIR}/titanic.csv > ${FILE_OUT_DIR}/titanic.filter.30.pretty.txt"

################################################################################

run_example \

################################################################################
