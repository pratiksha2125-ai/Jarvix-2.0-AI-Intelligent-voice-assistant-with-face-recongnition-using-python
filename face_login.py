# from deepface import DeepFace
# import time
# import os
# import cv2
# # print("Current folder:", os.getcwd())
# # print("Files:", os.listdir())
# #
# # print("Face folder exists:", os.path.exists("face"))
# # print("Inside face folder:", os.listdir("face") if os.path.exists("face") else "No face folder")
# #
# # print("Image exists:", os.path.exists("face/pratiksha.jpg"))
#
# def face_login():
#
#     camera = cv2.VideoCapture(0)
#
#     print("Face scanning started...")
#
#     last_check = 0
#
#     registered_face = r"C:\Users\Pratiksha\PycharmProjects\PythonProject\AI assistance\face\pratiksha.jpeg"
#
#     while True:
#
#         ret, frame = camera.read()
#
#         if not ret:
#             continue
#
#         cv2.imshow("Jarvis Face Login", frame)
#
#         # Check face every 3 seconds
#         if time.time() - last_check > 3:
#
#             last_check = time.time()
#
#             # Save current camera frame
#             current_face = "pratiksha.jpeg"
#             cv2.imwrite(current_face, frame)
#
#             try:
#
#                 result = DeepFace.verify(
#                     img1_path=registered_face,
#                     img2_path=current_face,
#                     enforce_detection=False
#                 )
#
#                 print(result["verified"])
#
#                 if result["verified"]:
#
#                     print("Face recognized")
#
#                     camera.release()
#                     cv2.destroyAllWindows()
#
#                     # Remove temporary image
#                     if os.path.exists(current_face):
#                         os.remove(current_face)
#
#                     return True
#
#                 else:
#                     print("Unknown face")
#
#             except Exception as e:
#                 print("Error:", e)
#
#
#         # Press ESC to exit
#         if cv2.waitKey(1) == 27:
#             break
#
#
#     camera.release()
#     cv2.destroyAllWindows()
#
#     return False



from deepface import DeepFace
import time
import os
import cv2


def face_login():

    camera = cv2.VideoCapture(0)

    print("Face scanning started...")

    last_check = 0

    registered_face = r"C:\Users\Pratiksha\PycharmProjects\PythonProject\AI assistance\face\pratiksha.jpeg"

    while True:

        ret, frame = camera.read()

        if not ret:
            continue

        cv2.imshow("Jarvis Face Login", frame)

        if time.time() - last_check > 3:

            last_check = time.time()

            current_face = "current_face.jpg"
            cv2.imwrite(current_face, frame)

            try:
                result = DeepFace.verify(
                    img1_path=registered_face,
                    img2_path=current_face,
                    enforce_detection=False
                )

                print(result["verified"])

                if result["verified"]:
                    print("Face recognized")

                    camera.release()
                    cv2.destroyAllWindows()

                    return True

                else:
                    print("Unknown face")

            except Exception as e:
                print("Error:", e)

        if cv2.waitKey(1) == 27:
            break


    camera.release()
    cv2.destroyAllWindows()

    return False