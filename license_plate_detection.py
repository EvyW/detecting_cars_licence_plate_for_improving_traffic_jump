from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
from skimage.transform import resize
from skimage import measure
from skimage.measure import regionprops
import matplotlib.patches as patches
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
import os

class class_license_plate_ID_detection:

    def license_plate_ID_detection(car_image):

        # 1) DETECTION OF THE LICENSE PLATE
        def license_plate_detection(car_image):
            car_image = car_image

            # Print dimensions of the image
            #print( "Dimension of image:",car_image.shape)

            # Make image grey scale pixel with ranges between 0 & 255
            gray_car_image = car_image * 255
            fig, (ax1, ax2) = plt.subplots(1, 2)
            ax1.imshow(gray_car_image, cmap="gray")
            threshold_value = threshold_otsu(gray_car_image)
            binary_car_image = gray_car_image > threshold_value
            ax2.imshow(binary_car_image, cmap="gray")
            plt.show()

            # Get all the connected regions and groups them together
            label_image = measure.label(binary_car_image)
            fig, (ax1) = plt.subplots(1)
            ax1.imshow(gray_car_image, cmap="gray");

            # Regionprops creates a list of properties of all the labelled regions
            for region in regionprops(label_image):
                if region.area < 50:
                    #if the region is so small then it's likely not a license plate
                    continue
                # Bounding box coordinates
                minRow, minCol, maxRow, maxCol = region.bbox
                rectBorder = patches.Rectangle((minCol, minRow), maxCol-minCol, maxRow-minRow, edgecolor="red", linewidth=2, fill=False)
                ax1.add_patch(rectBorder)
            # Draw a red rectangle over those regions
            plt.show()

            # Get all the connected regions and groups them together
            label_image = measure.label(binary_car_image)

            # Get the maximum and minimum dimensions that a license plate can have
            plate_dimensions = (0.08*label_image.shape[0], 0.2*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])
            min_height, max_height, min_width, max_width = plate_dimensions
            plate_objects_cordinates = []
            plate_like_objects = []
            fig, (ax1) = plt.subplots(1)
            ax1.imshow(gray_car_image, cmap="gray");

            # Create a list of properties of all the labelled regions with regionprops
            for region in regionprops(label_image):
                if region.area < 50:
                    # If  the region is so small then it's likely not a license plate
                    continue
                # Bounding box coordinates
                min_row, min_col, max_row, max_col = region.bbox
                region_height = max_row - min_row
                region_width = max_col - min_col
                # ensuring that the region identified satisfies the condition of a typical license plate
                if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
                    plate_like_objects.append(binary_car_image[min_row:max_row,
                                              min_col:max_col])
                    plate_objects_cordinates.append((min_row, min_col,
                                                          max_row, max_col))
                    rectBorder = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="red", linewidth=2, fill=False)
                    ax1.add_patch(rectBorder)
            # Draw a red rectangle over regions that can be a license plate
            plt.show()

            return plate_like_objects


        # 2) CHARACTER SEGMENTATION
        def character_segmentation(car_image):
            # Detect license plate in the image and get the object
            plate_like_objects = license_plate_detection(car_image)

            # Select license plate
            license_plate = np.invert(plate_like_objects[1])
            labelled_plate = measure.label(license_plate)
            fig, ax1 = plt.subplots(1)
            ax1.imshow(license_plate, cmap="gray")

            # Assume that the width of a license plate should be between 5% and 15% of the license plate,  and height should be between 35% and 60%
            # this eliminate some regions that are not likely the license plate
            character_dimensions = (0.35*license_plate.shape[0], 0.60*license_plate.shape[0], 0.05*license_plate.shape[1], 0.15*license_plate.shape[1])
            min_height, max_height, min_width, max_width = character_dimensions

            # Segment characters
            characters = []
            counter = 0
            column_list = []
            for regions in regionprops(labelled_plate):
                y0, x0, y1, x1 = regions.bbox
                region_height = y1 - y0
                region_width = x1 - x0

                if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
                    roi = license_plate[y0:y1, x0:x1]

                    # Draw a red bordered rectangle over the character.
                    rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red",
                                                   linewidth=2, fill=False)
                    ax1.add_patch(rect_border)

                    # Resize the characters to 20X20 and then append each character into the characters list
                    resized_char = resize(roi, (20, 20))
                    characters.append(resized_char)

                    # Keep track of the arrangement of the characters
                    column_list.append(x0)
            # Plot image
            plt.show()

            return [characters, column_list]



        # 3.1) CHARACTER RECOGNITION - build model for predicting
        def character_recognition():
            letters = [
                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
                        'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T',
                        'U', 'V', 'W', 'X', 'Y', 'Z'
                    ]

            # Function to read the training data
            def read_training_data(training_directory):
                image_data = []
                target_data = []
                for each_letter in letters:
                    for each in range(10):
                        image_path = os.path.join(training_directory, each_letter, each_letter + '_' + str(each) + '.jpg')
                        # read each image of each character
                        img_details = imread(image_path, as_gray=True)
                        # convert each character image to binary image
                        binary_image = img_details < threshold_otsu(img_details)
                        # Flat the 2D array of each image because the ML classifier requires each sample to be a 1D array
                        flat_bin_image = binary_image.reshape(-1)
                        image_data.append(flat_bin_image)
                        target_data.append(each_letter)

                return (np.array(image_data), np.array(target_data))

            # Function to perform cross-validation
            def cross_validation(model, num_of_fold, train_data, train_label):
                # Use cross validation to measure the accuracy of a model
                accuracy_result = cross_val_score(model, train_data, train_label, cv=num_of_fold)
                print("Cross Validation Result for ", str(num_of_fold), " -fold")
                # print accuracy
                print(accuracy_result * 100)

            # Set current directory
            current_dir = os.path.dirname(os.path.realpath(__file__))
            training_dataset_dir = os.path.join(current_dir, 'training_data')

            # read training data
            image_data, target_data = read_training_data(training_dataset_dir)

            # Build  SVM (support vector machine) model for prediction
            svc_model = SVC(kernel='linear', probability=True)
            # crossvalidate
            cross_validation(svc_model, 4, image_data, target_data)

            # Train the model with all the input data
            svc_model.fit(image_data, target_data)

            return svc_model


        # 3.1) CHARACTER RECOGNITION - predict characters

        # build prediction model for character recognition (using support vector machine)
        svc_model = character_recognition()

        # segment/identify characters in license plate
        character_segm = character_segmentation(car_image)
        characters = character_segm[0]

        # Predict license plate
        classification_result = []
        for each_character in characters:
            # Convert to a 1D array
            each_character = each_character.reshape(1, -1);
            result = svc_model.predict(each_character)
            classification_result.append(result)
        # Print resulting prediction
        plate_string = ''
        for eachPredict in classification_result:
            plate_string += eachPredict[0]
        #print(plate_string)

        # Sort the letters in the right order and print the license plate
        column_list = character_segm[1]
        column_list_copy = column_list[:]
        column_list.sort()
        rightplate_string = ''
        for each in column_list:
            rightplate_string += plate_string[column_list_copy.index(each)]
        print('License Plate ID: ', rightplate_string)

