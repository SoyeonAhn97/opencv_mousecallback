import cv2
import numpy as np

pt1 = (0, 0)
pt2 = (0, 0)

# 흰색 캔버스 생성
img = np.ones((512, 512, 3), np.uint8)*255

# 마우스 콜백 함수로 원 그리기
def mouse_callback(event, x, y, flags, params):
    global img, pt1, pt2
    
    # 오른쪽 마우스 버튼을 눌렀을 때 원 그리기
    if event==cv2.EVENT_RBUTTONDOWN:
        pt1 = (x, y)
    elif event==cv2.EVENT_RBUTTONUP:
        pt2 = (x, y)
        radius = int(((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)**0.5)  # 두 좌표 간의 거리로 반지름 계산
        cv2.circle(img, pt1, radius, (0, 255, 0), 1)  # 원 그리기
        cv2.imshow('img', img)

    # 왼쪽 마우스 버튼을 눌렀을 때 사각형 그리기
    elif event==cv2.EVENT_LBUTTONDOWN:
        pt1 = (x, y)
    elif event==cv2.EVENT_LBUTTONUP:
        pt2 = (x, y)

        # shift누른 상태에서 왼쪽 마우스 버튼 눌렀을 때 삼각형 그리기
        if flags & cv2.EVENT_FLAG_SHIFTKEY:
            # 삼각형의 세 꼭짓점 좌표 설정 (임의로 정한 좌표)
            pt3 = (pt1[0], pt2[1]) # 직각삼각형의 나머지 꼭짓점
            triangle_draw = np.array([pt1, pt2, pt3])
            cv2.drawContours(img, [triangle_draw], 0, (0, 0, 255), 1) # 삼각형 그리기
        else:
            # Shift 키가 눌리지 않았을 때는 사각형 그리기
            cv2.rectangle(img, pt1, pt2, (255, 0, 0), 1) # 사각형 그리기

        cv2.imshow('img', img)


# 도형을 리사이즈하는 함수
def resize_image(image, scale, interpolation):
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    resized = cv2.resize(image, (width, height), interpolation=interpolation)
    return resized

def blur_image(image, ksize):
    return cv2.GaussianBlur(image, (ksize, ksize), 0)

# 도형을 저장하는 함수
def save_image(image, filename):
    cv2.imwrite(filename, image)

cv2.namedWindow('img')
cv2.setMouseCallback('img', mouse_callback, [img])

while True:
    cv2.imshow('img', img)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('s'): # S 키를 누르면 도형이 그려진 이미지를 저장
        save_image(img, 'original_img.png')
        print("Original image saved as 'original_image.png'.")

    elif key == ord('r'):  # 'r' 키를 누르면 이미지를 2배로 확대 후 저장
        resized_img = resize_image(img, 2.0, cv2.INTER_LINEAR)
        save_image(resized_img, 'resized_image_2x.png')
        cv2.imshow('Resized Image', resized_img)
        print("Resized image (2x) saved as 'resized_image_2x.png'.")

    elif key == ord('d'):  # 'd' 키를 누르면 이미지를 0.5배로 축소 후 저장

        # 세 가지 보간 방법으로 축소한 이미지를 저장 및 비교
        resized_img_area = resize_image(img, 0.5, cv2.INTER_AREA) # INTER_AREA 사용
        resized_img_linear = resize_image(img, 0.5, cv2.INTER_LINEAR) # INTER_LINEAR 사용
        resized_img_cubic = resize_image(img, 0.5, cv2.INTER_CUBIC) # INTER_CUBIC 사용

        # 블러 처리
        blurred_img_area = blur_image(resized_img_area, 5) # 블러 커널 크기 설정
        blurred_img_linear = blur_image(resized_img_linear, 5)
        blurred_img_cubic = blur_image(resized_img_cubic, 5)
        
        # 블러 처리된 이미지 저장
        save_image(blurred_img_area, 'blurred_image_0.5x_area.png')
        save_image(blurred_img_linear, 'blurred_image_0.5x_linear.png')
        save_image(blurred_img_cubic, 'blurred_image_0.5x_cubic.png')
        
        # 각 보간 방법으로 축소된 이미지 및 블러 처리된 이미지 보여주기
        # cv2.imshow('Resized Image (INTER_AREA)', resized_img_area)
        # cv2.imshow('Resized Image (INTER_LINEAR)', resized_img_linear)
        # cv2.imshow('Resized Image (INTER_CUBIC)', resized_img_cubic)
        cv2.imshow('Blurred Image (INTER_AREA)', blurred_img_area)
        cv2.imshow('Blurred Image (INTER_LINEAR)', blurred_img_linear)
        cv2.imshow('Blurred Image (INTER_CUBIC)', blurred_img_cubic)
        
        # print("Resized images saved:")
        # print(" - resized_image_0.5x_area.png (INTER_AREA)")
        # print(" - resized_image_0.5x_linear.png (INTER_LINEAR)")
        # print(" - resized_image_0.5x_cubic.png (INTER_CUBIC)")
        print("Blurred images saved:")
        print(" - blurred_image_0.5x_area.png (INTER_AREA)")
        print(" - blurred_image_0.5x_linear.png (INTER_LINEAR)")
        print(" - blurred_image_0.5x_cubic.png (INTER_CUBIC)")

    elif key == 27:  # ESC 키를 누르면 종료
        break

cv2.destroyAllWindows()