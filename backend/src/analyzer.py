import cv2
import mediapipe as mp
import numpy as np

class Analyzer():

    def __init__(self, video) -> None:
        self.flag_done = False

        self.LEFT_IRIS = [474,475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]
        #setup
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_face_mesh = mp.solutions.face_mesh
        # For webcam input:
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.cap = cv2.VideoCapture(video)

        #data
        self.left_eye_pos = list() #euclian center distance
        self.right_eye_pos = list() #euclian center distance
    

    def run_analyzer(self) -> None:
        self.flag_done = False
        with self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
            while self.cap.isOpened():
                success, image = self.cap.read()
                if not success:
                    print("\n\t*The task was done!*\n")
                    self.flag_done = True
                    break

                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(image)

                img_h, img_w = image.shape[:2]

                # Draw the face mesh annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
                        self.mp_drawing.draw_landmarks(
                            image=image,
                            landmark_list=face_landmarks,
                            connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=self.mp_drawing_styles
                            .get_default_face_mesh_tesselation_style())
                        self.mp_drawing.draw_landmarks(
                            image=image,
                            landmark_list=face_landmarks,
                            connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=self.mp_drawing_styles
                            .get_default_face_mesh_contours_style())
                        self.mp_drawing.draw_landmarks(
                            image=image,
                            landmark_list=face_landmarks,
                            connections=self.mp_face_mesh.FACEMESH_IRISES,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=self.mp_drawing_styles
                            .get_default_face_mesh_iris_connections_style())
                        
                        (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[self.LEFT_IRIS])
                        (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[self.RIGHT_IRIS])
                        center_left = np.array([l_cx, l_cy], dtype=np.int32)
                        center_right = np.array([r_cx, r_cy], dtype=np.int32)
                        
                        print("Euclian distance from left eye: ", end='')
                        print(center_left)
                        print("Euclian distance from right eye: ", end='')
                        print(center_right)

                        self.left_eye_pos.append(center_left)
                        self.right_eye_pos.append(center_right)

                    # Flip the image horizontally for a selfie-view display.
                    cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
                    if cv2.waitKey(5) & 0xFF == 27:
                        break
            self.cap.release()

# TESTE
# obj_analyzer = Analyzer("../../server/video.mp4")
# obj_analyzer.run_analyzer()

# if not obj_analyzer.flag_done:
#     print("\n\t*Some problem ocurred in execution :(*\n")