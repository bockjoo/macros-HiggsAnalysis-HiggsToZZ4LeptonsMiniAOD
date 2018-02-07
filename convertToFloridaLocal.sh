#!/bin/bash
chans="4mu 2e2mu 4e"
for chan in $chans ; do
   cp filelist_${chan}_2016_Spring16_AN_Bari_miniaod.txt filelist_${chan}_2016_Spring16_AN_Florida_miniaod.txt
   sed -i 's|/lustre/cms|/raid/raid7/bockjoo/MonoHiggs|g' filelist_${chan}_2016_Spring16_AN_Florida_miniaod.txt
done
exit 0

