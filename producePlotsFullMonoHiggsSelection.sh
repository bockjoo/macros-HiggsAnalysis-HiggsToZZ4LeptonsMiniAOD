#!/bin/bash
variables="hM4l_9 hPFMET_10"
#variables="hM4l_8_100_800 hPFMET_10"
chans="4l 4mu 2e2mu 4e"
#chans="4mu 2e2mu 4e"
#nrebins="1 1 1 2 10"
#uselogys="1 1 1 1 1"
#useratios="1 1 1 1 1"
nrebins="2 10"
uselogys="1 1"
useratios="1 1"
energy=13TeV
for chan in $chans ; do
   inputfile=filelist_${chan}_2016_Spring16_AN_Florida_miniaod.txt
   i=0
   for v in $variables ; do
      i=$(expr $i + 1)
      #nrebin=$(echo $nrebins | awk "{print \$n}")
      nrebin=$(echo $nrebins | cut -d" " -f$i)
      uselogy=$(echo $uselogys | cut -d" " -f$i)
      useratio=$(echo $useratios | cut -d" " -f$i)
      echo Executing python plotExercises.py $v $nrebin $uselogy $useratio $inputfile
      #break
      python plotExercises.py $v $nrebin $uselogy $useratio $inputfile
      logplot= ; [ $uselogy -eq 1 ] && logplot=_log
      ratioplot= ; [ $useratio -eq 1 ] && ratioplot=_ratio
      theplot=plots/h_${v}_${chan}_${energy}${ratioplot}${logplot}.pdf
      if [ ] ; then
        output="`display $theplot &`"
        theps=$!
        echo $theplot Sleeping 10 seconds
        sleep 10
        kill $theps
      fi
      echo INFO $theplot
   done
done
exit 0

