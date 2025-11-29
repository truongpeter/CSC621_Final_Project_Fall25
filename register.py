# TESTS:
# Running Python:                             OK
# Running sitk.Show :                         OK
# Running sitk.Show with volumetric:          OK convert_file
# Running up to HistogramMatchingImageFilter: OK
# Running DemonsRegistrationFilter:           CRASH
#   No explicit reason. Running function attempt register
#   with patient 1 and patient 2 (p1 & p2) on demons regular
#   and p1 and p1 on demons symmetric both crash.

import SimpleITK as sitk

#export SITK_SHOW_COMMAND=~/Downloads/fiji-latest-linux64-jdk/Fiji/fiji

# converts a path leading to a directory of dicom files
# to an image
def convert_file(path):
	reader = sitk.ImageSeriesReader()

	reader.SetFileNames(reader.GetGDCMSeriesFileNames(path))

	return reader.Execute()

def attempt_register(fixed, moving): 
	img_fixed = convert_file(fixed)
	img_moving = convert_file(moving)

	#i_f_pixel_id = img_fixed.GetPixelID()
	#print(i_f_pixel_id in (sitk.sitkUInt8, sitk.sitkInt8))
	# is false

	matcher = sitk.HistogramMatchingImageFilter()
	matcher.SetNumberOfHistogramLevels(1024)
	matcher.SetNumberOfMatchPoints(7)
	matcher.ThresholdAtMeanIntensityOn()

	img_matcher = matcher.Execute(img_moving, img_fixed)
	
	#apply demons
	demons = sitk.DemonsRegistrationFilter()
	demons.SetNumberOfIterations(1)
	demons.SetStandardDeviations(1.0)

	#crashed
	displacement_field = demons.Execute(img_fixed, img_matcher)
	print("check")

patient1 = "/home/a/main/Dataset/Data/Patient1"
patient2 = "/home/a/main/Dataset/Data/Patient2"

#sitk.Show(convert_file(patient2))

attempt_register(patient1, patient2)
