from django.shortcuts import render, redirect
from Guest.models import Student
from deepface import DeepFace
import os
import cv2

# REGISTER STUDENT

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        roll = request.POST.get('roll')
        email = request.POST.get('email')
        password = request.POST.get('password')
        photo = request.FILES.get('photo')

        student = Student.objects.create(
            name=name,
            roll_number=roll,
            email=email,
            password=password,
            photo=photo
        )
        return redirect('face_verify')

    return render(request, 'register.html')


# FACE VERIFY
def face_verify(request):
    if request.method == "POST":
        test_image = request.FILES.get('photo')

        temp_path = "media/temp.jpg"
        with open(temp_path, 'wb+') as f:
            for chunk in test_image.chunks():
                f.write(chunk)

        students = Student.objects.all()

        for student in students:
            try:
                result = DeepFace.verify(
                    img1_path=temp_path,
                    img2_path=student.photo.path,
                    model_name='Facenet',
                    detector_backend='skip'
                )

                print(result)
                if result['verified']:
                    return render(request, 'success.html', {'student': student})

            except Exception as e:
                print(e)
                continue

        return render(request, 'failed.html')

    return render(request, 'verify.html')

def live_face(request):
    #  Use DroidCam IP
    cap = cv2.VideoCapture("http://192.168.1.3:4747/video")

    recognized_student = None
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Process every 10th frame (faster)
        if frame_count % 10 != 0:
            continue

        temp_path = "media/frame.jpg"
        cv2.imwrite(temp_path, frame)

        students = Student.objects.all()

        for student in students:
            try:
                result = DeepFace.verify(
                    img1_path=temp_path,
                    img2_path=student.photo.path,
                    model_name='Facenet',
                    detector_backend='opencv'
                )

                if result['distance'] < 0.6:
                    cap.release()
                    cv2.destroyAllWindows()
                    return render(request, 'success.html', {'student': student})

            except Exception as e:
                print(e)
                continue

        cv2.imshow("DroidCam Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return render(request, 'failed.html')