import numpy as np
import cv2
import pyzed.sl as sl

class ZedTracking(object):

    def __init__(self, fname):
        input_type = sl.InputType()
        input_type.set_from_svo_file(fname)
        init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
        self.cam = sl.Camera()
        err = self.cam.open(init)
        if err != sl.ERROR_CODE.SUCCESS:
            print(repr(err))
            exit()

        obj_param = sl.ObjectDetectionParameters()
        obj_param.enable_tracking = True
        obj_param.image_sync = True
        obj_param.enable_mask_output = True
        if obj_param.enable_tracking:
            self.cam.enable_positional_tracking()
        err = self.cam.enable_object_detection(obj_param)
        if err != sl.ERROR_CODE.SUCCESS:
            print(repr(err))
            self.cam.close()
            exit()

        return

    def _video_writer_setup(self, fname):
        image_size = self.cam.get_camera_information().camera_resolution
        width = image_size.width
        height = image_size.height
        video_writer = cv2.VideoWriter(str(fname),
                                       cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                       self.cam.get_camera_information().camera_fps,
                                       (width, height))
        return video_writer

    def _random_color(self, seed):
        colors = [(255, 255, 255),
                  (255, 0, 0),
                  (0, 255, 0),
                  (0, 0, 255),
                  (255, 255, 0),
                  (0, 255, 255),
                  (255, 0, 255)]
        return colors[seed % len(colors)]

    def detect(self, visualization=False, fname=None):
        if visualization and (fname == None):
            print("file name not provided!")
            exit()

        runtime = sl.RuntimeParameters()
        if visualization:
            mat = sl.Mat()
            video_writer = self._video_writer_setup(fname)
        nb_frames = self.cam.get_svo_number_of_frames()

        objects = sl.Objects()
        obj_runtime = sl.ObjectDetectionRuntimeParameters()
        obj_runtime.detection_confidence_threshold = 50

        all_ped_id = []
        all_ped_pos = []
        all_ped_vel = []

        while True:
            err = self.cam.grab(runtime)
            if err == sl.ERROR_CODE.SUCCESS:
                svo_pos = self.cam.get_svo_position()
                self.cam.retrieve_objects(objects, obj_runtime)
                if objects.is_new:
                    curr_ped_id = []
                    curr_ped_pos = []
                    curr_ped_vel = []
                    curr_ped_bbox = []
                    curr_ped_conf = []
                    obj_array = objects.object_list
                    for obj in obj_array:
                        if obj.label == sl.OBJECT_CLASS.PERSON:
                            curr_ped_id.append(obj.id)
                            curr_ped_pos.append(obj.position)
                            curr_ped_vel.append(obj.velocity)
                            curr_ped_bbox.append(obj.bounding_box_2d)
                            curr_ped_conf.append(obj.confidence)
                    all_ped_id.append(curr_ped_id)
                    all_ped_pos.append(curr_ped_pos)
                    all_ped_vel.append(curr_ped_vel)
                if visualization:
                    self.cam.retrieve_image(mat, sl.VIEW.LEFT)
                    img = mat.get_data().astype(np.uint8)
                    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
                    for i, bbox in enumerate(curr_ped_bbox):
                        bbox = bbox.astype(np.int)
                        color = self._random_color(curr_ped_id[i])
                        cv2.rectangle(img, tuple(bbox[0]), tuple(bbox[2]), color, 2)
                        cv2.putText(img, str(curr_ped_conf[i]), tuple(bbox[0]),
                                    cv2.FONT_HERSHEY_PLAIN, 1, color)
                    video_writer.write(img)
                if svo_pos >= (nb_frames - 1):
                    print("End of Video!")
                    break

        if visualization:
            video_writer.release()

        return all_ped_id, all_ped_pos, all_ped_vel

    def save_raw_vid(self, fname):
        runtime = sl.RuntimeParameters()
        mat = sl.Mat()
        video_writer = self._video_writer_setup(fname)
        nb_frames = self.cam.get_svo_number_of_frames()

        while True:
            err = self.cam.grab(runtime)
            if err == sl.ERROR_CODE.SUCCESS:
                svo_pos = self.cam.get_svo_position()
                self.cam.retrieve_image(mat, sl.VIEW.LEFT)
                #self.cam.retrieve_image(mat, sl.VIEW.RIGHT)
                #self.cam.retrieve_image(mat, sl.VIEW.DEPTH)
                img = mat.get_data().astype(np.uint8)
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
                video_writer.write(img)
                if svo_pos >= (nb_frames - 1):
                    print("End of Video!")
                    break

        video_writer.release()
        return
            
        
    def close(self):
        self.cam.disable_object_detection()
        self.cam.close()        
        return
