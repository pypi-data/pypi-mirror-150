import pointextract #Import this package

pointextract.set_foler_location(set_2dimg_folder="/home/xxx/tempimg/",set_3dobj_folder="/home/xxx/tempobj/") #Set the output folder for 2d images and 3d object
pointextract.display_foler_location() #Display output folders for 2D images and 3D objects

pointextract.build_on_each_folder("/home/xxx/source",THRESAHOLDED_BOX_NUMBER=0,BACKGROUND_NUMBER=0)
#This function will convert all folders with tiff images under '/home/xxx/source' to new folders with 001-xxx.png. CAUTION! This function's target is all folders under '/home/xxx/source', if you want to only convert one folder, you still need put it under '/home/xxx/source'.
#THRESAHOLDED_BOX_NUMBER is image cropping parameters. It will find a rectangle area to crop out the pixels whose brightness is below the threshold value. By increasing this parameter, the final image size will be reduced.
#BACKGROUND_NUMBER is the image post-processing parameters. All pixels whose pixels whose brightness is below the threshold value will be set to 0 as pure black

pointextract.extractpoints_from2D_build3Dobj(input_folder='/home/xxx/image',output_name='testtemp')
#This function will read all images under '/home/xxx/image', convert them to a 3D object as name of 'testtemp.pcd'. CAUTION! Unlike the build_on_each_folder() function, the target of this function is one folder!