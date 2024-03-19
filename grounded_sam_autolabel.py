from autodistill_grounded_sam import GroundedSAM
from autodistill.detection import CaptionOntology
import cv2
import supervision as sv
import numpy as np
import glob
from os import path

base_model = GroundedSAM(ontology=CaptionOntology({"floor": "floor"}))
classes = base_model.ontology.classes()
img_dir = "E:/images/"
output_dir = "E:/labels/"

for file in glob.glob(path.join(img_dir, '*.png')):
    name = path.basename(file)[:-4]
    detections = base_model.predict(path.join(img_dir, file))
    print(name)
    mask = detections.mask[0]
    image = cv2.imread(file)

    color_mask = np.zeros_like(image).astype(np.uint8)
    color_mask[:,:,:][mask==True] = [128,64,128]
    color_mask[:,:,:][mask==False] = [128,128,128]
    cv2.imwrite(path.join(output_dir, name+'_color_mask.png') ,color_mask)
    
    label_mask = np.zeros_like(image).astype(np.uint8)
    label_mask[:,:,:][mask==True] = [7,7,7]
    label_mask[:,:,:][mask==False] = [35,35,35]
    cv2.imwrite(path.join(output_dir, name+'_mask.png') ,label_mask)
    cv2.imwrite(path.join(output_dir, name+'_watershed_mask.png') ,label_mask)

# labels = [
#     f"{classes[class_id]} {confidence:0.2f}"
#     for _, _, confidence, class_id, _
#     in detections
# ]


# mask_annotator = sv.MaskAnnotator()
# annotated_frame = mask_annotator.annotate(
#     scene=image.copy(),
#     detections=detections
# )

# sv.plot_image(annotated_frame, size=(8, 8))