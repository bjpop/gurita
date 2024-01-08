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
 'gurita box -y age -x class --hue class --out "${IMG_OUT_DIR}/box.class.age.sex.hue.png" < "${DATA_DIR}/titanic.csv"'
	
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
	
################################################################################

run_example \
	
################################################################################

run_example \
	
################################################################################
