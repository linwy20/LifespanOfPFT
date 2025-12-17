# Created on Fri 2023-06-09 21:39:52 
# @author: Wanyi

# export lifespan, pft and growthform txt files to csv

library(rtry)
# 选特定列输出：rtry_select_col()


# process Lifespan
input_path <- "/hard/linwy20/pft_distribution/snow/Lifespan/27303.txt"
input <- rtry_import(input_path)
rtry_export(input, file.path("./", "lifespan_unprocessed.csv"),quote = TRUE, encoding = "UTF-8")


# process PFT
input_path <- "/hard/linwy20/pft_distribution/snow/Pft/27418.txt"
input <- rtry_import(input_path)
rtry_export(input, file.path("./", "pft_unprocessed.csv"),quote = TRUE, encoding = "UTF-8")


# process GrowthForm
input_path <- "/hard/linwy20/pft_distribution/snow/Growthform/28729.txt"
input <- rtry_import(input_path)
rtry_export(input, file.path("./", "growthform_unprocessed.csv"),quote = TRUE, encoding = "UTF-8")
