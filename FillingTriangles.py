from LineDrawAlgorithm import Image
import numpy as np

t0 = np.array([[10, 70], [50, 160], [70, 80]])
t1 = np.array([[180, 50], [150, 1], [70, 180]])
t2 = np.array([[180, 150], [120, 160], [130, 180]])


class TriangleImage(object):

    # def __init__(self):


    def draw_triangle_1(self, image, p1, p2, p3, colour):
        image.draw_line(p1[0], p1[1], p2[0], p2[1], colour)
        image.draw_line(p2[0], p2[1], p3[0], p3[1], colour)
        image.draw_line(p1[0], p1[1], p3[0], p3[1], colour)


    def draw_triangle_2(self, image, p1, p2, p3, color):
        if p1[1] == p2[1] and p1[1] == p3[1]:
            return 0
        if p1[1] > p2[1]:
            p1, p2 = p2, p1
        if p1[1] > p3[1]:
            p1, p3 = p3, p1
        if p2[1] > p3[1]:
            p2, p3 = p3, p2
        total_height = p3[1] - p1[1]
        total_height = int(total_height)


        for i in range(0, total_height):
            second_half = i > (p2[1] - p1[1]) or (p2[1] == p1[1])
            segment_height = (p3[1] - p2[1]) if second_half else (p2[1] - p1[1])
            alpha = i/total_height
            beta = (i - ((p2[1] - p1[1]) if second_half else 0))/segment_height
            A = p1 + (p3 - p1) * alpha
            B = (p2 + (p3 - p2) * beta) if second_half else (p1 + (p2 - p1) * beta)
            if A[0] > B[0]:
                A, B = B, A
            for j in range(int(A[0]), int(B[0] + 1)):
                image.set_pixel(j, p1[1] + i, color)


        '''
        for y in range(p1[1], p2[1]+1):
            segment_height = p2[1] - p1[1] + 1
            segment_height = int(segment_height)
            alpha = (y - p1[1]) / total_height
            beta = (y - p1[1]) / segment_height
            A = p1 + (p3 - p1) * alpha
            B = p1 + (p2 - p1) * beta
            if A[0] > B[0]:
                A, B = B, A
            for j in range(int(A[0]), int(B[0])+1):
                image.set_pixel(j, y, color)
        for y in range(p2[1], p3[1]+1):
            segment_height = p3[1] - p2[1] + 1
            segment_height = int(segment_height)
            alpha = (y - p1[1]) / total_height
            beta = (y - p2[1]) / segment_height
            A = p1 + (p3 - p1) * alpha
            B = p2 + (p3 - p2) * beta
            if A[0] > B[0]:
                A, B = B, A
            for j in range(int(A[0]), int(B[0])+1):
                image.set_pixel(j, y, color)
        '''


        # image.draw_line(p1[0], p1[1], p2[0], p2[1], (0, 255, 0))
        # image.draw_line(p2[0], p2[1], p3[0], p3[1], (0, 255, 0))
        # image.draw_line(p3[0], p3[1], p1[0], p1[1], (255, 0, 0))



if __name__ == '__main__':
    triangle = TriangleImage()
    image = Image(256, 256)
    # triangle.draw_triangle_1(image, t0[0, :], t0[1, :], t0[2, :], (255, 0, 0))
    # triangle.draw_triangle_1(image, t1[0, :], t1[1, :], t1[2, :], (255, 255, 255))
    # triangle.draw_triangle_1(image, t2[0, :], t2[1, :], t2[2, :], (0, 255, 0))

    triangle.draw_triangle_2(image, t0[0, :], t0[1, :], t0[2, :], (255, 0, 0))
    triangle.draw_triangle_2(image, t1[0, :], t1[1, :], t1[2, :], (255, 255, 255))
    triangle.draw_triangle_2(image, t2[0, :], t2[1, :], t2[2, :], (0, 255, 0))

    image.write("triangle.jpg")




